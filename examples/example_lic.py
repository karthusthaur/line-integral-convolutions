## ###############################################################
## MODULES
## ###############################################################
import sys
import numpy as np
import matplotlib.pyplot as plt

from skimage.exposure import equalize_adapthist

from src import fields
from src import utils
from src import lic


## ###############################################################
## MAIN PROGRAM
## ###############################################################
def main(
    size,
    num_iterations  = 1,
    num_repetitions = 1,
    bool_filter     = True,
    bool_equalise   = True,
    bool_debug      = False,
  ):
  print("Started running demo script...")
  ## create figure canvas
  fig, _ = plt.subplots(figsize=(6,6))
  ## define domain
  print("Initialising quantities...")
  dict_field   = fields.vfield_lotka_volterra(size)
  vfield       = dict_field["vfield"]
  streamlength = dict_field["streamlength"]
  num_rows     = dict_field["num_rows"]
  num_cols     = dict_field["num_cols"]
  bounds_rows  = dict_field["bounds_rows"]
  bounds_cols  = dict_field["bounds_cols"]
  sfield       = np.random.rand(num_rows, num_cols) # random background
  ## apply the LIC a few times: equivelant to painting over with a few brush strokes
  print("Computing LIC...")
  for _ in range(num_repetitions):
    for _ in range(num_iterations): sfield = lic.compute_lic(vfield, sfield, streamlength)
    if bool_filter:                 sfield = utils.filter_high_pass(sfield, sigma=8.0)
  if bool_equalise:                 sfield = equalize_adapthist(sfield)
  ## visualise the LIC
  print("Plotting data...")
  fig, _ = utils.plot_lic(
    sfield      = sfield,
    vfield      = vfield,
    bounds_rows = bounds_rows,
    bounds_cols = bounds_cols,
    bool_debug  = bool_debug
  )
  ## save and close the figure
  print("Saving figure...")
  fig_name = f"example_lic.png"
  fig.savefig(fig_name, dpi=300, bbox_inches="tight")
  plt.close(fig)
  print("Saved:", fig_name)
  return 1


## ###############################################################
## SCRIPT ENTRY POINT
## ###############################################################
if __name__ == "__main__":
  main(
    size            = 2000,
    num_iterations  = 2,
    num_repetitions = 2,
    bool_filter     = 1,
    bool_equalise   = 1,
    bool_debug      = 0,
  )
  sys.exit(0)


## END OF SCRIPT