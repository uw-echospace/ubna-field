# Automated detection protocol

#### These are instructions for running batdetect2 using the bat-detector-msds pipeline on recovered nighttime recordings

## Pre-steps:

- Fork `aditya-uw/bat-detector-msds` to access the batdetect2-pipeline branch in that repository.
  - This is where the bash script that runs the pipeline is stored.
- Download the forked repository with `git clone (your forked repository)` on the Linux machine with the mounted UBNA hard drives.
- Follow the forked repository's README.md instructions about `pip install -r requirements.txt` and updating the submodule.
  - It is ideal to install requirements and dependencies in a virtual environment with python=3.x.

## Pipeline steps:
1) Open the cloned repository with `cd ~/bat-detector-msds`
2) Use the field records to find where your recovered nighttime recorder data has been uploaded. For example, `/mnt/ubna_data_02/recover-20230609/UBNA_012`
3) Use the command: `nohup sh scripts/pipeline_for_recovered_deployments.sh "/mnt/ubna_data_02/recover-20230609" "UBNA_012" "true" "true" &`
   - `nohup (command) &` will keep the pipeline running regardless of ssh connection and write the output into a nohup.out file. This file will be stored amidst the files in bat-detector-msds
   - `sh scripts/pipeline_for_recovered_deployments.sh` runs the bash script that runs the detection pipeline. It takes 4 arguments:
      - Upload folder path: `/mnt/ubna_data_02/recover-20230609`
      - Nighttime SD card name: `UBNA_012`
      - String “boolean” whether detector should be run: “true”
      - String “boolean” whether summary figure should be generated: “true”
         - The reason for the booleans is because generating detections is only a 1-time operation but generating figures can be needed multiple times to update figure format using the detections.csv.
4) The detections.csv and figures are saved into `bat-detector-msds/output_dir/recover-DATE/SD_UNIT` .
   - The naming conventions of each file will remember recover-DATE and SD_UNIT to trace back to where the data came from.


### Slight modifications to pipeline:
Deleting segments after detections have been generated for all files recovered.
