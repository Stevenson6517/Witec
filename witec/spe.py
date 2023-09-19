from collections import deque, UserDict
from collections.abc import Set, Mapping
from dataclasses import dataclass
from numbers import Number
import textwrap
import os
import sys
from typing import Optional

from dateutil import parser
import numpy as np

import witec.winspec


# ref: https://stackoverflow.com/a/32935278
def map_nested_dicts_modify(dictionary, func):
    """Apply a function to all byte items of a dictionary, recursively."""
    for key, value in dictionary.items():
        if isinstance(value, Mapping):
            map_nested_dicts_modify(value, func)
        elif isinstance(value, bytes):
            dictionary[key] = func(value)


def get_user_attributes(cls, exclude_methods=True):
    base_attrs = dir(type("dummy", (object,), {}))
    this_cls_attrs = dir(cls)
    res = []
    for attr in this_cls_attrs:
        if base_attrs.count(attr) or (callable(getattr(cls, attr)) and exclude_methods):
            continue
        res += [attr]
    return res


def get_dict(obj):
    keys = {}
    for attr in get_user_attributes(obj):
        if attr.startswith("_"):
            continue
        keys[attr] = getattr(obj, attr)
    return keys


@dataclass
class SPE:
    file: str
    dtype: Optional[type] = np.int32

    def __post_init__(self):
        self.contents = witec.winspec.read_spe(self.file)
        self._restore_datatypes(self.dtype)

    def __str__(self):
        description = {
            "Filename": self.spefname,
            "Size in memory (kb)": "{:,d}".format(round(self.size / 1e3)),
            "Observation date": self.date,
            "Data shape": self.data.shape,
            "Accumulations": self.accumulations,
            "Exposure (sec)": self.exposure,
            "Background corrected": self.background,
            "Flatfield corrected": self.flatfield,
            "Chip Temp (C)": self.chip_temp,
            "Axis": "\n" + textwrap.indent(self.axis.info, prefix="\t"),
        }
        return "\n".join([f"{key:<30}: {value}" for key, value in description.items()])

    def _restore_datatypes(self, dtype=np.int16):
        """Reduce contents filesize by converting data to numerical type."""
        self.contents["data"] = np.asarray(self.contents["data"], dtype=dtype)

    @property
    def data(self):
        """Extract a 2D array of acquisitions of shape (n, spectrum).

        Bins all pixels in a vertical column and sums the intensity in each bin.
        Each spectrum is a 1D array that is the same width as the ROI during acquisition.
        """
        # return np.sum(self.contents["data"], axis=1, dtype=self.dtype)
        return self.contents.data

    @property
    def axis(self):
        # return SPEAxis(self.contents["XCALIB"])
        axis = self.header["xcalibration"]
        poly_order = axis["polynom_order"]
        poly_coeff = axis["polynom_coeff"]
        indices = np.linspace(
            1, self.header["xdim"], self.header["xdim"], dtype=np.uint16
        )
        calibrate = np.poly1d(np.array(poly_coeff[2::-1]))
        return calibrate(indices)

    @property
    def igain(self):
        return self.contents["IGAIN"]

    @property
    def exposure(self):
        return self.contents["EXPOSURE"]

    @property
    def spefname(self):
        return self.contents["SPEFNAME"]

    @property
    def date(self):
        return parser.parse(self.contents["OBSDATE"].decode("UTF-8")).date()

    @property
    def chip_temp(self):
        return self.contents["CHIPTEMP"]

    @property
    def comments(self):
        return self.contents["COMMENTS"].decode("UTF-8")

    @property
    def accumulations(self):
        return self.contents["ACCUMULATIONS"]

    @property
    def flatfield(self):
        return self.contents["FLATFIELD"]

    @property
    def background(self):
        return self.contents["BACKGROUND"]

    # Helpful variables
    @property
    def slug(self):
        return os.path.splitext((self.spefname))[0]

    @property
    def basename(self):
        return os.path.basename(self.slug)

    @property
    def size(self):
        """Recursively iterate to sum size of object & members."""
        ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)
        _seen_ids = set()

        def inner(obj):
            obj_id = id(obj)
            if obj_id in _seen_ids:
                return 0
            _seen_ids.add(obj_id)
            size = sys.getsizeof(obj)
            if isinstance(obj, ZERO_DEPTH_BASES):
                pass  # bypass remaining control flow and return
            elif isinstance(obj, (tuple, list, Set, deque)):
                size += sum(inner(i) for i in obj)
            elif isinstance(obj, Mapping) or hasattr(obj, "items"):
                size += sum(inner(k) + inner(v) for k, v in getattr(obj, "items")())
            # Check for custom object instances - may subclass above too
            if hasattr(obj, "__dict__"):
                size += inner(vars(obj))
            if hasattr(obj, "__slots__"):  # can have __slots__ with __dict__
                size += sum(
                    inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s)
                )
            return size

        return inner(self)


@dataclass
class SPEAxis(dict):
    axis: dict
    calibration: Optional[str] = "poly"

    def __post_init__(self):
        xcalib = {}
        for key, value in self.axis.items():
            if isinstance(value, bytes):
                xcalib[key] = int.from_bytes(
                    value, byteorder="big"
                )  # value.decode("utf") # or windows-1252?
            elif isinstance(value, tuple) and isinstance(value[0], bytes):
                xcalib[key] = self._bytes_to_string(value)
            else:
                xcalib[key] = value
        self.axis = xcalib
        self.update(xcalib)

    def _bytes_to_string(self, array, encoding="utf-8"):
        string = []
        for byte in array:
            string.append(byte.decode(encoding))
        return "".join(string).strip("\x00")

    @property
    def info(self):
        info = {
            "Label": self.label,
            "Center wavelength (nm)": self.axis["SpecCenterWlNm"],
            "Grating (g/mm)": self.axis["SpecGrooves"],
        }
        return "\n".join([f"{key:<22}: {value}" for key, value in info.items()])

    @property
    def ccd_columns(self):
        return int(self.axis["pixel_position"][2])

    @property
    def label(self):
        return self.axis["string"]

    @property
    def units(self):
        return self.label.split("[")[1].split("]")[0]

    @property
    def indices(self):
        return np.linspace(1, self.ccd_columns, self.ccd_columns, dtype=np.uint16)

    @property
    def values(self):
        """Map calibrated wavelength to the CCD pixels in ROI."""
        if self.calibration == "poly":
            calibrate = np.poly1d(np.array(self.axis["polynom_coeff"][2::-1]))
            return calibrate(self.indices)
        if self.calibration == "linear":
            start_wl = self.axis["calib_value"][0]
            end_wl = self.axis["calib_value"][2]
            return np.linspace(start_wl, end_wl, self.ccd_columns)
