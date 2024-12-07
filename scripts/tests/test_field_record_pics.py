import pytest
import os
import re
from io import TextIOWrapper
import csv

from scripts.tests.test_field_records import csv_file_fixture

FOLDER_PATH = "field_records/pics/"

@pytest.mark.pics
def test_folder_files_regex_and_extension(csv_file_fixture: TextIOWrapper):
    """
    Tests deployment picture file names.
    """
    def get_all_deployment_dates(csv_file_fixture: TextIOWrapper):
        """
        Gets all deployment dates from ubna_2023.csv.
        """
        reader = csv.reader(csv_file_fixture)
        deployment_dates_reformatted = []
        for row_index, row in enumerate(reader):
            if row_index != 0:
                deployment_date_reformatted = row[0].split("T")[0].replace("-", "")
                deployment_dates_reformatted.append(deployment_date_reformatted)
        # Remove duplicate values
        deployment_dates_reformatted = [*set(deployment_dates_reformatted)]
        return deployment_dates_reformatted

    deployment_dates_reformatted = get_all_deployment_dates(csv_file_fixture)
    folder_path = FOLDER_PATH
    files = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".jpg", ".jpeg")):
            files.append(file_name)

    for deployment_date_reformatted in deployment_dates_reformatted:
        found = False
        regex_pattern = rf"deploy-{deployment_date_reformatted}-audiomoth-(\w+)\.(jpg|jpeg|JPG|JPEG)"
        for file_name in files:
            if re.match(regex_pattern, file_name):
                found = True
        if not found:
            pytest.fail(f"No such file matches the regex pattern {regex_pattern} for the deployment date " f"{deployment_date_reformatted}."

