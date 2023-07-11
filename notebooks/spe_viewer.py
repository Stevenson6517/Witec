# # WinSpec Viewer for Princeton Instruments
#
# A simple notebook to explore the spectra in a .spe file
#
# Abilities:
# - View single spe spectrum
# - View a series of spectra linked in one file

# +
from collections import deque
from collections.abc import Set, Mapping
from dateutil import parser
from glob import glob
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
from numbers import Number
import numpy as np
import os
import re
import sys

import winspec

class SPE:
    def __init__(self, file):
        self.spe_dict = winspec.read_spe(file)
        self.restore_datatypes()
        self.extract_metadata()
        self.build_spectroscopic_dataset()

    def __repr__(self):
        description = {
            'Filename' : self.SPEFNAME,
            'Observation date' : self.OBSDATE,
            'Data shape' : self.spe_dict['data'].shape,
            'Accumulations' : self.ACCUMULATIONS,
            'Exposure (sec)' : self.EXPOSURE,
            'Background corrected' : self.BACKGROUND,
            'Flatfield corrected' : self.FLATFIELD,
            'Center wavelength (nm)' : self.XCALIB['SpecCenterWlNm'],
            'Grating (g/mm)' : self.XCALIB['SpecGrooves'],
            'Chip Temp (C)' : self.CHIPTEMP,
            'Size in memory (kb)' : '{:,d}'.format(round(self.getsize()/1e3))
        }
        return '\n'.join([f'{key:<22}: {value}' for key, value in description.items()])

    def restore_datatypes(self):
        """Reduce spe_dict filesize by converting data to uint16."""
        self.spe_dict['data'] = np.asarray(self.spe_dict['data'], dtype=np.int32)
        return None

    def extract_metadata(self):
        self.IGAIN = self.spe_dict['IGAIN']
        self.EXPOSURE = self.spe_dict['EXPOSURE']
        self.SPEFNAME = self.spe_dict['SPEFNAME']
        self.OBSDATE = parser.parse(self.spe_dict['OBSDATE'].decode('UTF-8')).date()
        self.CHIPTEMP = self.spe_dict['CHIPTEMP']
        self.COMMENTS = self.spe_dict['COMMENTS'].decode('UTF-8')
        self.XCALIB = self.spe_dict['XCALIB']
        self.ACCUMULATIONS = self.spe_dict['ACCUMULATIONS']
        self.FLATFIELD = self.spe_dict['FLATFIELD']
        self.BACKGROUND = self.spe_dict['BACKGROUND']
        # Helpful variables
        self.slug = self.strip_extension(self.SPEFNAME)
        self.basename = os.path.basename(self.slug)
        return None
    
    def bytes_to_string(self, array, encoding='utf-8'):
        string = []
        for byte in array:
            string.append(byte.decode(encoding))
        return ''.join(string)

    def extract_main_dataset(self):
        """Extract a 2D array of acquisitions of shape (n, spectrum).
        
        Bins all pixels in a vertical column and sums the intensity in each bin.
        Each spectrum is a 1D array that is the same width as the ROI during acquisition.
        """
        return np.sum(self.spe_dict['data'], axis=1, dtype=np.int32)

    def build_spectroscopic_dataset(self, calibration='poly'):
        """Map calibrated wavelength to the CCD pixels in ROI."""
        columns = int(self.XCALIB['pixel_position'][2])
        self.spectroscopic_indices = np.linspace(1, columns, columns, dtype=np.uint16)
        if calibration == 'poly':
            calibrate = np.poly1d(np.array(self.XCALIB['polynom_coeff'][2::-1]))
            self.spectroscopic_values = calibrate(self.spectroscopic_indices)
        elif calibration == 'linear':
            start_wl = self.XCALIB['calib_value'][0]
            end_wl = self.XCALIB['calib_value'][2]
            self.spectroscopic_values = np.linspace(start_wl, end_wl, columns)
        label = self.XCALIB['string']
        label = self.bytes_to_string(label).strip('x\00')
        label = label.replace('[', '(').replace(']', ')')
        self.spectroscopic_label = label
        self.spectroscopic_units = label.split('(')[1].split(')')[0]
        return None

    def extract_positions_from_file(self, filename):
        """Extract relevant data from an accompanying file to be fed into position dataset.
        
        Files may be an exported .dat file or a .WIP file.
        """
        search_pattern = {'PointsPerLine' : 'Points',
                          'LinesPerImage' : 'Lines',
                          'ScanWidth' : 'Width',
                          'ScanHeight' : 'Height',
                          'ScanUnit' : 'Unit',
                         }
        match = dict.fromkeys(search_pattern,)
        with open(filename, 'r', encoding='latin-1') as f:
            header = f.readlines()[1:70]
            for key, pattern in search_pattern.items():
                for line in header:
                    if re.search(pattern, line):
                        try:
                            # Normal match will result in string of numbers
                            value = line.split()[-1]
                            assert len(value) < 4
                        except AssertionError:
                            # Handles case where ScanUnit is buried in binary string
                            refined_pattern = r'StandardUnit(.{1,})UnitKind'
                            # Match everything between the words above
                            binary_match = re.search(refined_pattern, line).group(1)
                            value = binary_match[-6:-4] # pick out bits that correspond to unit
                        match[key] = value
                        break
        return match.values() # PointsPerLine, LinesPerImage, ScanWidth, ScanHeight, ScanUnit

    def read_positions_from_arguments(self, PointsPerLine, LinesPerImage, ScanWidth=None, ScanHeight=None, ScanUnit=None):
        """Read user specified dimensions and supply default values for nonspecified parameters"""
        ScanWidth = ScanWidth if ScanWidth else PointsPerLine
        ScanHeight = ScanHeight if ScanHeight else LinesPerImage
        ScanUnit = ScanUnit if ScanUnit else 'index'
        return PointsPerLine, LinesPerImage, ScanWidth, ScanHeight, ScanUnit

    def prompt_for_positions(self):
        """Ask user to supply image dimensions; supply default values for nonspecified parameters"""
        x = input('Points per Line:')
        y = input('Lines per Image:')
        return x, y, x, y, 'index'

    def gather_position_data(self, supplemental=None, PointsPerLine=None,
                             LinesPerImage=None, ScanWidth=None, ScanHeight=None, ScanUnit=None):
        """Search for position data from supplemental file or arguments. Prompt otherwise."""
        if supplemental is not None:
            params = self.extract_positions_from_file(supplemental)
        elif PointsPerLine is not None and LinesPerImage is not None:
            params = self.read_positions_from_arguments(PointsPerLine, LinesPerImage,
                                                        ScanWidth=ScanWidth, ScanHeight=ScanHeight,
                                                        ScanUnit=ScanUnit)
        else:
            params = self.prompt_for_positions()
        return params

    def build_position_dataset(self, PointsPerLine, LinesPerImage, ScanWidth, ScanHeight, ScanUnit):
        """Correlate the acquisition number with a physical position coordinate."""
        # The dimensions of image (x,y) acquired in a spectral image
        self.x_pixels = int(PointsPerLine)
        self.y_pixels = int(LinesPerImage)
        step_x = float(ScanWidth) / self.x_pixels 
        step_y = float(ScanHeight) / self.y_pixels 
        self.position_units = ScanUnit
        
        position_indices = []
        for y in range(self.y_pixels):
            for x in range(self.x_pixels):
                position_indices.append((x,y))
        
        self.position_indices = np.asarray(position_indices, dtype=np.uint16)
        self.position_values = self.position_indices * (step_x, step_y)
        return None

    def link_supplemental(self, file):
        """Incorporate a supplemental data file that contains position data."""
        params = self.extract_positions_from_file(file)
        self.supplemental = file
        self.build_position_dataset(*params)
        return None

    def strip_extension(self, filename):
        return os.path.splitext((filename))[0]

    def getsize(self):
        """Recursively iterate to sum size of object & members."""
        ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)
        _seen_ids = set()
        def inner(obj):
            obj_id = id(obj)
            if obj_id in _seen_ids:
                return 0
            _seen_ids.add(obj_id)
            size = sys.getsizeof(obj)
            if isinstance(obj, ZERO_DEPTH_BASES):
                pass # bypass remaining control flow and return
            elif isinstance(obj, (tuple, list, Set, deque)):
                size += sum(inner(i) for i in obj)
            elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
                size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
            # Check for custom object instances - may subclass above too
            if hasattr(obj, '__dict__'):
                size += inner(vars(obj))
            if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
                size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
            return size
        return inner(self)

    def add_colorbar(self, im, aspect=20, pad_fraction=0.5, **kwargs): # See https://nbviewer.jupyter.org/github/mgeier/python-audio/blob/master/plotting/matplotlib-colorbar.ipynb
        """Add a properly scaled colorbar to a plot image."""
        divider = axes_grid1.make_axes_locatable(im.axes)
        width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
        pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
        current_ax = plt.gca()
        cax = divider.append_axes("right", size=width, pad=pad)
        plt.sca(current_ax)
        return im.axes.figure.colorbar(im, cax=cax, **kwargs)

    def find_nearest(self, array, value):
        """Return the index in array that is closest to value."""
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx
    
    def index_from_coord(self, real_coord):
        """Return the index corresponding to a specified coordinate from the heatmap.
        
        Parameters
        ----------
        real_coord : (x, y) tuple
            The coordinates corresponding to the location in the scaled image. Top left is (0, 0).
        
        Returns
        -------
        index : int
            The matching index of the main_dataset corresponding to the real coordinate.
        """
        condition = np.logical_and(self.position_values[:, 0] == real_coord[0],
                                   self.position_values[:, 1] == real_coord[1])
        return np.argwhere(condition)[0][0]
        
    
    def spectrum(self, index):
        """Return a single spectrum from the main dataset."""
        spectra = self.extract_main_dataset()
        return spectra[index]
    
    def plot_spectrum(self, ax, index, **kwargs):
        spectrum = ax.plot(self.spectroscopic_values, self.spectrum(index), **kwargs)
        ax.set_xlabel(self.spectroscopic_label)
        ax.set_ylabel('Intensity')
        return spectrum

    def heatmap(self, ax, supplemental=None, PointsPerLine=None, LinesPerImage=None, ScanWidth=None,
                ScanHeight=None, ScanUnit=None, start_wl=None, end_wl=None, **kwargs):
        # Specify default behavior
        if not start_wl:
            start_wl = round(self.spectroscopic_values[0])
        if not end_wl:
            end_wl = round(self.spectroscopic_values[-1])
        if not hasattr(self, 'position_indices'):
            # Position dataset does not already exist. Search arguments or prompt for values
            print("Missing additional position data.\n")
            params = self.gather_position_data(supplemental=supplemental,
                                               PointsPerLine=PointsPerLine, LinesPerImage=LinesPerImage,
                                               ScanWidth=ScanWidth, ScanHeight=ScanHeight,
                                               ScanUnit=ScanUnit)
            self.build_position_dataset(*params)
        
        # Calculate supplemental plotting parameters
        x = self.position_values[:, 0]
        y = self.position_values[:, 1]
        extents = (x[0], x[-1], y[-1], y[0])  # left, right, bottom, top
        start = self.find_nearest(self.spectroscopic_values, start_wl)
        end = self.find_nearest(self.spectroscopic_values, end_wl)
        
        # Format data to plot
        data = self.extract_main_dataset()
        integrated_counts = np.sum(data[:, start:end], axis=1)
        integrated_counts_2D = integrated_counts.reshape(self.y_pixels, self.x_pixels)
        
        # Generate and format plot
        heatmap = ax.imshow(integrated_counts_2D, extent=extents, **kwargs)
        self.add_colorbar(heatmap)
        ax.set_xlabel(f'Position ({self.position_units})')
        ax.set_ylabel(f'Position ({self.position_units})')
        ax.set_title(f'{self.basename}\n({start_wl}\u2013{end_wl} nm)')
        return heatmap
# -

# files = sorted(glob('Ryan/Si-Pillars/*.SPE'))
files = sorted(glob('Ryan/WashU/*.SPE'))
for i, file in enumerate(files):
    print(i, file)

# Pick file from above (0-indexed)

file = files[5]
spe_object = SPE(file)
spe_object

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




