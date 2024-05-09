"""
This file helps bundle matching datasets from a Winspec external spectrum
dataset and a WITec Project file.

By assumption, a single .SPE file contains several sequential spectral
acquisitions under identical settings, and a WITec Project file contains
information about the spatial coordinates of those acquisitions. The main
function of this module generates a single HDF5 container file that represents
the main dataset as a 2D array of spectra (each represented as a 1D array of
intensity values per CCD pixel) and ancillary datasets that map each index of
this 2D array to specific coordinates and wavelengths.

The structure of the HDF5 file is modeled after a pyUSID dataset.  This
container file aims to preserve as much header information as is present in
each of the required input file.

"""
import pathlib
import numpy as np
import h5py
import sidpy
import pyUSID as usid

from witec.spe import SPE
import witec.winspec
from witec.project import Witec
import witec.utils


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """Write dictionary keys as hdf5 groups and contents as datasets. Nested
    keys are structured as nested groups.
    """
    # argument type checking
    if not isinstance(dic, dict):
        raise ValueError("must provide a dictionary")
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(h5file, h5py._hl.files.File):
        raise ValueError("must be an open h5py file")
    # save items to the hdf5 file
    for key, item in dic.items():
        if isinstance(item, (list, tuple)):
            item = np.array(item)
        if not isinstance(key, str):
            raise ValueError("dict keys must be strings to save to hdf5")
        # save strings, numpy.int64, and numpy.float64 types
        if isinstance(item, (np.int64, np.float64, str, float, np.float32, int)):
            h5file[path + key] = item
            # if not h5file[path + key][()] == item:
            #     raise ValueError('The data representation in the HDF5 file does not match the original dict.')
        # save numpy arrays
        elif isinstance(item, np.ndarray):
            try:
                h5file[path + key] = item
            except:
                item = np.array(item).astype("|S9")
                h5file[path + key] = item
            if not np.array_equal(h5file[path + key][()], item):
                raise ValueError(
                    "The data representation in the HDF5 file does not match the original dict."
                )
        # save dictionaries
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + "/", item)
        # other types cannot be saved and will result in an error
        else:
            raise ValueError("Cannot save %s type." % type(item))


def to_hdf5(project=None, winspec=None, output=None, *, metadata=None):
    """Combine a Witec Project file with contents from an associated Winspec
    acquisition.
    """
    if project is None:
        project = input("Specify a Witec Project file: ")
    if winspec is None:
        winspec = input("Specify a Winspec file: ")
    if output is None:
        default = pathlib.Path(winspec).with_suffix(".hdf5")
        default_choice = input(f"Use default filename, {default}? (y/n) -> ")
        if default_choice.lower() in ("y", "yes"):
            output = default
        else:
            output = input("Specify an output file: ")
    spe_object = SPE(winspec)
    spe_metadata = spe_object.header
    wip_object = Witec(project)

    # Pick out spatial coordinates from Witec file
    wip_info = witec.utils.metadata_from_wip(project)

    # Assume we want the info from the first available information tag
    default_tag = wip_info["Tag 0"]

    points_per_line = int(default_tag["Points per Line"])
    scan_width = float(default_tag["Scan Width [µm]"])
    start_x = float(default_tag["Scan Origin X [µm]"])
    stop_x = start_x + scan_width

    lines_per_image = int(default_tag["Lines per Image"])
    scan_height = float(default_tag["Scan Height [µm]"])
    start_y = float(default_tag["Scan Origin Y [µm]"])
    stop_y = start_y + scan_height

    number_of_images = int(default_tag["Number of Images"])
    scan_depth = float(default_tag["Scan Depth [µm]"])
    start_z = float(default_tag["Scan Origin Z [µm]"])
    stop_z = start_z + scan_depth

    z_rotation = default_tag["Z-Rotation [°]"]

    pos_x_vals = np.linspace(start_x, stop_x, points_per_line)
    pos_y_vals = np.linspace(start_y, stop_y, lines_per_image)
    spec_vals = spe_object.axis

    pos_dims = [
        usid.Dimension("x", "um", pos_x_vals),
        usid.Dimension("y", "um", pos_y_vals),
    ]
    spec_dims = [usid.Dimension("Wavelength", "nm", spec_vals)]
    # Map between header datatype field and numpy datatype
    _datatype_map = {0: np.float32, 1: np.int32, 2: np.int16, 3: np.uint16}
    dtype = _datatype_map[spe_object.header["datatype"]]

    with h5py.File(output, "w") as h5:
        h5_meas_group = sidpy.prov_utils.create_indexed_group(h5, "Measurement")
        h5_raw = usid.hdf_utils.write_main_dataset(
            h5_meas_group,  # parent HDF5 group
            main_data=np.sum(spe_object.data, axis=2),
            main_data_name="Raw_Data",  # Name of main dataset
            quantity="Intensity",  # Physical quantity contained in Main dataset
            units="a.u.",  # Units for the physical quantity
            dtype=_datatype_map[spe_object.header["datatype"]],
            pos_dims=pos_dims,  # Position dimensions
            spec_dims=spec_dims,  # Spectroscopic dimensions
            compression="gzip",
        )
        # Metadata
        recursively_save_dict_contents_to_group(
            h5, "Measurement_000/Winspec/", spe_metadata
        )
        recursively_save_dict_contents_to_group(
            h5, "Measurement_000/", wip_object.contents
        )
        if metadata:
            recursively_save_dict_contents_to_group(
                h5, "Measurement_000/Metadata/", metadata
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="convert",
        description="Search for matching .WIP and .SPE files and combine them into a single .hdf5 file in pyUSID format",
    )
    parser.add_argument(
        "filename",
        type=str,
        help="A single .SPE or .WIP file with an accompanying counterpart .WIP or .SPE with the same base name",
    )
    parser.add_argument(
        "--winspec",
        type=str,
        default=None,
        help="An explicit .SPE file if its base name differs from filename",
    )
    parser.add_argument(
        "--witec",
        type=str,
        default=None,
        help="An explicit .WIP file if its base name differs from filename",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="An explicit name for the resultant .hdf5 file. If NONE, defaults to same as filename but with .hdf5 extension",
    )
    parser.add_argument(
        "-m",
        "--meta",
        type=str,
        action="append",
        help="An additional metadata YAML dictionary to be inserted into the .hdf5 file",
    )
    args = parser.parse_args()

    filename = pathlib.Path(args.filename)
    if args.winspec is None:
        args.winspec = filename.with_suffix(".SPE")
    if args.witec is None:
        args.witec = filename.with_suffix(".WIP")
    if args.output is None:
        args.output = filename.with_suffix(".hdf5")

    metadata = witec.utils.metadata_from_name(args.filename)
    if args.meta:
        for meta in args.meta:
            metadata.update(witec.utils.metadata_from_yaml(meta))

    to_hdf5(
        project=args.witec, winspec=args.winspec, output=args.output, metadata=metadata
    )
    print(f"Contents written to {args.output}")
