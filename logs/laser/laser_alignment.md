---
date: Thu Jan 25 14:10:21 CST 2024
author: David Curie
---

# Laser alignment investigation

```python
# Necessary packages for this notebook
import pathlib

import matplotlib.pyplot as plt
import numpy as np
from witec.spe import SPE
import scienceplots

import pyAvantes  # Custom GitHub library

def view_spectrum(ax, data1, data2, param_dict):
    """A wrapper to apply common formatting options to all plots"""
    ax.set_title("Laser line spectrum")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Intensity")
    ax.plot(data1, data2, **param_dict)
    ax.legend()
    return ax
    
# Location of reference data directory, relative to this document
data_directory = pathlib.Path("../../data")
target_directory = pathlib.Path(__name__).parent / "media"
```

## Problem

Spectra obtained in the WITec confocal microscope contain an unexpected
fluorescence near the laser line of the Verdi V-5 laser (532 nm). These
spectral features are affecting any meaningful ability to perform
photoluminescence studies on various substrates. The fluorescence appears on
a variety of substrates.

See the following example spectrum below, which was obtained by focusing the
laser from the fiber assembly onto a suspended glass cover slip and measuring
the reflected laser light through a 532 nm long pass filter.

```python
source = data_directory / "substrate-tests" / "substrate-tests_cover-slip.spe"
target = target_directory / source.name
winspec = SPE(source)

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, winspec.axis, winspec.data[0], {"label":"Glass cover slip"})
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Laser line reflected off glass cover slip](media/substrate-tests_cover-slip.svg)

The image shows that there is unexpected fluorescence at wavelengths beyond
532 nm. It is believed that the spectral features are solely from the laser
reflection and not fluorescence from the glass slide because this spectrum is
nearly identical in feature set to those from a bare silicon substrate.
Moreover, the glass cover slide is suspended several centimeters above the
nearest interacting surface to ensure that the collected light is primarily
from the reflection at the glass surface and not from an interaction below the
glass.


## Investigation

It is unknown if these spectral features are part of a messy laser line or if
the fluorescence is coming from anywhere along the optic path from the laser to
the spectrometer.

The primary investigation looks first at the laser light directly from the Verdi V-5.

### Details

The Verdi V-5 laser is set to its lowest power (0.01 W) and passed through
various ND filters before going into a fiber directly to an Avantes
spectrometer.

The Avantes spectrometer contains an SMA fiber input port and an accompanying
multi-mode fiber. The fiber is mounted to a fiber coupler lens and placed by
hand directly in the beam path of the Verdi V-5 laser. Thorlas 1-inch diameter
ND filters (ND10A, ND20A, ND30A, ND40A, ND50A) attenuate the signal by 1, 2, 3,
4, or 5 orders of magnitude and can be arranged in sequence via threaded
retaining rings. For clarity, one order of magnitude reduction corresponds to
a 10% transmission.

### Investigate laser signal directly

The measurement below shows a representative spectral line profile of the Verdi
V-5 laser as it is loosely coupled to the Avantes fiber port after two ND
filters.

```python
source = data_directory / "laser" / "Verdi-V5_spec_0010mW_f-ND50A_f-ND40A_1000ms_2024-01-24-14-56-00.RAW8"
target = target_directory / source.name
avantes = pyAvantes.Raw8(source)

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, avantes.wavelength, avantes.scope, {"label":f"{avantes.comment}"})
    ax.set_xlim(520, 570)
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Verdi laser line with unsaturated emission](media/Verdi-V5_spec_0010mW_f-ND50A_f-ND40A_1000ms_2024-01-24-14-56-00.svg)

The image shows an expected response from a single mode laser; that is,
a single wavelength with a fairly narrow spectral linewidth.

### Investigate laser signal with better alignment

The measurement above was repeated, but this time the Avantes fiber was moved
gently through the beam spot until more spectral features showed up on the
spectrometer.

```python
source = data_directory / "laser" / "Verdi-V5_spec_0010mW_f-ND50A_f-ND40A_1000ms_2024-01-24-15-05-00.RAW8"
target = target_directory / source.name
avantes = pyAvantes.Raw8(source)

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, avantes.wavelength, avantes.scope, {"label":f"{avantes.comment}"})
    ax.set_xlim(520, 570)
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Verdi laser line with saturated emission](media/Verdi-V5_spec_0010mW_f-ND50A_f-ND40A_1000ms_2024-01-24-15-05-00.svg)

The image show the same response but with a saturated intensity at the expected wavelength of 532 nm.

During collection of the above measurement, I noticed occasional spikes in the
spectrum, accompanied by a much wider spectral line width of the laser.
I couldn't reliably find these positions to record them at this scale, but my
assumption is that they occur when the laser light is maximally coupled into
the Avantes fiber. Furthermore, I worry that the ND filter arrangements that
I am using to protect the Avantes spectrometer from direct laser light exposure
are preventing me from seeing the weak fluorescence signal that pervades my
sensitive photoluminescence measurements.

### Investigate laser signal at higher intensity

I repeated the above measurement, but reduced the total amount of filtering
before collecting the light into the Avantes fiber so that I could see more of
the side band activity accompanying the laser line. Even though I knew the
laser line would appear saturated on the spectrometer, I took care to not
investigate for too long of a time with these reduced protections.

```python
source = data_directory / "laser" / "Verdi-V5_spec_0010mW_f-ND20A_f-ND50A_1000ms_2024-01-24-15-09-00.RAW8" 
target = target_directory / source.name
avantes = pyAvantes.Raw8(source)

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, avantes.wavelength, avantes.scope, {"label":f"{avantes.comment}"})
    ax.set_xlim(520, 570)
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Verdi laser line with reduced filtering](media/Verdi-V5_spec_0010mW_f-ND20A_f-ND50A_1000ms_2024-01-24-15-09-00.svg)

The image above shows a clear evolution of spectral features beyond the
expected single-frequency 532 nm laser line. In particular, there is a clearly
visible second emission line at an undetermined wavelength above 532 nm
(nominally 534 nm). It is evident that these features appear when the signal is
maximally coupled into the Avantes fiber. My working assumption is that maximum
coupling occurs when the fiber core is coaxial with the TEM~00~ mode from the
laser.

### Investigate laser signal with better coupling

To investigate this further, I switched focus to the single-mode fiber I knew
to be well-aligned with the Verdi output that normally runs to the input of the
WITec system. This fiber has a notched FC/PC connector at its end that doesn't
directly mate with the input port where the Avantes multi-mode fiber is
supposed to connect to the spectrometer, but I could carefully hold the
single-mode fiber close to the Avantes input port and still read an appreciable
signal.

To compensate for the loss of coupling efficiency in the mismatch of fibers,
I reduced the ND filter arrangement on the light incident on the single-mode
fiber. I recorded the output spectrum of the Verdi laser again, but the key
difference between this measurement and the previous direct laser measurements
is that the laser goes through a 10x confocal microscope objective and into
a single-mode fiber instead of using the supplied Avantes multi-mode fiber.

```python
source = data_directory / "laser" / "Verdi-V5_spec_0010mW_f-ND40A_1000ms_2024-01-24-15-16-00.RAW8" 
target = target_directory / source.name
avantes = pyAvantes.Raw8(source)

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, avantes.wavelength, avantes.scope, {"label":f"{avantes.comment}"})
    ax.set_xlim(520, 570)
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Verdi laser line after lens and single-mode fiber](media/Verdi-V5_spec_0010mW_f-ND40A_1000ms_2024-01-24-15-16-00.svg)

The image above shows clear signs of secondary signals other than the expected
532 nm emission line. It is still unclear if these interactions are introduced
from the coupling lens, are artifacts of a dirty fiber face, are leftover modes
from the Nd:YVO~4~ illumination in the Verdi laser, are improperly filtered
emission lines from the Verdi etalon, or are something else.

Two key results are shown together for visual comparison to highlight the
similarity of this observed secondary signal with the fluorescence observed in
the WITec assembly.

```python
avantes_source = data_directory / "laser" / "Verdi-V5_spec_0010mW_f-ND40A_1000ms_2024-01-24-15-16-00.RAW8" 
avantes = pyAvantes.Raw8(avantes_source)

winspec_source = data_directory / "substrate-tests" / "substrate-tests_cover-slip.spe"
winspec = SPE(winspec_source)
target = target_directory / "fiber_microscope_comparison"

def normalize(array):
    return (array - np.min(array)) / (np.max(array) - np.min(array))

with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    view_spectrum(ax, avantes.wavelength, normalize(avantes.scope), {"label":f"{avantes.comment}"})
    view_spectrum(ax, winspec.axis, normalize(winspec.data[0]), {"label":"Glass cover slip"})
    ax.set_xlim(520, 570)
    ax.set_title("Normalized comparison of laser line")
    figname = target.with_suffix(".svg")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
    plt.show()
```

![Comparison of Verdi emission through fiber or microscope](media/fiber_microscope_comparison.svg)

It is clear there's a correlation of the laser signal as measured directly
before the WITec microscope and immediately after the WITec microscope, which
further rules out fluorescence effects from any substrates investigated in the
microscope.

It is still unclear if this is an optics problem (i.e. an issue with the
single-mode fiber or accompanying coupling lens), or if this is an inherent
flaw in the Verdi output. I don't have a fiber scope handy to look for debris
or burn marks at the face of the input fiber, so I turn my attention to
investigating the Verdi output.

