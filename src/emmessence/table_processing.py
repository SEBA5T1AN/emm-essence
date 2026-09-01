import numpy as np

from .profilespec import (
    map_profiles,
    object_profile_matrix,
)




def create_single_tables(data: dict) -> dict:
    tables = {}

    tables["N"] = data["N"].table

    tables["C"] = data["C"].table.assign(
        zone=lambda df: df["node"].map(tables["N"]["zone"]),
    )
    tables["C"] = tables["C"].assign(
        profileKey=map_profiles(
            tables["C"],
            data["C_P_AVA"],
        ),
    )

    tables["STO"] = data["STO"].table.assign(
        zone=lambda df: df["node"].map(tables["N"]["zone"]),
        e2pCharge=lambda df: (
            df["energyCapacity"] / df["chargePower"]
        ),
        e2pDischarge=lambda df: (
            df["energyCapacity"] / df["dischargePower"]
        ),
    )
    tables["STO"] = tables["STO"].assign(
        minProfileKey=map_profiles(
            tables["STO"],
            data["STO_P_MIN_LEVEL"],
        ),
        maxProfileKey=map_profiles(
            tables["STO"],
            data["STO_P_MAX_LEVEL"],
        ),
        natProfileKey=map_profiles(
            tables["STO"],
            data["STO_P_NAT_INFLOW"],
        ),
    )

    tables["D"] = data["D"].table.assign(
        zone=lambda df: df["node"].map(tables["N"]["zone"]),
    )

    tables["C_P_AVA"] = object_profile_matrix(
        objectTable=tables["C"],
        profileSpec=data["C_P_AVA"],
    )
    tables["STO_P_MAX_LEVEL"] = object_profile_matrix(
        objectTable=tables["STO"],
        profileSpec=data["STO_P_MAX_LEVEL"],
    )
    tables["STO_P_MIN_LEVEL"] = object_profile_matrix(
        objectTable=tables["STO"],
        profileSpec=data["STO_P_MIN_LEVEL"],
    )
    tables["STO_P_NAT_INFLOW"] = object_profile_matrix(
        objectTable=tables["STO"],
        profileSpec=data["STO_P_NAT_INFLOW"],
    )
    tables["D_P"] = object_profile_matrix(
        objectTable=tables["D"],
        profileSpec=data["D_P"],
    )

    for name in [
        "C_T",
        "STO_T",
        "D_T",
        "L",
        "M",
        "Z",
        "TR",
        "IA",
        "EA",
    ]:
        tables[name] = data[name].table

    return tables


def group_tables(tables: dict) -> dict:
    C = (
        tables["C"]
        .assign(
            originalIndices=np.arange(len(tables["C"])),
            originalKeys=tables["C"].index,
        )
        .groupby(
            [
                "zone",
                "converterType",
                "isInvestment",
                "profileKey",
            ],
            as_index=False,
        )
        .agg(
            capacity=("capacity", "sum"),
            originalIndices=("originalIndices", list),
            originalKeys=("originalKeys", list),
        )
    )

    STO = (
        tables["STO"]
        .assign(
            originalIndices=np.arange(len(tables["STO"])),
            originalKeys=tables["STO"].index,
        )
        .groupby(
            [
                "zone",
                "storageType",
                "isInvestment",
                "e2pCharge",
                "e2pDischarge",
                "naturalInflow",
                "minProfileKey",
                "maxProfileKey",
                "natProfileKey",
            ],
            as_index=False,
        )
        .agg(
            energyCapacity=("energyCapacity", "sum"),
            originalIndices=("originalIndices", list),
            originalKeys=("originalKeys", list),
        )
    )

    D = (
        tables["D"]
        .assign(
            originalIndices=np.arange(len(tables["D"])),
            originalKeys=tables["D"].index,
        )
        .groupby(
            ["zone", "demandType"],
            as_index=False,
        )
        .agg(
            totalLoad=("totalLoad", "sum"),
            originalIndices=("originalIndices", list),
            originalKeys=("originalKeys", list),
        )
    )

    converter_indices = C["originalIndices"].str[0].to_numpy()
    storage_indices = STO["originalIndices"].str[0].to_numpy()
    demand_indices = D["originalIndices"].str[0].to_numpy()

    result = tables.copy()

    result.update({
        "C": C,
        "STO": STO,
        "D": D,
        "C_P_AVA": tables["C_P_AVA"][converter_indices],
        "STO_P_MAX_LEVEL": tables["STO_P_MAX_LEVEL"][storage_indices],
        "STO_P_MIN_LEVEL": tables["STO_P_MIN_LEVEL"][storage_indices],
        "STO_P_NAT_INFLOW": tables["STO_P_NAT_INFLOW"][storage_indices],
        "D_P": tables["D_P"][demand_indices],
    })

    return result
