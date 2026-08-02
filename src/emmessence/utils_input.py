import math
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any




def valid_str_tuple(line: str, separator: str, unique = True) -> tuple[str, ...]:
    entries = tuple_with_stripped_values(line, separator)
    if unique:
        ensure_unique_values(entries)
    result = []
    for entry in entries:
        castedEntry = valid_str(entry)
        result.append(castedEntry)
    return tuple(result)

def valid_int_tuple(line: str, separator: str) -> tuple[int, ...]:
    entries = tuple_with_stripped_values(line, separator)
    result = []
    for entry in entries:
        castedEntry = valid_int(entry)
        result.append(castedEntry)
    return tuple(result)

def valid_float_tuple(line: str, separator: str) -> tuple[float, ...]:
    entries = tuple_with_stripped_values(line, separator)
    result = []
    for entry in entries:
        castedEntry = valid_float(entry)
        result.append(castedEntry)
    return tuple(result)

def valid_bool_tuple(line: str, separator: str) -> tuple[bool, ...]:
    entries = tuple_with_stripped_values(line, separator)
    result = []
    for entry in entries:
        castedEntry = valid_bool(entry)
        result.append(castedEntry)
    return tuple(result)


def load_profile(path: str, separator, fields: list[tuple[str, type]]) -> Iterator[dict[str, Any]]:
    try:
        with Path(path).open(encoding="utf-8") as file:
            block = []
            for line in file:
                line = line.strip()
                if not line:
                    block.clear()
                    continue
                block.append(line)
                if len(block) == len(fields):
                    result = parse_profile(block, separator, fields)
                    block.clear()
                    yield result
    except ValueError as err:
        raise ValueError(
            f"\nFile: '{path}'\n"
            f"{err}\n"
        ) from err

def parse_profile(block: list[str], separator: str, fields: list[tuple[str, type]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for line, (attribute, datatype, *thresholds) in zip(block, fields):
        try:
            if (datatype == str):
                castedLine = valid_str(line)
            elif (datatype == int):
                castedLine = valid_int(line)
                check_value_in_range(castedLine, thresholds)
            elif (datatype == float):
                castedLine = valid_float(line)
                check_value_in_range(castedLine, thresholds)
            elif (datatype == bool):
                castedLine = valid_bool(line)
            elif (datatype == tuple[str, ...]):
                castedLine = valid_str_tuple(line, separator)
            elif (datatype == tuple[int, ...]):
                castedLine = valid_int_tuple(line, separator)
                for element in castedLine:
                    check_value_in_range(element, thresholds)
            elif (datatype == tuple[float, ...]):
                castedLine = valid_float_tuple(line, separator)
                for element in castedLine:
                    check_value_in_range(element, thresholds)
            elif (datatype == tuple[bool, ...]):
                castedLine = valid_bool_tuple(line, separator)
            else:
                raise ValueError(
                    f"Datatype '{datatype}' for attribute '{attribute}' is untypical. "
                    f"Use str, int, float, bool instead."
                )
            result[attribute] = castedLine
        except ValueError as err:
            preview = line[:64].rstrip("\n")
            if len(line) > 64:
                preview += "..."
            raise ValueError(
                f"Line: '{preview}'\n"
                f"Reason: {err}"
            ) from err
    return result




def load_table(
    path: str,
    separator: str,
    fields: list[tuple[str, type]],
    hasHeader: bool,
) -> Iterator[dict[str, Any]]:
    try:
        with Path(path).open(encoding="utf-8") as file:
            if(hasHeader):
                next(file, None)
            for line in file:
                if not line:
                    continue
                result = parse_table(line, separator, fields)
                yield result
    except ValueError as err:
        raise ValueError(
            f"\nFile: '{path}'\n"
            f"{err}\n"
        ) from err


def parse_table(
    line: str,
    separator: str,
    fields: list[tuple[str, type]]
) -> dict[str, Any]:
    strippedEntries = tuple_with_stripped_values(line, separator)
    if len(strippedEntries) != len(fields):
        cleanLine = line.rstrip("\n")
        raise ValueError(
            f"Line: '{cleanLine}':\n"
            f"Reason: Expected {len(fields)} columns, got {len(strippedEntries)}."
        )

    result: dict[str, Any] = {}
    for entry, (attribute, datatype, *thresholds) in zip(strippedEntries, fields):
        try:
            if (datatype == str):
                castedEntry = valid_str(entry)
            elif (datatype == int):
                castedEntry = valid_int(entry)
                check_value_in_range(castedEntry, thresholds)
            elif (datatype == float):
                castedEntry = valid_float(entry)
                check_value_in_range(castedEntry, thresholds)
            elif (datatype == bool):
                castedEntry = valid_bool(entry)
            else:
                raise ValueError(
                    f"Datatype '{datatype}' is untypical. "
                    f"Use str, int, float, bool instead."
                )
            result[attribute] = castedEntry
        except ValueError as err:
            clean = line.rstrip("\n")
            raise ValueError(
                f"Line: '{clean}'\n"
                f"Attr: '{attribute}'\n"
                f"Reason: {err}"
            ) from err

    return result




def tuple_with_stripped_values(line: str, separator: str):
    return tuple(entry.strip() for entry in line.split(separator))


def ensure_unique_values(entries: tuple):
    if not len(entries) == len(set(entries)):
        raise ValueError("Values are not unique.")


def valid_str(entry: str):
    if not re.fullmatch(r"[A-Za-z0-9_]+", entry):
        raise ValueError(
            f"Invalid value '{entry}'. Forbidden character(s). "
            f"Only A-Z, a-z, 0-9 and _ are allowed."
        )
    return entry


def valid_bool(entry: str):
    if entry in ("TRUE", "True", "true", "1"):
        return True
    if entry in ("FALSE", "False", "false", "0"):
        return False
    raise ValueError(f"Invalid value '{entry}'. Not allowed for type bool.")


def valid_int(entry: str):
    strippedEntry = entry.strip()
    match = re.fullmatch(r"([+-]?)(\d+)", strippedEntry)
    if not match:
        raise ValueError(f"Invalid int syntax: '{entry}'")
    sign, digits = match.groups()
    if len(digits) > 1 and digits.startswith("0"):
        raise ValueError(f"Invalid value '{entry}'. Leading zeros are not allowed.")
    return int(strippedEntry)


def valid_float(entry: str):
    strippedEntry = entry.strip().lower()

    try:
        result = float(strippedEntry)
    except ValueError:
        raise ValueError(f"Invalid float syntax: '{entry}'")
    if math.isnan(result):
        raise ValueError(f"Invalid value '{entry}'. Not a number.")
    elif math.isinf(result):
        raise ValueError(f"Invalid value '{entry}'. Infinity.")

    mantissa, e, exponent = strippedEntry.partition("e")
    whole, dot, fractional = mantissa.partition(".")

    wholeNoSign = whole.lstrip("+-")
    if len(wholeNoSign) > 1 and wholeNoSign.startswith("0"):
        raise ValueError(
            f"Invalid value '{entry}'. "
            f"Leading zeros in mantissa are not allowed."
        )

    if e:
        exponentNoSign = exponent.lstrip("+-")
        if len(exponentNoSign) > 2 and exponentNoSign.startswith("00"):
            raise ValueError(
                f"Invalid value '{entry}'. "
                f"Leading zeros in exponent are not allowed."
            )

    return result

def check_value_in_range(aValue, twoThresholds):
    if not (len(twoThresholds) == 2
            and aValue >= twoThresholds[0]
            and aValue <= twoThresholds[1]):
        raise ValueError(
            f"Value '{aValue}' is not in the given range "
            f"[{twoThresholds[0]}, {twoThresholds[1]}]."
        )
