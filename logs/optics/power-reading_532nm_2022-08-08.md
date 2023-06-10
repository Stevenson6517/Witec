---
date: 2022-08-08
description: 'Laser power readings throughout the beampath'
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

The measurements from Aug 04 suggest there is a significant loss of power
throughout the optical system. The measurements below are an attempt to isolate
where the attenuation is coming from.

| Set Power (W) | Location           | Measured Power (mW) |
|---------------|--------------------|---------------------|
| 0.01          | Verdi exit shutter | 13.45 ± 0.12        |
| 0.01          | Fiber exit         | 5.3 ± 0.3           |
| 0.02          | Verdi exit shutter | 23.1  ± 0.1         |
# Notes

- The power at the Verdi exit behaves normally; when set at a nominal 10 mW,
  the actual power is measured around 10 mW.
- Potential sources of loss:
    - Attenuation through the fiber (rated for wrong wavelength)
    - Poor coupling from free-space into the fiber (misaligned objective lens)

## Conclusions

- Need to check alignment of the objective lens
