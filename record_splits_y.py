import subprocess
import time
import sys
import yaml

# Plays the entire bag file
def play_bag(input_bagfile):
    play_cmd = ["ros2", "bag", "play", input_bagfile]
    return subprocess.Popen(play_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Separate process for playing bags

# Records all topics from the bag file
def record_bag(output_bagfile):
    record_cmd = ["ros2", "bag", "record", "-a", "-o", output_bagfile]
    return subprocess.Popen(record_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # Separate process for recording bags

def split_bag(input_bag, output_bag, start_time_sec, end_time_sec):
    # Validates start and end time
    if end_time_sec <= start_time_sec:
        print("Error: End time must be greater than start time.")
        sys.exit(1)

    # Calculates wait_before_record and record_duration
    wait_before_record = start_time_sec
    record_duration = end_time_sec - start_time_sec

    # Starts playing the entire bag file
    print(f"Playing the bag file {input_bag}...")
    play_process = play_bag(input_bag)

    # Waits for the specified time before starting the recording
    print(f"Waiting for {wait_before_record} seconds to start recording...")
    time.sleep(wait_before_record)

    # Starts recording
    print(f"Recording the bag file {output_bag} from {start_time_sec} to {end_time_sec} seconds...")
    record_process = record_bag(output_bag)

    # Records for the specified duration
    time.sleep(record_duration)

    # Stops the recording process
    print("Stopping the recording...")
    record_process.terminate()

    # Stops the playback process after the total play time
    print("Stopping the bag file playback...")
    play_process.terminate()

    print(f"Recording saved as: {output_bag}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    # Loads the configuration from the YAML file
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            input_bag = config['input_bag']
            output_bag = config['output_bag']
            start_time_sec = float(config['start_time'])
            end_time_sec = float(config['end_time'])
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    split_bag(input_bag, output_bag, start_time_sec, end_time_sec)

