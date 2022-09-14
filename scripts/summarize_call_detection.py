from pathlib import Path
import site

import pandas as pd

import matplotlib.pyplot as plt
import numpy as np

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import time

def read_detection(detection_dir, recording_name, call_type):
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
    call_type : `str`
        - The type of detections that will be read.
        - Can either be 'lf' or 'hf'

    Returns
    ------------
    df_detection : `pandas.DataFrame`
        - DataFrame detection table corresponding to the given recover folder, date, and time.
        - Table mainly provides information on how many calls were detected by RavenPro
          in the recording period.
    """
    
    file_name = f"{call_type}_{recording_name}.txt"
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
          start times of each recording.
        - End Time (UTC) are `datetime.time` objects in UTC format corresponding to the 
          end times of each recording.
        - # of LF/HF detections are `int` objects that represent the # of call detections 
          of the respective type in each recording.
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


def generate_all_df_from_site(df_fr, site_name, detection_dir):
    """Given the deployment field records and a desired location to look into, this function looks
    into the folder where all detection folders are stored to construct a DataFrame table of all actvity 
    detected from that location .
    
    Parameters
    ------------
    df_fr : `pandas.DataFrame`
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
          from the given location.
        - Smaller DataFrame tables follow the same structure as the ones produced by generate_df()
    """

    cond3 = df_fr["Site"]==site_name
    df_site = df_fr[cond3]
    dfs = []

    for index, row in df_site.iterrows():
        folder_name = row["Upload folder name"]
        sd_card = row["SD card #"]
        recover_folder = f"{folder_name}-{sd_card:03}-detect" 

        if (folder_name!="UPLOAD_FOLDER"):
            df = generate_df(f"{detection_dir}/{recover_folder}")
            dfs.append(df)

    return pd.concat(dfs)


def pad_day_of_df(df_day, date):
    """Pad DataFrame tables with 0 LF/HF detections when recordings from that time slot do not exist in given data library.

    Parameters
    ------------
    df_day : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all data gathered from a date.
    date : `datetime.date`
        - The date that the DataFrame table corresponds to

    Returns
    ------------
    df_day : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - If df_day originally had missing time slots as an effect of the recorder either stopping before 24:00 
          or starting after 00:00, df_day will now be padded with rows representing data from the missing time slots.
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
    # We insert this dataframe in the beginning of df_day.
    s_time = df_day["Start Time (UTC)"].iloc[0]
    st_row = time(0, 0, 0)
    while (st_row < s_time):
        file_info = dt.combine(date, st_row)
        recording_name = file_info.strftime("%Y%m%d_%H%M%S.WAV")
        e_time = (file_info+td(minutes=29, seconds=55)).time()
        left_pad_df.loc[len(left_pad_df.index)] = [recording_name, date, st_row, e_time, None, None]
        st_row = (file_info+td(minutes=30)).time()
    
    df_day = pd.concat([left_pad_df, df_day])
    
    # This section builds a dataframe of empty values from the end time of the recordings to 24:00.
    # This way we can make each plot comparable on the right edge.
    # We insert this dataframe at the end of df_day.
    st_row = df_day["Start Time (UTC)"].iloc[-1]
    e_time = time(23, 30, 0)
    while (st_row < e_time):
        file_info = dt.combine(date, st_row)
        recording_name = file_info.strftime("%Y%m%d_%H%M%S.WAV")
        et_row = (file_info+td(minutes=29, seconds=55)).time()
        st_row = (file_info+td(minutes=30)).time()
        right_pad_df.loc[len(right_pad_df.index)] = [recording_name, date, st_row, et_row, None, None]
        
    df_day = pd.concat([df_day, right_pad_df])
    
    return df_day


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
        df_day = df.loc[df['Date'] == date]
        
        df_day = pad_day_of_df(df_day, date)
        
        fig = df_day.plot.bar(x="Start Time (UTC)", figsize=(12, 4), fontsize=12, rot=60)
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


def plot_matrix(df, site, call_type):
    """Plots a colormap activity grid where each column represents a date, each row represents a time, 
    and each cell value represents the # of detections of the given type of call.

    Parameters
    ------------
    df : `pandas.DataFrame` [`str`, `datetime.date`, `datetime.time`, `datetime.time`, `int`, `int`]
        - A DataFrame table corresponding to all detection data gathered from the recording of a deployment session.
        - Consists of [File Names, Date, Start Time (UTC), End Time (UTC), # of LF detections, # of HF detections].
    site : `str`
        - The location where the recordings were gathered from.
    call_type : `str`
        - Parameter for which type of call activity the user wants to look at
        - Can either be "LF" or "HF", case-sensitive.
    """

    plt.figure(figsize=(8, 8))
    
    # Cuts out the time columns from the dataframe to only show the cell values
    plt.imshow(df.to_numpy()[:,2:].astype("float64"))
    plt.title(f"{call_type} Activity from {site}", fontsize=14)
    plt.ylabel("Start Time of Recording (UTC)", fontsize=14)
    plt.xlabel("Date of Recording (YYYY-MM-DD)", fontsize=14)

    # Set the x and y axis according to the date and time columns of the DataFrame respectively
    plt.yticks(np.arange(0, df.shape[0], 2), df["Start (UTC)"][::2])
    plt.xticks(np.arange(0, df.shape[1]-2), df.columns[2:], rotation = 90)
    plt.colorbar()
    plt.show()


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
        df_fr = pd.read_csv(path_to_records, sep=',') 

    return df_fr


def get_site_name(df_fr, DATE, SD_CARD_NUM):
    """Gets the location where an AudioMoth was deployed at a certain date
    using the deployment field records.

    Parameters
    ------------
    df_fr : `pandas.DataFrame`
        - DataFrame table that matches the information in the .md file 
        - stored as `repo_root_level/field_records/ubna_2022b.md`
    DATE : `str`
        The date when an AudioMoth was deployed
    SD_CARD_NUM : `str`
        The SD card inside the AudioMoth to identify which AudioMoth the user wants.

    Returns
    ------------
    site_name : `str`
        - Name of the location where the Audiomoth was deployed at that date
        according to the field records.
        - If the deployment is not recorded, site_name will be "(Site not found in Field Records)"
    """

    cond1 = df_fr["Upload folder name"]==f"recover-{DATE}"
    cond2 =  df_fr["SD card #"]==int(SD_CARD_NUM)
    site = df_fr.loc[cond1&cond2, "Site"]
    
    if (site.empty):
        site_name = "(Site not found in Field Records)"
    else:
        site_name = site.item()
    
    return site_name


def generate_call_type_matrix_from_df(df, call_type, audio_dur=[0, 29, 55]):
    """This function creates a matrix where each row represents a time slot, 
    each column represents a date in the given session, and each cell holds the # of detections
    for the given type of bat call.
    
    Parameters
    ------------
    df : df : `pandas.DataFrame`
        - A table of columns: File Names, Date, Start Time (UTC), End Time (UTC), # of LF and HF detections.
        - File Names are `str` objects corresponding to recordings formatted as "DATE_TIME.WAV".
        - Date are `datetime.datetime` objects corresponding to the date of each recording.
        - Start Time (UTC) are `datetime.time` objects in UTC format corresponding to the 
          start times of each recording.
        - End Time (UTC) are `datetime.time` objects in UTC format corresponding to the 
          end times of each recording.
        - # of LF/HF detections are `int` objects that represent the # of call detections 
          of the respective type in each recording.
    call_type : `str`
        - The type of calls that we want the matrix's cell values to represent.
        - Can either be "LF" or "HF", case-sensitive
    audio_dur : `list` [`int`], optional
        - The length of each AudioMoth recording as configured. As default, 29min and 55secs.
        - Passed in as a list of `int` objects representing [HH, MM, SS].

    Returns
    ------------
    df_time : `pandas.DataFrame` [[`str`, `str`, `datetime.date`, `datetime.date`, ...], 
                                  [`datetime.time`, `datetime.time`, `int`, `int`, ...], 
                                  [`datetime.time`, `datetime.time`, `int`, `int`, ...], 
                                  ...]
        - A grid of activity across dates and over times.
        - The first row is for headers. This is where the first column says "Start (UTC)"
          and the second column says "End (UTC)". Every column after displays the date
          as a `datetime.date` object for the dates in the given session.
        - All rows after the first row in the first two columns hold the starting time and
          ending time for the recordings as `datetime.time` objects.
        - All cells after the first two columns and the first row are `int` values
          representing the # of detections detected at that time and day of the given type.
    """
    
    # Create empty DataFrame object with all the required columns    
    df_time = pd.DataFrame(columns=["Start (UTC)", "End (UTC)"])

    # By the end of this loop, df_time will be a dataframe with time rows from 00:00 to 23:30 
    # corresponding to all AudioMoth recordings
    time_row = time()
    # Since there are guaranteed 48 values from 00:00 to 23:30 every 00:30, this part is hard-coded
    for i in range(48):
        # Create an end time using a datetime operations
        file_info = dt.combine(dt.now(), time_row)
        # The computation here always rounds up start time to either 29min 55secs or 59min 55secs
        e_time = (file_info + td(minutes=(audio_dur[1]-(file_info.minute%30)), seconds=(audio_dur[2]-file_info.second))).time()

        # Add new row with the extracted information: "Start (UTC)" is time_row and "End (UTC)" is e_time
        df_time.loc[len(df_time.index)] = [time_row, e_time]

        # Increase time_row by 30 minutes because AudioMoth recording/sleep sessions are 30min long
        time_row = (file_info+td(minutes=30)).time()

    # Gather a list of all unique dates from DataFrame
    unique_dates = df["Date"].unique()

    # This loop will populate df_time with new columns where each columns will represent a day's detections from 00:00 to 23:30
    for date in unique_dates:
        # Get the DataFrame corresponding to each date
        df_day = df.loc[df["Date"]==date]

        # Create an empty DataFrame column for that date which we will populate
        dets = pd.DataFrame(columns=[date])
        # By the end of this loop, dets will be populated where there is data.
        for e_time in df_time["End (UTC)"]:
            # We use the fact that end times in our correct df_time DataFrame must exist in our df_day DataFrame
            sr = df_day.loc[df_day["End Time (UTC)"]==e_time][f"# of {call_type} detections"]
            # If the end time does not exist, that recording's detections does not exist in our df_day DataFrame
            # This allows us to check for NaN cases and skip over those rows to insert the right data in the right location
            if (sr.empty):
                dets.loc[len(dets.index)] = float('nan')
            else:
                dets.loc[len(dets.index)] = sr.iloc[0]

        # Create a new column in df_time and assign dets to it
        df_time[date] = dets
    
    return df_time