import warnings
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field

import pandas as pd




def _validate_squence_of_strings(attribute, emptinessAllowed):
    if not isinstance(attribute, Sequence) or isinstance(attribute, str):
        raise TypeError("Attribute 'referenceNames' must be a sequence of strings.\n")
    if not attribute and not emptinessAllowed:
        raise ValueError("Attribute 'referenceNames' must not be empty.\n")
    if not all(isinstance(x, str) and len(x)>0 for x in attribute):
        raise TypeError("Attribute 'referenceNames' must contain only strings.\n")

def _is_nonnumeric_field(item, tuplesAllowed):
    allowedTypes = (str, bool)
    if tuplesAllowed:
        allowedTypes = (str, bool, tuple[str, ...], tuple[bool, ...])
    return (
        isinstance(item, tuple)
        and (len(item) == 2)
        and isinstance(item[0], str)
        and item[1] in allowedTypes
    )

def _is_numeric_field(item, tuplesAllowed):
    allowedTypes = (int, float)
    if tuplesAllowed:
        allowedTypes = (int, float, tuple[int, ...], tuple[float, ...])
    return (
        isinstance(item, tuple)
        and (len(item) == 4)
        and isinstance(item[0], str)
        and item[1] in allowedTypes
        and isinstance(item[2], float)
        and isinstance(item[3], float)
    )




@dataclass
class Spec(ABC):
    referenceNames: list[str]
    path: str
    fields: tuple[tuple[str, type[str | bool]] |
                  tuple[str, type[int | float], float, float],
                  ...]
    separator: str = ","
    parents: list["Spec"] = field(default_factory=list)
    excludedKeys: list[str] = field(default_factory=list)
    table: pd.DataFrame | None = None

    def __post_init__(self):
        self._validate_referenceNames()
        self._validate_path()
        self._validate_fields()
        self._validate_separator()
        self._validate_parents()
        self._validate_excludedKeys()
        if self.table is None:
            self._enrich_with_dataframe()
            self._drop_excludedKeys()
    
    def _validate_referenceNames(self):
        _validate_squence_of_strings(
            attribute = self.referenceNames,
            emptinessAllowed = False
        )
        self.referenceNames = list(self.referenceNames)
    
    def _validate_path(self):
        if not (isinstance(self.path, str) and len(self.path) > 0):
            raise TypeError("Attribute 'path' must be of type 'str'.\n")

    def _validate_fields(self):
        tuplesAllowed = self._are_tuples_valid_attribute_values()
        if not isinstance(self.fields, tuple):
            raise TypeError("Attribute 'fields' must be a tuple.\n")
        if not all (
            _is_nonnumeric_field(item, tuplesAllowed)
            or _is_numeric_field(item, tuplesAllowed)
            for item in self.fields
        ):
            raise TypeError(
                "Attribute 'fields' must be a tuple.\n"
                "Each element must follow one of these patterns:\n"
                "  (key, type)                         for str, bool and their tuple variants\n"
                "  (key, type, lowerLimit, upperLimit) for int, float and their tuple variants\n"
            )

    def _validate_separator(self):
        if not isinstance(self.separator, str):
            raise TypeError("Attribute 'separator' must be of type 'str'.\n")
        if self.separator not in [",", ";", "\t"]:
            raise ValueError("Attribute 'separator' must be a comma, semicolon, or tab\n")

    def _validate_parents(self):
        if not isinstance(self.parents, Sequence) or isinstance(self.parents, str):
            raise TypeError("Attribute 'parents' must be a sequence of Specs.\n")
        if not all(isinstance(x, Spec) for x in self.parents):
            raise TypeError("Attribute 'parents' must contain only Specs.\n")
        self.parents = list(self.parents)
    
    def _validate_excludedKeys(self):
        _validate_squence_of_strings(
            attribute = self.excludedKeys,
            emptinessAllowed = True
        )
        self.excludedKeys = list(self.excludedKeys)

    def _enrich_with_dataframe(self):
        df = self._get_dataframe_from_csv()
        if df is None:
            raise RuntimeError("Dataframe is 'None'.\n")
        self.table = df
    
    def _drop_excludedKeys(self):
        missing = set(self.excludedKeys) - set(self.table.index)
        if missing:
            warnings.warn(
                f"\n@user_specs of '{self.referenceNames[0]}'\n"
                f"Excluded keys not found in dataframe:\n"
                f"{sorted(missing)}\n"
            )
        if self.excludedKeys:
            self.table = self.table.drop(index = self.excludedKeys, errors = "ignore")

    def _are_tuples_valid_attribute_values(self):
        return False
    
    @abstractmethod
    def _values_need_definitions(self):
        pass

    @abstractmethod
    def _get_dataframe_from_csv(self):
        pass
