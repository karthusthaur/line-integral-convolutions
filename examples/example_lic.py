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
## PROGRAM PARAMETERS
## ###############################################################
BOOL_DEBUG    = 0
BOOL_FILTER   = 1
BOOL_EQUALISE = 1


## ###############################################################
## MAIN PROGRAM
## ###############################################################
def main(size, num_iterations=1, num_repetitions=1):
  print("Started running demo script...")
  ## create figure canvas
  fig, _ = plt.subplots(figsize=(6,6), )
  ## define domain
  print("Initialising quantities...")
  dict_field   = fields.vFieldLotkaVolterra(size)
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
    for _ in range(num_iterations): sfield = lic.computeLIC(vfield, sfield, streamlength)
    if BOOL_FILTER:                 sfield = utils.filterHighPass(sfield)
  if BOOL_EQUALISE:                 sfield = equalize_adapthist(sfield)
  ## visualise the LIC
  print("Plotting data...")
  fig, _ = utils.plotLIC(
    sfield      = sfield,
    vfield      = vfield,
    bounds_rows = bounds_rows,
    bounds_cols = bounds_cols,
    bool_debug  = BOOL_DEBUG
  )
  ## save and close the figure
  print("Saving figure...")
  fig_name = f"example_lic.png"
  fig.savefig(fig_name, dpi=200, bbox_inches="tight")
  plt.close(fig)
  print("Saved:", fig_name)
  return 1


## ###############################################################
## SCRIPT ENTRY POINT
## ###############################################################
if __name__ == "__main__":
  main(
    size            = 500,
    num_iterations  = 3,
    num_repetitions = 3
  )
  sys.exit(0)


## END OF SCRIPT