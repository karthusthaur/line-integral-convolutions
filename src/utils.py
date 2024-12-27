## This file is part of the "line-integral-convolutions" project.
## Copyright (c) 2024 Neco Kriel.
## Licensed under the MIT License. See LICENSE for details.


## ###############################################################
## IMPORT MODULES
## ###############################################################
import time
import numpy as np
import matplotlib.pyplot as plt

from scipy import ndimage
from matplotlib.colors import to_rgba


## ###############################################################
## START OF UTILITY FUNCTIONS
## ###############################################################
def time_func(func):
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_elapsed = time.time() - time_start
        print(f"{func.__name__}() took {time_elapsed:.3f} seconds to execute.")
        return result

    return wrapper


def filter_high_pass(sfield: np.ndarray, sigma: float = 3.0):
    lowpass = ndimage.gaussian_filter(sfield, sigma)
    gauss_highpass = sfield - lowpass
    return gauss_highpass


def plot_lic(
    sfield: np.ndarray,
    vfield: np.ndarray,
    bounds_rows=None,
    bounds_cols=None,
    bool_debug=False,
):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(
        sfield,
        cmap="bone",
        origin="lower",
        extent=[bounds_rows[0], bounds_rows[1], bounds_cols[0], bounds_cols[1]],
    )
    if bool_debug:
        coords_row = np.linspace(bounds_rows[0], bounds_rows[1], sfield.shape[0])
        coords_col = np.linspace(bounds_cols[0], bounds_cols[1], sfield.shape[1])
        mg_x, mg_y = np.meshgrid(coords_col, coords_row, indexing="xy")
        color = to_rgba("green", alpha=0.75)
        ax.streamplot(
            mg_x,
            mg_y,
            vfield[0],
            vfield[1],
            color=color,
            arrowstyle="->",
            linewidth=1.0,
            density=0.5,
            arrowsize=0.5,
            broken_streamlines=False,
        )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(bounds_rows)
    ax.set_ylim(bounds_cols)
    return fig, ax


## END OF UTILITY FUNCTIONS
