# solvent dictionary



nhexane = dict(
    number = 40, # from marcus book
    BP = 341.9,
    FP = 177.8,
    VDW_vol = 68.3,
    dipole = 0.09,
    dielectric = 1.88,
    refractive_index = 1.3723,
    viscosity = 0.294,
    Trouton = 10.2,
    alpha = 0.0,
    beta = 0.0,
    pi_star = -0.11,
    E_T_30 = 31.0,
    ETN = 0.009,
    logP = 3.9,
    Flory_Huggins = 1.42,
    )

benzene = dict(
    number = 120,
    BP = 353.2,
    FP = 278.7,
    VDW_vol = 48.4,
    dipole = 0.0,
    dielectric = 2.27,
    refractive_index = 1.4979,
    viscosity = 0.603,
    Trouton = 10.5,
    alpha = 0.0,
    beta = 0.1,
    pi_star = 0.55,
    E_T_30 = 34.3,
    ETN = 0.111,
    logP = 2.13,
    Flory_Huggins = 0.2,
    )


toluene = dict(
    number = 130,
    BP = 383.8,
    FP = 178.2,
    VDW_vol = 59.5,
    dipole = 0.31,
    dielectric = 2.38,
    refractive_index = 1.4941,
    viscosity = 0.533,
    Trouton = 10.4,
    alpha = 0.0,
    beta = 0.11,
    pi_star = 0.49,
    E_T_30 = 33.9,
    ETN = 0.099,
    logP = 2.69,
    Flory_Huggins = 0.27,
    )


THF = dict(
    number = 740,
    BP = 339.1,
    FP = 164.8,
    VDW_vol = 43.5,
    dipole = 1.75,
    dielectric = 7.58,
    refractive_index = 1.4050,
    viscosity = 0.462,
    Trouton = 10.7,
    alpha = 0.0,
    beta = 0.55,
    pi_star = 0.55,
    E_T_30 = 37.4,
    ETN = 0.207,
    logP = 0.46,
    Flory_Huggins = 0.28,
    )

CH2Cl2 = dict(
    number = 1540,
    BP = 312.8,
    FP = 178.2,
    VDW_vol = 34.7,
    dipole = 1.14,
    dielectric = 8.93,
    refractive_index = 1.421,
    viscosity = 0.411,
    Trouton = 10.9,
    alpha = 0.13,
    beta = 0.1,
    pi_star = 0.82,
    E_T_30 = 40.7,
    ETN = 0.309,
    logP = 1.15,
    Flory_Huggins = 0.29,
    )

CHCl3 = dict(
    number = 1600,
    BP = 334.3,
    FP = 209.6,
    VDW_vol = 43.5,
    dipole = 1.15,
    dielectric = 4.89,
    refractive_index = 1.442,
    viscosity = 0.536,
    Trouton = 10.7,
    alpha = 0.2,
    beta = 0.1,
    pi_star = 0.58,
    E_T_30 = 39.1,
    ETN = 0.259,
    logP = 1.94,
    Flory_Huggins = 0.08,
    )

solvents = dict(
    nhexane = nhexane,
    benzene = benzene,
    toluene = toluene,
    THF = THF, 
    CH2Cl2 = CH2Cl2,
    CHCl3 = CHCl3,
    )