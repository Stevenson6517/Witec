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

# This definition will take the title of a WIP file and create a
# dictionary with all of the fields and their paired values established
# in the file name
# It will print out these values as well


def parse_fields(text):
    # Sanitize input
    text_name = os.path.basename(text)
    slug, ext = os.path.splitext(text_name)
    fields_sep = slug.split("_")
    sample, location, identifier, meas_type = fields_sep[0:4]
    datestring = fields_sep[-1]
    set_fields = set(fields_sep)
    existing_fields = set([sample, location, identifier, meas_type, datestring])
    source_settings = set_fields.difference(existing_fields)
    # Assign values to dictionary
    fields = {}
    fields["sample"] = sample
    fields["location"] = location
    fields["identifier"] = identifier
    fields["meas-type"] = meas_type
    fields["source-settings"] = assign_settings(source_settings)
    fields["datetime"] = assign_datetime(datestring)
    return fields


# https://stackoverflow.com/questions/9507648/datetime-from-string-in-python-best-guessing-string-format
def assign_datetime(s_date):
    # TODO: Move this list to an external file
    date_patterns = [
        # Y(ear) m(onth) d(ay)
        "%Y%m%d",
        "%Y-%m-%d",
        # + H(our) M(inute)
        "%Y%m%d-%H%M",
        "%Y%m%d-%H-%M",
        "%Y-%m-%dT%H%M",
        "%Y-%m-%dT%H-%M",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d-%H-%M",
        # + H(our) M(inute) w/ timezones
        "%Y%m%d-%H%M%z",
        "%Y%m%d-%H-%M%z",
        "%Y-%m-%dT%H%M%z",
        "%Y-%m-%dT%H-%M%z",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%d-%H-%M%z",
        # + S(econds)
        "%Y%m%d-%H%M%S",
        "%Y%m%d-%H-%M-%S",
        "%Y-%m-%dT%H%M%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H-%M-%S",
        "%Y-%m-%d-%H-%M-%S",
        "%Y-%m-%d-%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        # + S(econds) w/ timezones
        "%Y%m%d-%H%M%S%z",
        "%Y%m%d-%H-%M-%S%z",
        "%Y-%m-%dT%H%M%S%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H-%M-%S%z",
        "%Y-%m-%d-%H-%M-%S%z",
        "%Y-%m-%d-%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
    ]

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


def assign_settings(source_settings):
    settings = {}
    for field in source_settings:
        try:
            value, unit = split_field_by_value(field)
            if unit == "m":
                settings["wavelength (m)"] = value
            if unit == "W":
                settings["excitation source"] = "laser"
                settings["set power (W)"] = value
            if unit == "s":
                settings["exposure time (s)"] = value

        except:
            value, name = split_field_by_name(field)
            if value == "obj":
                settings["objective"] = name
            if value == "f":
                settings["filter"] = name
            if value == "LED":
                settings["excitation source"] = value
                settings["LED details"] = name
    return settings


def split_field_by_value(string):
    value, unit = re.findall(("(^\d*)(\D*$)"), string)[0]
    return assign_value(value, unit)


def split_field_by_name(string):
    value_name = string.split("-")
    value, name = value_name[0], value_name[1]
    return value, name


def assign_value(value, unit):
    scale, unit_SI = parse_unit(unit)
    return int(value) * scale, unit_SI


def parse_unit(unit):
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
