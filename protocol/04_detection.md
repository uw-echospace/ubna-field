# Detection protocol


## Open up the RavenPro application

1. Log into the lab computer
2. Open up terminal on the computer
3. Copy paste the following lines to terminal, hit ENTER after each one and wait for RavenPro's start-up image to appear
    ```bash
    $ cd /opt/RavenPro1.6
    $ ./RavenPro.sh
    ```
    
    
## Viewing a Sound File

1. Open up a sound file on RavenPro by going to File->"Open Sound Files..." in the main menu.
2. Browse for the sound file you want to view using the "Look In:" menu bar.
3. Select the desired sound file you want to view and hit ENTER.
4. You will be taken to a "Configure New Sound Window".
5. Selecting "Open entire sound" will open the entire audio file which may take a while in our case.
6. Selecting "Page sound" will load the audio file in segments that are "page size" long and quicker to load.
7. You may ignore all other options and hit ENTER.
8. RavenPro will generate a waveform view and a spectrogram view.
9. The bottom scroll bar will scroll through the audio while the + and - help you zoom in.
10. The top scroll bar (which only appears if you selected "Page sound") scrolls through the segments.
11. The <- and -> arrows change the audio to the next segment.


## Running the Single-File Detector

1. Once you have a sound opened, open the detector we are using by going to Tools->Detector->"Band Limited Energy Detector" in the main menu.
2. Double-click on "Spectrogram" inside the right dialog box of "Available Signals and Views" and hit OK.
3. You are now configuring your detector to detect what you want. Load in a preset configuration for either LF calls or HF calls by going to Preset in the top menu of this window. Hit OK.
4. RavenPro will open a progress manager dialog box for you to watch the detector's progress.
5. Once the detector is done, you will have a table of entries named "Band Limited Energy Detector".
6. You may click on any of these entries or configure RavenPro to scroll through all of them.
7. If no entries exist, RavenPro could not find any calls that matched our configuration descriptions.


## Running the Batch Detector

1. You do not need to have any audio opened for this.
2. Go to Tools->"Batch Detector..." to open the Batch Detector window.
3. Click on the "Detector:" dialog and select "Band Limited Energy Detector".
4. To add the sound files you want to run your detector on, click on Add. This will open up a browsing window where you can navigate to your recordings.
5. To select multiple recordings. Decide on a starting point and ending point for your recordings. Click on the starting point and then click on the ending point while holding SHIFT on your keyboard. This should automatically select all the recordings in between. Hit ENTER to finalize.
6. The "Configure Detector" dialog will now be activated. Click on it and load in a preset configuration for either LF or HF calls by going to Preset in the top menu of this window. Stay on this window.
7. Go to the "Table" setting below Preset. If you loaded in an LF preset, change File Names to LF<f>.txt. If you loaded in a HF preset, change File Names to HF<f>.txt. Hit OK.
8. You will be taken back to the batch detector window. Hit OK again and the progress manager will pop up to show the detector's progress on all the files you have added in.
9. Once your detector is done, repeat these steps for detecting the other type of call using the other detector preset. The batch detector will remember the files you added in. All you need to change is the detector configuration using "Configure Detector".


## Organizing the Batch Detector's Detections

1. The batch detector stores all of its detection tables in /home/USERNAME/RavenPro1.6/Selections/
2. The detection tables files have the file names that we gave in step 7 of Running the Batch Detector.
3. For organization of these files, the files are categorized into DATE folders and further categorized into folders for LF detections or HF detections. The folder titles are as follows:
 - YYYYMMDD/YYYYMMDD_LFdetections
 - YYYYMMDD/YYYYMMDD_HFdetections
4. For example, all detection tables from recordings in 2022-07-01 will go into a 20220701 folder. All detection tables created with LF presets (distinguished by LF as their first 2 characters) will go into a subfolder inside 20220701 known as 20220701_LFdetections. All detection tables created with HF presets (distinguised by HF as their first 2 characters) will go into a subfolder inside 20220701 known as 20220701_HFdetections.
