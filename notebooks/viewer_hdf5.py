# # View hdf5 files stored in pyUSID format
#
# Learn about the ways we can open and use hdf5 files generated by this project
#
# > This notebook is part of an experimental branch. The exact syntax of the
# attribute access may change.
#
# ## File structure
#
# Every hdf5 file is structured in pyUSID format. Full compatibility with the
# [pycroscopy][pycroscopy] ecosystem is available, but this notebook aims to
# highlight how one could use default extraction methods to inspect the
# contents of a single hdf5 file.
#
# [pycroscopy]: https://github.com/pycroscopy/pycroscopy
#
# The pyUSID format exects that the main meausurment of an instrument
# acquisition process is saved as a 2D array and is identifiable with some
# mandatory metadata describing the acquisition.
#
# In the hdf5 files generated by this project, measurements live under a group
# called `Measurement_XXX` where `XXX` is a sequentially increasing index
# starting from `000`. In this group, there is a main dataset called `Raw_Data`
# structured as a 2D array.
#
# The ancillary datasets `Position_Indices` and `Position_Values` together
# describe a mapping that allows the association of each index in the 2D
# `Raw_Data` with physical coordinates. These coordinates may be expressed in
# real units (i.e. `m`) or in instrument units (i.e. `pixel`).
#
# The ancillary datasets `Spectroscopic_Indices` and `Spectroscopic_Values`
# together describe a mapping that allows the association of each array in the
# 2D `Raw_Data` with appropriate labels. This mapping may represent a
# wavelength association with each CCD pixel or a specific channel for (R,G,B)
# image data.

# +
import pathlib
import sys

import h5py
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
import numpy as np
import pyUSID as usid


# See https://nbviewer.jupyter.org/github/mgeier/python-audio/blob/master/plotting/matplotlib-colorbar.ipynb
def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1.0 / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


# This project saves data in a network drive, available only from a Vanderbilt
# IP address.
# If you connect your personal computer to this network drive, you
# can access its files
if "darwin" in sys.platform:
    NETWORK_PATH = "/Volumes/HaglundNAS/"
elif "win32" in sys.platform:
    NETWORK_PATH = (
        "Z://"  # Adjust as necessary, depending on how you mounted network drive
    )
NETWORK_DIR = pathlib.Path(NETWORK_PATH)

# By default, search the data directory from the network path above.
# In the event the network drive is unavailable, assume local data is saved
# with this project in a folder named `data`, available from the project root
# (or one directory behind this notebook).
if NETWORK_DIR.exists():
    print(
        "Connected to Network Directory. Defaulting search to the following location:"
    )
    DATA_DIR = pathlib.Path(NETWORK_DIR, "curieda/data")
else:
    print("Network Directory unavailable. Defaulting search to the following location:")
    DATA_DIR = pathlib.Path("../data")
print(DATA_DIR)

# +
# Find a specific file by search patterns
search_pattern = "*.hdf5"

# List matching files
h5_files = sorted(DATA_DIR.glob(search_pattern))
for i, file in enumerate(h5_files):
    print(i, file.name)

# +
# Select a file according to desired index above
h5_path = list(h5_files)[0]

# Load the file manually
with h5py.File(h5_path, mode="r") as h5_file:
    # Print a directory tree
    for key in h5_file.keys():
        print(key)
        for dataname in h5_file[key].keys():
            print("   ", dataname)
# -

# The below snippet shows how you might access datasets within a single hdf5 file.
#
# Group access mimics typical dictionary access for Python dictionaries, but
# remain compressed in memory for typical access. This means the dictionary
# values are lost when you close the file.

# +
# View the Raw Data as a 2D array
with h5py.File(h5_path, mode="r") as h5_file:
    # Extract datasets
    temporary_main_dataset = h5_file["Measurement_000"]["Raw_Data"]
    temporary_position_dataset = h5_file["Measurement_000"]["Position_Values"]
    temporary_spectroscopic_dataset = h5_file["Measurement_000"]["Spectroscopic_Values"]

    # Show that extrated datasets are still bundled
    print("DISPLAYING DATASETS AS PYTHON SEES THEM IN MEMORY\n")
    print(temporary_main_dataset)
    print(temporary_position_dataset)
    print(temporary_spectroscopic_dataset)

    # Access the values of the datasets with [()] notation
    print("\n-------------------------------")
    print("DISPLAYING CONTENTS OF DATASETS\n")
    print("Main dataset:\n", temporary_main_dataset[()])
    print("Position dataset:\n", temporary_position_dataset[()])
    print("Spectroscopic dataset:\n", temporary_spectroscopic_dataset[()])

print("\n---------------------------------------------")
print("DISPLAYING DATASETS AFTER THE FILE IS CLOSED\n")
print("Main dataset:", temporary_main_dataset)
print("Position dataset:", temporary_position_dataset)
print("Spectroscopic dataset:", temporary_spectroscopic_dataset)
# -

# If you need continued access to the contents of a single hdf5 file after the
# file is closed, write the contents to another variable as a copy.

# +
# View the Raw Data as a 2D array
with h5py.File(h5_path, mode="r") as h5_file:
    # Extract datasets
    temporary_main_dataset = h5_file["Measurement_000"]["Raw_Data"]
    temporary_position_dataset = h5_file["Measurement_000"]["Position_Values"]
    temporary_spectroscopic_dataset = h5_file["Measurement_000"]["Spectroscopic_Values"]

    # Show that extrated datasets are still bundled
    main_dataset = temporary_main_dataset[()].copy()
    position_dataset = temporary_position_dataset[()].copy()
    spectroscopic_dataset = temporary_spectroscopic_dataset[()].copy()

print("Main dataset:", main_dataset.shape, "\n", main_dataset, "\n")
print("Position dataset:", position_dataset.shape, "\n", position_dataset, "\n")
print(
    "Spectroscopic dataset:",
    spectroscopic_dataset.shape,
    "\n",
    spectroscopic_dataset,
    "\n",
)
# -

# As an example of how you can use this data to create custom visualizations in
# native Python syntax, consider the following.
#
# The cell below will create a 2D image representing the intensity values
# gathered at each coordinate of an `External Spectrum` acquired from
# _ScanCtrlSpectroscopyPlus_. The 2D main dataset is converted to a 3D array
# whose shape is determined by the number of unique x and y coordinates from
# the position dataset.

# +
rows = np.unique(position_dataset[:, 0])  # x coordinates
cols = np.unique(position_dataset[:, 1])  # y coordinates
position_values = np.reshape(position_dataset, (len(rows), len(cols), -1))

intensity_values = np.sum(
    main_dataset, axis=1
)  # Sum intensity across all pixels in each spectrum
intensity_map = np.reshape(
    intensity_values, (len(rows), len(cols), -1)
)  # shape (x, y, I) where I is Intensity

with plt.style.context("default"):
    fig, ax = plt.subplots()
    ax.set_title(f"{h5_path.stem}\n")
    img = ax.imshow(intensity_map, cmap="gist_stern")
    add_colorbar(img, label="Intensity")
    ax.set_aspect("equal")
    output = h5_path.with_suffix(".png")
    fig.savefig(output, dpi=300, bbox_inches="tight")
    print(f"Figure saved to {output}")
    plt.show()
# -

# # pyUSID native exploration
#
# Because the files are saved in pyUSID format, you can make use of some of
# pyUSID's helper scripts.
#
# > Make sure you have pyUSID installed in your conda environment (`conda
# install -c conda-forge pyusid`). This dependency is not yet commited to the
# main repository, so if you followed instructions to install your dependencies
# as outlined in the `main` Git branch, and then switched branches to
# `feature/hdf5` to run this notebook, you won't have the updated dependency.
# Once you install this dependency once, you won't need to install it again
# when switching branches.

# +

with h5py.File(h5_path, mode="r") as h5_file:
    h5_main = usid.hdf_utils.get_all_main(h5_file)[-1]
    h5_main.visualize()
    plt.show()
# -
