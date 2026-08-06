import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import override

import numpy as np
import pandas as pd

from . import utils_input as utl_input
from .spec import Spec
from .utils_logging import shorten_path




def _pair_combinations(left: tuple, right: tuple) -> tuple:
    result = []
    for leftItem in left:
        for rightItem in right:
            result.append((leftItem, rightItem))
    return result




@dataclass(kw_only=True)
class ProfileSpec(Spec):
    idRow: str
    nodeRow: str
    typeRow: str
    tsRow: str
    timesteps: int
    isCompositional: bool
    defaultValue: float
    assignments = None

    def __post_init__(self):
        self._validate_row_names()
        self._validate_timesteps()
        super().__post_init__()
        self._validate_timeseries_size()
        if self.assignments is None:
            self._enrich_with_assignments()
        self._enrich_with_default_profile()
        if self.isCompositional:
            self._validateProfileSum()
    
    def _validate_row_names(self):
        attributeNames = [item[0] for item in self.fields]
        if any(name not in attributeNames for name in [
            self.idRow,
            self.nodeRow,
            self.typeRow,
            self.tsRow
        ]):
            raise ValueError(
                "The row names do not match the row names of the datatype schema.\n"
            )
    
    def _validate_timesteps(self):
        if self.timesteps < 1:
            raise ValueError(
                "Attribute 'timesteps' must be a positive natural number.\n"
            )

    def _validate_timeseries_size(self):
        for key, element in self.table.iterrows():
            length = len(element[self.tsRow])
            if length != self.timesteps:
                raise ValueError(
                    f"\n@{self.referenceNames[0]}\n"
                    f"The timeseries of '{key}' "
                    f"(in file '{shorten_path(self.path)}') "
                    f"has {length} elements, "
                    f"but should have {self.timesteps} elements.\n"
                )
    
    def _enrich_with_assignments(self):
        assignments = self._get_assignments()
        wrongAssignments = {k:v for k,v in assignments.items() if len(v)>1 or len(v)<1}
        if wrongAssignments:
            wrongAssignmentsString = "".join(
                f"\t{key} <- {sorted(values)}\n"
                for key, values in sorted(wrongAssignments.items())
            )
            raise ValueError(
                f"\n@{self.referenceNames[0]}\n"
                f"Following node-type-pairs (in file '{shorten_path(self.path)}') "
                f"do not have one profile assigned:\n"
                f"{wrongAssignmentsString}"
                "Please resolve those conflicting assignments.\n"
            )
        self.assignments = {k:v[0] for k,v in assignments.items()}

    def _get_assignments(self):
        dataframe = self.table
        result = defaultdict(list)
        for key, element in dataframe.iterrows():
            pairs = _pair_combinations(element[self.nodeRow], element[self.typeRow])
            for pair in pairs:
                result[pair].append(key)
        return result
    
    def _enrich_with_default_profile(self):
        row = {col: None for col in self.table.columns}
        row[self.tsRow] = tuple(self.defaultValue for _ in range(self.timesteps))
        self.table.loc["default"] = pd.Series(row)

    def _validateProfileSum(self):
        for key, element in self.table.iterrows():
            tsSum = sum(element[self.tsRow])
            if abs(tsSum-1) > 1e-4:
                raise ValueError(
                    f"\n@{self.referenceNames[0]}\n"
                    f"The timeseries of '{key}' "
                    f"(in file '{shorten_path(self.path)}') "
                    f"has a sum of '{tsSum}', "
                    f"which is outside the given tolerance to 1.\n"
                )

    def _are_tuples_valid_attribute_values(self):
        return True
    
    @override
    def _values_need_definitions(self):
        return False

    @override
    def _get_dataframe_from_csv(self) -> pd.DataFrame:
        df = pd.DataFrame.from_records(
            utl_input.load_profile(self.path, self.separator, self.fields)
        )
        df = df.set_index(self.idRow)
        if not df.index.is_unique:
            raise ValueError(f"Duplicate values found in index column '{self.idRow}'.")
        return df




def object_profile_matrix(objectTable: pd.DataFrame, profileSpec: ProfileSpec):
    profileKeys = _map_profiles(objectTable, profileSpec)
    result = np.array(profileSpec.table.loc[profileKeys, profileSpec.tsRow].tolist())
    return result

def _map_profiles(objectTable: pd.DataFrame, profileSpec: ProfileSpec):
    profiles = {}
    unassignedCombiKeys = []
    for objKey in objectTable.index:
        objNode = objectTable.at[objKey, profileSpec.nodeRow]
        objType = objectTable.at[objKey, profileSpec.typeRow]
        objCombiKey = (objNode, objType)
        profileKey = profileSpec.assignments.get(objCombiKey)
        if profileKey is None:
            profiles[objKey] = "default"
            unassignedCombiKeys.append(objCombiKey)
        else:
            profiles[objKey] = profileKey
    if unassignedCombiKeys:
        missing = "".join(f"\t{combiKey}\n" for combiKey in sorted(unassignedCombiKeys))
        logging.info(
            f"\n@{profileSpec.referenceNames[0]}\n"
            f"Following {profileSpec.nodeRow}-{profileSpec.typeRow} combinations "
            f"are in use, but have no profile assigned to "
            f"(in file '{shorten_path(profileSpec.path)}'):\n"
            f"{missing}"
            f"Therefore the default profile with a value of {profileSpec.defaultValue} "
            f"will be assigned.\n"
        )
    result = pd.Series(profiles, name="profileKey")
    return result
