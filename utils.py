# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from datetime import datetime
import os
import re

import yaml

import winspec

# This definition will take the title of a WIP file and create a
# dictionary with all of the fields and their paired values established
# in the file name
# It will print out these values as well


def metadata_from_name(filename):
    basename = os.path.basename(filename)
    slug, ext = os.path.splitext(basename)
    fields_sep = slug.split("_")
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
    dates = "witec/conventions/dates.yaml"
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
            value, name = _split_field_by_name(field)
            if value == "obj":
                settings["objective"] = name
            if value == "f":
                settings["filter"] = name
            if value == "LED":
                settings["excitation source"] = value
                settings["LED details"] = name
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
    ##Somehow we end up with a text file from the wip file.
    ##The text variable below was just a practice file for me to use and should be changed

    # wip_text = extract_text(filename)
    wip_text = "hBN-10_loc-uppercenter_eye_exts-r_532nm_0800mW_f-ND10A_obj-50x_1000ms_2023-06-27_1.txt"
    metadata_wip = _parse_wiptextfile(wip_text)
    return metadata_wip


def _parse_wiptextfile(wip_text):
    with open(wip_text, "r", encoding="latin-1") as f:
        content = f.readlines()
        wip_dict = {}
        for i in content:
            if re.findall("^.*:\t.*\n$", i) != []:
                wip_dict[re.findall("^(.*):\t.*\n$", i)[0]] = re.findall(
                    "^.*:\t(.*)\n$", i
                )[0]
    return wip_dict


def metadata_from_spe(filename):
    metadata_spe = winspec.read_spe(filename)
    del metadata_spe["data"]
    return metadata_spe


def metadata_from_yaml(yaml_string):
    with open(yaml_string, "r", encoding="utf-8") as stream:
        metadata_yaml = yaml.safe_load(stream)
    return metadata_yaml


def assemble_metadata(basename, *yaml):
    metadata = {}
    metadata["WIP"] = metadata_from_wip(basename + ".WIP")
    metadata["SPE"] = metadata_from_spe(basename + ".SPE")
    metadata["Experiment"] = metadata_from_name(basename)
    for file in yaml:
        metadata.update(metadata_from_yaml(file))
    return metadata


# +
