# Lab preparation protocol


## Initiate GitHub field record entries

1. Log into GitHub if you are not already logged in
2. Navigate to the project repository [union_bay_bats](https://github.com/uw-echospace/union-bay-bats)
3. Navigate to [field_records/ubna_2023.csv](https://github.com/uw-echospace/union-bay-bats/tree/main/field_records/ubna_2023.csv)
4. Click the pencil button on the upper-right corner of the file view so that you can edit this md file
5. Start a new row in `field_records/ubna_2023.csv` by copy-pasting the template row at the bottom of file (but don't remove the template)


## Prepare AudioMoth units

For each AudioMoth, go through the following so that you partially fill in 1 row on the field datasheet:
1. Fill in today's date
2. Take an AudioMoth unit and record the unit number
3. Insert an SD card into the AudioMoth and record the SD card number
4. Put in fully charged batteries, measure the total voltage from the +/- pins on the board, and record the beginning voltage
5. Connect AudioMoth to the computer, load the pre-saved [audiomoth.config](../ConfigurationDetails/2023_BatAudio192kHz_night.config) file, and click on `Configure AudioMoth`
6. Go through the configured sampling rate (192 kHz), gain (medium), filter (none), and amplitude threshold (none) to make sure all are configured correctly, and record all settings on the field datasheet
7. Disconnect the Audiomoth and switch the Audiomoth to CUSTOM mode briefly. After a few seconds, the Audiomoth’s red LED should start rapidly flashing. This means that it is recording without any errors.
8. Switch it back into USB/OFF mode so that the AudioMoth is in stand-by mode
9. Put AudioMoth in a ziploc bag and make sure the blinking lights are covered with tape


## Commit GitHub field record entries

Once you are done with entering information for all the AudioMoth units you plan to deploy today:
1. Scroll to the bottom and enter a commit message "lab prep" or something makes sense
2. Choose "Create a new branch for this commit and start a pull request"
3. Enter a branch name: `deploy-DATE`, where `DATE` is today's date in YYYYMMDD format
4. Create a Pull Request with title : `deploy-DATE`, just like what you had for the deployment

## Check field kit / gear

Check all items in the field kit:
- Field datasheet
- Spare fully-charged batteries
- Spare re-formatted SD cards
- Utility knife
- Sharpie (thick and thin)
- Electric tape
- Duct tape
- Gear ties
- Ziploc bag
- Bug spray
- Wader / boots

