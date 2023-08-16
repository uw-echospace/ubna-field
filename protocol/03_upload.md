# Data uploading protocol


## Set up data uploading

1. Log into the lab computer
2. Open up terminal on the computer
3. Copy paste the following line to terminal, hit ENTER and make sure files start to transfer
    ```bash
    $ rsync -ahvP /media/USERNAME/UBNA_* /mnt/ubna_data_02/recover-DATE
    ```
    Remember to swap out USERNAME with your actual username and DATE with today's date in YYYYMMDD format (e.g. `recover-20220715`)
4. **Only in specific circumstances**: In the case where Audiomoths were configured prior to the previous deployment, the uploader must check to see if the configuration change actually occured and was recorded properly. Navigate to the folder containing the uploaded data of each newly configured Audiomoth (e.g `/mnt/ubna_data_02/recover-20220715/UBNA_001`) using `cd` commands. In each folder, run the `cat CONFIG.TXT` command, examine the configuration records, and report any discrepencies between the configuration values and the field record data.

## Navigate to GitHub field record

1. Log into GitHub if you are not already logged in
2. Navigate to the project repository [union_bay_bats](https://github.com/uw-echospace/union-bay-bats)
3. Go to the branch you created earlier today with branch name: `deploy-DATE`, where `DATE` is today's date in YYYYMMDD format
3. Navigate to `field_records/ubna_2023.csv` (make sure you are still in the above branch!)
4. Click the pencil button on the upper-right corder of the file view so that you can edit this md file


## Enter information in field datasheet

1. Locate the entries corresponding to the previous deployment (i.e. those that you have just recovered from field)
2. Transcribe the following fields from field datasheet to GitHub:
    - Time recovered (local) of the previous units
3. Measure the total voltage from the +/- pins on the board, and record the ending voltage
4. Record the upload folder name
5. Record the uploader initial


## Add deployment pictures

1. Navigate to the folder `field_records/pics`
2. Name your pic files following the format `deploy-DATE-audiomoth-NUM`, where `DATE` is today's date in YYYYMMDD format and `NUM` is the AudioMoth unit number for the one shown in the picture
3. Upload pictures into `field_records/pics`, by clicking "Add file --> Upload files" on the upper-right corner


## Commit GitHub field record entries

Once you are done with entering information for all the AudioMoth units you just recovered today:
1. Scroll to the bottom and enter a commit message "upload data" or something makes sense


## Tidy things up

1. Put all batteries from the recovered units to charge
2. Double check field kit and replace/refill any needed items
3. Check out with @leewujung or @yjcheong, either in-person or on Slack
