from dataclasses import dataclass
from typing import override

import pandas as pd
import pandas.testing as pdt
import pytest

from emmessence.spec import Spec, _is_nonnumeric_field, _is_numeric_field




@dataclass
class DummySpec(Spec):
    @override
    def _values_need_definitions(self):
        return False
    
    @override
    def _get_dataframe_from_csv(self):
        return self.table
    
    @override
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




def valid_dummyspec_factory(
    referenceNames = None,
    path = "aValidPath",
    fields = (
        ("key", str),
        ("val", int, 0.0, 9.0),
    ),
    separator = ",",
    table = pd.DataFrame(
        data = {
            "key": ["K1", "K2", "K3"],
            "val": [4, 5, 6]
        }
    ).set_index("key"),
    parents = None,
    excludedKeys = None,
):
    referenceNames = ["aValidReferenceName"] if referenceNames is None else referenceNames
    parents = [] if parents is None else parents
    excludedKeys = [] if excludedKeys is None else excludedKeys
    return DummySpec(
        referenceNames = referenceNames,
        path = path,
        fields = fields,
        separator = separator,
        parents = parents,
        excludedKeys = excludedKeys,
        table = table,
)




@pytest.mark.parametrize(
    "validReferenceNames",
    [
        ["a"],
        ["abc", "def"],
        ["string", "string"],
    ]
)
def test_spec_referenceNames_ok(validReferenceNames):
    aSpec = valid_dummyspec_factory(referenceNames = validReferenceNames)
    assert aSpec.referenceNames == validReferenceNames


@pytest.mark.parametrize(
    "referenceNamesForTypeError",
    [
        "aString",
        0,
        1,
        123,
        2.3,
        True,
        set(),
        dict(),
        {},
        [""],
        ["string", "string", 3],
        ["string", True, "string"],
        [set(), "string", "string"],
        ["string", "string", ["string", "string"]],
    ]
)
def test_spec_referenceNames_typeError(referenceNamesForTypeError):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(referenceNames = referenceNamesForTypeError)


@pytest.mark.parametrize(
    "emptySequences",
    [
        tuple(),
        (),
        list(),
        [],
    ]
)
def test_spec_referenceNames_valueError(emptySequences):
    with pytest.raises(ValueError):
        valid_dummyspec_factory(referenceNames = emptySequences)


@pytest.mark.parametrize(
    "validPathNames",
    [
        " ",
        "a",
        "C:/myFolder1/myFolder2/myFile",
    ]
)
def test_spec_pathNames_ok(validPathNames):
    aSpec = valid_dummyspec_factory(path = validPathNames)
    assert aSpec.path == validPathNames


@pytest.mark.parametrize(
    "pathNameForTypeError",
    [
        "",
        0,
        2.3,
        True,
        list(),
        set(),
        dict(),
    ]
)
def test_spec_pathNames_typeError(pathNameForTypeError):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(path = pathNameForTypeError)


@pytest.mark.parametrize(
    "validFields",
    [
        (("validNonnumericKey", str),),
        (("validNumericKey", float, 0.0, 1.0),),
    ]
)
def test_validate_fields_ok(validFields):
    aSpec = valid_dummyspec_factory(fields = validFields)
    assert aSpec.fields == validFields


@pytest.mark.parametrize(
    "fieldsForTypeError",
    [
        "str",
        'A',
        2,
        2.0,
        True,
        [1, 2, 3],
        list(),
        [],
        set(),
        dict(),
        {},
    ]
)
def test_validate_fields_fails(fieldsForTypeError):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(fields = fieldsForTypeError)


@pytest.mark.parametrize(
    "validNonnumericNoTuple",
    [
        ("validKey", str),
        ("validKey", bool),
    ]
)
def test_is_nonnumeric_field_no_tuple_ok(validNonnumericNoTuple):
    assert(
        _is_nonnumeric_field(
            item = validNonnumericNoTuple,
            tuplesAllowed = False
        )
    )


@pytest.mark.parametrize(
    "invalidNonnumericNoTuple",
    [
        ("validKey", int),
        ("validKey", float),
        ("validKey", tuple[str, ...]),
        ("validKey", tuple[bool, ...]),

        ("validKey"),
        ("validKey",),
        ("validKey", ...),
        ("validKey", str, str),
        ("validKey", bool, bool),
        (str),
        (str,),
        (str, ...),

        (2, str),
        (2.0, str),
        (True, str),
        (bool, str),

        "str",
        'A',
        2,
        2.0,
        True,
        [1, 2, 3],
        list(),
        [],
        set(),
        dict(),
        {},
        tuple(),
        (),
    ]
)
def test_is_nonnumeric_field_no_tuple_fails(invalidNonnumericNoTuple):
    assert(
        not _is_nonnumeric_field(
            item = invalidNonnumericNoTuple,
            tuplesAllowed = False
        )
    )


@pytest.mark.parametrize(
    "validNonnumericWithTuple",
    [
        ("validKey", str),
        ("validKey", bool),
        ("validKey", tuple[str, ...]),
        ("validKey", tuple[bool, ...]),
    ]
)
def test_is_nonnumeric_field_with_tuple_ok(validNonnumericWithTuple):
    assert(
        _is_nonnumeric_field(
            item = validNonnumericWithTuple,
            tuplesAllowed = True
        )
    )


@pytest.mark.parametrize(
    "invalidNonnumericWithTuple",
    [
        ("validKey", int),
        ("validKey", float),

        ("validKey"),
        ("validKey",),
        ("validKey", ...),
        ("validKey", str, str),
        ("validKey", bool, bool),
        (str),
        (str,),
        (str, ...),

        (2, str),
        (2.0, str),
        (True, str),
        (bool, str),

        "str",
        'A',
        2,
        2.0,
        True,
        [1, 2, 3],
        list(),
        [],
        set(),
        dict(),
        {},
        tuple(),
        (),
    ]
)
def test_is_nonnumeric_field_with_tuple_fails(invalidNonnumericWithTuple):
    assert(
        not _is_nonnumeric_field(
            item = invalidNonnumericWithTuple,
            tuplesAllowed = True
        )
    )


@pytest.mark.parametrize(
    "validNumericNoTuple",
    [
        ("validKey", int, 0.0, 1.0),
        ("validKey", float, 0.0, 1.0),
    ]
)
def test_is_numeric_field_no_tuple_ok(validNumericNoTuple):
    assert(
        _is_numeric_field(
            item = validNumericNoTuple,
            tuplesAllowed = False
        )
    )


@pytest.mark.parametrize(
    "invalidNumericNoTuple",
    [
        ("validKey", str),
        ("validKey", bool),
        ("validKey", tuple[int, ...], 0.0, 1.0),
        ("validKey", tuple[float, ...], 0.0, 1.0),

        ("validKey"),
        ("validKey",),
        ("validKey", ...),
        ("validKey", int, 0.0, 1.0, 2.0),
        ("validKey", float, 0.0, 1.0, 2.0),
        (int),
        (int,),
        (int, ...),

        (2, int, 0.0, 1.0),
        (2.0, int, 0.0, 1.0),
        (True, int, 0.0, 1.0),
        (bool, int, 0.0, 1.0),

        "str",
        'A',
        2,
        2.0,
        True,
        [1, 2, 3],
        list(),
        [],
        set(),
        dict(),
        {},
        tuple(),
        (),
    ]
)
def test_is_numeric_field_no_tuple_fails(invalidNumericNoTuple):
    assert(
        not _is_numeric_field(
            item = invalidNumericNoTuple,
            tuplesAllowed = False
        )
    )


@pytest.mark.parametrize(
    "validNumericWithTuple",
    [
        ("validKey", int, 0.0, 1.0),
        ("validKey", float, 0.0, 1.0),
        ("validKey", tuple[int, ...], 0.0, 1.0),
        ("validKey", tuple[float, ...], 0.0, 1.0),
    ]
)
def test_is_numeric_field_with_tuple_ok(validNumericWithTuple):
    assert(
        _is_numeric_field(
            item = validNumericWithTuple,
            tuplesAllowed = True
        )
    )


@pytest.mark.parametrize(
    "invalidNumericWithTuple",
    [
        ("validKey", str),
        ("validKey", bool),

        ("validKey"),
        ("validKey",),
        ("validKey", ...),
        ("validKey", int, 0.0, 1.0, 2.0),
        ("validKey", float, 0.0, 1.0, 2.0),
        (int),
        (int,),
        (int, ...),

        (2, int, 0.0, 1.0),
        (2.0, int, 0.0, 1.0),
        (True, int, 0.0, 1.0),
        (bool, int, 0.0, 1.0),

        "str",
        'A',
        2,
        2.0,
        True,
        [1, 2, 3],
        list(),
        [],
        set(),
        dict(),
        {},
        tuple(),
        (),
    ]
)
def test_is_numeric_field_with_tuple_fails(invalidNumericWithTuple):
    assert(
        not _is_numeric_field(
            item = invalidNumericWithTuple,
            tuplesAllowed = True
        )
    )


@pytest.mark.parametrize(
    "validSeparator",
    [
        ",",
        ";",
        "\t",
    ]
)
def test_validate_separator_ok(validSeparator):
    aTableSpec = valid_dummyspec_factory(separator = validSeparator)
    assert aTableSpec.separator == validSeparator


@pytest.mark.parametrize(
    "invalidSeparatorType",
    [
        tuple(),
        4.5,
        True,
    ]
)
def test_validate_separator_typeError(invalidSeparatorType):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(separator = invalidSeparatorType)


@pytest.mark.parametrize(
    "invalidSeparatorValue",
    [
        "",
        " ",
        "-",
    ]
)
def test_validate_separator_valueError(invalidSeparatorValue):
    with pytest.raises(ValueError):
        valid_dummyspec_factory(separator = invalidSeparatorValue)


@pytest.mark.parametrize(
    "validParents",
    [
        [],
        [valid_dummyspec_factory()],
        [valid_dummyspec_factory(), valid_dummyspec_factory()],
        (),
        (valid_dummyspec_factory(),),
        (valid_dummyspec_factory(), valid_dummyspec_factory()),
    ]
)
def test_validate_parents_ok(validParents):
    aTableSpec = valid_dummyspec_factory(parents = validParents)
    assert aTableSpec.parents == list(validParents)


@pytest.mark.parametrize(
    "invalidParents",
    [
        valid_dummyspec_factory(),
        (valid_dummyspec_factory()),
        "str",
        2.0,
        [valid_dummyspec_factory(), ...],
        [valid_dummyspec_factory(), 0.0],
        [valid_dummyspec_factory(), "str"],
    ]
)
def test_validate_parents_fails(invalidParents):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(parents = invalidParents)


@pytest.mark.parametrize(
    "validExcludedKeys",
    [
        ["a"],
        ["abc", "def"],
        ["string", "string"],
    ]
)
def test_spec_excludedKeys_ok(validExcludedKeys):
    aSpec = valid_dummyspec_factory(referenceNames = validExcludedKeys)
    assert aSpec.referenceNames == validExcludedKeys

@pytest.mark.parametrize(
    "emptySequences",
    [
        tuple(),
        (),
        list(),
        [],
    ]
)
def test_validate_excludedKeys_emptiness_ok(emptySequences):
    aSpec = valid_dummyspec_factory(excludedKeys = emptySequences)
    assert aSpec.excludedKeys == list(emptySequences)


@pytest.mark.parametrize(
    "excludedKeysForTypeError",
    [
        "aString",
        0,
        1,
        123,
        2.3,
        True,
        set(),
        dict(),
        {},
        [""],
        ["string", "string", 3],
        ["string", True, "string"],
        [set(), "string", "string"],
        ["string", "string", ["string", "string"]],
    ]
)
def test_validate_excludedKeys_typeError(excludedKeysForTypeError):
    with pytest.raises(TypeError):
        valid_dummyspec_factory(excludedKeys = excludedKeysForTypeError)


def test_spec_enrich_with_dataframe_ok():
    expectedTable = pd.DataFrame(
        data = {
            "key": ["K1", "K2", "K3"],
            "val": [4, 5, 6]
        }
    ).set_index("key")
    aSpec = valid_dummyspec_factory()
    pdt.assert_frame_equal(aSpec.table, expectedTable)


def test_spec_enrich_with_dataframe_fails():
    with pytest.raises(RuntimeError):
        valid_dummyspec_factory(table = None)


@pytest.mark.parametrize(
    "validDroppingKeys, expectedResultingKeys",
    [
        (["K1"], ("K2", "K3",)),
        (["K2", "K3"], ("K1",)),
        (["K1", "K2", "K3"], tuple()),
    ]
)
def test_drop_excludedKeys_ok(validDroppingKeys, expectedResultingKeys):
    aSpec = valid_dummyspec_factory(excludedKeys = validDroppingKeys)
    assert(tuple(aSpec.table.index) == expectedResultingKeys)


def test_drop_excludedKeys_warn():
    with pytest.warns(UserWarning):
        aSpec = valid_dummyspec_factory(excludedKeys = ["K"])
    assert(tuple(aSpec.table.index) == ("K1", "K2", "K3",))
