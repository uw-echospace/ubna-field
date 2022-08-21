import summarize_call_detection
from pathlib import Path
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Search arguments for DATE and SD_CARD#
parser.add_argument('-DATE', type=str, required=True)
parser.add_argument('-SD', type=str, required=True)

# Parse the argument
args = parser.parse_args()

# Get the required parameters
recover_folder = f"recover-{args.DATE}-{args.SD}-detect"
# detection_dir is the recover-DATE-UNIT_NUM-detect folder where our detections are.
detection_dir = f"notebooks/detections"

field_records = summarize_call_detection.get_field_records(Path("notebooks/ubna_2022b.csv"))
site_name = summarize_call_detection.get_site_name(field_records, args.DATE, args.SD)
print(f"Looking at data from {site_name}...")

df = summarize_call_detection.generate_df(f"{detection_dir}/{recover_folder}")

summarize_call_detection.plot_total(df, site_name)