"""This module provides utility functions for assembling metadata from a
filename with coresponding WIP and SPE files.

The main function, assemble_metadata, will extract and assemble all
metadata from a similarly named SPE file and WIP file based on a
user-supplied basename. Additional metadata can be included at runtime
by supplying a yaml file with a dictionary of common settings.

Use the tools in this file in other scripts in this project by importing
this file and calling any necessary functions.

>>> import witec.utils as utils

>>> target = "path/to/file" # SPE file or WIP file
>>> basename = os.path.splitext(target)[0] # path w/o extension
>>> supplemental = [
...         layout.yaml,
...         authorship.yaml,
...         sample.yaml,
...         ]
>>> extracted_dict = utils.assemble_metadata(basename, *supplemental)
"""


from datetime import datetime
import pathlib
import re

import yaml

from witec.project import Witec
import witec.winspec


def metadata_from_name(filename):
    """Parse metadata from a structured filename into a dictionary.

    Parameters
    ----------
    filename : str
        The path to a structured filename with the following keys:
        "sample_location_identifier_meas-type{_settings}_datetime_meas-num"
        Values in {} are optional and may contain multiple fields.
        Directory structure, if present in the file name, is ignored.

    Returns
    -------
    fields : dict
        key: value pairs, where values are extracted from filename
    """
    basename = pathlib.Path(filename).name
    slug = pathlib.Path(basename).stem
    fields_sep = slug.split("_")
    fields_sep = [field for field in fields_sep if field != ""]
    sample, location, identifier, meas_type = fields_sep[0:4]
    measurement_number = fields_sep[-1]
    datestring = fields_sep[-2]
    set_fields = set(fields_sep)
    existing_fields = set(
        [sample, location, identifier, meas_type, datestring, measurement_number]
    )
    source_settings = set_fields.difference(existing_fields)
    # Assign values to dictionary
    fields = {}
    fields["sample"] = sample
    fields["location"] = location
    fields["identifier"] = identifier
    fields["meas-type"] = meas_type
    fields["source-settings"] = _assign_settings(source_settings)
    fields["datetime"] = _assign_datetime(datestring)
    fields["measurement number"] = measurement_number
    return fields


# https://stackoverflow.com/questions/9507648/datetime-from-string-in-python-best-guessing-string-format
def _assign_datetime(s_date):
    dates = pathlib.Path(pathlib.Path(__file__).parent, "conventions/dates.yaml")
    with open(dates, "r", encoding="utf-8") as stream:
        date_patterns = yaml.safe_load(stream)
    for pattern in date_patterns:
        try:
            date = datetime.strptime(s_date, pattern).replace(microsecond=0)
            # If timezone is already present, don't overwrite it
            if date.utcoffset():
                return date.isoformat()
            # Otherwise, assume local time zone
            return date.astimezone().isoformat()
        except ValueError:
            pass


def _assign_settings(source_settings):
    settings = {}
    for field in source_settings:
        try:
            value, unit = _split_field_by_value(field)
            if unit == "m":
                settings["wavelength (m)"] = value
            if unit == "W":
                settings["excitation source"] = "laser"
                settings["set power (W)"] = value
            if unit == "s":
                settings["exposure time (s)"] = value

        except:
            try:
                value, name = _split_field_by_name(field)
                if value == "obj":
                    settings["objective"] = name
                if value == "f":
                    settings["filter"] = name
                if value == "LED":
                    settings["excitation source"] = value
                    settings["LED details"] = name
                else:
                    settings[value] = name
            except:
                settings["other"] = field

    return settings


def _split_field_by_value(string):
    value, unit = re.findall(("(^\d*)(\D*$)"), string)[0]
    return _assign_value(value, unit)


def _split_field_by_name(string):
    value_name = string.split("-")
    value, name = value_name[0], value_name[1]
    return value, name


def _assign_value(value, unit):
    scale, unit_SI = _parse_unit(unit)
    return int(value) * scale, unit_SI


def _parse_unit(unit):
    if len(unit) > 1:
        if unit[0] == "m":
            scale = 1e-3
        if unit[0] in ["u", "µ"]:
            scale = 1e-6
        if unit[0] == "n":
            scale = 1e-9
        if unit[0] == "p":
            scale = 1e-12
    else:
        scale = 1

    unit_SI = unit[-1]

    return scale, unit_SI


def metadata_from_wip(filename):
    """Extract metadata from a Witec Project file as a dictionary.

    Parameters
    ----------
    filename : str
        Path to a WitecProject file, with .WIP extension.

    Returns
    -------
    metadata_wip : dict
        Acqusition settings and user notes from a project.
    """
    wip = Witec(filename)
    metadata_wip = {}
    data_keys = wip.data.keys()
    for data_key in data_keys:
        try:
            data_text = wip.info(wip.data[data_key])
            metadata_wip[data_key] = _parse_wiptextfile(data_text)
        except TypeError:
            continue
    return metadata_wip


def _parse_wiptextfile(wip_text):
    lines = re.sub("\t", "", wip_text).splitlines()
    wip_dict = {}
    wip_dict["Information"] = lines[0]
    for line in lines[1:]:
        try:
            key, *values = line.split(":")
            value = ":".join(values)
        except ValueError:
            continue
        wip_dict[key] = value
    return {key: value for key, value in wip_dict.items() if value}


def metadata_from_spe(filename):
    """Extract the full header from a winspec .SPE file.

    Parameters
    ----------
    filename : str
        Path to a winspec file, with .SPE extension.

    Returns
    -------
    metadata_spe : dict
        Acquisition and calibration settings.
    """
    return witec.winspec.SpeFile(filename).header


def metadata_from_yaml(yaml_string):
    """Extract and categorize the data from a given yaml file into a dictionary"""
    with open(yaml_string, "r", encoding="utf-8") as stream:
        metadata_yaml = yaml.safe_load(stream)
    return metadata_yaml


def assemble_metadata(basename, *yaml):
    """Gather metadata from similarly named basename.SPE and basename.WIP files.

    Parameters
    ----------
    basename : str
        "Path/to/directory/structured_filename"

    yaml: str (optional)
        Path to additonal yaml file(s) where other settings are stored.

    Returns
    -------
    metadata : dict
        Combined dictionary of settings from .WIP, .SPE, and yaml files

    Assumptions
    -----------
    A .WIP and .SPE file exist in the same directory and with an
    identical naming structure such that their full file paths differ
    only by filetype extension.

    Notes
    -----
    - Each additional (optional) argument after the required basename
      argument is assumed to be a yaml dictionary, applied left-to-right.
    - If the same metadata key is present in multiple yaml files, the value from
      the last dictionary overwrites the original value.
    """
    metadata = {}
    metadata["WIP"] = metadata_from_wip(pathlib.Path(basename).with_suffix(".WIP"))
    metadata["SPE"] = metadata_from_spe(pathlib.Path(basename).with_suffix(".SPE"))
    metadata["Experiment"] = metadata_from_name(basename)
    for file in yaml:
        metadata.update(metadata_from_yaml(file))
    return metadata
