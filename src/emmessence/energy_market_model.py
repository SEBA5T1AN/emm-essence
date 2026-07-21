from .utils_logging import setup_logging, pyo_var_to_csv
logger = setup_logging()
# ruff: noqa: E402
from .user_specs import T_COUNT
from .user_specs import CO2_PRICE
from .user_specs import CONVERTERS_DATA
from .user_specs import CONVERTER_TYPES_DATA
from .user_specs import STORAGES_DATA
from .user_specs import STORAGE_TYPES_DATA
from .user_specs import DEMANDS_DATA
from .user_specs import DEMAND_TYPES_DATA
from .user_specs import LINES_DATA
from .user_specs import MEDIA_DATA
from .user_specs import NODES_DATA
from .user_specs import ZONES_DATA
from .user_specs import TRADE_LIMITS_DATA
from .user_specs import IMPORT_ACCESSES_DATA
from .user_specs import EXPORT_ACCESSES_DATA
from .user_specs import CONVERTER_AVA_PROFILES_DATA
from .user_specs import DEMAND_PROFILES_DATA
from .user_specs import STORAGE_LEVEL_PROFILES_DATA
from .user_specs import STORAGE_MAX_PROFILES_DATA
from .user_specs import STORAGE_MIN_PROFILES_DATA
from .user_specs import STORAGE_NAT_IN_PROFILES_DATA
from .user_specs import RESULTS_DIR
from .profilespec import object_profile_matrix
from .utils_key_matching import check_used_but_undefined_keys
from .utils_key_matching import check_unused_but_defined_keys
from .utils_key_matching import exclusion_chain_reaction
from .utils_key_matching import inform_about_excluded_keys
from .utils_mapping import create_sector_zone_dict

from itertools import chain

import numpy as np
import pyomo.environ as pyo




if CO2_PRICE <= 0:
    raise ValueError(
        f"\n@user_specs\n"
        f"Invalid 'CO2_PRICE': {CO2_PRICE}. "
        f"The value must be greater than 0\n"
    )

exclusion_chain_reaction(
    subject = MEDIA_DATA,
    keySubset = MEDIA_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = ZONES_DATA,
    keySubset = ZONES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = NODES_DATA,
    keySubset = NODES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = CONVERTER_TYPES_DATA,
    keySubset = CONVERTER_TYPES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGE_TYPES_DATA,
    keySubset = STORAGE_TYPES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = DEMAND_TYPES_DATA,
    keySubset = DEMAND_TYPES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = CONVERTERS_DATA,
    keySubset = CONVERTERS_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGES_DATA,
    keySubset = STORAGES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = DEMANDS_DATA,
    keySubset = DEMANDS_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = IMPORT_ACCESSES_DATA,
    keySubset = IMPORT_ACCESSES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = EXPORT_ACCESSES_DATA,
    keySubset = EXPORT_ACCESSES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = TRADE_LIMITS_DATA,
    keySubset = TRADE_LIMITS_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = CONVERTER_AVA_PROFILES_DATA,
    keySubset = CONVERTER_AVA_PROFILES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = DEMAND_PROFILES_DATA,
    keySubset = DEMAND_PROFILES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGE_LEVEL_PROFILES_DATA,
    keySubset = STORAGE_LEVEL_PROFILES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGE_MAX_PROFILES_DATA,
    keySubset = STORAGE_MAX_PROFILES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGE_MIN_PROFILES_DATA,
    keySubset = STORAGE_MIN_PROFILES_DATA.excludedKeys
)
exclusion_chain_reaction(
    subject = STORAGE_NAT_IN_PROFILES_DATA,
    keySubset = STORAGE_NAT_IN_PROFILES_DATA.excludedKeys
)

inform_about_excluded_keys(subject = MEDIA_DATA)
inform_about_excluded_keys(subject = ZONES_DATA)
inform_about_excluded_keys(subject = NODES_DATA)
inform_about_excluded_keys(subject = CONVERTER_TYPES_DATA)
inform_about_excluded_keys(subject = STORAGE_TYPES_DATA)
inform_about_excluded_keys(subject = DEMAND_TYPES_DATA)
inform_about_excluded_keys(subject = CONVERTERS_DATA)
inform_about_excluded_keys(subject = STORAGES_DATA)
inform_about_excluded_keys(subject = DEMANDS_DATA)
inform_about_excluded_keys(subject = IMPORT_ACCESSES_DATA)
inform_about_excluded_keys(subject = EXPORT_ACCESSES_DATA)
inform_about_excluded_keys(subject = TRADE_LIMITS_DATA)
inform_about_excluded_keys(subject = CONVERTER_AVA_PROFILES_DATA)
inform_about_excluded_keys(subject = DEMAND_PROFILES_DATA)
inform_about_excluded_keys(subject = STORAGE_LEVEL_PROFILES_DATA)
inform_about_excluded_keys(subject = STORAGE_MAX_PROFILES_DATA)
inform_about_excluded_keys(subject = STORAGE_MIN_PROFILES_DATA)
inform_about_excluded_keys(subject = STORAGE_NAT_IN_PROFILES_DATA)

check_used_but_undefined_keys(subject = CONVERTER_TYPES_DATA)
check_used_but_undefined_keys(subject = STORAGE_TYPES_DATA)
check_used_but_undefined_keys(subject = DEMAND_TYPES_DATA)
check_used_but_undefined_keys(subject = NODES_DATA)
check_used_but_undefined_keys(subject = ZONES_DATA)
check_used_but_undefined_keys(subject = MEDIA_DATA)

check_unused_but_defined_keys(subject = CONVERTER_TYPES_DATA)
check_unused_but_defined_keys(subject = STORAGE_TYPES_DATA)
check_unused_but_defined_keys(subject = DEMAND_TYPES_DATA)
check_unused_but_defined_keys(subject = NODES_DATA)
check_unused_but_defined_keys(subject = ZONES_DATA)
check_unused_but_defined_keys(subject = MEDIA_DATA)

C = CONVERTERS_DATA.table
C_T = CONVERTER_TYPES_DATA.table
STO = STORAGES_DATA.table
STO_T = STORAGE_TYPES_DATA.table
D = DEMANDS_DATA.table
D_T = DEMAND_TYPES_DATA.table
L = LINES_DATA.table
M = MEDIA_DATA.table
N = NODES_DATA.table
Z = ZONES_DATA.table
TR = TRADE_LIMITS_DATA.table
IA = IMPORT_ACCESSES_DATA.table
EA = EXPORT_ACCESSES_DATA.table

C_P_AVA = object_profile_matrix(
    objectTable = C,
    profileSpec = CONVERTER_AVA_PROFILES_DATA
)
D_P = object_profile_matrix(
    objectTable = D,
    profileSpec = DEMAND_PROFILES_DATA
)
STO_P_LEVEL = object_profile_matrix(
    objectTable = STO,
    profileSpec = STORAGE_LEVEL_PROFILES_DATA
)
STO_P_MAX = object_profile_matrix(
    objectTable = STO,
    profileSpec = STORAGE_MAX_PROFILES_DATA
)
STO_P_MIN = object_profile_matrix(
    objectTable = STO,
    profileSpec = STORAGE_MIN_PROFILES_DATA
)
STO_P_NAT = object_profile_matrix(
    objectTable = STO,
    profileSpec = STORAGE_NAT_IN_PROFILES_DATA
)








# sectors
m_sectorType = M['sectorType'].to_numpy()
m_endo_set = np.where(m_sectorType == 0)[0]
m_exo_oneway_set = np.where(m_sectorType == 1)[0]
m_exo_twoway_set = np.where(m_sectorType == 2)[0]
SECTORS = M.index


# zones
z_count = len(Z)
ZONES = Z.index.to_numpy()


# converters
c_cap0 = C['capacity'].to_numpy()
c_sector1Type = C['converterType'].map(C_T['outputMedium']).map(M['sectorType']).to_numpy()
c_set = np.where(c_sector1Type != 1)[0]
c_sec0 = C['converterType'].map(C_T['inputMedium']).to_numpy()[c_set]
c_sec1 = C['converterType'].map(C_T['outputMedium']).to_numpy()[c_set]
c_zone = C['node'].map(N['zone']).to_numpy()[c_set]
allOutgoingConverters = create_sector_zone_dict(
    sectorArray = c_sec0, allowedSectors = SECTORS,
    zoneArray = c_zone, allowedZones = ZONES
)
allIncomingConverters = create_sector_zone_dict(
    sectorArray = c_sec1, allowedSectors = SECTORS,
    zoneArray = c_zone, allowedZones = ZONES
)
# converters costs
c_fixCosts_om = C['converterType'].map(C_T['omCostFix']).to_numpy()
c_fixCosts_inv = C['converterType'].map(C_T['invCost']).to_numpy()
c_varCosts_om = C['converterType'].map(C_T['omCostVar']).to_numpy()
c_emFactor = C['converterType'].map(C_T['inputMedium']).map(M['emissionFactor']).to_numpy()
c_eff = C['converterType'].map(C_T['efficiency']).to_numpy()
c_fixCosts_om_inv = c_fixCosts_om + c_fixCosts_inv
c_varCosts_om_co2 = c_varCosts_om + (c_emFactor*CO2_PRICE) / c_eff


# demands
d_priceElast = D['demandType'].map(D_T['priceElasticity']).to_numpy()
d_refPrice = D['demandType'].map(D_T['referencePrice']).to_numpy()
d_totalLoad = D['totalLoad'].to_numpy()
d_load0 = d_totalLoad[:, None] * D_P
d_curveM = d_refPrice[:, None] / (d_priceElast[:, None]*d_load0)
d_curveA = d_refPrice[:, None] + d_curveM*d_load0
d_sectorType = D['demandType'].map(D_T['medium']).map(M['sectorType']).to_numpy()
d_set = np.where(d_sectorType == 0)[0]
d_sec = D['demandType'].map(D_T['medium']).to_numpy()[d_set]
d_zone = D['node'].map(N['zone']).to_numpy()[d_set]
allDemands = create_sector_zone_dict(
    sectorArray = d_sec, allowedSectors = SECTORS,
    zoneArray = d_zone, allowedZones = ZONES
)


# trades
tr_limits = TR[['limitForward', 'limitBackward']].to_numpy()
tr_sectorType = TR['medium'].map(M['sectorType']).to_numpy()
tr_set = np.where(tr_sectorType == 0)[0]
tr_sec = TR['medium'].to_numpy()[tr_set]
tr_zone0 = TR['sourceZone'].to_numpy()[tr_set]
tr_zone1 = TR['targetZone'].to_numpy()[tr_set]
allIncomingTrades = create_sector_zone_dict(
    sectorArray = tr_sec, allowedSectors = SECTORS,
    zoneArray = tr_zone1, allowedZones = ZONES
)
allOutgoingTrades = create_sector_zone_dict(
    sectorArray = tr_sec, allowedSectors = SECTORS,
    zoneArray = tr_zone0, allowedZones = ZONES
)


# import accesses, export accesses
ia_limit = IA['limitPerTimestep'].to_numpy()
ea_limit = EA['limitPerTimestep'].to_numpy()
ia_mediumPrice = IA['medium'].map(M['price']).to_numpy()
ea_mediumPrice = EA['medium'].map(M['price']).to_numpy()
ea_sectorType = EA['medium'].map(M['sectorType']).to_numpy()
ia_set = [i for i in range(len(IA))]
ea_set = np.where(ea_sectorType != 1)[0]
ia_sec = IA['medium'].to_numpy()[ia_set]
ea_sec = EA['medium'].to_numpy()[ea_set]
ia_zone = IA['node'].map(N['zone']).to_numpy()[ia_set]
ea_zone = EA['node'].map(N['zone']).to_numpy()[ea_set]
allImportAccesses = create_sector_zone_dict(
    sectorArray = ia_sec, allowedSectors = SECTORS,
    zoneArray = ia_zone, allowedZones = ZONES
)
allExportAccesses = create_sector_zone_dict(
    sectorArray = ea_sec, allowedSectors = SECTORS,
    zoneArray = ea_zone, allowedZones = ZONES
)








#""" pyomo
model = pyo.ConcreteModel()
model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

model.SEC_N = pyo.Set(initialize = m_endo_set)
model.SEC_XO = pyo.Set(initialize = m_exo_oneway_set)
model.SEC_XT = pyo.Set(initialize = m_exo_twoway_set)
model.Z = pyo.RangeSet(0, z_count-1)
model.D = pyo.Set(initialize = d_set)
model.C = pyo.Set(initialize = c_set)
model.TR = pyo.Set(initialize = tr_set)
model.TR_DIR = pyo.Set(initialize = [0, 1])
model.IA = pyo.Set(initialize = ia_set)
model.EA = pyo.Set(initialize = ea_set)
model.T = pyo.RangeSet(0, T_COUNT-1)

model.c_cap = pyo.Var(model.C, bounds=lambda m,c: (0, c_cap0[c]))
model.c_out = pyo.Var(model.C, model.T, domain=pyo.NonNegativeReals)
model.ia_volume = pyo.Var(model.IA, model.T, bounds=lambda m,ia,t: (0, ia_limit[ia]))
model.ea_volume = pyo.Var(model.EA, model.T, bounds=lambda m,ea,t: (0, ea_limit[ea]))
model.demand = pyo.Var(model.D, model.T, domain=pyo.NonNegativeReals)
model.trade = pyo.Var(model.TR, model.T, model.TR_DIR, bounds=lambda m,tr,t,tr_d: (0, tr_limits[tr][tr_d]))


def objective_rule(model):
    welfare = pyo.quicksum(
        model.demand[d, t] * (
            d_curveA[d, t]
            - 0.5 * d_curveM[d, t] * model.demand[d, t]
        )
        for d in model.D
        for t in model.T
    )
    all_fix_costs_for_om_and_invest = pyo.quicksum(
        model.c_cap[c] * c_fixCosts_om_inv[c]
        for c in model.C
    )
    all_var_costs_for_om_and_co2 = pyo.quicksum(
        model.c_out[c, t] * c_varCosts_om_co2[c]
        for c in model.C
        for t in model.T
    )
    all_import_costs = pyo.quicksum(
        model.ia_volume[ia, t] * ia_mediumPrice[ia]
        for ia in model.IA
        for t in model.T
    )
    all_export_revenues = pyo.quicksum(
        model.ea_volume[ea, t] * ea_mediumPrice[ea]
        for ea in model.EA
        for t in model.T
    )
    all_export_penalties = 1e-4 * pyo.quicksum(
        model.ea_volume[ea, t]
        for ea in model.EA
        for t in model.T
    )
    all_flow_penalties = 1e-4 * pyo.quicksum(
        model.trade[tr, t, 0] + model.trade[tr, t, 1]
        for tr in model.TR
        for t in model.T
    )
    result = (
        welfare
        - all_fix_costs_for_om_and_invest
        - all_var_costs_for_om_and_co2
        - all_import_costs
        + all_export_revenues
        - all_export_penalties
        - all_flow_penalties
    )
    return result

model.obj = pyo.Objective(rule=objective_rule, sense=pyo.maximize)


def energy_balance_endo(model, secEndo, z, t):
    incomingConverters = allIncomingConverters[secEndo][z]
    outgoingConverters = allOutgoingConverters[secEndo][z]
    imports = allImportAccesses[secEndo][z]
    exports = allExportAccesses[secEndo][z]
    incomingTrades = allIncomingTrades[secEndo][z]
    outgoingTrades = allOutgoingTrades[secEndo][z]
    demands = allDemands[secEndo][z]

    if not any([
        incomingConverters,
        outgoingConverters,
        imports,
        exports,
        incomingTrades,
        outgoingTrades,
        demands,
    ]):
        return pyo.Constraint.Skip
    
    lhs = (
        pyo.quicksum(
            model.c_out[c, t]
            for c in incomingConverters
        )
        + pyo.quicksum(
            model.ia_volume[ia, t]
            for ia in imports
        )
        + pyo.quicksum(
            model.trade[tr, t, 0]
            for tr in incomingTrades
        )
        - pyo.quicksum(
            model.trade[tr, t, 1]
            for tr in incomingTrades
        )
    )
    rhs = (
        pyo.quicksum(
            model.demand[d, t]
            for d in demands
        )
        + pyo.quicksum(
            model.c_out[c, t] / c_eff[c]
            for c in outgoingConverters
        )
        + pyo.quicksum(
            model.ea_volume[ea, t]
            for ea in exports
        )
        + pyo.quicksum(
            model.trade[tr, t, 0]
            for tr in outgoingTrades
        )
        - pyo.quicksum(
            model.trade[tr, t, 1]
            for tr in outgoingTrades
        )
    )
    return (lhs == rhs)


def energy_balance_exo_twoway(model, secExoTwoway, t):
    incomingConverters = list(chain.from_iterable(allIncomingConverters[secExoTwoway].values()))
    outgoingConverters = list(chain.from_iterable(allOutgoingConverters[secExoTwoway].values()))
    imports = list(chain.from_iterable(allImportAccesses[secExoTwoway].values()))
    exports = list(chain.from_iterable(allExportAccesses[secExoTwoway].values()))

    if not incomingConverters and not outgoingConverters and not imports and not exports:
        return pyo.Constraint.Skip
    
    lhs = (
        pyo.quicksum(
            model.c_out[c, t]
            for c in incomingConverters
        )
        + pyo.quicksum(
            model.ia_volume[ia, t]
            for ia in imports
        )
    )
    rhs = (
        pyo.quicksum(
            model.c_out[c, t] / c_eff[c]
            for c in outgoingConverters
        )
        + pyo.quicksum(
            model.ea_volume[ea, t]
            for ea in exports
        )
    )
    return (lhs == rhs)


def energy_balance_exo_oneway(model, secExoOneway, t):
    imports = list(chain.from_iterable(allImportAccesses[secExoOneway].values()))
    outgoingConverters = list(chain.from_iterable(allOutgoingConverters[secExoOneway].values()))

    if not imports and not outgoingConverters:
        return pyo.Constraint.Skip
    
    lhs = (
        pyo.quicksum(
            model.ia_volume[ia, t]
            for ia in imports
        )
    )
    rhs = (
        pyo.quicksum(
            model.c_out[c, t] / c_eff[c]
            for c in outgoingConverters
        )
    )
    return (lhs == rhs)


def available_conversion(model, c, t):
    return model.c_out[c, t] <= model.c_cap[c] * C_P_AVA[c, t]


model.con0 = pyo.Constraint(model.SEC_N, model.Z, model.T, rule=energy_balance_endo)
model.con1 = pyo.Constraint(model.SEC_XT, model.T, rule=energy_balance_exo_twoway)
model.con2 = pyo.Constraint(model.SEC_XO, model.T, rule=energy_balance_exo_oneway)
model.con3 = pyo.Constraint(model.C, model.T, rule=available_conversion)


solver = pyo.SolverFactory("gurobi")
solver.solve(model)


pyo_var_to_csv(var = model.c_out, path = RESULTS_DIR)
pyo_var_to_csv(var = model.c_cap, path = RESULTS_DIR)
pyo_var_to_csv(var = model.ia_volume, path = RESULTS_DIR)
pyo_var_to_csv(var = model.ea_volume, path = RESULTS_DIR)
pyo_var_to_csv(var = model.demand, path = RESULTS_DIR)
pyo_var_to_csv(var = model.trade, path = RESULTS_DIR)
#"""
