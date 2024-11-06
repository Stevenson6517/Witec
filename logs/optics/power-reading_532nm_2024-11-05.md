---
date: 2024-11-05
description: 'Laser power measurements throughout the beam path'
measured by:
- David Curie
- Richarda Niemann
laser:
    - model: 'Verdi-5W'
    - serial: 'V5-G5403'
    - manufacture date: 'Dec-2004'
    - wavelength: 532
measurement:
    - device: 'Thorlabs PM101'
    - model: 'M00702598'
    - serial: '210608107'
    - calibration date: '2021-05-19'
    - mode: 'Mean over 4000 samples'
---

We modified the multi-mode fiber that comes out of the WITec microscope and
into the spectrometer to now enter a motorized assembly to couple the output
light either into a spectrometer or a Hanbury Brown–Twiss interferometer by way
of two multi-mode fibers.

During routine alignment into the multi-mode fiber assembly, we regularly
attenuate the laser power. We bumped the single-mode fiber that accepts the
Verdi free-space laser, so we thought it best to re-align the single-mode fiber
to the Verdi output.


Configuration
: Verdi -> 10x objective -> SM fiber -> LL filter -> 50:50 BS -> Obj -> Sample -> Obj -> 50:50 BS -> MM assembly out

Diode current
: 23.42 A

| Set power (W) | Location                             | Measured Power (mW) |
|---------------|--------------------------------------|---------------------|
| 0.01          | Verdi shutter                        | 14.42 ± 0.2        |
| 0.01          | Single-mode fiber out                | 8.1   ± 0.2         |
| 0.01          | Sample (50x objective)               | 1.10  ± 0.03        |
| 0.01          | Sample (100x objective)              | 0.34  ± 0.01        |
