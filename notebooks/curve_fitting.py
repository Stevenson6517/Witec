# # Apply Guassian, Lorentzian, and Voigt lineshapes to spectral maps

# +
import pathlib
from pprint import pprint
import sys

import h5py
from lmfit.models import (
    LorentzianModel,
    ConstantModel,
    VoigtModel,
    SplitLorentzianModel,
)
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
import numpy as np
from tqdm import tqdm


# See https://nbviewer.jupyter.org/github/mgeier/python-audio/blob/master/plotting/matplotlib-colorbar.ipynb
def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1.0 / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


# https://stackoverflow.com/a/57295298
def add_lorentz_peak(prefix, center, amplitude=1e3, sigma=0.1):
    """Automate lmfit model creation for a Lorentzian peak."""
    peak = SplitLorentzianModel(prefix=prefix)
    pars = peak.make_params()
    pars[prefix + "center"].set(center, min=530, max=570)
    pars[prefix + "amplitude"].set(amplitude, min=0, max=6e5)
    pars[prefix + "sigma"].set(sigma, min=0)
    pars[prefix + "sigma_r"].set(sigma, min=0)
    # pars[prefix + "gamma"].set(sigma, vary=True, min=0)
    return peak, pars


# This project saves data in a network drive, available only from a Vanderbilt
# IP address. If you connect your personal computer to this network drive, you
# can access its files
if "darwin" in sys.platform:
    NETWORK_PATH = "/Volumes/HaglundNAS/"
elif "win32" in sys.platform:
    NETWORK_PATH = (
        "Z://"  # Adjust as necessary, depending on how you mounted network drive
    )
NETWORK_DIR = pathlib.Path(NETWORK_PATH)

# By default, search the data directory from the network path above. In the
# event the network drive is unavailable, assume local data is saved with this
# project in a folder named `data`, available from the project root (or one
# directory behind this notebook).
if NETWORK_DIR.exists():
    print("Connected to Network Directory. Searching the following location:")
    DATA_DIR = pathlib.Path(NETWORK_DIR, "curieda/data")
else:
    print("Network Directory unavailable. Searching the following location:")
    DATA_DIR = pathlib.Path("../data")
print(DATA_DIR)

# +
# Find a specific file by search patterns
search_pattern = "hBN-10-CH4/*TL_X07*.hdf5"

# List matching files
spe_files = sorted(DATA_DIR.glob(search_pattern))
for i, file in enumerate(spe_files):
    print(i, file.name)
# -

# Select a file according to desired index above
h5_path = list(spe_files)[1]
print(h5_path.name)

# ## Generate best fits
#
# > If you've already run a best fit analysis and stored the results in an
# .hdf5 file, you can skip this section and load the results into memory by
# skipping to the "Read dataset from file" section.

# Extract data into python variables
with h5py.File(h5_path, mode="r") as h5_file:
    # Extract datasets from container (visible in memory as long as file is open)
    temporary_main_dataset = h5_file["Measurement_000"]["Raw_Data"]
    temporary_position_dataset = h5_file["Measurement_000"]["Position_Values"]
    temporary_spectroscopic_dataset = h5_file["Measurement_000"]["Spectroscopic_Values"]

    # Copy datasets outside of container so they are visibile when file is closed
    main_dataset = temporary_main_dataset[()].copy()
    position_dataset = temporary_position_dataset[()].copy()
    spectroscopic_dataset = temporary_spectroscopic_dataset[()].copy()

# +
index = len(main_dataset) // 2
spectrum = main_dataset[index][100:-40]
# spectrum_corrected = main_dataset[index] - np.min(main_dataset[index])
wavelengths = spectroscopic_dataset[0][100:-40]

# Make a model to fit the spectra

model = ConstantModel(prefix="bkg_")
params = model.make_params(c=500)
params["bkg_c"].set(550, vary=False)

L_shoulder = SplitLorentzianModel(prefix="sL0_")
params.update(
    L_shoulder.make_params(
        center={"value": 536, "min": 535.5, "max": 536.5},
        sigma={"value": 0.1, "min": 0, "max": 1},
        sigma_r={"value": 2.5, "vary": False},
        amplitude={"value": 6.3e3, "min": 0},
    )
)
residue = SplitLorentzianModel(prefix="sL1_")
params.update(
    residue.make_params(
        center={"value": 544.6, "min": 544, "max": 545},
        sigma={"value": 5.2, "min": 5.0},
        sigma_r={"value": 1.64, "min": 1.5, "max": 2.5},
        amplitude={"value": 102e3, "min": 0},
    )
)
zpl = LorentzianModel(prefix="L2_")
params.update(
    zpl.make_params(
        center={"value": 546.35, "min": 546.0, "max": 546.6},
        sigma={"value": 0.8, "min": 0},
        amplitude={"value": 14e3, "min": 0},
    )
)
psb1 = VoigtModel(prefix="v3_")
params.update(
    psb1.make_params(
        center={"value": 549.6},
        sigma={"value": 0.31, "min": 0},
        # gamma={"value": 0.01, "vary": False, "min": 0},
        amplitude={"value": 2.5e3, "min": 0},
    )
)
psb2 = SplitLorentzianModel(prefix="sL4_")
params.update(
    psb2.make_params(
        center={"value": 555.8, "min": 555.5, "max": 556},
        sigma={"value": 1.1, "min": 1, "max": 1.5},
        sigma_r={"value": 1.2, "min": 1, "max": 1.5},
        amplitude={"value": 6.8e3, "min": 0},
    )
)
psb3 = VoigtModel(prefix="v5_")
params.update(
    psb3.make_params(
        center={"value": 560, "min": 559, "max": 561},
        sigma={"value": 0.2, "min": 0},
        # gamma={"value": 0.01, "vary": False, "min": 0},
        amplitude={"value": 1.0e2, "min": 0},
    )
)
psb4 = VoigtModel(prefix="v6_")
params.update(
    psb4.make_params(
        center={"value": 563.5, "min": 563.1, "max": 564},
        sigma={"value": 0.64, "min": 0.3, "max": 0.9},
        # gamma={"value": 1.6, "vary": False, "min": 0, max=2},
        amplitude={"value": 1.8e3, "min": 0},
    )
)

model += L_shoulder + residue + zpl + psb1 + psb2 + psb3 + psb4

init = model.eval(params, x=wavelengths)
result = model.fit(spectrum, params, x=wavelengths)
comps = result.eval_components()
print(result.fit_report(min_correl=0.5))

with plt.style.context("default"):
    fig, ax = plt.subplots()
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Intensity")
    ax.scatter(wavelengths, spectrum, s=1, color="gray", label="spectrum")
    ax.plot(wavelengths, result.best_fit, label="best fit", alpha=0.85)
    ax.plot(wavelengths, init, "-", label="initial fit", alpha=0.85)
    for name, comp in comps.items():
        ax.plot(wavelengths, comp, "--", linewidth=0.75, label=name, alpha=0.5)
    plt.legend()
    plt.show()
# -
# If the above fit looks good, run it on the entire dataset below.

# +
values = {}
stats = []
for spectrum in tqdm(main_dataset):
    spectrum = spectrum[100:-40]
    result = model.fit(spectrum, params, x=wavelengths)
    try:
        result_dict = result.uvars
    except AttributeError:
        result_dict = result.best_values
    for key, value in result_dict.items():
        if values.get(key):
            existing_value = values[key]
        else:
            existing_value = list()
        try:
            existing_value.append((value.n, value.s))
        except AttributeError:
            existing_value.append((value, 0))
        values[key] = existing_value
    stats.append(result.dumps())

# Format all data elements as array instead of list
for key, value in values.items():
    values[key] = np.asarray(value)
stats = np.asarray(stats)
# -

# Inspect values to see if they have been populated correctly
pprint(values)

# ## Write dataset to file
#
# If the above values dictionary is populated the way you want, run the next
# cell to save the results to the file.
#
# WARNING: Including the `stats` dataset will increase the .hdf5 file by
# approximately a factor of `n`, where `n` is the number of individual models
# in the composite model for your best fit.

with h5py.File(h5_path, mode="r+") as h5_file:
    dt = h5py.special_dtype(vlen=str)
    data_stats = np.asarray(stats, dtype=dt)
    h5_file.create_dataset(
        "Measurement_000/Analysis/Custom_fits/best_fit/stats", data=data_stats
    )
    for key, best_fit in values.items():
        h5_file.create_dataset(
            f"Measurement_000/Analysis/Custom_fits/best_fit/{key}",
            data=best_fit.astype(float),
        )

# ## Read dataset from file

# Quick sanity check to see that contents in h5 are retrievable
with h5py.File(h5_path, mode="r") as h5_file:
    best_fits = h5_file["Measurement_000/Analysis/Custom_fits/best_fit"]
    memory_results = {}
    for label, value in best_fits.items():
        if "bkg" in label or "stats" in label:
            continue
        memory_results[label] = value[()]
    my_results = memory_results.copy()

# Examine sample output
my_number, my_uncertainty = my_results["L2_amplitude"].T
pprint("Total number of keys:", len(my_results.keys()))
print("Size of complete key:", my_number.shape)  # Should be (num_pixels,)
keys_to_delete = []
# Remove any keys with missing data because they prevent the next resizing
# efforts to fail. Missing data occurs when a fit fails to optimize at
# a particular pixel.
for key, value in my_results.items():
    if len(value) != len(my_number):
        keys_to_delete.append(key)
print("Dropping the following incomplete keys:", keys_to_delete)
for key in keys_to_delete:
    del my_results[key]

# ## View components as maps

# +
# Extract physical coordinates for resizing
rows = np.unique(position_dataset[:, 0])  # x coordinates
cols = np.unique(position_dataset[:, 1])  # y coordinates
position_values = np.reshape(position_dataset, (len(rows), len(cols), -1))

# Sum intensity across all wavelengths in each spectrum
intensity_values = np.sum(main_dataset, axis=1)
# Reshape to (x, y, I) where I is Intensity
intensity_map = np.reshape(intensity_values, (len(rows), len(cols), -1))

# Plot the intensity value at each pixel
with plt.style.context("default"):
    fig, ax = plt.subplots()
    ax.set_title(f"{h5_path.stem}\n")
    img = ax.imshow(intensity_map, cmap="gist_stern")
    add_colorbar(img, label="Intensity")
    ax.set_aspect("equal")
    output = h5_path.with_suffix(".png")
    # fig.savefig(output, dpi=300, bbox_inches="tight")
    # print(f"Figure saved to {output}")
    plt.show()

# Do the above for each component in the best fits
COMPONENTS_SIZE = len(my_results)
with plt.style.context("default"):
    NCOLS = 3
    NROWS = COMPONENTS_SIZE // ncols + (COMPONENTS_SIZE % NCOLS > 0)
    fig = plt.figure(figsize=(NCOLS * 3, NROWS * 3))
    fig.suptitle(f"{h5_path.stem}")
    for i, component in enumerate(my_results):
        ax = plt.subplot(NROWS, NCOLS, i + 1)
        my_value, my_unc = my_results[component].T
        my_value = np.reshape(my_value, (len(rows), len(cols), -1))
        my_unc = np.reshape(my_unc, (len(rows), len(cols), -1))
        ax.set_title(f"{component}")
        ax.set_axis_off()
        add_colorbar(ax.imshow(my_value, cmap="gist_stern"))
    plt.tight_layout()
    plt.show()
