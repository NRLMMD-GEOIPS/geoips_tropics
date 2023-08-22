# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

# @ An algorithm plugin specifies data manipulation steps required for a particualr
# @ product. When and how the "algorithm" is applied is determined by the "product"
# @ family.

# @ Replace all instances of @ within this template with appropriate values for
# @ your particular use case.
# @ Once complete, remove all lines containing "@" from this file.

"""Sample algorithm plugin, duplicate of "89pct".

Duplicate of Passive Microwave 89 GHz Polarization Corrected Temperature.
Data manipulation steps for the "89test" product, duplicate of "89pct".
This algorithm expects Brightness Temperatures in units of degrees Kelvin
"""
import logging

LOG = logging.getLogger(__name__)

# @ This should always be "algorithms" interface for "algorithms" plugins.
# @ Available python module-based interfaces can be found within
# @ geoips/interfaces/module_based.
interface = "algorithms"

# @ Allowable algorithm "family"s can be found in
# @ geoips/interfaces/module_based/algorithms.py.
# @ The algorithm "family" identifies the allowable call signature
# @  * required positional parameters
# @  * required kwargs
# @  * allowable kwargs
# @ The processing workflows are able to pass data to the algorithm
# @ appropriately based on the specified family.
family = "list_numpy_to_numpy"

# @ The algorithm plugin "name" is a unique identifier for this algorithm plugin.
name = "pmw_89test"


# @ All geoips module-based plugins must name the top level callable function "call".
# @ The parameters and keyword arguments must match what is specified in
# @ geoips/interfaces/module_based/algorithms.py
def call(
    arrays,
    output_data_range,
    min_outbounds="crop",
    max_outbounds="mask",
    norm=False,
    inverse=False,
):
    """89pct product algorithm data manipulation steps.

    This algorithm expects Brightness Temperatures in units of degrees Kelvin,
    and returns degrees Kelvin

    Parameters
    ----------
    arrays : list of numpy.ndarray
        * list of numpy.ndarray or numpy.MaskedArray of channel data
          and other variables, in order of sensor "variables" list
        * Channel data should be in degrees Kelvin
    output_data_range: list of float
        * List containing minimum and maximum value for final output data.
    min_outbounds: str, default="crop"
        * Operation to perform for data below minimum value
        * crop or mask
    max_outbounds: str, default="mask"
        * Operation to perform for data above maximum value
        * crop or mask
    norm: bool, default=False
        * Specify whether to normalize the data or not.
    inverse: bool, default=False
        * Specify whether to invert the data or not.

    Returns
    -------
    numpy.ndarray
        * numpy.ndarray or numpy.MaskedArray of appropriately scaled channel data
        * degrees Kelvin.
    """
    # @ Put your actual data manipulation steps within the function body.
    # @ This is a duplicate of the 89pct algorithm.
    h89 = arrays[0]
    v89 = arrays[1]

    out = (1.7 * v89) - (0.7 * h89)

    from geoips.data_manipulations.corrections import apply_data_range

    data = apply_data_range(
        out,
        min_val=output_data_range[0],
        max_val=output_data_range[1],
        min_outbounds=min_outbounds,
        max_outbounds=max_outbounds,
        norm=norm,
        inverse=inverse,
    )

    return data
