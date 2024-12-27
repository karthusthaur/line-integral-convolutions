## This file is part of the "line-integral-convolutions" project.
## Copyright (c) 2024 Neco Kriel.
## Licensed under the MIT License. See LICENSE for details.


## ###############################################################
## IMPORT MODULES
## ###############################################################
import numpy as np

from numba import njit, prange

from src.utils import time_func


## ###############################################################
## LIC IMPLEMENTATION
## ###############################################################
@njit
def taper_pixel_contribution(streamlength: int, step_index: int) -> float:
    return 0.5 * (1 + np.cos(np.pi * step_index / streamlength))


@njit
def advect_streamline(
    vfield: np.ndarray,
    sfield_in: np.ndarray,
    start_row: int,
    start_col: int,
    dir_sgn: int,
    streamlength: int,
    bool_periodic_BCs: bool = True,
) -> tuple:
    weighted_sum = 0.0
    total_weight = 0.0
    row_float, col_float = start_row, start_col
    num_rows, num_cols = vfield.shape[1], vfield.shape[2]
    for step in range(streamlength):
        row_int = int(np.floor(row_float))
        col_int = int(np.floor(col_float))
        vel_col = dir_sgn * vfield[0, row_int, col_int]
        vel_row = dir_sgn * vfield[1, row_int, col_int]
        ## skip if the field magnitude is zero: advection has halted
        if abs(vel_row) == 0.0 and abs(vel_col) == 0.0:
            break
        ## compute how long the streamline advects before it leaves the current cell region (divided by cell-centers)
        if vel_row > 0.0:
            delta_time_row = (np.floor(row_float) + 1 - row_float) / vel_row
        elif vel_row < 0.0:
            delta_time_row = (np.ceil(row_float) - 1 - row_float) / vel_row
        else:
            delta_time_row = np.inf
        if vel_col > 0.0:
            delta_time_col = (np.floor(col_float) + 1 - col_float) / vel_col
        elif vel_col < 0.0:
            delta_time_col = (np.ceil(col_float) - 1 - col_float) / vel_col
        else:
            delta_time_col = np.inf
        ## equivelant to a CFL condition
        time_step = min(delta_time_col, delta_time_row)
        ## advect the streamline to the next cell region
        col_float += vel_col * time_step
        row_float += vel_row * time_step
        if bool_periodic_BCs:
            row_float = (row_float + num_rows) % num_rows
            col_float = (col_float + num_cols) % num_cols
        else:
            row_float = max(0.0, min(row_float, num_rows - 1))
            col_float = max(0.0, min(col_float, num_cols - 1))
        ## weight the contribution of the current pixel based on its distance from the start of the streamline
        contribution_weight = taper_pixel_contribution(streamlength, step)
        weighted_sum += contribution_weight * sfield_in[row_int, col_int]
        total_weight += contribution_weight
    return weighted_sum, total_weight


@njit(parallel=True)
def _compute_lic(
    vfield: np.ndarray,
    sfield_in: np.ndarray,
    sfield_out: np.ndarray,
    streamlength: int,
    num_rows: int,
    num_cols: int,
) -> np.ndarray:
    for row in prange(num_rows):
        for col in range(num_cols):
            forward_sum, forward_total = advect_streamline(
                vfield, sfield_in, row, col, +1, streamlength
            )
            backward_sum, backward_total = advect_streamline(
                vfield, sfield_in, row, col, -1, streamlength
            )
            total_sum = forward_sum + backward_sum
            total_weight = forward_total + backward_total
            if total_weight > 0.0:
                sfield_out[row, col] = total_sum / total_weight
            else:
                sfield_out[row, col] = 0.0
    return sfield_out


@time_func
def compute_lic(
    vfield: np.ndarray, sfield_in: np.ndarray = None, streamlength: int = None
):
    num_comps, num_rows, num_cols = vfield.shape
    sfield_out = np.zeros((num_rows, num_cols), dtype=np.float32)
    if sfield_in is None:
        sfield_in = np.random.rand(num_rows, num_cols).astype(np.float32)
    if streamlength is None:
        streamlength = 10
    return _compute_lic(vfield, sfield_in, sfield_out, streamlength, num_rows, num_cols)


## END OF LIC IMPLEMENTATION
