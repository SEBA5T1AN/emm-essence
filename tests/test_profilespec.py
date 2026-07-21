from emmessence.profilespec import ProfileSpec
from emmessence.profilespec import _pair_combinations
from emmessence.profilespec import _map_profiles
from emmessence.profilespec import object_profile_matrix

import pytest

import pandas as pd
import pandas.testing as pdt
import numpy as np
import numpy.testing as npt




def valid_profilespec_factory(
        referenceNames = None,
        path = "aValidPath",
        fields = None,
        tabledata = None,
        idRow = "key",
        nodeRow = "node",
        typeRow = "type",
        tsRow = "timeseries",
        timesteps = 4,
        defaultValue = 1.0,
        newTimeseries = None,
        keysMatter = False,
    ):
    referenceNames = ["aValidReferenceName"] if referenceNames is None else referenceNames
    
    if fields is None:
        fields = (
            ("key", str),
            ("node", tuple[str, ...]),
            ("type", tuple[str, ...]),
            ("timeseries", tuple[float, ...], 0.0, 1.0),
            ("description", str),
            ("scoring", str),
        )

    if tabledata is None:
        tabledata = {
            "key": ["key0", "key1"],
            "node": [("N1", "N2"), ("N3", "N4")],
            "type": [("Wind", "Solar"), ("Wind", "Solar")],
            "timeseries": [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]],
            "description": ["my first timeseries", "my second timeseries"],
            "scoring": ["good", "excellent"],
        }

    if newTimeseries is not None:
        tabledata = dict(tabledata)
        tabledata["timeseries"] = newTimeseries

    table = pd.DataFrame(data=tabledata)
    if keysMatter:
        table = table.set_index(idRow)
        if not table.index.is_unique:
            raise ValueError(f"Duplicate values found in index column '{idRow}'.")

    return ProfileSpec(
        referenceNames = referenceNames,
        path = path,
        fields = fields,
        table = table,
        idRow = idRow,
        nodeRow = nodeRow,
        typeRow = typeRow,
        tsRow = tsRow,
        timesteps = timesteps,
        defaultValue = defaultValue,
    )




@pytest.mark.parametrize(
    "validIdRow",
    [
        "key",
        "node",
        "type",
        "timeseries",
        "description",
        "scoring",
    ]
)
def test_validate_row_names_ok(validIdRow):
    aProfileSpec = valid_profilespec_factory(idRow = validIdRow)
    assert aProfileSpec.idRow == validIdRow


@pytest.mark.parametrize(
    "invalidIdRow",
    [
        "not existing column",
        42,
    ]
)
def test_validate_row_names_fails(invalidIdRow):
    with pytest.raises(ValueError):
        valid_profilespec_factory(idRow = invalidIdRow)


def test_validate_timesteps_ok():
    aProfileSpec = valid_profilespec_factory(timesteps = 4)
    assert aProfileSpec.timesteps == 4


@pytest.mark.parametrize(
    "invalidTimesteps",
    [
        -2,
        0
    ]
)
def test_validate_timesteps_fails(invalidTimesteps):
    with pytest.raises(ValueError):
        valid_profilespec_factory(timesteps = invalidTimesteps)


@pytest.mark.parametrize(
    "validTimeseries",
    [
        [[0.8, 0.8, 0.8, 0.8], [0.4, 0.4, 0.4, 0.4]],
        [[0.1, 0.1, 0.2, 0.2], [0.3, 0.3, 0.4, 0.4]],
    ]
)
def test_validate_timeseries_size_ok(validTimeseries):
    valid_profilespec_factory(newTimeseries = validTimeseries)


@pytest.mark.parametrize(
    "invalidTimeseries",
    [
        [[0.8, 0.8, 0.8, 0.8, 0.8], [0.4, 0.4, 0.4, 0.4, 0.4]],
        [[0.1, 0.1, 0.2], [0.3, 0.3, 0.4]],
    ]
)
def test_validate_timeseries_size_fails(invalidTimeseries):
    with pytest.raises(ValueError):
        valid_profilespec_factory(newTimeseries = invalidTimeseries)


@pytest.mark.parametrize(
    "dataframesA",
    [
        {
            'node': [("N1",)],
            'type': [("WindOn", "WindOff")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4)],
        },
        {
            'node': [("N1",),
                    ("N1",)],
            'type': [("WindOn",),
                    ("PV",)],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },
        {
            'node': [("N1", "N2"),
                    ("N1",)],
            'type': [("WindOn", "WindOff"),
                    ("Coal", "PV")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },
    ]
)
def test_validate_exclusive_assignments_ok(dataframesA):
    valid_profilespec_factory(tabledata = dataframesA)


@pytest.mark.parametrize(
    "dataframesB",
    [
        {
            'node': [("N1",)],
            'type': [("WindOn", "WindOn")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4)],
        },
        {
            'node': [("N1",),
                    ("N1",)],
            'type': [("WindOn",),
                    ("WindOn",)],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },
        {
            'node': [("N1", "N2"),
                    ("N1", "N6")],
            'type': [("WindOn", "WindOff"),
                    ("WindOn", "PV")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },
    ]
)
def test_enrich_with_assignments_fail(dataframesB):
    with pytest.raises(ValueError):
        valid_profilespec_factory(tabledata = dataframesB)


@pytest.mark.parametrize(
    "dataframesC, expectedC",
    [
        ({
            'node': [("N1",)],
            'type': [("WindOn", "WindOff")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4)],
        },{
            ("N1", "WindOn"): 0,
            ("N1", "WindOff"): 0,
        }),

        ({
            'node': [("N1",),
                        ("N1",)],
            'type': [("WindOn",),
                        ("PV",)],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },{
            ("N1", "WindOn"): 0,
            ("N1", "PV"): 1,
        }),

        ({
            'node': [("N1", "N2"),
                        ("N1",)],
            'type': [("WindOn", "WindOff"),
                        ("Coal", "PV")],
            'timeseries': [(0.1, 0.2, 0.3, 0.4),
                        (0.1, 0.2, 0.3, 0.4)],
        },{
            ("N1", "WindOn"): 0,
            ("N1", "WindOff"): 0,
            ("N2", "WindOn"): 0,
            ("N2", "WindOff"): 0,
            ("N1", "Coal"): 1,
            ("N1", "PV"): 1,
        }),
    ]
)
def test_enrich_with_assignments_ok(dataframesC, expectedC):
    aProfileSpec = valid_profilespec_factory(tabledata = dataframesC)
    assert(aProfileSpec.assignments == expectedC)


def test_enrich_with_default_profile_ok():
    aProfileSpec = valid_profilespec_factory(keysMatter = True)
    defaultEntry = aProfileSpec.table.loc["default"]
    expectedEntry = pd.Series(
        data = {
            "node": None,
            "type": None,
            "timeseries": (1.0, 1.0, 1.0, 1.0),
            "description": None,
            "scoring": None,
        },
        name = "default",
    )
    assert "default" in aProfileSpec.table.index
    pdt.assert_series_equal(defaultEntry, expectedEntry)


@pytest.mark.parametrize(
    "tupleLeft, tupleRight, expectedCombinations",
    [
        (
            ("L0",), ("R0", "R1"),
            [("L0", "R0"), ("L0", "R1")],
        ),
        (
            ("L0", "L1"), ("R0",),
            [("L0", "R0"), ("L1", "R0")],
        ),
        (
            ("L0", "L1"), ("R0", "R1"),
            [("L0", "R0"), ("L0", "R1"), ("L1", "R0"), ("L1", "R1")],
        ),
        (
            ("L0",), ("R0", "R0"),
            [("L0", "R0"), ("L0", "R0")],
        ),
    ]
)
def test_pair_combinations(tupleLeft, tupleRight, expectedCombinations):
    assert(_pair_combinations(tupleLeft, tupleRight) == expectedCombinations)


def test_map_profiles_ok():
    aTable = pd.DataFrame(
        data = {
            "node": ["N1", "N3", "N4", "N5"],
            "type": ["Wind", "Solar", "Wind", "Wind"],
            "capacity": [10, 10, 10, 10],
        },
        index=["Gen0", "Gen1", "Gen2", "Gen3"]
    )
    aProfileSpec = valid_profilespec_factory(keysMatter = True)
    profileKeys = _map_profiles(aTable, aProfileSpec)
    expectedProfileKeys = pd.Series(
        {
            "Gen0": "key0",
            "Gen1": "key1",
            "Gen2": "key1",
            "Gen3": "default",
        },
        name="profileKey"
    )
    pdt.assert_series_equal(profileKeys, expectedProfileKeys)


def test_object_profile_matrix_ok():
    aTable = pd.DataFrame(
        data = {
            "node": ["N1", "N3", "N4", "N5"],
            "type": ["Wind", "Solar", "Wind", "Wind"],
            "capacity": [10, 10, 10, 10],
        },
        index=["Gen0", "Gen1", "Gen2", "Gen3"]
    )
    aProfileSpec = valid_profilespec_factory(keysMatter = True)
    profiles = object_profile_matrix(aTable, aProfileSpec)
    expectedProfiles = np.array(
        [
            [0.1, 0.2, 0.3, 0.4],
            [0.5, 0.6, 0.7, 0.8],
            [0.5, 0.6, 0.7, 0.8],
            [1.0, 1.0, 1.0, 1.0],
        ],
    )
    npt.assert_array_equal(profiles, expectedProfiles)
