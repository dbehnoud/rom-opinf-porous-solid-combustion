from opinf.lift import LifterTemplate
from opinf.pre import TransformerMulti, ShiftScaleTransformer
from numpy import concatenate, split
from config import *


def _check_shapes(species, *args):
    
    if len(species) != NUM_SPECIES:
        raise ValueError(f"{NUM_SPECIES} species required, "
                         f"got {len(species)}")
    _shape = species[0].shape
    for spc in species:
        if spc.shape != _shape:
            raise ValueError("species must all have same shape")
    for other in args:
        if other.shape != _shape:
            raise ValueError("inputs not aligned with species")
        
def mass2molar(masses, xi):
    
    # Check shapes.
    _check_shapes(masses, xi)

    # Do the conversion from mass fractions to molar concentrations.
    return [mass_fraction / (xi * molar_mass)
            for mass_fraction, molar_mass in zip(masses, MOLAR_MASSES)]


def molar2mass(molars, xi):
    
    _check_shapes(molars, xi)

    # Do the conversion from molar concentrations to mass fractions.
    return [molar_conc * molar_mass * xi
            for molar_conc, molar_mass in zip(molars, MOLAR_MASSES)]


class EulerLifter(LifterTemplate):
    """Lifting map for the Euler equations transforming conservative
    variables to specific volume variables.
    """
    @staticmethod
    def lift( data):
       
        # Unpack the CFD data.
        vx, vy, T, Ts, rhophi, Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2, \
            Y_wood, Y_char = split(data,NUM_STATES)
        solids = [Y_wood, Y_char]
        masses = [Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2]
        xi = 1/rhophi
      
        # Compute molar concentrations.
        molars = mass2molar(masses, xi)

        # Put the lifted data together.
        return concatenate([vx, vy, T, Ts, xi] + molars + solids)
        

    @staticmethod
    def unlift(data):
        
        # Unpack the lifted data.
        vx, vy, T, Ts, xi,c_CH4, c_O2, c_H2O, c_CO2, c_CO, c_N2, \
            c_wood, c_char = split(data, NUM_ROMVARS)
        molars = [c_CH4, c_O2, c_H2O, c_CO2, c_CO, c_N2]
        rhophi = 1/xi
        # Compute mass fractions.
        masses = molar2mass(molars, xi)
        solids = [c_wood, c_char]

        # Put the unlifted data together.
        return concatenate([vx, vy, T, Ts, rhophi] + masses + solids)
       

def get_combustion_transformer():

    combustion_transformer = TransformerMulti(
        transformers=[
            #opinf.pre.ShiftScaleTransformer(
            #    name="pressure", centering=True, scaling="maxabs", verbose=False
            #),
            ShiftScaleTransformer(
                name="x-velocity", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="y-velocity", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="temperature", centering=True, scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                name="s-temperature", centering=True, scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="specific volume-by-phi", centering=True, scaling="minmax", verbose=True
                name="specific volume", centering=False, scaling="maxabs", verbose=False
            ),
            # opinf.pre.ShiftScaleTransformer(
            #     # name="phi", centering=True, scaling="minmax", verbose=True
            #    name="iphi", centering=True, scaling="maxabs", verbose=False
            # ),
            ShiftScaleTransformer(
                #name="methane", scaling="minmax", verbose=True
                name="methane", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="oxygen", scaling="minmax", verbose=True
                name="oxygen", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="water", scaling="minmax", verbose=True
                name="water", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="carbon dioxide", scaling="minmax", verbose=True
                name="carbon dioxide", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="carbon monoxide", scaling="minmax", verbose=True
                name="carbon monoxide", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="nitrogen", scaling="minmax", verbose=True
                name="nitrogen", scaling="maxabs", verbose=False
            ),
            # opinf.pre.ShiftScaleTransformer(
            #     #name="ngas", scaling="minmax", verbose=True
            #     name="ngas", scaling="maxabs", verbose=False
            # ),
            ShiftScaleTransformer(
                #name="wood", scaling="minmax", verbose=True
                name="wood", scaling="maxabs", verbose=False
            ),
            ShiftScaleTransformer(
                #name="char", scaling="minmax", verbose=True
                name="char", scaling="maxabs", verbose=False
            )
        ]
    )
    return combustion_transformer