---
date: 2024-01-26
author: David Curie
description: 'LBO optimization'
laser:
    - model: 'Verdi-5W'
    - serial: 'V5-G5403'
    - manufacture date: 'Dec-2004'
wavelength: 532
---

I am uncertain of the reliability of the Verdi output. Specifically, we notice
a non-linear response of the laser output power for a linear adjustment of the
set laser power as requested by the front panel.

From the Verdi manual:

> The conversion efficiency of the LBO frequency doubler is heavily
> dependent upon temperature. A temperature change of 1ºC can reduce the
> doubling efficiency by more than 50%. To compensate for the reduced
> efficiency, the laser will use more current to produce the desired
> 532 nm output. This will reduce the lifetime of the diodes.
> 
> As a solution to this potential problem, the Verdi V-2/V-5/V-6 software
> contains a menu routine which will perform a LBO temperature
> optimization automatically to maximize the conversion efficiency of the
> doubler. The LBO Optimization routine should be run when the diode
> current is observed to be 10% greater than baseline values.

I do not have a record of baseline values, but I suspect improper optimization
of the doubling crystal inside the Verdi.

I followed the procedures outlined by the _Verdi V-2/V-5/V-6 Laser Operator's
Manual_ under the section "LBO Temperature Optimization" (6-41).

## Pre-optimization settings

Jan 26 10:53:00 CST 2024
: Diode current set to 5.00 W with the shutter closed

| Diode \#1 Parameter | Value   |
|---------------------|---------|
| Voltage             | 1.83 V  |
| Current             | 23.58 A |


|          | Set    | Read   | Drive | Status |
|----------|--------|--------|-------|--------|
| LBO      | 148.70 | 148.68 | 6100  | lock   |
| Vanadate | 30.00  | 30.00  | -900  | lock   |
| Etalon   | 48.67  | 48.74  | 2290  | lock   |
| Diode #1 | 32.09  | 32.10  | 164   | lock   |

Drive values above are approximate.

Jan 26 10:59:00 CST 2024
: LBO Optimization began
: Process finished after 13:00:00 and before 13:45:00


## Post-optimization settings

| Diode \#1 Parameter | Value   |
|---------------------|---------|
| Voltage             | 1.83 V  |
| Current             | 23.45 A |
| Photocell           | 2.27 V  |


|          | Set    | Read   | Drive | Status |
|----------|--------|--------|-------|--------|
| LBO      | 148.80 | 148.80 | 5800  | lock   |
| Vanadate | 30.00  | 30.00  | -1350 | lock   |
| Etalon   | 48.67  | 48.74  | 796.8 | lock   |
| Diode #1 | 32.09  | 32.10  | 40    | lock   |
