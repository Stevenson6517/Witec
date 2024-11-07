---
date: 2024-11-06
description: 'Laser power measurements throughout the beam path'
measured by:
- David Curie
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

I am not happy with the touch-up alignment from November 5, 2024. My cause for
alarm is the significantly reduced output at the sample under the 100x
objective. I spent more time today touching up alignment into the single-mode
fiber.

Configuration
: Verdi -> 10x objective -> SM fiber -> LL filter -> 50:50 BS -> Obj -> Sample -> Obj -> 50:50 BS -> MM assembly out

Diode current
: 23.52 A

| Set power (W) | Location                             | Measured Power (mW) |
|---------------|--------------------------------------|---------------------|
| 0.01          | Single-mode fiber out                | 9.1   ± 0.4         |

