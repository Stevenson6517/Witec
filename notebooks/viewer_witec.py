# # View WITec Project files
#
# Learn about the ways we know how to open and inspec WITec Project files in this project.
#
# > This notebook is part of an experimental branch. The exact syntax of the attribute access may change.
#
# ## File structure
#
# Every WITec Project file is structured as a nested dictionary in binary form. The recipe for unpacking this dictionary is outlined in `witec/project.py`.
#
# The `witec/project.py` file in this project provides some high-level access to a WITec Project binary file. This notebook illustrates those high-level commands from the `Witec` class.

# +
import pathlib
import sys

from witec.project import Witec


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
search_pattern = "hBN-NA/*.WIP"

# List matching files
wip_files = sorted(DATA_DIR.glob(search_pattern))
for i, file in enumerate(wip_files):
    print(i, file.name)

# +
# Select a file according to desired index above
wip_file = list(wip_files)[0]

# Load the file as a class object
wip_object = Witec(wip_file)
print(wip_object)
# -

# ## Accessing raw contents
#
# The entire nested dictionary in binary form is extracted to a Witec file object as a Python dictionary. This dictionary can be viewed in totality using the `contents` attribute.
#
# This is a lengthy dictionary. Remember that in Jupyter Notebooks you can click on the left edge of a cell's border to collapse the contents.

wip_object.contents

# ## Accessing Info
#
# The Witec class provides some tailored attributes to access the most commonly needed information from a .WIP file. This information is helpful in making sense of an accompanying measurement, such as a Winspec .SPE file acquired during `External Spectrum`.
#
# During an `External Spectrum` acquisition in _ScanCtrlSpectroscopyPlus_, measurements are triggered at each pixel on a defined grid of coordinates. These coordinates are not explicitly stored in a .WIP file, but information helpful in recreating these coordinates is available in a rich-text document available from the _Witec Project_ project browser. The contents of this rich-text document can be extracted with the `info()` method.

wip_object.info()

# The above rich-text document is passed around as a string internally so that other scripts may make use of dedicated parsers.
#
# To see the contents in a prettier format, you can explicitly print the string in Python.

print(wip_object.info())

# ## Accessing Data
#
# _ScanCtrlSpectroscopyPlus_ is capable of performing measurements with its own built-in instruments. These can be configured from the `Measurement` menu, but they generally include sensor data from a connected photodetector and will be saved to a specific channel according to the configured `Measurement` options.
#
# These sensor readings are stored in a `Data` key under the nested Python dictionary. Each connected channel has its own nested dictionary of useful information, but the user is expected to navigate this dictionary and extract the useful information themselves because the structure of each dictionary is instrument-specific. Access all data dictionaries with the `data` attribute.

wip_object.data

# Explore each data dictionary by accessing its keys.

wip_object.data["Data 3"]


