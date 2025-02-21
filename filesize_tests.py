import os
import sys
import re
import matplotlib.pyplot as plt
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
    
    for file in os.listdir(folder_path):
        if file.lower().endswith(".wav"):
            timestamp = extract_timestamp(file)
            if timestamp:
                file_path = os.path.join(folder_path, file)
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                timestamps.append(timestamp)
                file_sizes.append(file_size)
    
    return timestamps, file_sizes

def plot_file_sizes(timestamps, file_sizes):
    plt.figure(figsize=(10, 5))
    plt.scatter(timestamps, file_sizes, label='File Size (MB)', color='b', marker='o')
    plt.plot(timestamps, file_sizes, linestyle='-', alpha=0.6)
    plt.xlabel('Time')
    plt.ylabel('File Size (MB)')
    plt.title('WAV File Size Over Time')
    plt.xticks(rotation=45)
    
    min_time = min(timestamps)
    max_time = max(timestamps)
    time_interval = timedelta(hours=6)
    tick_times = []
    
    rounded_start_time = min_time.replace(minute=0, second=0, microsecond=0)
    if min_time.minute >= 30:
        rounded_start_time += timedelta(hours=1)
    
    current_time = rounded_start_time
    while current_time <= max_time:
        tick_times.append(current_time)
        current_time += time_interval
    
    plt.xticks(tick_times, [t.strftime('%Y-%m-%d %H:%M') for t in tick_times])
    
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    timestamps, file_sizes = get_wav_file_sizes(folder_path)
    
    if timestamps:
        plot_file_sizes(timestamps, file_sizes)
    else:
        print("No valid WAV files found in the specified directory.")
