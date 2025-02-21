# WITec data formats

## ScanCtrlSpectroscopyPlus

The WITec AlphaSNOM is capable of collecting information in several
modes. In confocal microscopy mode, light may be collected by
transmission or reflection. In either transmission or reflection, the
collected light may be directed to an avalanche photodiode (APD) or a
spectrometer. The APD signal is represented by a single number
corresponding to the cumulative number of photons detected within a
given exposure interval, while a spectrometer will have an array of
values corresponding to the spectral intensity at various wavelengths.
Measurements can be collected at a single coordinate or grouped together
from a series of coordinates representing a 2D- or 3D-image acquisition.

In SNOM (Scattering Near-field Optical Microscopy) mode, the scattered
light is collected along an axis orthogonal to the plane of excitation
and directed to an APD. Typically this measurement is performed for a
series of coordinates within a 2D plane.

The measurement performed by the user will be saved in a WITecProject
file (`.WIP`) that contains the acquired data and relevant user
parameters like the acquisition mode, stage coordinates, exposure
settings, and timestamp. Figures generated from a subset of the raw data
may also be saved in the parent `.WIP` file.

These `.WIP` files are not trivial to inspect, but even if we could
inspect them, the various capabilities of the WITec AlphaSNOM mean that
the saved files may have data stored in uniquely shaped arrays depending
on the acquisition mode.

### WitecProject

The raw data from any `.WIP` file may be exported by WitecProject into a
plain text file, but this first requires a licensed working copy of the
software to open the file. Additionally, this plain-text version loses
any data compression put forth by the software to reduce file size,
meaning that the exported versions can easily be more than double the
original file size.

Some data governance policies require that the original data be archived
in the form it was generated by the instrument. Saving an easy-to-read
but needlessly-large duplicate alongside the original file is not
pragmatic, so this project provides helper functions to unpack the raw
data and a subset of the metadata from the original `.WIP` files.

Data files generated directly by tools of this software will store data
in the [HDF5][hdf5] format. Accessing these data files is still not
trivial to inspect with traditional file navigators, but this storage
standard is at least well-documented and many trusted third-party
extensions are available for opening `.hdf5` files.

[hdf5]: https://github.com/HDFGroup/hdf5

### Spectroscopy attachments 

Image acquisitions in confocal mode may gather a complete spectrum at
each pixel of the 2D- or 3D-scan through the use of an external
spectrometer. _ScanCtrlSpectroscopyPlus_ provides a way to trigger a
spectrometer or other external camera for acquisition at each
coordinate. The external instrument is responsible for storing and
managing the developing dataset, but _WITecProject_ is capable of
integrating this data into the `.WIP` file for image analysis.

In the case of _WITecProject v1.92_, the included setup contained a
license for a Princeton Instruments software, _WinSpec_, which handles
the spectrometer interface on Windows machines. (This program eventually
evolved into _LightField_, for readers other than legacy Windows XP
users, and files from _WinSpec_ can be opened in _LightField_.) The raw
spectroscopy data is stored with a `.SPE` extension and has its own set
of metadata relating to various things like the spectrometer
calibration, wavelength grating, and declared laser excitation source
during acquisition. Crucially, these `.SPE` files are unaware of any
imaging settings controlled by _ScanCtrlSpectroscopyPlus_ such as image
size or real coordinates. As with the `.WIP` files, these `.SPE` files
are not trivial to inspect. 

A single `.SPE` file can exist on its own, but if it is linked to a
`.WIP` file, the imaging tools will have access to both the real
coordinates (part of the `.WIP` file) and the intensity (part of the
`.SPE` file) when it generates figures. Linking the `.SPE` data to the
`.WIP` file is done through a manual import procedure in _WitecProject_,
which is sometimes neglected. If properly imported into a `.WIP` file,
the accompanying `.SPE` file is consumed in the process. It is unclear
if all of the `.SPE` metadata is preserved upon import, and the
_WitecProject v1.92_ software provides no easy way export the
spectroscopic subset back to its original `.SPE` format.

Users are faced with two competing choices:

1. Leave `.WIP` and `.SPE` files separate to preserve full metadata, but
   risk losing either file association during data cleanup or file
   renaming.
2. Combine `.WIP` and `.SPE` files to avoid breeding stray `.SPE` files
   that inevitably get separated from their associated `.WIP` acquisition.

This project provides another set of tools for inspecting and converting
`.SPE` files into `.hdf5` files. Users can then identify and combine
multiple metadata fields present in both `.WIP` and `.SPE` files in a
reversible manner. The caveat to the workflow is that the translators
provided by this project require access to both the `.SPE` and `.WIP`
files during the initial merging, meaning that this workflow enforces
option 1 above. The drawbacks can be mitigated by enforcing strict
naming conventions and maintaining identical filenames for associated
`.SPE` and `.WIP` content.

> Developer caveat: Having `.WIP` files that sometimes contain linked
> `.SPE` data and sometimes do not makes for a more complicated
> WIP-to-HDF5 conversion process
