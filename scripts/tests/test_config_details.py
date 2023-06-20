import pytest
from io import TextIOWrapper
import json

ALLDAY_PATH = "ConfigurationDetails/2023_BirdAudio48kHz_allday.config"
NIGHT_PATH = "ConfigurationDetails/2023_BatAudio192kHz_night.config"

@pytest.fixture(scope="function", autouse=True)
def config_allday_file_fixture() -> TextIOWrapper:
    """
    Grabs All Day file config.
    """
    text_file_path = ALLDAY_PATH
    file = open(text_file_path, 'r', encoding='utf-8')
    return file

@pytest.fixture(scope="function", autouse=True)
def config_night_file_fixture() -> TextIOWrapper:
    """
    Grabs Night file config.
    """
    text_file_path = NIGHT_PATH
    file = open(text_file_path, 'r', encoding='utf-8')
    return file

@pytest.mark.config
def test_naive_allday(config_allday_file_fixture: TextIOWrapper) -> None:
    """
    Naively checks All Day Configuration File for proper values.
    """
    expected_allday_values = [[{'startMins': 0, 'endMins': 1440}], True, True, True, 48000, 2, 1795, 5, False, False, False,
          True, False, 'none', 0, 0, False, 0.001, 0, False, 64, 12000, 0, 0.001, False, False, False,
          'percentage', '1.8.0', False, False, False, False, False]
    data = json.load(config_allday_file_fixture)
    for key_index, key in enumerate(data):
        assert expected_allday_values[key_index] == data[key]

@pytest.mark.config
def test_naive_night(config_night_file_fixture: TextIOWrapper) -> None:
    """
    Naively checks Night Configuration File for proper values.
    """
    expected_night_values = [[{'startMins': 180, 'endMins': 810}], True, True, True, 192000, 2, 1795, 5, False, False, False,
          True, False, 'none', 0, 0, False, 0.001, 0, False, 64, 48000, 0, 0.001, False, False, False,
          'percentage', '1.8.0', False, False, False, False, False]
    data = json.load(config_night_file_fixture)
    for key_index, key in enumerate(data):
        assert expected_night_values[key_index] == data[key]
