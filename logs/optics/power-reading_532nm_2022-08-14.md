---
date: 2022-08-14
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
comments: 'Realigned fiber into laser on 2022-08-14'
---

The measurements from Aug 08 suggested an improper alignment into the fiber.

I realigned the objective and adjusted the coupling to the fiber until I
reached the maximum laser throughput as measured by the power meter. I then
quantified the amount of power present at each optical checkpoint based on a
set power of 0.01 W as declared on the laser power supply.

| Location                        | Measured Power (mW) |
|---------------------------------|---------------------|
| After laser objective           | 10.5                |
| After fiber exit                | 6.1  ± 0.2          |
| After 50x microscope objective  | 1.5  ± 0.1          |
| After 100x microscope objective | 0.44 ± 0.03         |

# Notes

- It seems like there is still a significant loss of power from the fiber
  through the objectives
