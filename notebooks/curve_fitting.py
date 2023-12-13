# # Apply Guassian, Lorentzian, and Voigt lineshapes to spectral maps

# +
import pathlib
from pprint import pprint
import sys

import h5py
import matplotlib.pyplot as plt
from mpl_toolkits import axes_grid1
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import find_peaks, savgol_filter
from scipy.special import wofz
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


# http://emilygraceripka.com/blog/16
# https://stackoverflow.com/questions/61657107/fitting-multiple-lorentzians-to-brillouin-spectrum-using-scipy-in-python-3
def lorentzian(x, I, x0, gamma):
    """Return a single Lorentz curve
    L(x) = I[ γ^2 / (x - x0)^2 + γ^2]
    """
    return I * gamma**2 / ((x - x0) ** 2 + gamma**2)


def multi_lorentz(x, *params):
    """Return a sum of multiple Lorentz curves.
    The number of Lorentz curves is determined by the number of parameters,
    which are expected to be passed in multiples of 3.
    """
    assert not (len(params) % 3)
    return sum([lorentzian(x, *params[i : i + 3]) for i in range(0, len(params), 3)])


def gaussian(x, A, x0, sigma):
    """Return a single Gaussian curve
    G(x) = A[ 1/(σ * sqrt(2π)) * (exp(-(x-x0)^2) / 2σ^2 )
    """
    return (
        A
        * (1 / sigma * (np.sqrt(2 * np.pi)))
        * (np.exp(-((x - x0) ** 2 / (2 * (sigma**2)))))
    )


def multi_gauss(x, *params):
    """Return a sum of multiple Gaussian curves.
    The number of Gaussian curves is determined by the number of parameters,
    which are expected to be passed in multiples of 3.
    """
    assert not (len(params) % 3)
    return sum([guassian(x, *params[i : i + 3]) for i in range(0, len(params), 3)])


# https://www.digitaldesignjournal.com/python-voigt-profile/
def voigt_profile(x, amplitude, center, sigma, gamma):
    z = ((x - center) + 1j * gamma) / (sigma * np.sqrt(2))
    v = amplitude * wofz(z).real / (sigma * np.sqrt(2 * np.pi))
    return v


def multi_voigt(x, *params):
    """Return a sum of multiple Voigt profiles.
    The number of Voigt profiles is determined by the number of parameters,
    which are expected to be passed in multiples of 4.
    """
    assert not (len(params) % 4)
    return sum([voigt_profile(x, *params[i : i + 4]) for i in range(0, len(params), 4)])


# # https://stackoverflow.com/a/71227338
# # Modified for Lorentzian
# def lorentzian(x, *args):
#     """Composition function of arbitrary number of Lorentzian lineshapes.
#        The number of Lorentzian profiles is determined by the number of arguments.
#        Arguments are expected to appear in multiples of 3 (amp, cen, wid).
#     """
#     x = x.reshape(-1, 1)
#     amp = np.array(args[0::3]).reshape(1, -1)
#     cen = np.array(args[1::3]).reshape(1, -1)
#     wid = np.array(args[2::3]).reshape(1, -1)
#     return np.sum(amp * wid**2 / ((x-cen)**2 + wid**2), axis=1)

# def gaussian(x, *args):
#     """Composition function of arbitrary number of Gaussian lineshapes.
#        The number of Guassian profiles is determined by the number of arguments.
#        Arguments are expected to appear in multiples of 3 (amp, cen, sig).
#     """
#     x = x.reshape(-1, 1)
#     amp = np.array(args[0::3]).reshape(1, -1)
#     cen = np.array(args[1::3]).reshape(1, -1)
#     sig = np.array(args[2::3]).reshape(1, -1)
#     return np.sum(amp * (1/sig*(np.sqrt(2*np.pi)))*(np.exp(-((x-cen)**2 / (2 * (sig**2) )))), axis=1)

# def voigt(x, *args):
#     """Composition function of arbitrary number of Voigt lineshapes.
#        The number of Voigt profiles is determined by the number of arguments.
#        Arguments are expected to appear in multiples of 6 (L_amp, L_cen, L_wid, G_amp, G_cen, G_sig).
#     """
#     x = x.reshape(-1, 1)
#     components = list(zip(*[iter(args)]*3)) # bundles of [amp, cen, wid]
#     L_args = [arg for bundle in components[0::2] for arg in bundle]  # Pick out and unpack even bundles
#     G_args = [arg for bundle in components[1::2] for arg in bundle]  # Pick out and unpack odd bunldes
#     return (lorentzian(x, *L_args) + gaussian(x, *G_args))


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
index = 2950
spectrum = main_dataset[index]
spectrum_corrected = main_dataset[index] - np.min(main_dataset[index])
# background = main_dataset[0]
# corrected = spectrum - 0.9*background
wavelengths = spectroscopic_dataset[0]
ev = 1240 / wavelengths

# lorentz
# guesses = [
#     # amp, cen, wid
#     *[8e3, 532, 0.5],
#     *[4e3, 536, 0.4],
#     *[10e3, 545, 2],
#     *[10e3, 546, 0.4],
#     *[15e3, 550, 1],
#     *[2e3, 556, 1],
#     *[2e2, 560, 1],
#     *[8e2, 563, 1],
# ]

# lower_bounds = [
#     # amp, cen, wid
#     *[0, 531.5, 0.01],
#     *[0, 535, 0.01],
#     *[0, 544, 0.01],
#     *[0, 545, 0.01],
#     *[0, 549, 0.1],
#     *[0, 554, 0.01],
#     *[0, 559, 0.01],
#     *[0, 562, 0.01],
# ]

# upper_bounds = [
#     # amp, cen, wid
#     *[np.inf, 532.5, 1],
#     *[np.inf, 537, 1],
#     *[np.inf, 546, 5],
#     *[np.inf, 547, 1],
#     *[np.inf, 551, 2],
#     *[np.inf, 557, 5],
#     *[np.inf, 561, 5],
#     *[np.inf, 564, 5],
# ]

# voigt
guesses = [
    # amp, cen, wid
    *[8e3, 532, 0.5, 0.5],
    *[4e3, 536, 0.4, 0.5],
    *[10e3, 545, 2, 0.5],
    *[10e3, 546, 0.4, 0.5],
    *[15e3, 550, 1, 0.5],
    *[2e3, 556, 1, 0.5],
    *[2e2, 560, 1, 0.5],
    *[8e2, 563, 1, 0.5],
]

lower_bounds = [
    # amp, cen, wid
    *[0, 531.5, 0.01, 0.1],
    *[0, 535, 0.01, 0.1],
    *[0, 544, 0.01, 0.1],
    *[0, 545, 0.01, 0.1],
    *[0, 549, 0.1, 0.1],
    *[0, 554, 0.01, 0.1],
    *[0, 559, 0.01, 0.1],
    *[0, 562, 0.01, 0.1],
]
upper_bounds = [
    # amp, cen, wid
    *[np.inf, 532.5, 1, 1],
    *[np.inf, 537, 1, 1],
    *[np.inf, 546, 5, 1],
    *[np.inf, 547, 1, 1],
    *[np.inf, 551, 2, 1],
    *[np.inf, 557, 5, 1],
    *[np.inf, 561, 5, 1],
    *[np.inf, 564, 5, 1],
]

bounds = (lower_bounds, upper_bounds)

# Fit a single spectrum to a curve
popt, pcov = curve_fit(multi_voigt, wavelengths, spectrum_corrected, p0=guesses)
# popt, pcov = curve_fit(multi_voigt, wavelengths, spectrum_corrected, p0=guesses, bounds=bounds)
err = np.sqrt(np.diag(pcov))
# y_fit = lorentzian(wavelengths, *popt)
y_fit = multi_voigt(wavelengths, *popt)
print(*popt)
components = list(zip(*[iter(popt)] * 4))  # list of [amp, cen, wid] fit parameters
components_err = list(zip(*[iter(err)] * 4))  # list of [amp, cen, wid] fit parameters
pprint(pd.DataFrame(components))

with plt.style.context("default"):
    fig, ax = plt.subplots()
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Intensity")
    ax.plot(wavelengths, spectrum_corrected, label="corrected")
    ax.plot(wavelengths, y_fit, label="fit", alpha=0.85)
    for component in components:
        ax.plot(
            wavelengths,
            multi_voigt(wavelengths, *component),
            linewidth=0.75,
            label=round(component[1]),
            alpha=0.5,
        )
    plt.legend()
    plt.show()
# -
# If the above fit looks good, run it on the entire dataset below.

model = {
    "Equation": lorentzian,
    "Initial Guess": guesses,
    "Bounds": bounds,
    "Notes": "Spectra were first corrected according to 'spectra = spectra - np.min(spectra)'",
}
print(help(lorentzian))

# +
fits = []
errors = []
for spectrum in tqdm(main_dataset):
    spectrum = spectrum - np.min(spectrum)
    popt, pcov = curve_fit(lorentzian, wavelengths, spectrum, p0=guesses, bounds=bounds)
    err = np.sqrt(np.diag(pcov))
    y_fit = lorentzian(wavelengths, *popt)
    components = list(zip(*[iter(popt)] * 3))  # list of [amp, cen, wid] fit parameters
    components_err = list(
        zip(*[iter(err)] * 3)
    )  # list of [amp, cen, wid] fit parameters
    fits.append(components)
    errors.append(components_err)

# convert lists to arrays for better storage and access
fits = np.asarray(fits)
errors = np.asarray(errors)
# -

print("fits:", fits.shape)
print("errors:", errors.shape)

with h5py.File(h5_path, mode="r+") as h5_file:
    # Write datasets to h5 file for future access
    h5_file.create_dataset(
        "Measurement_000/Analysis/Lorentz_fits/model", data=str(model)
    )
    h5_file.create_dataset(
        "Measurement_000/Analysis/Lorentz_fits/optimized_params", data=fits
    )
    h5_file.create_dataset(
        "Measurement_000/Analysis/Lorentz_fits/optimized_errors", data=errors
    )

with h5py.File(h5_path, mode="r") as h5_file:
    data = h5_file["Measurement_000/Analysis/Lorentz_fits/model"]
    print(data[()])

# +
rows = np.unique(position_dataset[:, 0])  # x coordinates
cols = np.unique(position_dataset[:, 1])  # y coordinates
position_values = np.reshape(position_dataset, (len(rows), len(cols), -1))
fits = np.asarray(fits)

intensity_values = np.sum(
    main_dataset, axis=1
)  # Sum intensity across all pixels in each spectrum
intensity_map = np.reshape(
    intensity_values, (len(rows), len(cols), -1)
)  # shape (x, y, I) where I is Intensity

for peak in range(0, 8):
    amp, cen, wid = fits[:, peak, :].T
    amp_map = np.reshape(amp, (len(rows), len(cols), -1))
    cen_map = np.reshape(cen, (len(rows), len(cols), -1))
    wid_map = np.reshape(wid, (len(rows), len(cols), -1))
    with plt.style.context("default"):
        fig, axs = plt.subplots(1, 3, figsize=(12, 3.5))
        fig.suptitle(f"{round(cen[0])} nm peak")
        axs[0].set_title("Amplitude")
        axs[0].set_axis_off()
        amp_img = axs[0].imshow(amp_map, cmap="gist_stern")
        add_colorbar(amp_img)
        axs[1].set_title("Center wavelength")
        axs[1].set_axis_off()
        cen_img = axs[1].imshow(cen_map, cmap="gist_stern")
        add_colorbar(cen_img)
        axs[2].set_title("Width")
        axs[2].set_axis_off()
        wid_img = axs[2].imshow(wid_map, cmap="gist_stern")
        add_colorbar(wid_img)
        plt.tight_layout()
        plt.show()

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

# -
