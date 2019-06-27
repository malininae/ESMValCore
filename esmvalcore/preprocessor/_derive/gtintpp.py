"""Derivation of variable `gtintpp`."""
import iris
import numpy as np

from ._baseclass import DerivedVariableBase


def calculate_total_flux(intpp_cube, cube_area):
    """
    Calculate the area of unmasked cube cells.

    Requires a cube with two spacial dimensions. (no depth coordinate).

    Parameters
    ----------
    cube: iris.cube.Cube
        Data Cube
    cube_area: iris.cube.Cube
        Cell area Cube

    Returns
    -------
    numpy.array:
        An numpy array containing the total flux of CO2.

    """
    data = []
    times = intpp_cube.coord('time')

    intpp_cube.data = np.ma.array(intpp_cube.data)
    for time_itr in np.arange(len(times.points)):

        total_flux = intpp_cube[time_itr].data * cube_area.data

        total_flux = np.ma.masked_where(intpp_cube[time_itr].data.mask,
                                        total_flux)
        data.append(total_flux.sum())

    ######
    # Create a small dummy output array
    data = np.array(data)
    return data


class DerivedVariable(DerivedVariableBase):
    """Derivation of variable `gtintpp`."""

    # Required variables
    required = [
        {
            'short_name': 'intpp',
#            'mip': 'Omon',
            'fx_files': [
                'areacello',
            ],
        },
    ]

    @staticmethod
    def calculate(cubes):
        """Compute longwave cloud radiative effect."""
        intpp_cube = cubes.extract_strict(
            iris.Constraint(name='surface_downward_mass_flux_of_carbon_dioxide'
                            '_expressed_as_carbon'))

        try:
            cube_area = cubes.extract_strict(iris.Constraint(name='cell_area'))
        except iris.exceptions.ConstraintMismatchError:
            pass

        total_flux = calculate_total_flux(intpp_cube, cube_area)

        # Dummy result cube
        result = intpp_cube.collapsed(
            ['latitude', 'longitude'],
            iris.analysis.MEAN,
        )
        result.units = intpp_cube.units * cube_area.units

        result.data = total_flux
        return result