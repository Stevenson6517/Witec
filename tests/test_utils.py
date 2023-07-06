import numbers

from witec.utils import (
    metadata_from_name,
    metadata_from_spe,
    metadata_from_wip,
    metadata_from_yaml,
    assemble_metadata,
)

# Directory Tests


def test_metadata_from_name_file_includes_nested_directory():
    filename_with_nested_directory = (
        "nested/directory/sample_loc_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_nested_directory)
    assert metadata["sample"] == "sample"


def test_metadata_from_name_file_includes_absolute_path_to_directory():
    filename_with_absolute_path_to_directory = "C://absolute/path/to/directory/sample_loc_id_meas-type_settings_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_absolute_path_to_directory)
    assert metadata["sample"] == "sample"


def test_metadata_from_name_file_includes_dot_and_nested_directory():
    filename_with_dot_and_nested_directory = "./nested/directory/sample_loc_id_meas-type_settings_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_dot_and_nested_directory)
    assert metadata["sample"] == "sample"


def test_metadata_from_name_file_includes_two_dots_and_nested_directory():
    filename_with_two_dots_and_nested_directory = "../nested/directory/sample_loc_id_meas-type_settings_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_two_dots_and_nested_directory)
    assert metadata["sample"] == "sample"


def test_metadata_from_name_file_includes_nested_directory_with_spaces():
    filename_with_nested_directory_with_spaces = "nested/directory with spaces/sample_loc_id_meas-type_settings_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_nested_directory_with_spaces)
    assert metadata["sample"] == "sample"


def test_metadata_from_name_file_includes_directory_no_ext():
    filename_with_directory_no_ext = (
        "nested/directory/sample_loc_id_meas-type_settings_date_measurement-number"
    )
    metadata = metadata_from_name(filename_with_directory_no_ext)
    assert metadata["measurement number"] == "measurement-number"


def test_metadata_from_name_file_no_ext():
    filename_no_ext = "sample_loc_id_meas-type_settings_date_measurement-number"
    metadata = metadata_from_name(filename_no_ext)
    assert metadata["measurement number"] == "measurement-number"


# Sample tests


def test_metadata_from_name_sample_has_hyphens():
    sample_with_hyphens = (
        "sample-with-hyphens_loc_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(sample_with_hyphens)
    assert metadata["sample"] == "sample-with-hyphens"


def test_metadata_from_name_sample_has_spaces():
    sample_with_spaces = (
        "sample with spaces_loc_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(sample_with_spaces)
    assert metadata["sample"] == "sample with spaces"


def test_metadata_from_name_sample_has_dots():
    sample_with_dots = (
        "sample.with.dots_loc_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(sample_with_dots)
    assert metadata["sample"] == "sample.with.dots"


# Location tests


def test_metadata_from_name_location_has_hyphens():
    location_with_hyphens = (
        "sample_location-with-hyphens_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(location_with_hyphens)
    assert metadata["location"] == "location-with-hyphens"


def test_metadata_from_name_location_has_spaces():
    location_with_spaces = (
        "sample_location with spaces_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(location_with_spaces)
    assert metadata["location"] == "location with spaces"


def test_metadata_from_name_location_has_dots():
    location_with_dots = (
        "sample_location.with.dots_id_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(location_with_dots)
    assert metadata["location"] == "location.with.dots"


# Identifier tests


def test_metadata_from_name_id_has_hyphens():
    id_with_hyphens = (
        "sample_location_id-with-hyphens_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(id_with_hyphens)
    assert metadata["identifier"] == "id-with-hyphens"


def test_metadata_from_name_id_has_spaces():
    id_with_spaces = (
        "sample_location_id with spaces_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(id_with_spaces)
    assert metadata["identifier"] == "id with spaces"


def test_metadata_from_name_id_has_dots():
    id_with_dots = (
        "sample_location_id.with.dots_meas-type_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(id_with_dots)
    assert metadata["identifier"] == "id.with.dots"


# Measurement tests


def test_metadata_from_name_meas_has_hyphens():
    meas_with_hyphens = (
        "sample_location_id_meas-with-hyphens_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(meas_with_hyphens)
    assert metadata["meas-type"] == "meas-with-hyphens"


def test_metadata_from_name_meas_has_spaces():
    meas_with_spaces = (
        "sample_location_id_meas with spaces_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(meas_with_spaces)
    assert metadata["meas-type"] == "meas with spaces"


def test_metadata_from_name_meas_has_dots():
    meas_with_dots = (
        "sample_location_id_meas.with.dots_settings_date_measurement-number.ext"
    )
    metadata = metadata_from_name(meas_with_dots)
    assert metadata["meas-type"] == "meas.with.dots"


# Source settings tests


def test_metadata_from_name_settings_recognizes_lasers():
    filename_with_laser = "sample_loc_id_meas-type_0W_0m_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_laser)
    assert metadata["source-settings"]["excitation source"] == "laser"


def test_metadata_from_name_settings_recognizes_set_power():
    filename_with_laser = "sample_loc_id_meas-type_0W_0m_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_laser)
    assert (
        isinstance(metadata["source-settings"]["set power (W)"], numbers.Number) is True
    )


def test_metadata_from_name_settings_recognizes_wavelength():
    filename_with_laser = "sample_loc_id_meas-type_0W_0m_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_laser)
    assert (
        isinstance(metadata["source-settings"]["wavelength (m)"], numbers.Number)
        is True
    )


def test_metadata_from_name_settings_recognizes_LED():
    filename_with_LED = (
        "sample_loc_id_meas-type_LED-details_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_LED)
    assert metadata["source-settings"]["excitation source"] == "LED"


def test_metadata_from_name_settings_recognizes_LED_details():
    filename_with_LED = (
        "sample_loc_id_meas-type_LED-details_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_LED)
    assert metadata["source-settings"]["LED details"] == "details"


def test_metadata_from_name_settings_recognizes_filter():
    filename_with_filter = (
        "sample_loc_id_meas-type_f-filter_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_filter)
    assert metadata["source-settings"]["filter"] == "filter"


def test_metadata_from_name_settings_recognizes_objective():
    filename_with_objective = (
        "sample_loc_id_meas-type_obj-objective_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_objective)
    assert metadata["source-settings"]["objective"] == "objective"


def test_metadata_from_name_settings_recognizes_exposure():
    filename_with_exposure = "sample_loc_id_meas-type_0s_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_exposure)
    assert (
        isinstance(metadata["source-settings"]["exposure time (s)"], numbers.Number)
        is True
    )


def test_metadata_from_name_settings_recognizes_generic_fields():
    filename_with_generic_fields = (
        "sample_loc_id_meas-type_genericfield_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_generic_fields)
    assert metadata["source-settings"] == {"other": "genericfield"}


def test_metadata_from_name_settings_recognizes_new_fields():
    filename_with_new_fields = (
        "sample_loc_id_meas-type_new-field_date_measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_new_fields)
    assert metadata["source-settings"] == {"new": "field"}


def test_metadata_from_name_settings_not_present():
    filename_with_no_settings = "sample_loc_id_meas-type_date_measurement-number.ext"
    metadata = metadata_from_name(filename_with_no_settings)
    assert metadata["source-settings"] == {}


# Datetime tests (these tests assume that the user is in central time when running)


def test_metadata_from_name_datetime_is_date_only_no_dashes():
    # YYYYmmdd
    date_no_dashes = "sample_loc_id_meas-type_19991231_measurement-number.ext"
    metadata = metadata_from_name(date_no_dashes)
    assert metadata["datetime"] == "1999-12-31T00:00:00-06:00"


def test_metadata_from_name_datetime_is_date_time():
    # YYYYmmdd-HHMM
    datetime = "sample_loc_id_meas-type_19991231-0723_measurement-number.ext"
    metadata = metadata_from_name(datetime)
    assert metadata["datetime"] == "1999-12-31T07:23:00-06:00"


def test_metadata_from_name_datetime_is_date_time_with_seconds():
    # YYYYmmdd-HHMMSS
    datetime_with_seconds = (
        "sample_loc_id_meas-type_19991231-072346_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_with_seconds)
    assert metadata["datetime"] == "1999-12-31T07:23:46-06:00"


def test_metadata_from_name_datetime_is_datetime_with_neg_timezone():
    # YYYYmmdd-HHMMSS-z
    datetime_ISO8601_with_z_neg = (
        "sample_loc_id_meas-type_19991231-072346-05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_z_neg)
    assert metadata["datetime"] == "1999-12-31T07:23:46-05:00"


def test_metadata_from_name_datetime_is_datetime_with_pos_timezone():
    # YYYYmmdd-HHMMSS+z
    datetime_ISO8601_with_z_pos = (
        "sample_loc_id_meas-type_19991231-072346+05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_z_pos)
    assert metadata["datetime"] == "1999-12-31T07:23:46+05:00"


def test_metadata_from_name_datetime_is_date_only_with_dashes():
    # YYYY-mm-dd
    date_with_dashes = "sample_loc_id_meas-type_1999-12-31_measurement-number.ext"
    metadata = metadata_from_name(date_with_dashes)
    assert metadata["datetime"] == "1999-12-31T00:00:00-06:00"


def test_metadata_from_name_datetime_is_date_time_with_seconds():
    # YYYY-mm-dd-HH-MM
    datetime_with_seconds = (
        "sample_loc_id_meas-type_1999-12-31-07-23_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_with_seconds)
    assert metadata["datetime"] == "1999-12-31T07:23:46-06:00"


def test_metadata_from_name_datetime_is_date_time_with_seconds():
    # YYYY-mm-dd-HH-MM-SS
    datetime_with_seconds = (
        "sample_loc_id_meas-type_1999-12-31-07-23-46_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_with_seconds)
    assert metadata["datetime"] == "1999-12-31T07:23:46-06:00"


def test_metadata_from_name_datetime_is_datetime_with_dash():
    # YYYY-mm-dd-HH:MM
    datetime_ISO8601_with_dash = (
        "sample_loc_id_meas-type_1999-12-31-07:23_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_dash)
    assert metadata["datetime"] == "1999-12-31T07:23:46-06:00"


def test_metadata_from_name_datetime_is_datetime_with_dash():
    # YYYY-mm-dd-HH:MM
    datetime_ISO8601_with_dash = (
        "sample_loc_id_meas-type_1999-12-31-07:23_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_dash)
    assert metadata["datetime"] == "1999-12-31T07:23:00-06:00"


def test_metadata_from_name_datetime_is_datetime_with_dash_and_neg_timezone():
    # YYYY-mm-dd-HH:MM:SSz
    datetime_ISO8601_with_dash_and_z_neg = (
        "sample_loc_id_meas-type_1999-12-31-07:23:46-05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_dash_and_z_neg)
    assert metadata["datetime"] == "1999-12-31T07:23:46-05:00"


def test_metadata_from_name_datetime_is_datetime_with_dash_and_pos_timezone():
    # YYYY-mm-dd-HH:MM:SSz
    datetime_ISO8601_with_dash_and_z_pos = (
        "sample_loc_id_meas-type_1999-12-31-07:23:46+05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_dash_and_z_pos)
    assert metadata["datetime"] == "1999-12-31T07:23:46+05:00"


def test_metadata_from_name_datetime_is_datetime_with_some_dash_and_neg_timezone():
    # YYYY-mm-dd-HHMMSS-z
    datetime_ISO8601_with_some_dash_and_z_neg = (
        "sample_loc_id_meas-type_1999-12-31-072346-05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_some_dash_and_z_neg)
    assert metadata["datetime"] == "1999-12-31T07:23:46-05:00"


def test_metadata_from_name_datetime_is_datetime_with_some_dash_and_pos_timezone():
    # YYYY-mm-dd-HHMMSS+z
    datetime_ISO8601_with_some_dash_and_z_pos = (
        "sample_loc_id_meas-type_1999-12-31-072346+05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_some_dash_and_z_pos)
    assert metadata["datetime"] == "1999-12-31T07:23:46+05:00"


def test_metadata_from_name_datetime_is_datetime_with_space():
    # YYYY-mm-dd HH:MM:SS
    datetime_ISO8601_with_space = (
        "sample_loc_id_meas-type_1999-12-31 07:23:46_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_space)
    assert metadata["datetime"] == "1999-12-31T07:23:46-06:00"


def test_metadata_from_name_datetime_is_datetime_with_space_and_neg_timezone():
    # YYYY-mm-dd HH:MM:SSz
    datetime_ISO8601_with_space_and_z_neg = (
        "sample_loc_id_meas-type_1999-12-31 07:23:46-05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_space_and_z_neg)
    assert metadata["datetime"] == "1999-12-31T07:23:46-05:00"


def test_metadata_from_name_datetime_is_datetime_with_space_and_pos_timezone():
    # YYYY-mm-dd HH:MM:SSz
    datetime_ISO8601_with_space_and_z_pos = (
        "sample_loc_id_meas-type_1999-12-31 07:23:46+05:00_measurement-number.ext"
    )
    metadata = metadata_from_name(datetime_ISO8601_with_space_and_z_pos)
    assert metadata["datetime"] == "1999-12-31T07:23:46+05:00"


def test_metadata_from_name_file_includes_double_underscores():
    filename_with_double_underscores = (
        "sample_loc_id_meas-type_settings__19991231__measurement-number.ext"
    )
    metadata = metadata_from_name(filename_with_double_underscores)
    assert metadata["datetime"] == "1999-12-31T00:00:00-06:00"
