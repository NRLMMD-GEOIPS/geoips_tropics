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

"""Module containing colormap for ~89GHz PMW products."""

import logging

LOG = logging.getLogger(__name__)

interface = "colormappers"
family = "matplotlib"
name = "cmap_tropics91"


def call(data_range=[200, 280], cbar_label="TB (K)"):
    """Colormap for displaying TROPICS 91 GHz data.

    Parameters
    ----------
    data_range : list of float, default [180, 280]
        Min and max value for colormap.
        Ensure the data range matches the range of the
        algorithm specified for use with this colormap
        The TROPICS 91GHZ colormap MUST include 180 and 280

    Returns
    -------
    dict
        Dictionary of matplotlib plotting parameters, to ensure consistent image output
    """
    min_tb = data_range[0]
    max_tb = data_range[1]

    if min_tb > 200 or max_tb < 280:
        raise ("TROPICS 91GHz TB range MUST include 200 and 280")

    from geoips.image_utils.colormap_utils import create_linear_segmented_colormap

    transition_vals = [
        (min_tb, 210),
        (210, 220),
        (220, 230),
        (230, 240),
        (240, 250),
        (250, 270),
        (270, max_tb),
    ]
    transition_colors = [
        ("white", "#A4641A"),
        ("#A4641A", "#FC0603"),
        ("#FFFF99", "#F4CD03"),
        ("#66CDAA", "#008B8B"),
        ("#CCFFCC", "#0FB503"),
        ("#06DCFD", "#0708B5"),
        ("navy", "white"),
    ]

    # ticks = [xx[0] for xx in transition_vals]

    # special selection of label

    ticks = [200, 210, 220, 230, 240, 250, 260, 270, 280]

    # selection of min and max values for colormap if needed
    min_tb = transition_vals[0][0]
    max_tb = transition_vals[-1][1]

    LOG.info("Setting cmap")
    mpl_cmap = create_linear_segmented_colormap(
        "cmap_89h", min_tb, max_tb, transition_vals, transition_colors
    )

    LOG.info("Setting norm")
    from matplotlib.colors import Normalize

    mpl_norm = Normalize(vmin=min_tb, vmax=max_tb)

    # Must be uniform or proportional, None not valid for Python 3
    cbar_spacing = "proportional"
    mpl_tick_labels = None
    mpl_boundaries = None

    # from geoips.image_utils.mpl_utils import create_colorbar
    # only create colorbar for final imagery
    # cbar = create_colorbar(fig, mpl_cmap, mpl_norm, ticks, cbar_label=cbar_label)
    mpl_colors_info = {
        "cmap": mpl_cmap,
        "norm": mpl_norm,
        "cbar_ticks": ticks,
        "cbar_tick_labels": mpl_tick_labels,
        "cbar_label": cbar_label,
        "boundaries": mpl_boundaries,
        "cbar_spacing": cbar_spacing,
        "colorbar": True,
        "cbar_full_width": True,
    }

    # return cbar, min_tb, max_tb
    return mpl_colors_info
