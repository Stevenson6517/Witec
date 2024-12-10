#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A module of helper functions for parsing markdown format."""
from io import StringIO
import re

import pandas as pd


def _extract_markdown_table(file):
    """Extract a list of markdown tables identified in a file.

    Tables are identified by their leading | character.
    Empty lines separate tables from each other.
    Returned tables retain their original markdown formatting.
    """
    md_table_string = ""
    with open(file, "r", encoding="utf-8") as source:
        for line in source:
            # Search by | or newline (\n) at the start of each line (^)
            if re.search((r"^\||^\n"), line):
                md_table_string += line
    # Collapse multiple newlines into one empty line between tables and
    # strip leading and trailing newlines
    md_table_string = re.sub(r"\n{2,}", "\n\n", md_table_string).strip("\n")

    # Separate tables by newline and return as a list of separate tables
    return md_table_string.split("\n\n")


def _clean_dataframe(dataframe):
    """Sanitize formatting from a markdown table"""
    # Remove empty right column
    clean_df = dataframe.dropna(axis=1, how="all").copy()
    # Remove leading and trailing spaces in column names
    clean_df = clean_df.rename(columns=lambda x: x.strip())
    for col in clean_df:
        # Remove leading and trailing spaces in column values
        clean_df[col] = clean_df[col].str.strip()
        # Separate ± values into new error column
        if clean_df[col].str.contains("±").any():
            err_col = "± " + col
            clean_df[[col, err_col]] = clean_df[col].str.split(pat=r"±", expand=True)
    for col in clean_df:
        # Attempt to convert any column with numbers to numeric dtype
        try:
            clean_df[col] = pd.to_numeric(clean_df[col])
        except ValueError:
            continue
    try:
        clean_df.index = pd.to_numeric(clean_df.index)
    except ValueError:
        pass
    return clean_df


def extract_data(file, index=0):
    """Return a dataframe of a markdown table present in a file.

    Parameters
    ----------
    index : int
        If multiple markdown tables are present, select the extracted
        table by index. Default = 0.

    Returns
    -------
    data : pandas dataframe
        A sanitized version of the extracted markdown table.
    """
    md_table = _extract_markdown_table(file)
    options = {
        "delimiter": "|",
        "index_col": 1,
        "header": 0,
    }
    dataframe = pd.read_csv(StringIO(md_table[index]), **options).iloc[1:]
    return _clean_dataframe(dataframe)
