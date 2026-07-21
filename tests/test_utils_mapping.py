from emmessence.utils_mapping import create_sector_zone_dict

from collections import defaultdict

import numpy as np




def test_create_sector_zone_dict_ok():
    sectorArray = np.array(["A", "B", "A", "A", "C", "B"])
    zoneArray = np.array([10, 20, 20, 10, 10, 30])
    allowedSectors = np.array(["A", "B"])
    allowedZones = np.array([10, 20])
    result = create_sector_zone_dict(
        sectorArray,
        allowedSectors,
        zoneArray,
        allowedZones,
    )
    expected = defaultdict(lambda: defaultdict(list))
    expected[0][0] = [0, 3]
    expected[0][1] = [2]
    expected[1][1] = [1]
    assert result == expected


def test_create_empty_sector_zone_dict_ok():
    result = create_sector_zone_dict(
        np.array(["X"]),
        np.array(["A"]),
        np.array([99]),
        np.array([10]),
    )
    assert len(result) == 0
