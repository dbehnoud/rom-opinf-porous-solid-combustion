# Chemical species in the combustion reaction.
SPECIES = ["CH4", "O2", "H2O", "CO2", "CO", "N2"]
solids = ["wood",'char']

# Solution variables for the raw GEMS data.
STATE_VARIABLES = ["vx", "vy", "T", "Ts", "rhophi"] + SPECIES + solids


# Variables that the ROM learns from and makes predictions for.
ROM_VARIABLES = ["vx", "vy", "T","Ts", "xi"] + SPECIES + solids


NUM_SPECIES = len(SPECIES)                  # Number of chemical species.
NUM_STATES = len(STATE_VARIABLES)          # Number of GEMS variables.
NUM_ROMVARS = len(ROM_VARIABLES)            # Number of learning variables.


# Chemistry and physics -------------------------------------------------------
MOLAR_MASSES = [16.04,                      # Molar mass of CH4 [kg/kmol].
                32.0,                       # Molar mass of O2  [kg/kmol].
                18.0,                       # Molar mass of H2O [kg/kmol].
                44.01,                      # Molar mass of CO2 [kg/kmol].
                28.01,                      # Molar mass of CO [kg/kmol].
                28.01]                     # Molar mass of N2 [kg/kmol]. 

R_UNIVERSAL = 8.3144598                     # Univ. gas constant [J/(mol K)].
rho_s0 = 1050                               #[kg/m3]