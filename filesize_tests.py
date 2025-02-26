  GNU nano 6.2                                                                                                                                                                                                                                       filesize_tests1.py                                                                                                                                                                                                                                                 
import os
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def extract_timestamp(filename):
    match = re.match(r"(\d{8})_(\d{6})\.WAV", filename, re.IGNORECASE)
    if match:
        date_part, time_part = match.groups()
        return datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
    return None

def get_wav_file_sizes(folder_path):
    file_sizes = []
    timestamps = []
    
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(".wav"):
            timestamp = extract_timestamp(file)
            if timestamp:
                file_path = os.path.join(folder_path, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                timestamps.append(timestamp)
                file_sizes.append(file_size)
    
    return timestamps, file_sizes

def plot_file_sizes(folder_path, timestamps, file_sizes):
    
    # Ensure timestamps are sorted
    timestamps, file_sizes = zip(*sorted(zip(timestamps, file_sizes)))
    plt.figure(figsize=(12, 6))
    plt.scatter(timestamps, file_sizes, label='File Size (MB)', color='b', marker='o')
    plt.plot(timestamps, file_sizes, linestyle='-', alpha=0.6)
    plt.xlabel('Time')
    plt.ylabel('File Size (MB)')
    plt.title(f'WAV File Size Over Time for {os.path.basename(folder_path)} on {timestamps[0]}')
    
    
    
    # Set x-axis range from first date rounded down to the nearest multiple of 6 hours to exactly 2 weeks later
    min_time = timestamps[0].replace(minute=0, second=0, microsecond=0)
    min_time = min_time - timedelta(hours=min_time.hour % 6)  # Round down to nearest multiple of 6 hours
    max_time = min_time + timedelta(weeks=2)
    
    # Generate ticks every 6 hours
    tick_times = []
    current_time = min_time
    while current_time <= max_time:
        tick_times.append(current_time)
        # current_time += timedelta(hours=6)
        current_time += timedelta(days=1)
    
    # Format x-axis labels: show date only at midnight, otherwise show time
    labels = []
    for t in tick_times:
        #if t.hour == 0:
        #    labels.append(t.strftime('%Y-%m-%d'))  # Show year and date at midnight
        #else:
        #    labels.append(t.strftime('%H:%M'))  # Show only time otherwise
        labels.append(t.strftime('%Y-%m-%d'))
    plt.xticks(tick_times, labels, rotation=45)
    
    plt.legend()
    plt.grid()
    
    # Save the plot
    output_filename = os.path.join(os.getcwd(), f"filesizes_{os.path.basename(folder_path)}.png")
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved plot to {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path1> <folder_path2> ...")
        sys.exit(1)
    
    folder_paths = sys.argv[1:]
    
    for folder_path in folder_paths:
        timestamps, file_sizes = get_wav_file_sizes(folder_path)

        if timestamps:
            plot_file_sizes(folder_path, timestamps, file_sizes)
        else:
            print(f"No valid WAV files found in {folder_path}.")
