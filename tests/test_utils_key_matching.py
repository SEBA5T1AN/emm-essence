import pandas as pd
import pytest

from emmessence.tablespec import TableSpec
from emmessence.utils_key_matching import (
    any_root_usage,
    exclusion_chain_reaction,
    get_keys_in_definition,
    get_keys_in_use,
)



"""
                    key, midType1                               key, midType2
                    --------------                              --------------
                    top10, no                                   top20, mid21
                    top11, mid10                                top21, mid28
                    top12, mid11                                top22, mid29
                    top13, mid17                                top23, mid22
                    --------------                              --------------
                          |                                           |
                          |                                           |
key, wC00, wC01     key, botType10, wC10                        key, botType10, botType20, wC20
--------------      --------------------------------------      --------------------------------------
mid00, no, no       mid10, (u1d0p0B, u1d1p0B, u1d0p1B), no      mid20, (u0d0p1A, u0d1p0A), u0d1p1A, no
mid01, no, no       mid11, u1d1p1C, no                          mid21, u1d1p1A, u1d1p0A, no
mid02, no, no       mid12, (u0d0p1B, u0d1p1B, u0d1p0B), no      mid22, u1d0p0A, (u1d0p1A,u1d1p1B), no
--------------      --------------------------------------      --------------------------------------
      |                                 |                             |
      |_________________________________|_____________________________|
                                        |
                                    key, attr
                                    ------------
                                    u0d1p0A, no
                                    u0d1p0B, no
                                    u0d1p1A, no
                                    u0d1p1B, no
                                    u1d1p0A, no
                                    u1d1p0B, no
                                    u1d1p1A, no
                                    u1d1p1B, no
                                    u1d1p1C, no
                                    u0d1, no
                                    ------------
"""



@pytest.fixture
def TOP_1_DATA():
    return TableSpec(
        referenceNames = ["topType1"],
        parents = [],
        path = "top1.txt",
        fields = (
            ("key", str),
            ("midType1", str),
        ),
        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "midType1": [
                    "no",
                    "mid10",
                    "mid11",
                    "mid17",
                ],
            },
            index=[
                "top10",
                "top11",
                "top12",
                "top13",
            ],
        )
    )


@pytest.fixture
def TOP_2_DATA():
    return TableSpec(
        referenceNames = ["topType2"],
        parents = [],
        path = "top2.txt",
        fields = (
            ("key", str),
            ("midType2", str),
        ),
        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "midType2": [
                    "mid21",
                    "mid28",
                    "mid29",
                    "mid22",
                ],
            },
            index = [
                "top20",
                "top21",
                "top22",
                "top23",
            ],
        )
    )


@pytest.fixture
def MID_0_DATA():
    return TableSpec(
        referenceNames = ["midType0"],
        parents = [],
        path = "mid0.txt",
        fields = (
            ("key", str),
            ("wrongCol00", str),
            ("wrongCol01", str),
        ),
        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "wrongCol00": [
                    "no",
                    "no",
                    "no",
                ],
                "wrongCol01": [
                    "no",
                    "no",
                    "no",
                ],
            },
            index = [
                "mid00",
                "mid01",
                "mid02",
            ],
        )
    )


@pytest.fixture
def MID_1_DATA(TOP_1_DATA):
    return TableSpec(
        referenceNames = ["midType1"],
        parents = [TOP_1_DATA],
        path = "mid1.txt",
        fields = (
            ("key", str),
            ("botType10", str),
            ("wrongCol10", str),
        ),
        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "botType10": [
                    ("u1d0p0B", "u1d1p0B", "u1d0p1B"),
                    "u1d1p1C",
                    ("u0d0p1B", "u0d1p1B", "u0d1p0B"),
                ],
                "wrongCol10": [
                    "no",
                    "no",
                    "no",
                ],
            },
            index = [
                "mid10",
                "mid11",
                "mid12",
            ],
        )
    )


@pytest.fixture
def MID_2_DATA(TOP_2_DATA):
    return TableSpec(
        referenceNames = ["midType2"],
        parents = [TOP_2_DATA],
        path = "mid2.txt",
        fields = (
            ("key", str),
            ("botType10", str),
            ("botType20", str),
            ("wrongCol20", str),
        ),

        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "botType10": [
                    ("u0d0p1A", "u0d1p0A"),
                    "u1d1p1A",
                    "u1d0p0A",
                ],
                "botType20": [
                    "u0d1p1A",
                    "u1d1p0A",
                    ("u1d0p1A", "u1d1p1B"),
                ],
                "wrongCol20": [
                    "no",
                    "no",
                    "no",
                ],
            },
            index = [
                "mid20",
                "mid21",
                "mid22",
            ],
        )
    )


@pytest.fixture
def BOT_DATA(MID_0_DATA, MID_1_DATA, MID_2_DATA):
    return TableSpec(
        referenceNames = ["botType10", "botType20"],
        parents = [MID_0_DATA, MID_1_DATA, MID_2_DATA],
        path = "bot.txt",
        fields = (
            ("key", str),
            ("attr", str),
        ),
        idColumn = "key",
        hasHeader = True,
        table = pd.DataFrame(
            {
                "attr": [
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                    "no",
                ]
            },
            index = [
                "u0d1p0A",
                "u0d1p0B",
                "u0d1p1A",
                "u0d1p1B",
                "u1d1p0A",
                "u1d1p0B",
                "u1d1p1A",
                "u1d1p1B",
                "u1d1p1C",
                "u0d1",
            ],
        )
    )




@pytest.mark.parametrize(
    "fixtureNameA, expectedA",
    [
        (
            "BOT_DATA",
            set([
                "u1d0p0B",
                "u1d1p0B",
                "u1d0p1B",
                "u0d0p1A",
                "u0d1p0A",
                "u0d1p1A",
                "u1d1p1C",
                "u1d1p1A",
                "u1d1p0A",
                "u0d0p1B",
                "u0d1p1B",
                "u0d1p0B",
                "u1d0p0A",
                "u1d0p1A",
                "u1d1p1B",
            ]),
        ),

        (
            "MID_1_DATA",
            set([
                "no",
                "mid10",
                "mid11",
                "mid17",
            ]),
        ),

        (
            "MID_2_DATA",
            set([
                "mid21",
                "mid28",
                "mid29",
                "mid22",
            ]),
        ),
    ]
)
def test_get_keys_in_parents_use_ok(request, fixtureNameA, expectedA):
    dataobjectA = request.getfixturevalue(fixtureNameA)
    assert get_keys_in_use(dataobjectA, traceToRoot = False) == expectedA


def test_get_keys_in_roots_use_ok(BOT_DATA):
    assert get_keys_in_use(subject = BOT_DATA, traceToRoot = True) == set([
        "u1d0p0A",
        "u1d0p0B",
        "u1d0p1A",
        "u1d0p1B",
        "u1d1p0A",
        "u1d1p0B",
        "u1d1p1A",
        "u1d1p1B",
        "u1d1p1C",
    ])


@pytest.mark.parametrize(
    "fixtureNameB, expectedB",
    [
        (
            "BOT_DATA",
            set([
                "u0d1p0A",
                "u0d1p0B",
                "u0d1p1A",
                "u0d1p1B",
                "u1d1p0A",
                "u1d1p0B",
                "u1d1p1A",
                "u1d1p1B",
                "u1d1p1C",
                "u0d1",
            ]),
        ),

        (
            "MID_0_DATA",
            set([
                "mid00",
                "mid01",
                "mid02",
            ]),
        ),

        (
            "MID_1_DATA",
            set([
                "mid10",
                "mid11",
                "mid12",
            ]),
        ),

        (
            "MID_2_DATA",
            set([
                "mid20",
                "mid21",
                "mid22",
            ]),
        ),

        (
            "TOP_1_DATA",
            set([
                "top10",
                "top11",
                "top12",
                "top13",
            ]),
        ),

        (
            "TOP_2_DATA",
            set([
                "top20",
                "top21",
                "top22",
                "top23",
            ]),
        ),
    ]
)
def test_get_keys_in_definition_ok(request, fixtureNameB, expectedB):
    dataobjectB = request.getfixturevalue(fixtureNameB)
    assert get_keys_in_definition(dataobjectB) == expectedB


@pytest.mark.parametrize(
    "fixtureNameC, expectedC",
    [
        (
            "BOT_DATA",
            set([
                "u1d0p0B",
                "u1d0p1B",
                "u0d0p1A",
                "u0d0p1B",
                "u1d0p0A",
                "u1d0p1A",
            ]),
        ),

        (
            "MID_1_DATA",
            set([
                "mid17",
                "no",
            ]),
        ),

        (
            "MID_2_DATA",
            set([
                "mid28",
                "mid29",
            ]),
        ),
    ]
)
def test_used_via_parents_but_undefined_keys_ok(request, fixtureNameC, expectedC):
    dataobjectC = request.getfixturevalue(fixtureNameC)
    keysInUse = get_keys_in_use(subject = dataobjectC, traceToRoot = False)
    keysInDef = get_keys_in_definition(subject = dataobjectC)
    keysNoDef = keysInUse - keysInDef
    assert keysNoDef == expectedC


def test_used_via_roots_but_undefined_keys_ok(BOT_DATA):
    keysInUse = get_keys_in_use(subject = BOT_DATA, traceToRoot = True)
    keysInDef = get_keys_in_definition(subject = BOT_DATA)
    keysNoDef = keysInUse - keysInDef
    assert keysNoDef == set([
        "u1d0p0A",
        "u1d0p0B",
        "u1d0p1A",
        "u1d0p1B",
    ])


def test_unused_but_defined_keys_ok(BOT_DATA):
    keysInUse = get_keys_in_use(subject = BOT_DATA, traceToRoot = False)
    keysInDef = get_keys_in_definition(subject = BOT_DATA)
    keysNoUse = keysInDef - keysInUse
    assert keysNoUse == set(["u0d1",])


@pytest.mark.parametrize(
    "fixtureNameD, keyInDefinition, expectedRootUse",
    [
        ("BOT_DATA", "u0d1p0A", False),
        ("BOT_DATA", "u0d1p0B", False),
        ("BOT_DATA", "u0d1p1A", False),
        ("BOT_DATA", "u0d1p1B", False),
        ("BOT_DATA", "u1d1p0A", True),
        ("BOT_DATA", "u1d1p0B", True),
        ("BOT_DATA", "u1d1p1A", True),
        ("BOT_DATA", "u1d1p1B", True),
        ("BOT_DATA", "u1d1p1C", True),
        ("BOT_DATA", "u0d1", False),
    ]
)
def test_any_root_usage_ok(request, fixtureNameD, keyInDefinition, expectedRootUse):
    dataobjectD = request.getfixturevalue(fixtureNameD)
    assert(
        any_root_usage(
            subject = dataobjectD,
            keySubset = [keyInDefinition]
        ) == expectedRootUse
    )


def test_exclusion_chain_reaction_ok(BOT_DATA, MID_1_DATA, TOP_1_DATA):
    exclusion_chain_reaction(
        subject = BOT_DATA,
        keySubset = ["u1d1p0B"]
    )
    assert BOT_DATA.excludedKeys == []
    assert MID_1_DATA.excludedKeys == ["mid10"]
    assert TOP_1_DATA.excludedKeys == ["top11"]
