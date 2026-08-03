from pathlib import Path
from typing import Final

from .profilespec import ProfileSpec
from .tablespec import TableSpec

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
T_COUNT = 8760
CO2_PRICE = 113.4




def profile_factory(*,
    referenceNames: list[str],
    path: str,
    typeRow: str,
    defaultValue: float,
    lowerThreshold: float,
    upperThreshold: float
) -> "ProfileSpec":
    ID_ROW = "key"
    LOC_ROW = "node"
    TYPE_ROW = typeRow
    TS_ROW = "timeseries"
    return ProfileSpec(
        referenceNames = referenceNames,
        path = path,
        fields=(
            (ID_ROW, str),
            (LOC_ROW, tuple[str, ...]),
            (TYPE_ROW, tuple[str, ...]),
            (TS_ROW, tuple[float, ...], lowerThreshold, upperThreshold),
        ),
        separator = ",",
        idRow = ID_ROW,
        nodeRow = LOC_ROW,
        typeRow = TYPE_ROW,
        tsRow = TS_ROW,
        timesteps = T_COUNT,
        defaultValue = defaultValue,
    )




CONVERTER_AVA_PROFILES_DATA: Final = profile_factory(
    referenceNames = ["converterAvaProfile"],
    path = f"{DATA_DIR}/profiles/input_2030_converter_availability_profiles.txt",
    typeRow = "converterType",
    defaultValue = 1.0,
    lowerThreshold = 0.0,
    upperThreshold = 1.0,
)

DEMAND_PROFILES_DATA: Final = profile_factory(
    referenceNames = ["demandProfile"],
    path = f"{DATA_DIR}/profiles/input_2030_demand_profiles.txt",
    typeRow = "demandType",
    defaultValue = 1.0/T_COUNT,
    lowerThreshold = 0.0,
    upperThreshold = 1.0,
)

STORAGE_MAX_LEVEL_PROFILES_DATA: Final = profile_factory(
    referenceNames = ["storageMaxProfile"],
    path = f"{DATA_DIR}/profiles/input_2030_storage_max_level_profiles.txt",
    typeRow = "storageType",
    defaultValue = 1.0,
    lowerThreshold = 0.0,
    upperThreshold = 1.0,
)

STORAGE_MIN_LEVEL_PROFILES_DATA: Final = profile_factory(
    referenceNames = ["storageMinProfile"],
    path = f"{DATA_DIR}/profiles/input_2030_storage_min_level_profiles.txt",
    typeRow = "storageType",
    defaultValue = 0.0,
    lowerThreshold = 0.0,
    upperThreshold = 1.0,
)

STORAGE_NAT_INFLOW_PROFILES_DATA: Final = profile_factory(
    referenceNames = ["storageNaturalInflowProfile"],
    path = f"{DATA_DIR}/profiles/input_2030_storage_natural_inflow_profiles.txt",
    typeRow = "storageType",
    defaultValue = 0.0,
    lowerThreshold = 0.0,
    upperThreshold = 1.0,
)




CONVERTERS_DATA: Final = TableSpec(
    referenceNames = ["converter"],
    path = f"{DATA_DIR}/input_2030_converters.txt",
    fields = (
        ("key", str),
        ("node", str),
        ("converterType", str),
        ("isInvestment", bool),
        ("capacity", float, 0.0, 1e9),
    ),
    separator = ",",
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
    parents = [],
)

CONVERTER_TYPES_DATA: Final = TableSpec(
    referenceNames = ["converterType"],
    path = f"{DATA_DIR}/input_2030_converter_types.txt",
    fields = (
        ("key", str),
        ("inputMedium", str),
        ("outputMedium", str),
        ("efficiency", float, 0.0, 1.0),
        ("invCost", float, 0.0, 1e9),
        ("omCostFix", float, 0.0, 1e9),
        ("omCostVar", float, 0.0, 1e9),
        ("hasOutputBasedValues", bool),
    ),
    separator = ",",
    parents = [
        CONVERTERS_DATA,
        CONVERTER_AVA_PROFILES_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [("inputMedium", "outputMedium")],
    hasHeader = True,
)

STORAGES_DATA: Final = TableSpec(
    referenceNames = ["storage"],
    path = f"{DATA_DIR}/input_2030_storages.txt",
    fields = (
        ("key", str),
        ("node", str),
        ("storageType", str),
        ("isInvestment", bool),
        ("energyCapacity", float, 0.0, 1e9),
        ("chargePower", float, 0.0, 1e9),
        ("dischargePower", float, 0.0, 1e9),
        ("naturalInflow", float, 0.0, 1e9),
    ),
    separator = ",",
    parents = [],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

STORAGE_TYPES_DATA: Final = TableSpec(
    referenceNames = ["storageType"],
    path = f"{DATA_DIR}/input_2030_storage_types.txt",
    fields = (
        ("key", str),
        ("medium", str),
        ("efficiency", float, 0.0, 1.0),
        ("invCost", float, 0.0, 1e9),
        ("omCostFix", float, 0.0, 1e9),
        ("omCostVar", float, 0.0, 1e9),
    ),
    separator = ",",
    parents = [
        STORAGES_DATA,
        STORAGE_MAX_LEVEL_PROFILES_DATA,
        STORAGE_MIN_LEVEL_PROFILES_DATA,
        STORAGE_NAT_INFLOW_PROFILES_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

DEMANDS_DATA: Final = TableSpec(
    referenceNames = ["demand"],
    path = f"{DATA_DIR}/input_2030_demands.txt",
    fields = (
        ("key", str),
        ("node", str),
        ("demandType", str),
        ("totalLoad", float, 0.0, 1e9),
        ("lsEnergyCapacity", float, 0.0, 1e9),
        ("lsChargingPower", float, 0.0, 1e9),
    ),
    separator = ",",
    parents = [],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

DEMAND_TYPES_DATA: Final = TableSpec(
    referenceNames = ["demandType"],
    path = f"{DATA_DIR}/input_2030_demand_types.txt",
    fields = (
        ("key", str),
        ("medium", str),
        ("consumerGroup", str),
        ("isElastic", bool),
        ("priceElasticity", float, 0.0, 1e9),
        ("referencePrice", float, 0.0, 1e9),
    ),
    separator = ",",
    parents = [
        DEMANDS_DATA,
        DEMAND_PROFILES_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

IMPORT_ACCESSES_DATA: Final = TableSpec(
    referenceNames = ["importAccesses"],
    path = f"{DATA_DIR}/input_2030_import_accesses.txt",
    fields = (
        ("key", str),
        ("medium", str),
        ("node", str),
        ("limitPerTimestep", float, 0.0, 1e12),
    ),
    separator = ",",
    parents = [],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

EXPORT_ACCESSES_DATA: Final = TableSpec(
    referenceNames = ["exportAccesses"],
    path = f"{DATA_DIR}/input_2030_export_accesses.txt",
    fields = (
        ("key", str),
        ("medium", str),
        ("node", str),
        ("limitPerTimestep", float, 0.0, 1e12),
    ),
    separator = ",",
    parents = [],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

TRADE_LIMITS_DATA: Final = TableSpec(
    referenceNames = ["tradeLimits"],
    path = f"{DATA_DIR}/input_2030_trade_limits.txt",
    fields = (
        ("key", str),
        ("medium", str),
        ("sourceZone", str),
        ("targetZone", str),
        ("limitForward", float, 0.0, 1e9),
        ("limitBackward", float, 0.0, 1e9),
    ),
    separator = ",",
    parents = [],
    excludedKeys = ["TL1"],
    idColumn = "key",
    nonEqualColumnPairs = [("sourceZone", "targetZone")],
    hasHeader = True,
)

NODES_DATA: Final = TableSpec(
    referenceNames = ["node", "inputNode", "outputNode"],
    path = f"{DATA_DIR}/input_2030_nodes.txt",
    fields = (
        ("key", str),
        ("zone", str),
        ("isRedispatch", bool),
        ("areaShare", float, 0.0, 1.0),
    ),
    separator = ",",
    parents = [
        CONVERTERS_DATA,
        STORAGES_DATA,
        DEMANDS_DATA,
        CONVERTER_AVA_PROFILES_DATA,
        STORAGE_MAX_LEVEL_PROFILES_DATA,
        STORAGE_MIN_LEVEL_PROFILES_DATA,
        STORAGE_NAT_INFLOW_PROFILES_DATA,
        DEMAND_PROFILES_DATA,
        IMPORT_ACCESSES_DATA,
        EXPORT_ACCESSES_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

ZONES_DATA: Final = TableSpec(
    referenceNames = ["zone", "sourceZone", "targetZone"],
    path = f"{DATA_DIR}/input_2030_zones.txt",
    fields = (
        ("key", str),
        ("name", str),
    ),
    separator = ",",
    parents = [
        NODES_DATA,
        TRADE_LIMITS_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

MEDIA_DATA: Final = TableSpec(
    referenceNames = ["medium", "inputMedium", "outputMedium"],
    path = f"{DATA_DIR}/input_2030_media.txt",
    fields = (
        ("key", str),
        ("emissionFactor", float, 0.0, 1e9),
        ("price", float, 0.0, 1e9),
        ("sectorType", int, 0.0, 2.0),
    ),
    separator = ",",
    parents = [
        CONVERTER_TYPES_DATA,
        STORAGE_TYPES_DATA,
        DEMAND_TYPES_DATA,
        IMPORT_ACCESSES_DATA,
        EXPORT_ACCESSES_DATA,
        TRADE_LIMITS_DATA,
    ],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [],
    hasHeader = True,
)

LINES_DATA: Final = TableSpec(
    referenceNames = ["line"],
    path = f"{DATA_DIR}/input_2030_lines.txt",
    fields = (
        ("key", str),
        ("inputNode", str),
        ("outputNode", str),
        ("capacity", float, 0.0, 1e9),
        ("gamma", float, 0.0, 1e9),
        ("isDC", bool),
    ),
    separator = ",",
    parents = [],
    excludedKeys = [],
    idColumn = "key",
    nonEqualColumnPairs = [("inputNode", "outputNode")],
    hasHeader = True,
)
