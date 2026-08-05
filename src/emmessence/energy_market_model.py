from itertools import chain

import numpy as np
import pyomo.environ as pyo

from .profilespec import object_profile_matrix
from .user_specs import (
    CO2_PRICE,
    CONVERTER_AVA_PROFILES_DATA,
    CONVERTER_TYPES_DATA,
    CONVERTERS_DATA,
    DEMAND_PROFILES_DATA,
    DEMAND_TYPES_DATA,
    DEMANDS_DATA,
    EXPORT_ACCESSES_DATA,
    IMPORT_ACCESSES_DATA,
    LINES_DATA,
    MEDIA_DATA,
    NODES_DATA,
    RESULTS_DIR,
    STORAGE_MAX_LEVEL_PROFILES_DATA,
    STORAGE_MIN_LEVEL_PROFILES_DATA,
    STORAGE_NAT_INFLOW_PROFILES_DATA,
    STORAGE_TYPES_DATA,
    STORAGES_DATA,
    T_COUNT,
    TRADE_LIMITS_DATA,
    ZONES_DATA,
)
from .utils_key_matching import (
    check_unused_but_defined_keys,
    check_used_but_undefined_keys,
    exclusion_chain_reaction,
    inform_about_excluded_keys,
)
from .utils_logging import pyo_var_to_csv
from .utils_mapping import create_sector_zone_dict




def run() -> None:
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
        subject = STORAGE_MAX_LEVEL_PROFILES_DATA,
        keySubset = STORAGE_MAX_LEVEL_PROFILES_DATA.excludedKeys
    )
    exclusion_chain_reaction(
        subject = STORAGE_MIN_LEVEL_PROFILES_DATA,
        keySubset = STORAGE_MIN_LEVEL_PROFILES_DATA.excludedKeys
    )
    exclusion_chain_reaction(
        subject = STORAGE_NAT_INFLOW_PROFILES_DATA,
        keySubset = STORAGE_NAT_INFLOW_PROFILES_DATA.excludedKeys
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
    inform_about_excluded_keys(subject = STORAGE_MAX_LEVEL_PROFILES_DATA)
    inform_about_excluded_keys(subject = STORAGE_MIN_LEVEL_PROFILES_DATA)
    inform_about_excluded_keys(subject = STORAGE_NAT_INFLOW_PROFILES_DATA)

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
    STO_P_MAX_LEVEL = object_profile_matrix(
        objectTable = STO,
        profileSpec = STORAGE_MAX_LEVEL_PROFILES_DATA
    )
    STO_P_MIN_LEVEL = object_profile_matrix(
        objectTable = STO,
        profileSpec = STORAGE_MIN_LEVEL_PROFILES_DATA
    )
    STO_P_NAT_INFLOW = object_profile_matrix(
        objectTable = STO,
        profileSpec = STORAGE_NAT_INFLOW_PROFILES_DATA
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
    c_isInvestment = C['isInvestment'].to_numpy()
    c_cap0 = C['capacity'].to_numpy()
    c_outputBased = C['converterType'].map(C_T['hasOutputBasedValues']).to_numpy()
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
    c_fixCosts_inv = C['converterType'].map(C_T['invCost']).to_numpy() * c_isInvestment
    c_fixCosts_om = C['converterType'].map(C_T['omCostFix']).to_numpy()
    c_varCosts_om = C['converterType'].map(C_T['omCostVar']).to_numpy()
    c_emFactor = C['converterType'].map(C_T['inputMedium']).map(M['emissionFactor']).to_numpy()
    c_eff = C['converterType'].map(C_T['efficiency']).to_numpy()
    c_cap0 = np.where(
        c_outputBased,
        c_cap0,
        c_cap0 * c_eff
    )
    c_fixCosts_inv = np.where(
        c_outputBased,
        c_fixCosts_inv,
        c_fixCosts_inv/c_eff
    )
    c_fixCosts_om = np.where(
        c_outputBased,
        c_fixCosts_om,
        c_fixCosts_om/c_eff
    )
    c_varCosts_om = np.where(
        c_outputBased,
        c_varCosts_om,
        c_varCosts_om/c_eff
    )
    c_fixCosts_om_inv = c_fixCosts_om + c_fixCosts_inv
    c_varCosts_om_co2 = c_varCosts_om + (c_emFactor*CO2_PRICE) / c_eff


    # storages
    sto_isInvestment = STO['isInvestment'].to_numpy()
    sto_cap = STO['energyCapacity'].to_numpy()
    sto_maxCharge = STO['chargePower'].to_numpy()
    sto_maxDischarge = STO['dischargePower'].to_numpy()
    sto_cap2charge = sto_cap / sto_maxCharge
    sto_cap2discharge = sto_cap / sto_maxDischarge
    sto_natInflow = STO['naturalInflow'].to_numpy()
    sto_eff = STO['storageType'].map(STO_T['efficiency']).to_numpy()
    sto_fixCosts_om = STO['storageType'].map(STO_T['omCostFix']).to_numpy()
    sto_fixCosts_inv = STO['storageType'].map(STO_T['invCost']).to_numpy() * sto_isInvestment
    sto_varCosts_om = STO['storageType'].map(STO_T['omCostVar']).to_numpy() ###
    sto_fixCosts_om_inv = sto_fixCosts_om + sto_fixCosts_inv

    sto_sectorType = STO['storageType'].map(STO_T['medium']).map(M['sectorType']).to_numpy()
    sto_set = np.where(sto_sectorType != 1)[0]
    sto_sec = STO['storageType'].map(STO_T['medium']).to_numpy()[sto_set]
    sto_zone = STO['node'].map(N['zone']).to_numpy()[sto_set]
    allStorages = create_sector_zone_dict(
        sectorArray = sto_sec, allowedSectors = SECTORS,
        zoneArray = sto_zone, allowedZones = ZONES
    )


    # demands
    d_isElastic = D['demandType'].map(D_T['isElastic']).to_numpy()
    d_priceElast = D['demandType'].map(D_T['priceElasticity']).to_numpy()
    d_refPrice = D['demandType'].map(D_T['referencePrice']).to_numpy()
    d_totalLoad = D['totalLoad'].to_numpy()
    d_lsCap = D['lsEnergyCapacity'].to_numpy()
    d_lsPower = D['lsChargingPower'].to_numpy()
    d_load0 = d_totalLoad[:, None] * D_P
    d_sectorType = D['demandType'].map(D_T['medium']).map(M['sectorType']).to_numpy()
    d_var_set = np.where((d_sectorType == 0) & (d_isElastic))[0]
    d_fix_set = np.where((d_sectorType == 0) & (~d_isElastic))[0]
    d_curveM = d_refPrice[d_var_set, None] / (d_priceElast[d_var_set, None]*d_load0[d_var_set])
    d_curveA = d_refPrice[d_var_set, None] + d_curveM*d_load0[d_var_set]
    d_sec = D['demandType'].map(D_T['medium']).to_numpy()
    d_zone = D['node'].map(N['zone']).to_numpy()
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

    model.SEC_TYPE_0 = pyo.Set(initialize = m_endo_set)
    model.SEC_TYPE_1 = pyo.Set(initialize = m_exo_oneway_set)
    model.SEC_TYPE_2 = pyo.Set(initialize = m_exo_twoway_set)
    model.Z = pyo.RangeSet(0, z_count-1)
    model.D_VAR = pyo.Set(initialize = d_var_set)
    model.D_FIX = pyo.Set(initialize = d_fix_set)
    model.C = pyo.Set(initialize = c_set)
    model.STO = pyo.Set(initialize = sto_set)
    model.TR = pyo.Set(initialize = tr_set)
    model.TR_DIR = pyo.Set(initialize = [0, 1])
    model.IA = pyo.Set(initialize = ia_set)
    model.EA = pyo.Set(initialize = ea_set)
    model.T = pyo.RangeSet(0, T_COUNT-1)

    model.c_cap = pyo.Var(model.C, bounds=lambda m,c: (0, c_cap0[c]))
    model.c_out = pyo.Var(model.C, model.T, domain=pyo.NonNegativeReals)
    model.sto_cap = pyo.Var(model.STO, bounds=lambda m,sto: (0, sto_cap[sto]))
    model.sto_level = pyo.Var(model.STO, model.T, domain=pyo.NonNegativeReals)
    model.sto_charge = pyo.Var(model.STO, model.T, domain=pyo.NonNegativeReals)
    model.sto_discharge = pyo.Var(model.STO, model.T, domain=pyo.NonNegativeReals)
    model.sto_spill = pyo.Var(model.STO, model.T, bounds=lambda m,sto,t: (0, sto_natInflow[sto] * STO_P_NAT_INFLOW[sto, t])) # or domain=pyo.NonNegativeReals)
    model.ia_volume = pyo.Var(model.IA, model.T, bounds=lambda m,ia,t: (0, ia_limit[ia]))
    model.ea_volume = pyo.Var(model.EA, model.T, bounds=lambda m,ea,t: (0, ea_limit[ea]))
    model.demand = pyo.Var(model.D_VAR, model.T, domain=pyo.NonNegativeReals)
    model.dsm_level = pyo.Var(model.D_VAR, model.T, bounds=lambda m,d,t: (0, d_lsCap[d]))
    model.dsm_charge = pyo.Var(model.D_VAR, model.T, bounds=lambda m,d,t: (0, d_lsPower[d]))
    model.dsm_discharge = pyo.Var(model.D_VAR, model.T, bounds=lambda m,d,t: (0, d_lsPower[d]))
    model.trade = pyo.Var(model.TR, model.T, model.TR_DIR, bounds=lambda m,tr,t,tr_d: (0, tr_limits[tr][tr_d]))


    def objective_rule(model):
        welfare = pyo.quicksum(
            model.demand[d, t] * (
                d_curveA[d, t]
                - 0.5 * d_curveM[d, t] * model.demand[d, t]
            )
            for d in model.D_VAR
            for t in model.T
        )
        all_converter_fix_costs = pyo.quicksum(
            model.c_cap[c] * c_fixCosts_om_inv[c]
            for c in model.C
        )
        all_converter_var_costs = pyo.quicksum(
            model.c_out[c, t] * c_varCosts_om_co2[c]
            for c in model.C
            for t in model.T
        )
        all_storage_fix_costs = pyo.quicksum(
            model.sto_cap[sto] * sto_fixCosts_om_inv[sto]
            for sto in model.STO
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
            - all_converter_fix_costs
            - all_converter_var_costs
            - all_storage_fix_costs
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
        storages = allStorages[secEndo][z]
        imports = allImportAccesses[secEndo][z]
        exports = allExportAccesses[secEndo][z]
        incomingTrades = allIncomingTrades[secEndo][z]
        outgoingTrades = allOutgoingTrades[secEndo][z]
        varDemands = np.intersect1d(allDemands[secEndo][z], d_var_set)
        fixDemands = np.intersect1d(allDemands[secEndo][z], d_fix_set)

        if not any([
            incomingConverters,
            outgoingConverters,
            storages,
            imports,
            exports,
            incomingTrades,
            outgoingTrades,
            varDemands,
            fixDemands,
        ]):
            return pyo.Constraint.Skip
        
        lhs = (
            pyo.quicksum(
                model.dsm_charge[d, t]
                for d in varDemands
            )
            + pyo.quicksum(
                model.c_out[c, t]
                for c in incomingConverters
            )
            + pyo.quicksum(
                model.sto_discharge[sto, t]
                for sto in storages
            )
            + pyo.quicksum(
                model.ia_volume[ia, t]
                for ia in imports
            )
            + pyo.quicksum(
                model.trade[tr, t, 0]
                - model.trade[tr, t, 1]
                for tr in incomingTrades
            )
        )
        rhs = (
            pyo.quicksum(
                model.demand[d, t]
                + model.dsm_discharge[d, t]
                for d in varDemands
            )
            + pyo.quicksum(
                d_load0[d, t]
                for d in fixDemands
            )
            + pyo.quicksum(
                model.c_out[c, t] / c_eff[c]
                for c in outgoingConverters
            )
            + pyo.quicksum(
                model.sto_charge[sto, t]
                for sto in storages
            )
            + pyo.quicksum(
                model.ea_volume[ea, t]
                for ea in exports
            )
            + pyo.quicksum(
                model.trade[tr, t, 0]
                - model.trade[tr, t, 1]
                for tr in outgoingTrades
            )
        )
        return (lhs == rhs)


    def energy_balance_exo_twoway(model, secExoTwoway, t):
        incomingConverters = list(chain.from_iterable(allIncomingConverters[secExoTwoway].values()))
        outgoingConverters = list(chain.from_iterable(allOutgoingConverters[secExoTwoway].values()))
        storages = list(chain.from_iterable(allStorages[secExoTwoway].values()))
        imports = list(chain.from_iterable(allImportAccesses[secExoTwoway].values()))
        exports = list(chain.from_iterable(allExportAccesses[secExoTwoway].values()))

        if not any([
            incomingConverters,
            outgoingConverters,
            storages,
            imports,
            exports,
        ]):
            return pyo.Constraint.Skip
        
        lhs = (
            pyo.quicksum(
                model.c_out[c, t]
                for c in incomingConverters
            )
            + pyo.quicksum(
                model.sto_discharge[sto, t]
                for sto in storages
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
                model.sto_charge[sto, t]
                for sto in storages
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


    def converter_available_capacity(model, c, t):
        return model.c_out[c, t] <= model.c_cap[c] * C_P_AVA[c, t]

    def storage_available_charge(model, sto, t):
        return model.sto_charge[sto, t] * sto_cap2charge[sto] <= model.sto_cap[sto]

    def storage_available_discharge(model, sto, t):
            return model.sto_discharge[sto, t] * sto_cap2discharge[sto] <= model.sto_cap[sto]

    def storage_min_capacity(model, sto, t):
        return (
            model.sto_level[sto, t]
            >= STO_P_MIN_LEVEL[sto, t] * model.sto_cap[sto]
        )

    def storage_max_capacity(model, sto, t):
        return (
            model.sto_level[sto, t]
            <= STO_P_MAX_LEVEL[sto, t] * model.sto_cap[sto]
        )

    def storage_balance(model, sto, t):
        if t == model.T.first():
            prev = model.T.last()
        else:
            prev = model.T.prev(t)
        return (
            model.sto_level[sto, t]
            == model.sto_level[sto, prev]
            + model.sto_charge[sto, t] * sto_eff[sto]
            - model.sto_discharge[sto, t]
            + sto_natInflow[sto] * STO_P_NAT_INFLOW[sto, t]
            - model.sto_spill[sto, t]
        )

    def demand_side_management(model, d, t):
        if t == model.T.first():
            prev = model.T.last()
            level_factor = 1.00
        else:
            prev = model.T.prev(t)
            level_factor = 1.01
        return (
            model.dsm_level[d, t]
            == level_factor * model.dsm_level[d, prev] ###
            + model.dsm_charge[d, t] * 1.0 ### eff
            - model.dsm_discharge[d, t]
        )


    model.con0 = pyo.Constraint(model.SEC_TYPE_0, model.Z, model.T, rule=energy_balance_endo)
    model.con1 = pyo.Constraint(model.SEC_TYPE_2, model.T, rule=energy_balance_exo_twoway)
    model.con2 = pyo.Constraint(model.SEC_TYPE_1, model.T, rule=energy_balance_exo_oneway)
    model.con3 = pyo.Constraint(model.C, model.T, rule=converter_available_capacity)
    model.con4 = pyo.Constraint(model.STO, model.T, rule=storage_available_charge)
    model.con5 = pyo.Constraint(model.STO, model.T, rule=storage_available_discharge)
    model.con6 = pyo.Constraint(model.STO, model.T, rule=storage_min_capacity)
    model.con7 = pyo.Constraint(model.STO, model.T, rule=storage_max_capacity)
    model.con8 = pyo.Constraint(model.STO, model.T, rule=storage_balance)
    model.con9 = pyo.Constraint(model.D_VAR, model.T, rule=demand_side_management)


    solver = pyo.SolverFactory("gurobi")
    solver.solve(model)


    pyo_var_to_csv(var = model.c_out, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.c_cap, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.sto_cap, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.sto_level, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.sto_charge, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.sto_discharge, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.sto_spill, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.ia_volume, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.ea_volume, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.demand, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.dsm_level, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.dsm_charge, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.dsm_discharge, path = RESULTS_DIR)
    pyo_var_to_csv(var = model.trade, path = RESULTS_DIR)
    #"""
