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
# #!/usr/bin/env python3
from datetime import datetime
import os

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
    fields["source-settings"] = source_settings
    fields["datetime"] = assign_datetime(datestring)
    return fields


def assign_datetime(string):
    split = ((string.split(".")[0]).split("+"))[0]
    digits = ["0"] * 14
    n = 0
    for i in [*split]:
        if i.isdigit():
            digits[n] = i
            n = n + 1

    year = int("".join(digits[0:4]))
    month = int("".join(digits[4:6]))
    day = int("".join(digits[6:8]))
    hour = int("".join(digits[8:10]))
    minute = int("".join(digits[10:12]))
    seconds = int("".join(digits[12:14]))

    iso_8601_datetime_str = (
        datetime(year, month, day, hour, minute, seconds).astimezone().isoformat()
    )

    return iso_8601_datetime_str


# -
