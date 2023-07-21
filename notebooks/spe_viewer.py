# # WinSpec Viewer for Princeton Instruments
#
# A simple notebook to explore the spectra in a .spe file
#
# Abilities:
# - View single spe spectrum
# - View a series of spectra linked in one file

# +
from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
from numbers import Number
import numpy as np

import subprocess
import sys
import os
import matplotlib.pyplot as plt
from warnings import warn
import h5py
import pyUSID as usid
import sidpy as sid
import SciFiReaders as sr

# from IPython.display import clear_output
# # %matplotlib inline

import witec.utils
from witec.spe import SPE
from witec.winspec import SpeFile
from witec.project import Witec
# -

data_path = r'../BELine_0004.h5'
dr = sr.NSIDReader(data_path)
# import inspect
# from pprint import pprint
# pprint(inspect.getmembers(dr))
dataset_sid = dr.read()[0]
fig = dataset_sid.plot();

h5_path = '../delete_me.hdf5'
with h5py.File(h5_path, mode='r') as h5_file:
    h5_main = usid.hdf_utils.get_all_main(h5_file)[-1]
    # usid.plot_utils.use_nice_plot_params()
    h5_main.visualize()



# Network drive must be mounted locally for path to be available
# Otherwise, use data directory from this project
network_path = Path("/Volumes/public/David Curie/Data/")
if network_path.exists():
    data_dir = network_path
else:
    data_dir = "../data"
spe_files = list(Path.glob(data_dir, "hBN-WashU/*.SPE"))
for i, spe_file in enumerate(spe_files):
    print(i, spe_file.name)

# Pick file from above (0-indexed)

spe_file = spe_files[6]
spe_object = SpeFile(spe_file)
# spe_object = SPE(spe_file)
print(spe_object)

# +
# Look for position data in accompanying WIP file
wip_file = f"{spe_object.slug}.WIP"
wip_object = Witec(wip_file)

print(witec.utils.assemble_metadata(spe_object.slug))

# +
# Look for position data in another file
supplemental = f'{spe_object.slug}.WIP'
spe_object.link_supplemental(supplemental)
plt.style.use(['default', 'science', 'notebook'])

fig, ax = plt.subplots()
spe_object.heatmap(ax, start_wl=690, end_wl=697, cmap='jet', vmin=None, vmax=None)
# fig.patch.set_alpha(0)
figname = f'{spe_object.slug}.png'
fig.savefig(figname, bbox_inches='tight')
print(f'Figure saved to {figname}')
plt.show()

# +
loc = (60, 54) # location in real coordinates from heatmap
index = spe_object.index_from_coord(loc)

fig, ax = plt.subplots()
spe_object.plot_spectrum(ax, index)
title = f'{spe_object.basename}\nindex: {index} location: {loc}'
ax.set_title(title)
# ax.set_ylim(500, 1200)
ax.set_xlim(690, 698)
figname = f'{spe_object.slug}_spectrum-{index}.png'
fig.savefig(figname, bbox_inches='tight')
print(f'Figure saved to {figname}')
plt.show()
# -

fig, ax = plt.subplots()
spe_object.plot_spectrum(ax, 0)
plt.show()

# Open the file and inspect its shape

# file = '405_Cu.SPE'
data = spe_object.spe_dict['data']
data.shape # (number of acquisitions, rows per acquisition, columns per acquisition)

# In spectroscopy mode, CCD pixels in the y-direction are binned together vertically so that the
# spectrum appears as a set of intensity values per column. This means `rows per acquisition` is 1
# and the final dimension in the above dataset corresponds to the intensity values in each column.
#
# In imaging mode, the CCD pixels keep track of intensity at each (x,y) coordinate. In this case,
# `rows per acquisition` corresponds to the height of the CCD array or Region of Interest (ROI)
# and the final dimension in the above dataset corresponds to the intensity values across the width
# of the CCD or ROI at each row.
#
# We can bin these values manually in case the user accidentally acquired the spectrum in image mode.
#
# The following block of code sums the intensity from all rows and collapses the row dimensions so that
# the spectra are stored as a 2D array consisting of _n_ arrays of length _CCD width_
# (where _CCD width_ is 1340 for PIXIS).
#
# The end result is an array of size (n, spectral_width) where index _n_ corresponds to the acquisition
# number and *spectral_width* is the width of the CCD. Each spectrum is accessed as:
# ```python
# >>> spectra[i]
# ```

# +
spectra = []

for acquisition in data:
   spectrum = acquisition.sum(axis=0) # Combine all rows
   spectra.append(spectrum) # Store to new list

spectra = np.asarray(spectra) # Convert list to array
print(spectra.shape)
# -

# If there are multiple spectra present, they probably came from a series of measurements
# over a 2x2 grid of spatial locations. If this is the case, we need to know the spatial
# dimensions of our image for us to map the spectra to an image.

# +
# The dimensions of image (x,y) acquired in a spectral image
x_width = 98  # Adjust this based on the known number of columns, unique to each file
y_width = 98  # Adjust this based on the known number of rows, unique to each file
position_indices = []
for y in range(y_width):
   for x in range(x_width):
       position_indices.append((x,y))

position_indices = np.asarray(position_indices)

step_xy = 1e-6 # Step size between measured acquisitions
position_values = position_indices * step_xy
# -

# Specify coordinates from ancillary data
x = position_values[:, 0]
y = position_values[:, 1]
x_min = np.amin(x)
x_max = np.amax(x)
y_min = np.amin(y)
y_max = np.amax(y)
extents = (x_min, x_max, y_max, y_min)  # left, right, bottom, top

# +
# Specify integration region
start_wl = 600
end_wl = 800

# Transform main_dataset based on dimensions and selected integration
start, end = 0, 1340
# start = find_nearest(spectroscopic_values, start_wl)
# end = find_nearest(spectroscopic_values, end_wl)
# integrated_counts = np.sum(main_dataset, axis=1)
integrated_counts = np.sum(spectra[:, start:end], axis=1)
integrated_counts_2D = integrated_counts.reshape(y_width, x_width)

# Plot the data as an image
fig, ax = plt.subplots()
heatmap = ax.imshow(integrated_counts_2D, extent=extents, cmap='RdBu_r')
# heatmap = ax.imshow(integrated_counts_2D)
ax.set_aspect('equal')
# ax.xaxis.set_visible(False)
# ax.yaxis.set_visible(False)
ax.set_title('PL Intensity', fontsize='small')
spe_object.add_colorbar(heatmap)
# fig.set_alpha(0.1)
# fig.savefig(f'{file}.png')
# -

for spectrum in spectra[0:20]:
   fig, ax = plt.subplots()
   ax.plot(spe_object.spectroscopic_values, spectrum)
   ax.set_xlabel('Wavelength (nm)')
   ax.set_ylabel('Intensity')
   plt.show()




