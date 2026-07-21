from .spec import Spec
from . import utils_input as utl_input
from .utils_logging import shorten_path

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import override

import pandas as pd




def _is_pair_of_different_columns(item):
    return (
        isinstance(item, tuple)
        and (len(item) == 2)
        and isinstance(item[0], str)
        and isinstance(item[1], str)
        and item[0] != item[1]
    )




@dataclass(kw_only=True)
class TableSpec(Spec):
    idColumn: str
    nonEqualColumnPairs: list[tuple[str, str]] = field(default_factory=list)
    hasHeader: bool

    def __post_init__(self):
        self._validate_idColumn()
        self._validate_nonEqualColumnPairs()
        self._validate_hasHeader()
        super().__post_init__()
        self._validate_differing_columns()
    
    def _validate_idColumn(self):
        if not (isinstance(self.idColumn, str) and len(self.idColumn) > 0):
            raise TypeError("Attribute 'idColumn' must be of type 'str'.\n")
        attributeNames = [item[0] for item in self.fields]
        if self.idColumn not in attributeNames:
            raise ValueError(
                f"The idColumn '{self.idColumn}' "
                f"was not found in the column names: {attributeNames}."
            )
    
    def _validate_nonEqualColumnPairs(self):
        if not isinstance(self.nonEqualColumnPairs, Sequence) or isinstance(self.nonEqualColumnPairs, str):
            raise TypeError(
                "Attribute 'nonEqualColumnPairs' must be a sequence of Specs.\n"
            )
        if not all(
            _is_pair_of_different_columns(item)
            for item in self.nonEqualColumnPairs
        ):
            raise TypeError(
                "Attribute 'nonEqualColumnPairs' must contain only "
                "tuples of two different str values.\n"
            )
        attributeNames = [item[0] for item in self.fields]
        columnNames = [
            column
            for pair in self.nonEqualColumnPairs
            for column in pair
        ]
        if any(name not in attributeNames for name in columnNames):
            raise ValueError(
                "The names of the non-equal columns do not "
                "match the column names of the datatype schema.\n"
            )
        self.nonEqualColumnPairs = list(self.nonEqualColumnPairs)
    
    def _validate_differing_columns(self):
        for key, element in self.table.iterrows():
            for pair in self.nonEqualColumnPairs:
                value0 = element[pair[0]]
                value1 = element[pair[1]]
                if(value0 == value1):
                    raise ValueError(
                        f"\n@{self.referenceNames[0]}\n"
                        f"The columns '{pair[0]}', '{pair[1]}' at key '{key}' "
                        f"(in file '{shorten_path(self.path)}') "
                        f"have the same value '{value0}', "
                        f"but should have different ones.\n"
                    )

    def _validate_hasHeader(self):
        if not isinstance(self.hasHeader, bool):
            raise TypeError(
                "Attribute 'hasHeader' must be of type bool. "
                "Valid values are: [True, False]\n"
            )
    
    def _are_tuples_valid_attribute_values(self):
        return False
    
    @override
    def _values_need_definitions(self):
        return not self.parents

    @override
    def _get_dataframe_from_csv(self) -> pd.DataFrame:
        df = pd.DataFrame.from_records(
            utl_input.load_table(self.path, self.separator, self.fields, self.hasHeader)
        )
        df = df.set_index(self.idColumn)
        if not df.index.is_unique:
            raise ValueError(f"Duplicate values found in index column '{self.idColumn}'.")
        return df
