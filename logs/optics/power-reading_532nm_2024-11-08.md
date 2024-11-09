---
date: 2024-11-08
description: 'Laser power measurements at increasing power'
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

We previously observed a non-linear correspondence between the set power from
the Verdi control panel and the measured laser power at the sample through each
of the 50x or 100x objectives. I want to investigate if this non-linear
response is from a poor alignment into the fiber and/or objectives, or if this
is a response from the laser itself.

I monitored the power directly from the single-mode fiber recently aligned to
the Verdi output from November 6, 2024. To allow me to increase the laser power
beyond the damage threshold of the fiber, I attenuated the laser with
a Thorlabs neutral density filter with OD 2 (ND020A).

I began my investigation informally by quickly checking the low-power readings
at set power values of 0.01 W, 0.1 W, 0.2 W, and 0.3 W. After it was clear that
the measured power at the output of the single-mode fiber was not linearly
correlated with the set power, I began a more systematic documentation of the
results.


Configuration
: Verdi -> ND020A -> 10x objective -> SM fiber

Procedure
: Set power, wait ~10 seconds, read avg power over 4000 measurements directly at fiber tip

| Set Power (W) | Measured Power (µW) | Diode current (A) |
|---------------|---------------------|-------------------|
| 0.4           | 189                 |                   |
| 0.5           | 312                 |                   |
| 0.6           | 470                 |                   |
| 0.7           | 640                 |                   |
| 0.8           | 775                 |                   |
| 0.9           | 850                 |                   |
| 1.0           | 865                 |                   |
| 1.1           | 690                 |                   |
| 1.2           | 565                 |                   |
| 1.3           | 430                 |                   |
| 1.4           | 280                 |                   |
| 1.3           | 1130                |                   |
| 1.2           | 1150                |                   |
| 1.1           | 975                 |                   |
| 1.0           | 860                 |                   |
| 0.9           | 680                 |                   |
| 0.8           | 520                 |                   |
| 0.7           | 374                 | 26.49 A           |
| 0.6           | 252                 |                   |
| 0.5           | 157                 | 26.39 A           |
| 0.4           | 92                  | 26.28 A           |
| 0.3           | 45                  | 26.03 A           |
| 0.2           | 20                  | 25.78 A           |
| 0.1           | 5.7                 | 25.22 A           |
| 0.01          | 0.6                 | 23.46 A           |

I realized part way through my measurements that the diode current changed as
a function of the requested set power, so I began documenting this parameter as
well. I further realized that the response between the set power and measured
power was different when I ramped up the laser power versus when I ramped down
the laser power, with a more apparent linear response from the diode when the
laser ramped down from high power.

I am not yet convinced whether the non-linear correspondence between the set
power and measured power is a result of improper fiber alignment or from an
irregularity in the laser diode, although I have suspicions it is from the
latter.
