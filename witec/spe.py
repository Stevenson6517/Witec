from collections import deque, UserDict
from collections.abc import Set, Mapping
from dataclasses import dataclass
from numbers import Number
import textwrap
import os
import sys
from typing import Optional
import struct

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
        self.contents = witec.winspec.SpeFile(self.file)

    @property
    def data(self):
        """Extract a 2D array of acquisitions of shape (n, spectrum).

        Bins all pixels in a vertical column and sums the intensity in each bin.
        Each spectrum is a 1D array that is the same width as the ROI during acquisition.
        """
        # return np.sum(self.contents["data"], axis=1, dtype=self.dtype)
        return self.contents.data

    @property
    def header(self):
        header = get_dict(self.contents.header)
        header["Comments"] = "".join(
            byte.decode() for byte in struct.unpack("400p", header["Comments"])
        )  # witec.winspec.c_char_Array_5_Array_80
        header["ROIinfblk"] = get_dict(
            header["ROIinfblk"]
        )  # witec.winspec.ROIinfo_Array_10
        header["SpecMirrorLocation"] = struct.unpack(
            "2H", header["SpecMirrorLocation"]
        )  # witec.winspec.c_short_Array_2
        header["SpecMirrorPos"] = struct.unpack(
            "2H", header["SpecMirrorPos"]
        )  # witec.winspec.c_short_Array_2
        header["SpecSlitLocation"] = struct.unpack(
            "4H", header["SpecSlitLocation"]
        )  # witec.winspec.c_short_Array_4
        header["SpecSlitPos"] = struct.unpack(
            "4I", header["SpecSlitPos"]
        )  # witec.winspec.c_short_Array_4
        header["xcalibration"] = get_dict(
            header["xcalibration"]
        )  # witec.winspec.AxisCalibration
        header["ycalibration"] = get_dict(
            header["ycalibration"]
        )  # witec.winspec.AxisCalibration
        for calib in ["xcalibration", "ycalibration"]:
            for key in header[calib]:
                if "string" in key:
                    header[calib][key] = struct.unpack(
                        f"{len(header[calib][key])}s", header[calib][key]
                    )[0]
                else:
                    try:
                        header[calib][key] = struct.unpack(
                            f"{len(header[calib][key])}B", header[calib][key]
                        )
                    except struct.error:
                        header[calib][key] = struct.unpack(
                            f"{len(header[calib][key])}d", header[calib][key]
                        )
                    except TypeError:
                        continue
        map_nested_dicts_modify(header, lambda v: v.decode("ascii"))

        return header

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
