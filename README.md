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
