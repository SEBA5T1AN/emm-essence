from .utils_key_matching import (
    check_unused_but_defined_keys,
    check_used_but_undefined_keys,
    exclusion_chain_reaction,
    inform_about_excluded_keys,
)




def preprocess_data(data: dict) -> dict:
    apply_exclusions(data)
    run_logic_checks(data)
    return data


def apply_exclusions(data: dict) -> None:
    converterKeysWithInvalidDirection = data["C"].table.index[
    data["C"].table["converterType"]
        .map(data["C_T"].table["outputMedium"])
        .map(data["M"].table["sectorType"])
        == 1
    ]
    data["C"].excludedKeys.extend(
        converterKeysWithInvalidDirection
    )

    storageKeysForFixPriceMedia = data["STO"].table.index[
        data["STO"].table["storageType"]
        .map(data["STO_T"].table["medium"])
        .map(data["M"].table["sectorType"])
        == 1
    ]
    data["STO"].excludedKeys.extend(
        storageKeysForFixPriceMedia
    )

    demandKeysOfExoSectors = data["D"].table.index[
        data["D"].table["demandType"]
        .map(data["D_T"].table["medium"])
        .map(data["M"].table["sectorType"])
        != 0
    ]
    data["D"].excludedKeys.extend(
        demandKeysOfExoSectors
    )

    tradeLimitsForExoSectors = data["TR"].table.index[
        data["TR"].table["medium"]
        .map(data["M"].table["sectorType"])
        != 0
    ]
    data["TR"].excludedKeys.extend(
        tradeLimitsForExoSectors
    )

    exportAccessKeysForFixPriceMedia = data["EA"].table.index[
        data["EA"].table["medium"]
        .map(data["M"].table["sectorType"])
        == 1
    ]
    data["EA"].excludedKeys.extend(
        exportAccessKeysForFixPriceMedia
    )

    exclusion_subject_names = [
        "M",
        "Z",
        "N",
        "C_T",
        "STO_T",
        "D_T",
        "C",
        "STO",
        "D",
        "IA",
        "EA",
        "TR",
        "C_P_AVA",
        "D_P",
        "STO_P_MAX_LEVEL",
        "STO_P_MIN_LEVEL",
        "STO_P_NAT_INFLOW",
    ]

    for name in exclusion_subject_names:
        subject = data[name]
        exclusion_chain_reaction(
            subject=subject,
            keySubset=subject.excludedKeys,
        )

    for name in exclusion_subject_names:
        inform_about_excluded_keys(
            subject=data[name],
        )


def run_logic_checks(data: dict) -> None:
    subject_names = [
        "C_T",
        "STO_T",
        "D_T",
        "N",
        "Z",
        "M",
    ]

    for name in subject_names:
        check_used_but_undefined_keys(
            subject=data[name],
        )

    for name in subject_names:
        check_unused_but_defined_keys(
            subject=data[name],
        )
