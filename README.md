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

See the [How To Guide](docs/how_to.md) for instructions on how to use
the instruments connected to the WITec AlphaSNOM in Stevenson 6517.

### Viewing Jupyter notebooks

Jupyter notebooks are a useful way to explore data and develop code
interactively, but they don't track well under version control. The
[jupytext][jupytext] extension for Jupyter Lab allows markdown files
(`.md`) and plain python files (`.py`) to be treated as interactive
python notebooks (`.ipynb`) while maintaining their simpler file formats
for better version control.

This project contains several Jupyter notebooks to help users understand
the scripts and types of data generated by the WITec AlphaSNOM. When you
first clone this repository, all notebooks will be in `.py` format, but
you can pair them to an interactive notebook or open them as an
interactive notebook with Jupytext. See their documentation on [paired
notebooks][jupytext-paired-notebooks] for help.

[jupytext]: https://jupytext.readthedocs.io/en/latest/
[jupytext-paired-notebooks]: https://jupytext.readthedocs.io/en/latest/paired-notebooks.html

## Contributing

Notice any errors? Tell us about them.

This lab is run by scientists, not software developers. Newcomers are welcome.
Check out our [guidelines](CONTRIBUTING.md) on how you can help.
