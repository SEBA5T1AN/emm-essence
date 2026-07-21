from .spec import Spec
from .utils_logging import shorten_path

import logging
import warnings
from collections import defaultdict
from collections.abc import Iterable
from typing import Hashable

import pandas as pd




def get_keys_in_use(subject: Spec, traceToRoot: bool):
    result, _ = usages_in_parents(subject, traceToRoot)
    result = result.keys()
    return set(result)

def get_keys_in_definition(subject: Spec):
    result = subject.table.index
    return set(result)


def check_used_but_undefined_keys(subject: Spec):
    keysInUse = get_keys_in_use(subject = subject, traceToRoot = False)
    keysInDef = get_keys_in_definition(subject)
    undefinedKeys = keysInUse - keysInDef
    usageDict, isErrorProne = usages_in_parents(subject = subject, traceToRoot = False)
    undefinedDict = {k: usageDict[k] for k in undefinedKeys if k in usageDict}
    if undefinedKeys:
        details = ''.join(
            f"\t'{key}' -> " +
            "\n\t\t".join(str(v) for v in sorted(values)) +
            "\n"
            for key, values in sorted(undefinedDict.items())
        )
        message = (
            f"\n@{subject.referenceNames[0]}\n"
            f"Following keys are not defined "
            f"(in file '{shorten_path(subject.path)}') "
            f"but the model uses them via these paths:\n"
            f"{details}"
            f"The file '{shorten_path(subject.path)}' defines all available keys:\n"
            f"{sorted(keysInDef)}\n"
        )
        if isErrorProne:
            raise ValueError(message)
        else:
            warnings.warn(message)

def check_unused_but_defined_keys(subject: Spec):
    keysInUse = get_keys_in_use(subject = subject, traceToRoot = False)
    keysInDef = get_keys_in_definition(subject)
    unusedKeys = keysInDef - keysInUse
    if unusedKeys:
        logging.info(
            f"\n@{subject.referenceNames[0]}\n"
            f"Following keys are defined (in file '{shorten_path(subject.path)}') "
            f"but never used:\n"
            f"{sorted(unusedKeys)}\n"
        )


def unique_values(df: pd.DataFrame, cols: Iterable[Hashable]):
    connectingColumns = df.columns.intersection(cols)
    return (
        df.loc[df.index != "default", connectingColumns]
        .stack()
        .explode()
        .dropna()
        .unique()
    )

def usages_in_parents(subject: Spec, traceToRoot: bool):
    result = defaultdict(set)
    for parent in subject.parents:
        mentionedKeys = unique_values(df = parent.table, cols = subject.referenceNames)
        for key in mentionedKeys:
            if traceToRoot and not any_root_usage(subject, [key]):
                continue
            isErrorProne = parent._values_need_definitions()
            usageInfo = (
                shorten_path(parent.path) +
                f" -> {'CAUSES ERROR' if isErrorProne else 'uncritical'}"
            )
            result[key].add(usageInfo)
    return result, isErrorProne


def any_root_usage(subject: Spec, keySubset: Iterable[Hashable]):
    if not subject.parents:
        return True
    for parent, connectedKeys in iter_parent_connections(subject, keySubset):
        if any_root_usage(parent, connectedKeys):
            return True
    return False

def exclusion_chain_reaction(subject: Spec, keySubset: Iterable[Hashable]):
    if not subject.parents:
        return
    for parent, connectedKeys in iter_parent_connections(subject, keySubset):
        parent.table = parent.table.drop(connectedKeys)
        parent.excludedKeys.extend(connectedKeys)
        exclusion_chain_reaction(parent, connectedKeys)

def iter_parent_connections(subject: Spec, keySubset: Iterable[Hashable]):
    for parent in subject.parents:
        namesOfConnectingColumns = parent.table.columns.intersection(subject.referenceNames)
        if namesOfConnectingColumns.empty:
            continue

        croppedTable = parent.table[namesOfConnectingColumns]

        def cellContainsValueOfKeySubset(cellValue, keySubset):
            if isinstance(cellValue, (tuple, list, set)):
                return any(v in keySubset for v in cellValue)
            return (cellValue in keySubset)

        connectedLines = croppedTable.map(
            lambda cellValue: cellContainsValueOfKeySubset(cellValue, keySubset)
        ).any(axis=1)

        if not connectedLines.any():
            continue

        connectedKeys = parent.table.index[connectedLines]
        yield parent, connectedKeys


def inform_about_excluded_keys(subject: Spec):
    excludedKeys = set(subject.excludedKeys)
    if excludedKeys:
        logging.info(
            f"\nExclusions @{subject.referenceNames[0]}\n"
            f"Following keys are directly or indirectly excluded "
            f"(from file '{shorten_path(subject.path)}'):\n"
            f"{sorted(excludedKeys)}\n"
        )
