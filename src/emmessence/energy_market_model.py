from itertools import chain

import numpy as np
import pyomo.environ as pyo

from .data_preprocessing import preprocess_data
from .table_processing import (
    create_single_tables,
    group_tables,
)
from .user_specs import (
    CO2_PRICE,
    GROUPING_ENABLED,
    RESULTS_DIR,
    T_COUNT,
    allDataObjects,
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

    preprocessedData = preprocess_data(allDataObjects)
    singleTables = create_single_tables(preprocessedData)
    tables = (
        group_tables(singleTables)
        if GROUPING_ENABLED
        else singleTables
    )

    C = tables["C"]
    C_T = tables["C_T"]
    STO = tables["STO"]
    STO_T = tables["STO_T"]
    D = tables["D"]
    D_T = tables["D_T"]
    IA = tables["IA"]
    EA = tables["EA"]
    TR = tables["TR"]
    N = tables["N"]
    Z = tables["Z"]
    M = tables["M"]
    L = tables["L"]
    C_P_AVA = tables["C_P_AVA"]
    STO_P_MAX_LEVEL = tables["STO_P_MAX_LEVEL"]
    STO_P_MIN_LEVEL = tables["STO_P_MIN_LEVEL"]
    STO_P_NAT_INFLOW = tables["STO_P_NAT_INFLOW"]
    D_P = tables["D_P"]








    # sector
    m_sectorType = M['sectorType'].to_numpy()
    m_endo_set = np.where(m_sectorType == 0)[0]
    m_exo_oneway_set = np.where(m_sectorType == 1)[0]
    m_exo_twoway_set = np.where(m_sectorType == 2)[0]
    SECTORS = M.index


    # zone
    ZONES = Z.index.to_numpy()


    # converter
    c_eff = C['converterType'].map(C_T['efficiency']).to_numpy()
    c_outputBased = C['converterType'].map(C_T['hasOutputBasedValues']).to_numpy()
    ioFactor = np.where(c_outputBased, 1.0, c_eff)
    c_cap0 = C['capacity'].to_numpy() * ioFactor
    # converter costs
    c_emFactor = C['converterType'].map(C_T['inputMedium']).map(M['emissionFactor']).to_numpy()
    c_fixCosts_inv = C['converterType'].map(C_T['invCost']).to_numpy() * C['isInvestment'].to_numpy() / ioFactor
    c_fixCosts_om = C['converterType'].map(C_T['omCostFix']).to_numpy() / ioFactor
    c_varCosts_om = C['converterType'].map(C_T['omCostVar']).to_numpy() / ioFactor
    c_fixCosts = c_fixCosts_om + c_fixCosts_inv
    c_varCosts = c_varCosts_om + (c_emFactor*CO2_PRICE) / c_eff
    # converter dicts
    allOutgoingConverters = create_sector_zone_dict(
        sectorArray = C['converterType'].map(C_T['inputMedium']).to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = C['zone'].to_numpy(),
        allowedZones = ZONES
    )
    allIncomingConverters = create_sector_zone_dict(
        sectorArray = C['converterType'].map(C_T['outputMedium']).to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = C['zone'].to_numpy(),
        allowedZones = ZONES
    )


    # storage
    sto_cap = STO['energyCapacity'].to_numpy()
    sto_e2pCharge = STO['e2pCharge'].to_numpy()
    sto_e2pDischarge = STO['e2pDischarge'].to_numpy()
    sto_natInflow = STO['naturalInflow'].to_numpy()
    sto_eff = STO['storageType'].map(STO_T['efficiency']).to_numpy()
    # storage costs
    sto_fixCosts_om = STO['storageType'].map(STO_T['omCostFix']).to_numpy()
    sto_fixCosts_inv = STO['storageType'].map(STO_T['invCost']).to_numpy() * STO['isInvestment'].to_numpy()
    sto_varCosts_om = STO['storageType'].map(STO_T['omCostVar']).to_numpy() ###
    sto_fixCosts = sto_fixCosts_om + sto_fixCosts_inv
    # storage dict
    allStorages = create_sector_zone_dict(
        sectorArray = STO['storageType'].map(STO_T['medium']).to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = STO['zone'].to_numpy(),
        allowedZones = ZONES
    )


    # demand
    d_totalLoad = D['totalLoad'].to_numpy()
    d_lsCap = D['demandType'].map(D_T['lsEnergyAsTimestepsOfAvgLoad']).to_numpy() * d_totalLoad/T_COUNT
    d_lsPower = d_lsCap / D['demandType'].map(D_T['lsE2P']).to_numpy()
    d_load0 = d_totalLoad[:, None] * D_P
    # demand sets
    d_isElastic = D['demandType'].map(D_T['isElastic']).to_numpy()
    d_var_set = np.where(d_isElastic)[0]
    d_fix_set = np.where(~d_isElastic)[0]
    # variable demand
    d_priceElast = D['demandType'].map(D_T['priceElasticity']).to_numpy()
    d_refPrice = D['demandType'].map(D_T['referencePrice']).to_numpy()
    d_curveM = d_refPrice[d_var_set, None] / (d_priceElast[d_var_set, None]*d_load0[d_var_set])
    d_curveA = d_refPrice[d_var_set, None] + d_curveM*d_load0[d_var_set]
    # demand dict
    allDemands = create_sector_zone_dict(
        sectorArray = D['demandType'].map(D_T['medium']).to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = D['zone'].to_numpy(),
        allowedZones = ZONES
    )


    # trade
    tr_limits = TR[['limitForward', 'limitBackward']].to_numpy()
    tr_sec = TR['medium'].to_numpy()
    allIncomingTrades = create_sector_zone_dict(
        sectorArray = tr_sec,
        allowedSectors = SECTORS,
        zoneArray = TR['targetZone'].to_numpy(),
        allowedZones = ZONES
    )
    allOutgoingTrades = create_sector_zone_dict(
        sectorArray = tr_sec,
        allowedSectors = SECTORS,
        zoneArray = TR['sourceZone'].to_numpy(),
        allowedZones = ZONES
    )


    # import accesses, export accesses
    ia_limit = IA['limitPerTimestep'].to_numpy()
    ea_limit = EA['limitPerTimestep'].to_numpy()
    ia_mediumPrice = IA['medium'].map(M['price']).to_numpy()
    ea_mediumPrice = EA['medium'].map(M['price']).to_numpy()
    allImportAccesses = create_sector_zone_dict(
        sectorArray = IA['medium'].to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = IA['node'].map(N['zone']).to_numpy(),
        allowedZones = ZONES
    )
    allExportAccesses = create_sector_zone_dict(
        sectorArray = EA['medium'].to_numpy(),
        allowedSectors = SECTORS,
        zoneArray = EA['node'].map(N['zone']).to_numpy(),
        allowedZones = ZONES
    )








    #""" pyomo
    model = pyo.ConcreteModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

    model.SEC_TYPE_0 = pyo.Set(initialize = m_endo_set)
    model.SEC_TYPE_1 = pyo.Set(initialize = m_exo_oneway_set)
    model.SEC_TYPE_2 = pyo.Set(initialize = m_exo_twoway_set)
    model.Z = pyo.RangeSet(0, len(Z)-1)
    model.D = pyo.RangeSet(0, len(D)-1)
    model.D_VAR = pyo.Set(initialize = d_var_set)
    model.D_FIX = pyo.Set(initialize = d_fix_set)
    model.C = pyo.RangeSet(0, len(C)-1)
    model.STO = pyo.RangeSet(0, len(STO)-1)
    model.TR = pyo.RangeSet(0, len(TR)-1)
    model.TR_DIR = pyo.Set(initialize = [0, 1])
    model.IA = pyo.RangeSet(0, len(IA)-1)
    model.EA = pyo.RangeSet(0, len(EA)-1)
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
    model.dsm_level = pyo.Var(model.D, model.T, bounds=lambda m,d,t: (0, d_lsCap[d]))
    model.dsm_charge = pyo.Var(model.D, model.T, bounds=lambda m,d,t: (0, d_lsPower[d]))
    model.dsm_discharge = pyo.Var(model.D, model.T, bounds=lambda m,d,t: (0, d_lsPower[d]))
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
            model.c_cap[c] * c_fixCosts[c]
            for c in model.C
        )
        all_converter_var_costs = pyo.quicksum(
            model.c_out[c, t] * c_varCosts[c]
            for c in model.C
            for t in model.T
        )
        all_storage_fix_costs = pyo.quicksum(
            model.sto_cap[sto] * sto_fixCosts[sto]
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
        demands = allDemands[secEndo][z]
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
                for d in demands
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
                for d in varDemands
            )
            + pyo.quicksum(
                d_load0[d, t]
                for d in fixDemands
            )
            + pyo.quicksum(
                model.dsm_discharge[d, t]
                for d in demands
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
        return model.sto_charge[sto, t] * sto_e2pCharge[sto] <= model.sto_cap[sto]

    def storage_available_discharge(model, sto, t):
            return model.sto_discharge[sto, t] * sto_e2pDischarge[sto] <= model.sto_cap[sto]

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
            + model.dsm_charge[d, t]
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
    model.con9 = pyo.Constraint(model.D, model.T, rule=demand_side_management)


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
