from opinf.lift import LifterTemplate
from numpy import concatenate
from config import *

def _check_shapes(species, *args):
    """Ensure NUM_SPECIES species are passed in (mass fractions or molar
    concentrations) and that each argument has the same shape.
    """
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
    """Convert mass fractions to molar concentrations following

    Parameters
    ----------
    masses : list of NUM_SPECIES (domain_size, num_snapshots) ndarrays
        Mass fractions for each of the chemical species.
    xi : (domain_size, num_snapshots) ndarray
        Specific volume of the mixture [m^3/kg]

    Returns
    -------
    molars : list of NUM_SPECIES (domain_size, num_snapshots) ndarrays
        Molar concentrations for each chemical species [mol/m^3].
    """
    # Check shapes.
    _check_shapes(masses, xi)

    # Do the conversion from mass fractions to molar concentrations.
    return [mass_fraction / (xi * molar_mass)
            for mass_fraction, molar_mass in zip(masses, MOLAR_MASSES)]


def molar2mass(molars, xi):
    """Convert molar concentrations to mass fractions following

    Parameters
    ----------
    molars : list of NUM_SPECIES (domain_size, num_snapshots) ndarrays
        Molar concentrations for each chemical species [mol/m^3].
    xi : (domain_size, num_snapshots) ndarray
        Secific volume (1/density) [m^3/kg].

    Returns
    -------
    masses : list of NUM_SPECIES (domain_size, num_snapshots) ndarrays
        Mass fractions for each of the chemical species.
    """
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
        """Transform CFD data to the lifted variables,

        [p, v_x, v_y, T, Ts, phi, Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2, Y_ngas]
        -->
        [p, v_x, v_y, T, Ts, xi/phi, c_CH4, c_O2, c_H2O, c_CO2, c_CO, c_N2, ].

        Parameters
        ----------
        data : (NUM_STATES*dof, num_snapshots) ndarray
        Unscaled, untransformed CFD data.

        Returns
        -------
         : (NUM_ROMVARS*dof, num_snapshots) ndarray
            Nonscaled, lifted data.
        """
        # Unpack the CFD data.
        vx, vy, T, Ts, rhophi, Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2, \
            Y_wood, Y_char = np.split(data,NUM_STATES)
        solids = [Y_wood, Y_char]
        masses = [Y_CH4, Y_O2, Y_H2O, Y_CO2, Y_CO, Y_N2]
        xi = 1/rhophi
      
        # Compute molar concentrations.
        molars = mass2molar(masses, xi)

        # Put the lifted data together.
        return concatenate([vx, vy, T, Ts, xi] + molars + solids)
        

    @staticmethod
    def unlift(data):
        """Transform the learning variables back to the GEMS variables,

        [p, v_x, v_y, T, xi, c_CH4, c_O2, c_H2O, c_CO2]
        -->
        [p, v_x, v_y, T, Y_CH4, Y_O2, Y_H2O, Y_CO2]

        Parameters
        ----------
        data : (NUM_ROMVARS*dof, num_snapshots) ndarray
        Nonscaled, lifted data.

        Returns
        -------
        unlifed_data : (NUM_GEMSVARS*dof, num_snapshots) ndarray
        Unscaled, untransformed GEMS data.
        """
        # Unpack the lifted data.
        vx, vy, T, Ts, xi,c_CH4, c_O2, c_H2O, c_CO2, c_CO, c_N2, \
            c_wood, c_char = np.split(data, NUM_ROMVARS)
        molars = [c_CH4, c_O2, c_H2O, c_CO2, c_CO, c_N2]
        rhophi = 1/xi
        # Compute mass fractions.
        masses = molar2mass(molars, xi)
        solids = [c_wood, c_char]

        # Put the unlifted data together.
        return concatenate([vx, vy, T, Ts, rhophi] + masses + solids)
       