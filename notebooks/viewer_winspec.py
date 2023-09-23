# # View Winspec data files
#
# Learn about the ways we know how to open and inspec Winspec files in this project.
#
# > This notebook is part of an experimental branch. The exact syntax of the attribute access may change.
#
# ## File structure
#
# Every Winspec file contains a header with a predefined set of attributes and a variable number of datasets. The header describes necessary instrument settings to reproduce a measurement and necessary file metadata to properly identify and unpack the datasets.
#
# A single spectrum is stored as a 1D array of intensity values. These intensity values are described according to a Region of Interest in the spectrometer CCD. The CCD pixels are mapped separately to a wavelength according to internal calibration parameters in the file header. The wavelengths of each spectrum are computed on the fly and are not stored with each spectrum.
#
# The header contains information on the datatype of the stored spectra. In the case where multiple spectra are saved in one file, the data portion of the file will appear as an array of 1D intensity values (one array for each spectrum).
#
# The `witec/winspec.py` file in this project provides some low-level access to this binary file and the `witec/spe.py` file wraps these low-level access commands in a structured high-level class. This notebook illustrates those high-level commands from the `SPE` class.

# +
import pathlib
import sys

from witec.spe import SPE


# This project saves data in a network drive, available only from a Vanderbilt IP address.
# If you connect your personal computer to this network drive, you can access its files
if "darwin" in sys.platform:
    NETWORK_PATH = "/Volumes/public/"
elif "win32" in sys.platform:
    NETWORK_PATH = "Z://"  # Adjust as necessary, depending on how you mounted network drive
NETWORK_DIR = pathlib.Path(NETWORK_PATH)

# By default, search the data directory from the network path above.
# In the event the network drive is unavailable, assume local data is saved with this project
# in a folder named `data`, available from the project root (or one directory behind this notebook).
if NETWORK_DIR.exists():
    print("Connected to Network Directory. Defaulting search to the following location:")
    DATA_DIR = pathlib.Path(NETWORK_DIR, "David Curie/Data")
else:
    print("Network Directory unavailable. Defaulting search to the following location:")
    DATA_DIR = pathlib.Path("../data")
print(DATA_DIR)

# +
# Find a specific file by search patterns
search_pattern = "hBN-NA/*.SPE"

# List matching files
spe_files = sorted(DATA_DIR.glob(search_pattern))
for i, file in enumerate(spe_files):
    print(i, file.name)

# +
# Select a file according to desired index above
spe_file = list(spe_files)[0]

# Load the file as a class object
spe_object = SPE(spe_file)
print(spe_object)
# -

# One an SPE class object has been created, you have access to some high-level attributes to better inspect the file.

# ## Inspect file header
#
# The `header` attribute returns all file metadata as a Python dictionary.
#
# This is a lengthy dictionary. Remember that in Jupyter Notebooks you can click on the left edge of a cell's border to collapse the contents.

spe_object.header

# Specific values from this dictionary can be access according to normal Python access rules for dictionaries.
#
# For instance, the below syntax allows you to access the acquisition date as a string.

spe_object.header["date"]

# You can also access nested items.
#
# For instance, the below syntax allows you to view the axis units. Photoluminescence spectra typically use `wavelength [nm]`, but Raman spectra may use `wavenumbers [cm-1]`.

spe_object.header["xcalibration"]["string"]

# ### Access wavelength calibrations
#
# The SPE class provides a helper function to calculate the axis wavelength based on the file header calibration data and the known ROI from the acquisition. These computed values can be returned from any SPE object as a numpy array with the attrtibue `axis`.

spe_object.axis

# ## Inspect data
#
# The `data` attribute returns all spectra as a structured numpy array.

spe_object.data

# The shape of the data hints at whether this is a single acquisition or a series of consequtive acquistions.
#
# The array is structured as: (`number of acquisitions`, `columns`, `rows`)
#
# The size of each acquisition matches the ROI during collection. For a full spectrum on the PIXIS spectrometer camera, the CCD is 1340 pixels wide and 100 pixels tall. The size of `columns` and `rows` depends on the data acquisition mode specified in Winspec.
#
# In spectroscopy mode, all vertical pixels in the specified ROI are binned together and counted as one pixel, so `rows = 1`.
#
# In imaging mode, each pixel is read independently, so `rows = number of vertical pixels specified in ROI`.

spe_object.data.shape


