import csv
import pytest
from io import TextIOWrapper
from typing import Tuple, Union
from datetime import datetime
import re

PATH = "field_records/ubna_2023.csv"

@pytest.fixture(scope="function", autouse=True)
def csv_file_fixture() -> TextIOWrapper:
    """
    Grabs CSV file object.
    """
    csv_path = PATH
    file = open(csv_path, 'r', encoding='utf-8')
    return file

@pytest.mark.csv
def test_csv_dimensions(csv_file_fixture: TextIOWrapper) -> None:
    """
    Tests CSV dimensions.
    """

    def count_rows_and_columns(csv_file: TextIOWrapper) -> Tuple[Union[int, float]]:
        """
        Counts rows and dimensions of CSV.
        """
        reader = csv.reader(csv_file)
        header = next(reader)
        num_columns = len(header)
        num_rows = sum(1 for _ in reader)
        return num_columns, num_rows
    
    num_columns, num_rows = count_rows_and_columns(csv_file_fixture)
    assert num_columns == 18, "The CSV file does not have 18 columns."
    assert num_rows % 6 == 0, "The number of rows in the CSV file is not a multiple of 6."

@pytest.mark.csv
def test_check_spaces(csv_file_fixture: TextIOWrapper) -> None:
    """
    Checks if entries begin and end with a single space. Fence cases are first column, 
    that should not start with a space, and the last column, that should not end with a space.
    """
    reader = csv.reader(csv_file_fixture)
    for row_index, row in enumerate(reader):
        if row_index != 0:
            for entry_index, entry in enumerate(row):
                if entry_index == 0:
                    assert not entry.startswith(' ') and not entry.startswith('  '), f"Entry '{entry}' does not start with a single space."
                    assert entry.endswith(' ') and not entry.endswith('  '), f"Entry '{entry}' does not end with a single space."
                elif entry_index == 17:
                    assert entry.startswith(' ') and not entry.startswith('  '), f"Entry '{entry}' does not start with a single space."
                    assert not entry.endswith(' ') and not entry.endswith('  '), f"Entry '{entry}' does not end with a single space."
                else:
                    assert entry.startswith(' ') and not entry.startswith('  '), f"Entry '{entry}' does not start with a single space."
                    assert entry.endswith(' ') and not entry.endswith('  '), f"Entry '{entry}' does not end with a single space."

@pytest.mark.csv
def test_check_columns(csv_file_fixture: TextIOWrapper) -> None:
    """
    Checks format of each individual column.
    """

    def is_valid_unknown_value_format(entry: str) -> bool:
        """
        Checks if entry is in unknown value format.
        """
        unknown_format_regex = r'^\([A-Za-z]+\-[A-Za-z]+\)$|^\([A-Za-z]+\w+\)$'
        return bool(re.match(unknown_format_regex, entry))

    def is_datetime_format(entry: str) -> bool:
        """
        Checks if string is in ISO8601 format.
        """
        datetime_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        return bool(re.match(datetime_regex, entry))
    
    def is_valid_audiomoth_label(entry: str) -> bool:
        """
        Checks if string is valid AudioMoth Label.
        """
        valid_strings = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        return entry in valid_strings
    
    def is_valid_sd_card(entry: str) -> bool:
        """
        Checks if string is valid SD card.
        """
        regex_pattern = r'^(0\d{2}|[1-9]\d{2})$'
        return re.match(regex_pattern, entry) is not None
    
    def is_valid_location(entry: str) -> bool:
        """
        Checks if string is valid location.
        """
        valid_strings = ['Telephone Field', 'Foliage', 'Central Pond']
        return entry in valid_strings
    
    def is_valid_latitude(entry: str) -> bool:
        """
        Checks if string is valid latitude.
        """
        regex_pattern = r'^\d{1,2}° \d{1,2}\' \d{1,2}\.\d{3}\'\' [NS]$'
        return re.match(regex_pattern, entry) is not None

    def is_valid_longitude(entry: str) -> bool:
        """
        Checks if string is valid longitude.
        """
        regex_pattern = r'^\d{1,3}° \d{1,2}\' \d{1,2}\.\d{3}\'\' [EW]$'
        return re.match(regex_pattern, entry) is not None
    
    def is_valid_battery_start(entry: str) -> bool:
        """
        Checks if string is valid battery start voltage.
        """
        regex_pattern = r'^(3|4)\.\d{3}$'
        return re.match(regex_pattern, str(entry)) is not None

    def is_valid_battery_end(entry: str) -> bool:
        """
        Checks if string is valid battery end voltage.
        """
        regex_pattern = r'^(3|4)\.\d{3}$'
        return re.match(regex_pattern, str(entry)) is not None

    def is_valid_person(entry: str) -> bool:
        """
        Checks if string is valid initials of valid deployer, scribe, and uploader.
        """
        valid_strings = ['AK', 'MB', 'WL', 'CT', 'YC']
        return entry in valid_strings
    
    def is_valid_recovery_date(entry: str) -> bool:
        """
        Checks if string is of valid recovery-date.
        """
        regex_pattern = r'^recover-(\d{8})$'
        match = re.match(regex_pattern, entry)
        if match:
            date_str = match.group(1)
            try:
                datetime.strptime(date_str, '%Y%m%d')
                return True
            except ValueError:
                return False
        return False

    def is_valid_notes(entry: str) -> bool:
        """
        Checks if string is valid notes. Valid notes must contain the following pattern, but other text may
        also be included.
        """
        regex_pattern = r'(Panasonic|Ikea) Batteries (Daytime|Nighttime) (0:00-24:00|3:00-13:30) UTC'
        if len(re.findall(regex_pattern, entry)) == 1:
            return True
        else:
            return False

    reader = csv.reader(csv_file_fixture)
    for row_index, row in enumerate(reader):
        if row_index != 0:
            for entry_index, entry in enumerate(row):
                entry = entry.strip()
                if entry_index == 0 or entry_index == 1:
                    assert is_datetime_format(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not in proper datetime format. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 2:
                    assert is_valid_audiomoth_label(entry),\
                    f"String {entry} is not valid AudioMoth label. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 3:
                    assert is_valid_sd_card(entry),\
                    f"String {entry} is not valid SD Card label. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 4:
                    assert is_valid_location(entry),\
                    f"String {entry} is not valid location. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 5:
                    assert is_valid_latitude(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not valid location. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 6:
                    assert is_valid_longitude(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not valid longitude. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 7:
                    assert entry == "192000" or entry == "48000",\
                    f"String {entry} is not valid sampling rate. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 8:
                    assert entry == "Medium",\
                    f"String {entry} is not valid gain. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 9:
                    assert entry == "None",\
                    f"String {entry} is not valid filter. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 10:
                    assert entry == "None",\
                    f"String {entry} is not valid amplitude threshold. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 11:
                    assert is_valid_battery_start(entry),\
                    f"String {entry} is not valid battery start voltage. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 12:
                    assert is_valid_battery_end(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not valid battery end voltage. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 13 or entry_index == 14 or entry_index == 15:
                    assert is_valid_person(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not valid initials of person. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 16:
                    assert is_valid_recovery_date(entry) or is_valid_unknown_value_format(entry),\
                    f"String {entry} is not valid recovery date. Failed entry in row {row_index + 1} column {entry_index + 1}."
                if entry_index == 17:
                    assert is_valid_notes(entry),\
                    f"String {entry} is not valid notes. Failed entry in row {row_index + 1} column {entry_index + 1}."