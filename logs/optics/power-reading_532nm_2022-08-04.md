---
date: 2022-08-04
description: 'Laser power measurements in 6517 at the sample'
measured by:
- David Curie
- Alex Klapowitz
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


| Set Power (W) | ND Filter | Microscope Objective | Measured Power (µW) |
|---------------|-----------|----------------------|---------------------|
| 0.01          | None      | 50x                  | 1.62                |
| 0.02          | None      | 50x                  | 2.74                |
| 0.03          | None      | 50x                  | 3.85                |
| 0.04          | None      | 50x                  | 5.00 ± 0.14         |
| 0.05          | None      | 50x                  | 6.10 ± 0.16         |
| 0.06          | None      | 50x                  | 7.15 ± 0.2          |
| 0.07          | None      | 50x                  | 8.5  ± 0.2          |
| 0.08          | None      | 50x                  | 9.6  ± 0.2          |
| 0.09          | None      | 50x                  | 10.6 ± 0.3          |
| 0.10          | None      | 50x                  | 11.6 ± 0.3          |
| 0.11          | None      | 50x                  | 12.7 ± 0.3          |
| 0.12          | None      | 50x                  | 13.7 ± 0.3          |
| 0.13          | None      | 50x                  | 14.9 ± 0.4          |
| 0.14          | None      | 50x                  | 15.9 ± 0.5          |
| 0.15          | None      | 50x                  | 17.0 ± 0.5          |
| 0.16          | None      | 50x                  | 18.4 ± 0.4          |
| 0.17          | None      | 50x                  | 18.9 ± 0.5          |
| 0.18          | None      | 50x                  | 20.0 ± 0.5          |
| 0.19          | None      | 50x                  | 20.6 ± 0.5          |
| 0.20          | None      | 50x                  | 21.5 ± 0.6          |
| 0.25          | None      | 50x                  | 25.4 ± 0.7          |
| 0.30          | None      | 50x                  | 29.0 ± 0.7          |
| 0.35          | None      | 50x                  | 33.3 ± 0.9          |
| 0.40          | None      | 50x                  | 36.3 ± 1.0          |
| 0.45          | None      | 50x                  | 39.0 ± 1.1          |
| 0.50          | None      | 50x                  | 40.5 ± 1.1          |
| 0.55          | None      | 50x                  | 42.8 ± 0.8          |
| 0.60          | None      | 50x                  | 43.1 ± 1.1          |
| 0.01          | None      | 100x                 | 0.44 ± 0.02         |
| 0.02          | None      | 100x                 | 0.75 ± 0.02         |
| 0.03          | None      | 100x                 | 1.05 ± 0.03         |
| 0.04          | None      | 100x                 | 1.35 ± 0.04         |
| 0.05          | None      | 100x                 | 1.64 ± 0.04         |
| 0.06          | None      | 100x                 | 1.92 ± 0.05         |
| 0.07          | None      | 100x                 | 2.24 ± 0.03         |
| 0.08          | None      | 100x                 | 2.60 ± 0.06         |
| 0.09          | None      | 100x                 | 2.89 ± 0.08         |
| 0.10          | None      | 100x                 | 3.13 ± 0.08         |
| 0.11          | None      | 100x                 | 3.37 ± 0.10         |
| 0.12          | None      | 100x                 | 3.7  ± 0.1          |
| 0.13          | None      | 100x                 | 3.97 ± 0.08         |
| 0.14          | None      | 100x                 | 4.2  ± 0.1          |
| 0.15          | None      | 100x                 | 4.38 ± 0.12         |
| 0.16          | None      | 100x                 | 4.6  ± 0.1          |
| 0.17          | None      | 100x                 | 4.75 ± 0.11         |
| 0.18          | None      | 100x                 | 4.95 ± 0.15         |
| 0.19          | None      | 100x                 | 5.13 ± 0.13         |
| 0.20          | None      | 100x                 | 5.40 ± 0.14         |
| 0.25          | None      | 100x                 | 6.6  ± 0.2          |
| 0.30          | None      | 100x                 | 7.6  ± 0.2          |
| 0.35          | None      | 100x                 | 8.8  ± 0.3          |
| 0.40          | None      | 100x                 | 10.0 ± 0.3          |
| 0.45          | None      | 100x                 | 11.3 ± 0.3          |
| 0.50          | None      | 100x                 | 12.8 ± 0.4          |
| 0.55          | None      | 100x                 | 14.6 ± 0.4          |
| 0.60          | None      | 100x                 | 16.7 ± 0.4          |

```python
import pathlib

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots

from markdown_tools import extract_data

# Gather variables from filename
filename = "power-reading_532nm_2022-08-04.md"
source = pathlib.Path(filename)
target = source.name

verdi_power = extract_data(source)
# set boolean masks
obj_50 = verdi_power["Microscope Objective"].isin(["50x"])
obj_100 = verdi_power["Microscope Objective"].isin(["100x"])
# Use boolean masks to pick subsets of entire dataframe
verdi_50 = verdi_power.loc[obj_50]
verdi_100 = verdi_power.loc[obj_100]
# Plot each subset
with plt.style.context(["default", "science", "notebook"]):
    fig, ax = plt.subplots()
    fig.suptitle(source.stem)
    verdi_50.plot(
        ax=ax,
        y="Measured Power (µW)",
        yerr="± Measured Power (µW)",
        label="50x",
    )
    verdi_100.plot(
        ax=ax,
        y="Measured Power (µW)",
        yerr="± Measured Power (µW)",
        label="100x",
    )
    ax.set_ylabel("Measured Power (µW)")

    figname = target.with_suffix(".png")
    fig.savefig(figname)
    print(f"Figure saved to {figname}")
plt.show()
```

![power plots of laser at various objectives](power-reading_532nm_2022-08-04.png "Laser plots")
