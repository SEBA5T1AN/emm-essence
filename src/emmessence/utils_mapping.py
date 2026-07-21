from collections import defaultdict

import numpy as np




def create_sector_zone_dict(sectorArray, allowedSectors, zoneArray, allowedZones):
    result = defaultdict(lambda: defaultdict(list))
    for index, sector, zone in zip(range(len(sectorArray)), sectorArray, zoneArray):
        sec = np.where(allowedSectors == sector)[0]
        z = np.where(allowedZones == zone)[0]
        if(len(sec) * len(z) != 1):
            continue
        result[sec.item()][z.item()].append(index)
    return result
