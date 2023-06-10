# :microscope: WITec

A set of tools for interacting with and processing results from a WITec
AlphaSNOM.

> This project is currently in active development. Expect frequent
> breaking changes.

## Introduction

The tools and analysis provided by this repository attempt to recreate
some of the functionality of `ScanCtrlSpectroscopyPlus.exe` and
`WitecProject.exe` that are made available to the native Windows
installation associated with a WITec AlphaSNOM.

This repository aims to replace the proprietary `.WIP` (WitecProject
file) with an open-source [HDF5][hdf5] format that better withstands
data governance needs as they relate to external validation and
reproducibility that outlives the legacy software needed to operate this
equipment.

See a brief primer on [WITec formats](docs/witec_formats.md) for help in
understanding the data formats saved by _ScanCtrlSpectroscopyPlus_. The
analysis scripts work best on `.SPE` and `.WIP` files that have been
converted to `.hdf5` files.

[hdf5]: https://github.com/HDFGroup/hdf5

## Getting started

After cloning this repository, create a `witec` virtual environment from the
[environment.yaml](environment.yaml) file provided by this repository. Issue
the following command from a terminal navigated to the root of this project.

```python
conda env create -f environment.yaml
```

> Expect this process to take several minutes

Activate the environment before running any scripts:

```python
conda activate witec
```

