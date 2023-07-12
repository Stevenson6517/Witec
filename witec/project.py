"""This module supplies a script that extracts data from a WITec Project
file.  The binary extraction algorithm implemented in the Witec class is
based off WITec Project 1.92.

A WITec file is a nested structure of binary strings pertaining to data
and experimental settings necessary to work with
ScanCtrlSpectroscopyPlus.

The structure of the binary data was gathered largely by members at
ElsevierSoftwareX, but their extraction was written in MATLAB. This
module is a rough attempt at a working port for Python.

BSD 3-Clause License
Copyright (c) 2019, Joonas T. Holmi (jtholmi@gmail.com)
All rights reserved.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

ref: https://github.com/ElsevierSoftwareX/SOFTX-D-20-00088/blob/15d72d95c9585ab7f2ad249d3f1ee8629896ae80/%2BWITio/%2Bdoc/README%20on%20WIT-tag%20format.txt
"""
import collections.abc
import logging
import struct

import witec.text_tools

log = logging.getLogger()


# ref: https://stackoverflow.com/a/32935278
def map_nested_dicts_modify(dictionary, func):
    """Apply a function to all byte items of a dictionary, recursively."""
    for key, value in dictionary.items():
        if isinstance(value, collections.abc.Mapping):
            map_nested_dicts_modify(value, func)
        elif isinstance(value, bytes):
            dictionary[key] = func(value)


class Witec:
    """A class to contain the converted data from a binary .WIP file

    Attributes
    ----------
    magic : str
        A filetype identifier hidden in the first 8 bytes of the file.
    dict : dict
        A nested data structure of the contents of a .WIP file
    """

    def __init__(self, file):
        with open(file, "rb") as raw:
            b_string = raw.read()
            # First 8 bytes describe file type
            self.magic = struct.unpack("<8s", b_string[:8])[0].decode()
            # Remaining bytes follow predictable pattern
            self.dict = self._extract_binary(b_string[8:])
            # Apply fixes to fields with known errors
            info = self.dict["WITec Project"]["Data"]["Data 1"]["TDStream"]
            info["StreamData"] = self._convert_information_tag(info["StreamData"])
            # Convert remaining strings in dictionary
            map_nested_dicts_modify(self.dict, lambda v: v.decode("windows-1252"))

    def _extract_binary(self, b_string):
        """Traverse through a byte string according to a fixed storage format."""
        wit = {}
        while b_string:
            shift = 0
            # First several bytes give name of field (variable in length)
            name, length = self._extract_name(b_string)
            shift += length
            # (1 x uint32) describes the data type at next pointer
            dtype = struct.unpack("<I", b_string[shift : (shift := shift + 4)])[0]
            log.debug("dtype: %s", dtype)
            # (1 x uint64) points to data start byte (absolute from start of file)
            start = struct.unpack("<Q", b_string[shift : (shift := shift + 8)])[0]
            log.debug("start: %s", start)
            # (1 x uint64) points to data end byte (absolute from start of file)
            end = struct.unpack("<Q", b_string[shift : (shift := shift + 8)])[0]
            log.debug("end: %s", end)
            size = end - start
            log.debug("size: %s", size)
            # Process data field according to type
            data_string = b_string[shift : (shift := shift + size)]
            if dtype == 0:  # wit
                string = struct.unpack(f"<{size}s", data_string)[0]
                data = self._extract_binary(string)
            elif dtype == 1:  # unused
                pass
            elif dtype == 2:  # double (short)
                data = struct.unpack(f"<{size}b", data_string)
            elif dtype == 3:  # single (byte)
                data = struct.unpack(f"<{size}b", data_string)
            elif dtype == 4:  # int64 (quad = long long)
                data = struct.unpack(f"<{size}q", data_string)
            elif dtype == 5:  # int32 (long)
                data = struct.unpack(f"<{size}b", data_string)
            elif dtype == 6 and (size % 4 == 0):  # uint32
                data = struct.unpack(f"<{size}I", data_string)
            elif dtype == 6:  # uint16
                data = struct.unpack(f"<{size}H", data_string)
            elif dtype == 7:  # uint8
                data = struct.unpack(f"<{size}B", data_string)
            elif dtype == 8:  # logical
                data = struct.unpack(f"<{size}?", data_string)
            elif dtype == 9:  # string
                string = struct.unpack(f"<{size}s", data_string)[0]
                data = b""
                while string:
                    word, offset = self._extract_name(string)
                    data += word
                    string = string[offset:]
            log.debug("data: %s", data)
            # Store evaluated bytes and repeat if necessary
            wit[name.decode()] = data
            b_string = b_string[shift:]
        return wit

    def _extract_name(self, b_string):
        """Read the first N+1 bytes of a long byte string."""
        shift = 0
        # (1 x uint32) describes size of label
        name_length = struct.unpack("<I", b_string[shift : (shift := shift + 4)])[0]
        log.debug("name length: %s", name_length)
        # (N x char) to label field
        name = struct.unpack(
            f"<{name_length}s", b_string[shift : (shift := shift + name_length)]
        )[0]
        log.debug("name: %s", name)
        return name, shift

    def _convert_information_tag(self, info_bmp):
        """Convert bitmap data back to string."""
        # Information metadata is classified as dtype=7 (uint8), so it is stored
        # as bitmap data by above extraction technique
        # Change its dtype so that it appears as words instead of numbers
        info = struct.pack(f"<{len(info_bmp)}B", *info_bmp)
        # strip info of rich-text formatting and return utf-8 string
        info = witec.text_tools.striprtf(info)
        info = info[:-1]  # Remove hidden b'\x00' at end of string
        return info
