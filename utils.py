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


# -
