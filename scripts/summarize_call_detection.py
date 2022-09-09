from pathlib import Path
import site

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import time

def read_detection(detection_dir, recording_name, det_type):
    """Finds a .txt RavenLite/Pro selection table matching the given arguments
     and reads it in as a Pandas DataFrame.
    
    Parameters
    ------------
    detection_dir : `str`
        - The folder where the detection tables corresponding to a date and SD card are stored.
        - Folder naming format: "recover-DATE-UNIT_NUM-detect"
    recording_name : `str`
        - The name of the recording whose detection table will be read by this function.
        - Recording name format: "DATE_TIME.WAV"
    det_type : `str`
        - The type of detections that will be read.
        - Can either be 'lf' or 'hf'

    Returns
    ------------
    df_detection : `pandas.DataFrame`
        - DataFrame detection table corresponding to the given recover folder, date, and time.
        - Table mainly provides information on how many calls were detected by RavenPro
        - in the recording period.
    """
    
    file_name = f"{det_type}_{recording_name}.txt"
    file_path = f"{detection_dir}/{file_name}"
    
    if (Path(file_path).is_file()):
        df_detection = pd.read_csv(file_path, sep='\t')
    else:
        print(f"{file_path} is empty")
        df_detection = pd.DataFrame()
            
    return df_detection


def generate_df(detection_dir, audio_dur=[0, 29, 55]):
    """Given a folder of detection tables, this function assembles a pandas.DataFrame 
    object of the of LF/HF RavenPro detections for each recording time period to produce a 
    # table of activity throughout the AudioMoth deployment session.
    
    Parameters
    ------------
    detection_dir : `str`
        - The folder where the detection tables corresponding to a date and SD card are stored.
        - Folder naming format: "recover-DATE-UNIT_NUM-detect"
    audio_dur : `list` [`int`], optional
        - The length of each AudioMoth recording as configured. As default, 29min and 55secs.
        - Passed in as a list of `int` objects representing [HH, MM, SS].

    Returns
    ------------
    df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A table of columns: File Names, Date, Start Time (UTC), End Time (UTC), # of LF and HF detections.
        - File Names are `str` objects corresponding to recordings formatted as "DATE_TIME.WAV".
        - Date are `datetime.datetime` objects corresponding to the date of each recording.
        - Start Time (UTC) are `datetime.time` objects in UTC format corresponding to the 
        - start times of each recording.
        - End Time (UTC) are `datetime.time` objects in UTC format corresponding to the 
        - end times of each recording.
        - # of LF/HF detections are `int` objects that represent the # of call detections 
        - of the respective type in each recording.
    """

    # Construct path object linked to the directory of files for datetime-parsing
    file_dir = Path(detection_dir)
    # We use this to only extract the original file names of the recordings.
    # The detection files will be assembled below.
    sorted_files = sorted(file_dir.glob('hf_*.txt'))

    # Create empty DataFrame object with all the required columns    
    df = pd.DataFrame(columns=["File Names", "Date", "Start Time (UTC)",
                       "End Time (UTC)", "# of LF detections", "# of HF detections"])
    
    # Iterate through all file paths to extract and store table information for each file
    for i, file in enumerate(sorted_files):
        # Extract name of each file as it is
        file_name = file.name
        # Extracting the datetime object from the name of each file
        file_info = dt.strptime(file_name, "hf_%Y%m%d_%H%M%S.WAV.txt")

        # Extract recording name, date, start time, and end time for each file
        recording_name = file_info.strftime("%Y%m%d_%H%M%S.WAV")
        date = file_info.date()
        s_time = file_info.time()
        e_time = (file_info + td(minutes=(audio_dur[1]-(file_info.minute%30)), seconds=(audio_dur[2]-file_info.second))).time()

        # Calling read_detection to return the table of selections as a dataframe
        # The detections appear twice: in waveform view and spectrogram view, 
        # so we half the total number of detections
        lf_file_detections = read_detection(detection_dir, recording_name, "lf")
        num_lf_detections = lf_file_detections.shape[0]/2
        hf_file_detections = read_detection(detection_dir, recording_name, 'hf')
        num_hf_detections = hf_file_detections.shape[0]/2
        
        # Add new row with the extracted information
        df.loc[len(df.index)] = [recording_name, date, s_time, e_time, num_lf_detections, num_hf_detections]
    
    return df


def generate_all_df_from_site(field_records, site_name, detection_dir):
    """Given the deployment field records and a desired location to look into, this function looks
    into the folder where all detection folders are stored to construct a DataFrame table of all actvity 
    detected from that location .
    
    Parameters
    ------------
    field_records : `pandas.DataFrame`
        - These deployment field records are updated with every deployment made in the field.
        - Converted from .md file stored as `repo_root_level/field_records/ubna_2022b.md`
    site_name : `str`
        - The location that this function will use to select its detection folders to generate tables from.
    detection_dir : `str`
        - The generate folder location where all detection folders are stored for all locations and dates.

    Returns
    ------------
    `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - An assembled DataFrame table made from smaller DataFrame tables to represent the total detected activity
        - from the given location.
        - Smaller DataFrame tables follow the same structure as the ones produced by generate_df()
    """

    cond3 = field_records["Site"]==site_name
    df_site = field_records[cond3]
    dfs = []

    for index, row in df_site.iterrows():
        folder_name = row["Upload folder name"]
        sd_card = row["SD card #"]
        recover_folder = f"{folder_name}-{sd_card:03}-detect" 

        if (folder_name!="UPLOAD_FOLDER"):
            df = generate_df(f"{detection_dir}/{recover_folder}")
            dfs.append(df)

    return pd.concat(dfs)


def pad_day_of_df(day_df, date):
    """Pad DataFrame tables with 0 LF/HF detections when recordings from that time slot do not exist in given data library.

    Parameters
    ------------
    day_df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all data gathered from a date.
    date : `datetime.date`
        - The date that the DataFrame table corresponds to

    Returns
    ------------
    day_df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - If day_df originally had missing time slots as an effect of the recorder either stopping before 24:00 
        - or starting after 00:00, day_df will now be padded with rows representing data from the missing time slots.
        - The # of LF and HF detections in these padded time slots will be None type objects.
    """

    # Create empty DataFrame object with all the required columns    
    left_pad_df = pd.DataFrame(columns=["File Names", "Date", "Start Time (UTC)",
                   "End Time (UTC)", "# of LF detections", "# of HF detections"])
    
    # Create empty DataFrame object with all the required columns    
    right_pad_df = pd.DataFrame(columns=["File Names", "Date", "Start Time (UTC)",
                   "End Time (UTC)", "# of LF detections", "# of HF detections"])

    # This section builds a dataframe of empty values from 0:00 to the first time of the recordings.
    # This way we can make each plot comparable on the left edge.
    # We insert this dataframe in the beginning of day_df.
    s_time = day_df["Start Time (UTC)"].iloc[0]
    st_row = time(0, 0, 0)
    while (st_row < s_time):
        file_info = dt.combine(date, st_row)
        recording_name = file_info.strftime("%Y%m%d_%H%M%S.WAV")
        e_time = (file_info+td(minutes=29, seconds=55)).time()
        left_pad_df.loc[len(left_pad_df.index)] = [recording_name, date, st_row, e_time, None, None]
        st_row = (file_info+td(minutes=30)).time()
    
    day_df = pd.concat([left_pad_df, day_df])
    
    # This section builds a dataframe of empty values from the end time of the recordings to 24:00.
    # This way we can make each plot comparable on the right edge.
    # We insert this dataframe at the end of day_df.
    st_row = day_df["Start Time (UTC)"].iloc[-1]
    e_time = time(23, 30, 0)
    while (st_row < e_time):
        file_info = dt.combine(date, st_row)
        recording_name = file_info.strftime("%Y%m%d_%H%M%S.WAV")
        et_row = (file_info+td(minutes=29, seconds=55)).time()
        st_row = (file_info+td(minutes=30)).time()
        right_pad_df.loc[len(right_pad_df.index)] = [recording_name, date, st_row, et_row, None, None]
        
    day_df = pd.concat([day_df, right_pad_df])
    
    return day_df


def plot_separate(df, site, save=False, save_folder="../results/raven_energy_detector_raw/call_num_summary/default/FIGS"):
    """Plots separate bar graph plots, # of LF/HF detections vs. Start Time (UTC), for each date in a given deployment session.

    Parameters
    ------------
    df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all detection data gathered from the recording of a deployment session.
        - Consists of [File Names, Date, Start Time (UTC), End Time (UTC), # of LF detections, # of HF detections].
    site : `str`
        - The location where the recordings were gathered from.
    save : `bool`, optional
        - Flag for whether user wants to save plots or not.
        - This is False by default
    save_folder : `str`, optional
        - File path for folder under which the individual date plots will be saved.
        - By default, this will go under `../results/raven_energy_detector_raw/call_num_summary/default/FIGS`
    """

    # To plot each day's activity separately, group by rows that have the same date
    # We need a list of unique dates from our detection files
    unique_dates = df["Date"].unique()
    
    # We plot for each date in our unique dates
    for date in unique_dates:
        day_df = df.loc[df['Date'] == date]
        
        day_df = pad_day_of_df(day_df, date)
        
        fig = day_df.plot.bar(x="Start Time (UTC)", figsize=(12, 4), fontsize=12, rot=60)
        fig.set_xlabel("Start Time (UTC)", fontsize=14)
        fig.set_ylabel("# of LF/HF detections", fontsize=14)
        fig.set_title(f"{date} in {site}", fontsize=14)
        fig.set_xticks(fig.get_xticks())
        fig.set_ylim([0, 1.1*max(df["# of LF detections"].max(), df["# of HF detections"].max())])
        plt.show()
        
        # If the user wants to save, it goes into the below path
        if save:
            save_dir = Path(save_folder)
            save_dir.mkdir(parents=True, exist_ok=True)
            save_path = Path(f"{save_folder}/{date}.png")
            fig.get_figure().savefig(save_path, facecolor='w', bbox_inches = "tight")


def plot_total(df, site, save=False, save_folder=f"../results/raven_energy_detector_raw/call_num_summary/default"):
    """Plots one full bar graph plot, # of LF/HF detections vs. Start Time (UTC)

    Parameters
    ------------
    df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all detection data gathered from the recording of a deployment session.
        - Consists of [File Names, Date, Start Time (UTC), End Time (UTC), # of LF detections, # of HF detections].
    site : `str`
        - The location where the recordings were gathered from.
    save : `bool`, optional
        - Flag for whether user wants to save plots or not.
        - This is False by default
    save_folder : `str`, optional
        - File path for folder under which the individual date plots will be saved.
        - By default, this will go under `../results/raven_energy_detector_raw/call_num_summary/default`
    """

    # To plot each day's activity separately, group by rows that have the same date
    # We need a list of unique dates from our detection files
    unique_dates = df["Date"].unique()
    
    fig = df.plot.bar(x="Start Time (UTC)", figsize=(12, 4), fontsize=12, rot=60)
    fig.set_xlabel("Start Time (UTC)", fontsize=14)
    fig.set_ylabel("# of LF/HF detections", fontsize=14)
    fig.set_title(f"Activity from {unique_dates[0]} to {unique_dates[-1]} in {site}", fontsize=14)
    fig.set_xticks(fig.get_xticks()[::len(unique_dates)])
    fig.set_ylim([0, 1.1*max(df["# of LF detections"].max(), df["# of HF detections"].max())])
    plt.show()
    
    # If the user wants to save, it goes into the below path
    if save:
        save_dir = Path(save_folder)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = Path(f"{save_folder}/activity.png")
        fig.get_figure().savefig(save_path, facecolor='w', bbox_inches = "tight")


def plot_matrix(df, site, type):
    """Plots a colormap activity grid where each column represents a date, each row represents a time, 
    and each cell value represents the # of detections of the given type of call.

    Parameters
    ------------
    df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all detection data gathered from the recording of a deployment session.
        - Consists of [File Names, Date, Start Time (UTC), End Time (UTC), # of LF detections, # of HF detections].
    site : `str`
        - The location where the recordings were gathered from.
    type : `str`
        - Parameter for which type of call activity the user wants to look at
        - Can either be "LF" or "HF".
    """

    plt.figure(figsize=(8, 8))
    
    # Cuts out the time columns from the dataframe to only show the cell values
    plt.imshow(df.to_numpy()[:,2:].astype("float64"))
    plt.title(f"{type} Activity from {site}", fontsize=14)
    plt.ylabel("Start Time of Recording (UTC)", fontsize=14)
    plt.xlabel("Date of Recording (YYYY-MM-DD)", fontsize=14)

    # Set the x and y axis according to the date and time columns of the DataFrame respectively
    plt.yticks(np.arange(0, df.shape[0], 2), df["Start (UTC)"][::2])
    plt.xticks(np.arange(0, df.shape[1]-2), df.columns[2:], rotation = 90)
    plt.colorbar()
    plt.show()


# Extracts field records from the current directory. Converts .csv to dataframe.
# Returns the dataframe

def get_field_records(path_to_records):
    """Extracts .csv field records from given path and converts it to DataFrame object.

    Parameters
    ------------
    path_to_records : `pathlib.Path`
        - Path to the location of .csv file field records

    Returns
    ------------
    fr : `pandas.DataFrame`
        - DataFrame table that matches the information in the .md file 
        - stored as `repo_root_level/field_records/ubna_2022b.md`
    """

    if (path_to_records.is_file()):
        fr = pd.read_csv(path_to_records, sep=',') 

    return fr


# Given:
# 1) DataFrame of field records
# 2) Specific date that exists in field records
# 3) SD Card # that was deployed on that date

# Returns:
# Location where SD card was deployed on that date in the field records

def get_site_name(fr, DATE, SD_CARD_NUM):
    cond1 = fr["Upload folder name"]==f"recover-{DATE}"
    cond2 =  fr["SD card #"]==int(SD_CARD_NUM)
    site = fr.loc[cond1&cond2, "Site"]
    
    if (site.empty):
        site_name = "(Site not found in Field Records)"
    else:
        site_name = site.item()
    
    return site_name


# Given:
# 1) A dataframe of recordings such as the ones generated from generate_df() or generate_df_from_site()
# 2) A type of call to focus on to fill the matrix with
# 3) A constant audio_dur corresponding to the AudioMoth's configurated recording duration per recording

# Returns:
# A matrix where each row is a time period, each column is a date, and each value is the # of detections
# of the given call type
# - Note: The first two columns are Start Time (UTC) and End Time (UTC) resepectively. 
#         This was done to better insert detection data.

def generate_dtype_matrix_from_df(df, dtype, audio_dur=[0, 29, 55]):
    # Create empty DataFrame object with all the required columns    
    time_df = pd.DataFrame(columns=["Start (UTC)", "End (UTC)"])

    # By the end of this loop, time_df will be a dataframe with time rows from 00:00 to 23:30 
    # corresponding to all AudioMoth recordings
    time_row = time()
    # Since there are guaranteed 48 values from 00:00 to 23:30 every 00:30, this part is hard-coded
    for i in range(48):
        # Create an end time using a datetime operations
        file_info = dt.combine(dt.now(), time_row)
        # The computation here always rounds up start time to either 29min 55secs or 59min 55secs
        e_time = (file_info + td(minutes=(audio_dur[1]-(file_info.minute%30)), seconds=(audio_dur[2]-file_info.second))).time()

        # Add new row with the extracted information: "Start (UTC)" is time_row and "End (UTC)" is e_time
        time_df.loc[len(time_df.index)] = [time_row, e_time]

        # Increase time_row by 30 minutes because AudioMoth recording/sleep sessions are 30min long
        time_row = (file_info+td(minutes=30)).time()

    # Gather a list of all unique dates from DataFrame
    unique_dates = df["Date"].unique()

    # This loop will populate time_df with new columns where each columns will represent a day's detections from 00:00 to 23:30
    for date in unique_dates:
        # Get the DataFrame corresponding to each date
        day_df = df.loc[df["Date"]==date]

        # Create an empty DataFrame column for that date which we will populate
        dets = pd.DataFrame(columns=[date])
        # By the end of this loop, dets will be populated where there is data.
        for e_time in time_df["End (UTC)"]:
            # We use the fact that end times in our correct time_df DataFrame must exist in our day_df DataFrame
            sr = day_df.loc[day_df["End Time (UTC)"]==e_time][f"# of {dtype} detections"]
            # If the end time does not exist, that recording's detections does not exist in our day_df DataFrame
            # This allows us to check for NaN cases and skip over those rows to insert the right data in the right location
            if (sr.empty):
                dets.loc[len(dets.index)] = float('nan')
            else:
                dets.loc[len(dets.index)] = sr.iloc[0]

        # Create a new column in time_df and assign dets to it
        time_df[date] = dets
    
    return time_df