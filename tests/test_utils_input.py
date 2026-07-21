from emmessence.utils_input import ensure_unique_values
from emmessence.utils_input import valid_str, valid_bool, valid_int, valid_float
from emmessence.utils_input import parse_table

import pytest




@pytest.fixture
def sep():
    return ","

@pytest.fixture
def spec():
    return [
        ("myString", str),
        ("myInt", int, float("-inf"), float("inf")),
        ("myFloat", float, float("-inf"), float("inf")),
        ("myBool", bool),
    ]




@pytest.mark.parametrize(
    "entriesA",
    [
        ("a", "b", "c"),
        (),
    ]
)
def test_ensure_unique_values_ok(entriesA):
    ensure_unique_values(entriesA)


@pytest.mark.parametrize(
    "nonuniqueValues",
    [
        ("a", "a"),
        ("", ""),
        ("a", "b", "a"),
    ]
)
def test_ensure_unique_values_raises(nonuniqueValues):
    with pytest.raises(ValueError):
        ensure_unique_values(nonuniqueValues)


@pytest.mark.parametrize(
    "validString",
    [
        "123",
        "abc",
        "ABC",
        "_",
        "my_name",
        "_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    ]
)
def test_valid_str_ok(validString):
    assert valid_str(validString) == str(validString)


@pytest.mark.parametrize(
    "invalidString",
    [
        "",
        " ",
        "a b"
        " ab",
        "ab ",
        "äöü",
        "+1",
    ]
)
def test_valid_str_raises(invalidString):
    with pytest.raises(ValueError):
        valid_str(invalidString)


@pytest.mark.parametrize(
    "validTrueValues",
    [
        "TRUE",
        "True",
        "true",
        "1"
    ]
)
def test_valid_bool_returns_true(validTrueValues):
    assert valid_bool(validTrueValues) is True


@pytest.mark.parametrize(
    "validFalseValues",
    [
        "FALSE",
        "False",
        "false",
        "0"
    ]
)
def test_valid_bool_returns_false(validFalseValues):
    assert valid_bool(validFalseValues) is False


@pytest.mark.parametrize(
    "invalidBool",
    [
        "true ", " true", "tr ue",
        "falsE", "truE",
        "yes", "y", "Y",
        "no", "n", "N",
        "00", "01", " 0", " 1",
        "0\n", "1\n",
    ]
)
def test_valid_bool_raises(invalidBool):
    with pytest.raises(ValueError):
        valid_bool(invalidBool)


@pytest.mark.parametrize(
    "validInt",
    [
        "12",
        " 12", "12 ", " 12 ",
        " +12", " -12", "+12 ", "-12 ",
    ]
)
def test_valid_int_ok(validInt):
    assert valid_int(validInt) == int(validInt.strip())


@pytest.mark.parametrize(
    "invalidInt",
    [
        "", " ", "+", "-",
        "1 2",
        "+ 1", "- 1",
        "1+", "1-",
        "++1", "--1",
        "1.2",
        "00", "01", "+01", "-01",
        "1a",
    ]
)
def test_valid_int_raises(invalidInt):
    with pytest.raises(ValueError):
        valid_int(invalidInt)


@pytest.mark.parametrize(
    "validFloat",
    [
        "12.0", "+12.0", "-12.0",
        ".5", "+.5", "-.5",
        " 12.0", "12.0 ", " 12.0 ",
        " +12.0", " -12.0", "+12.0 ", "-12.0 ",
        "1e2", "1E2", "1e+2", "1E-2",
        "1e02", "1E02", "1e+02", "1E-02",
    ]
)
def test_valid_float_ok(validFloat):
    assert valid_float(validFloat) == float(validFloat.strip())


@pytest.mark.parametrize(
    "invalidFloat",
    [
        "", " ", "+", "-",
        "inf", " inf", "inf ", " inf ", "nan", " nan", "nan ", " nan ",
        "1 2", "1 2.0", "1 2e3",
        "+ 1", "- 1", "+ 1.0", "- 1.0", "+ 1e3", "- 1e3",
        "1+", "1-", "1.0+", "1-.0", "1e3+", "1-e3",
        "++1", "--1", "++1.0", "--1.0", "++1e3", "--1e3",
        "1.2.0", "1e2.3",
        "00", "01", "+01", "-01", "00.0", "01.0", "+01.0", "-01.0",
        "00e3", "01e3", "+01e3", "-01e3",
        "1a", "1.0a", "1e3a",
    ]
)
def test_valid_float_raises(invalidFloat):
    with pytest.raises(ValueError):
        valid_float(invalidFloat)


def test_parse_valid_line(sep, spec):
    line = f"Line{sep}7{sep}0.5{sep}1"
    values = parse_table(line, sep, spec)
    assert values["myString"] == "Line"
    assert values["myInt"] == 7
    assert values["myFloat"] == 0.5
    assert values["myBool"]


def test_parse_strips_outer_spaces_ok(sep, spec):
    line = f" Line {sep} 7 {sep} 0.5 {sep} 1 "
    values = parse_table(line, sep, spec)
    assert values["myString"] == "Line"
    assert values["myInt"] == 7
    assert values["myFloat"] == 0.5
    assert values["myBool"]


def test_parse_wrong_column_count_too_few(sep, spec):
    line = f"Line{sep}7{sep}0.5"
    with pytest.raises(ValueError):
        parse_table(line, sep, spec)


def test_parse_wrong_column_count_too_many(sep, spec):
    line = f"Line{sep}7{sep}0.5{sep}1{sep}EXTRA"
    with pytest.raises(ValueError):
        parse_table(line, sep, spec)


def test_parse_whitespace_inside_field_should_fail(sep, spec):
    line = f"Li ne{sep}7{sep}0.5{sep}1"
    with pytest.raises(ValueError):
        parse_table(line, sep, spec)


@pytest.mark.parametrize(
    "invalidLineA",
    [
        f"{sep}7{sep}0.5{sep}1",
        f"Line{sep}{sep}0.5{sep}1",
        f"Line{sep}{sep}{sep}1",
        f"Line{sep}7{sep}0.5{sep}",
    ]
)
def test_parse_empty_string_should_fail(invalidLineA, sep, spec):
    with pytest.raises(ValueError):
        parse_table(invalidLineA, sep, spec)


@pytest.mark.parametrize(
    "invalidLineB",
    [
        f"Line{sep}{sep}0.5{sep}1",
        f"Line{sep}None{sep}0.5{sep}1",
        f"Line{sep}nan{sep}0.5{sep}1",
        f"Line{sep}inf{sep}0.5{sep}1",
        f"Line{sep}-inf{sep}0.5{sep}1",
        f"Line{sep}7.0{sep}0.5{sep}1",
        f"Line{sep}7 0{sep}0.5{sep}1",
        f"Line{sep}7aa{sep}0.5{sep}1",
        f"Line{sep}7+{sep}0.5{sep}1",
        f"Line{sep}7+1{sep}0.5{sep}1",
        f"Line{sep}07{sep}0.5{sep}1",
        f"Line{sep}+07{sep}0.5{sep}1",
        f"Line{sep}-07{sep}0.5{sep}1",
        f"Line{sep}007{sep}0.5{sep}1"
    ]
)
def test_parse_invalid_int_cast_should_fail(invalidLineB, sep, spec):
    with pytest.raises(ValueError):
        parse_table(invalidLineB, sep, spec)


@pytest.mark.parametrize(
    "invalidLineC",
    [
        f"Line{sep}7{sep}{sep}1",
        f"Line{sep}7{sep}None{sep}1",
        f"Line{sep}7{sep}nan{sep}1",
        f"Line{sep}7{sep}inf{sep}1",
        f"Line{sep}7{sep}-inf{sep}1",
        f"Line{sep}7{sep}0 5{sep}1",
        f"Line{sep}7{sep}0aa{sep}1",
        f"Line{sep}7{sep}0+{sep}1",
        f"Line{sep}7{sep}0+5{sep}1",
        f"Line{sep}7{sep}05{sep}1",
        f"Line{sep}7{sep}+05{sep}1",
        f"Line{sep}7{sep}-05{sep}1",
        f"Line{sep}7{sep}00{sep}1",
        f"Line{sep}7{sep}00.5{sep}1",
        f"Line{sep}7{sep}+00.5{sep}1",
        f"Line{sep}7{sep}-00.5{sep}1",
        f"Line{sep}7{sep}-00.5e12{sep}1",
        f"Line{sep}7{sep}-00.5E12{sep}1"
    ]
)
def test_parse_invalid_float_cast_should_fail(invalidLineC, sep, spec):
    with pytest.raises(ValueError):
        parse_table(invalidLineC, sep, spec)


@pytest.mark.parametrize(
    "invalidLineD",
    [
        f"Line{sep}7{sep}0.5",
        f"Line{sep}7{sep}0.5{sep}",
        f"Line{sep}7{sep}0.5{sep}None",
        f"Line{sep}7{sep}0.5{sep}nan",
        f"Line{sep}7{sep}0.5{sep}inf",
        f"Line{sep}7{sep}0.5{sep}-inf",
        f"Line{sep}7{sep}0.5{sep}1 0",
        f"Line{sep}7{sep}0.5{sep}1aa",
        f"Line{sep}7{sep}0.5{sep}1+",
        f"Line{sep}7{sep}0.5{sep}1+0",
        f"Line{sep}7{sep}0.5{sep}10",
        f"Line{sep}7{sep}0.5{sep}01",
        f"Line{sep}7{sep}0.5{sep}00",
        f"Line{sep}7{sep}0.5{sep}trUe",
        f"Line{sep}7{sep}0.5{sep}yes",
        f"Line{sep}7{sep}0.5{sep}y",
        f"Line{sep}7{sep}0.5{sep}ja",
        f"Line{sep}7{sep}0.5{sep}faLse",
        f"Line{sep}7{sep}0.5{sep}no",
        f"Line{sep}7{sep}0.5{sep}n",
        f"Line{sep}7{sep}0.5{sep}nein"
    ]
)
def test_parse_invalid_bool_cast_should_fail(invalidLineD, sep, spec):
    with pytest.raises(ValueError):
        parse_table(invalidLineD, sep, spec)
