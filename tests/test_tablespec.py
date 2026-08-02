import pandas as pd
import pandas.testing as pdt
import pytest

from emmessence.tablespec import TableSpec




def valid_tablespec_factory(
        referenceNames = None,
        path = "aValidPath",
        fields = (
            ("validCol1", str),
            ("validCol2", str),
            ("validCol3", str),
        ),
        table = pd.DataFrame(
            data = {
                "validCol1": ["A", "A"],
                "validCol2": ["B", "B"],
                "validCol3": ["C", "C"]
            }
        ),
        idColumn = "validCol1",
        nonEqualColumnPairs = None,
        hasHeader = True,
    ):
    referenceNames = ["aValidReferenceName"] if referenceNames is None else referenceNames
    nonEqualColumnPairs = [] if nonEqualColumnPairs is None else nonEqualColumnPairs
    return TableSpec(
        referenceNames = referenceNames,
        path = path,
        fields = fields,
        table = table,
        idColumn = idColumn,
        nonEqualColumnPairs = nonEqualColumnPairs,
        hasHeader = hasHeader,
    )




@pytest.mark.parametrize(
    "validIdColumn",
    [
        "validCol1",
        "validCol2",
        "validCol3",
    ]
)
def test_tablespec_validate_idColumn_ok(validIdColumn):
    aTableSpec = valid_tablespec_factory(idColumn = validIdColumn)
    assert aTableSpec.idColumn == validIdColumn


@pytest.mark.parametrize(
    "invalidIdColumn",
    [
        "some",
        "random",
        "column",
        "names",
    ]
)
def test_tablespec_validate_idColumn_fails(invalidIdColumn):
    with pytest.raises(ValueError):
        valid_tablespec_factory(idColumn = invalidIdColumn)


@pytest.mark.parametrize(
    "validNonEqualColumnPairs",
    [
        [("validCol1", "validCol2")],
        [("validCol1", "validCol3")],
        [("validCol1", "validCol2"), ("validCol2", "validCol3")],
        (("validCol1", "validCol2"), ("validCol2", "validCol3")),
    ]
)
def test_validate_nonEqualColumnPairs_ok(validNonEqualColumnPairs):
    aTableSpec = valid_tablespec_factory(
        nonEqualColumnPairs = validNonEqualColumnPairs
    )
    assert aTableSpec.nonEqualColumnPairs == list(validNonEqualColumnPairs)


@pytest.mark.parametrize(
    "nonEqualColumnPairsForTypeError",
    [
        set(),
        {1, 2, 3},
        dict(),
        {"a": 1, "b": 2},
        "string",
        42,

        ["validCol1", "validCol2"],
        [(42, 43)],
        [("validCol1",)],
        [("validCol1", "validCol1")],
        [["validCol1", "validCol2"]],
        [("validCol1", "validCol2", "validCol3")]
    ]
)
def test_validate_nonEqualColumnPairs_typeError(nonEqualColumnPairsForTypeError):
    with pytest.raises(TypeError):
        valid_tablespec_factory(
            nonEqualColumnPairs = nonEqualColumnPairsForTypeError
        )


@pytest.mark.parametrize(
    "nonEqualColumnPairsForValueError",
    [
        [("validCol4", "validCol5")],
        [("validCol1", "validCol4")],
        [("validCol1", "validCol2"), ("validCol1", "validCol4")],
    ]
)
def test_validate_nonEqualColumnPairs_valueError(nonEqualColumnPairsForValueError):
    with pytest.raises(ValueError):
        valid_tablespec_factory(
            nonEqualColumnPairs = nonEqualColumnPairsForValueError
        )


@pytest.mark.parametrize(
    "validHasHeader",
    [
        True,
        False,
    ]
)
def test_validate_hasHeader_ok(validHasHeader):
    aTableSpec = valid_tablespec_factory(hasHeader = validHasHeader)
    assert aTableSpec.hasHeader == validHasHeader


@pytest.mark.parametrize(
    "invalidHasHeader",
    [
        1,
        0,
        "string"
        'A',
        [],
        (),
        list(),
        set(),
        dict(),
        {},
        2.0,
    ]
)
def test_validate_hasHeader_fails(invalidHasHeader):
    with pytest.raises(TypeError):
        valid_tablespec_factory(hasHeader = invalidHasHeader)


def test_validate_differing_columns_ok():
    validTable = pd.DataFrame(
        data = {
            "validCol1": ["A", "A"],
            "validCol2": ["B", "B"],
        }
    )
    validNonEqualColumnPairs = [("validCol1", "validCol2")]
    aTableSpec = valid_tablespec_factory(
        table = validTable,
        nonEqualColumnPairs = validNonEqualColumnPairs,
    )
    pdt.assert_frame_equal(aTableSpec.table, validTable)
    assert aTableSpec.nonEqualColumnPairs == validNonEqualColumnPairs


def test_validate_differing_columns_fails():
    with pytest.raises(ValueError):
        valid_tablespec_factory(
            table = pd.DataFrame(
                data = {
                    "validCol1": ["A", "A"],
                    "validCol2": ["B", "A"],
                }
            ),
            nonEqualColumnPairs = [("validCol1", "validCol2")],
        )
