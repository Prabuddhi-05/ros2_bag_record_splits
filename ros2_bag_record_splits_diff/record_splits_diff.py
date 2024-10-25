import subprocess
import time
import sys
import yaml

# # Plays the entire bag file
def play_bag(input_bagfile):
    play_cmd = ["ros2", "bag", "play", input_bagfile]
    return subprocess.Popen(play_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Separate process for playing bags

# Records all topics from the bag file
def record_bag(output_bagfile):
    record_cmd = ["ros2", "bag", "record", "-a", "-o", output_bagfile]
    return subprocess.Popen(record_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # Separate process for recording bags
 
# Splits the bag file into multiple segments
def split_bag(input_bag, segments):
    print(f"Playing the bag file {input_bag}...")
    play_process = play_bag(input_bag)

    for segment in segments:
        start_time_sec = segment['start_time']
        end_time_sec = segment['end_time']
        output_bag = segment['output_bag']

        # Validates start and end time
        if end_time_sec <= start_time_sec:
            print(f"Error: End time must be greater than start time for {output_bag}.")
            continue
            
        # Calculates wait_before_record and record_duration
        wait_before_record = start_time_sec
        record_duration = end_time_sec - start_time_sec

        # Waits until the start time of the segment
        print(f"Waiting for {wait_before_record} seconds to start recording {output_bag}...")
        time.sleep(wait_before_record)

        # Starts recording
        print(f"Recording segment to {output_bag} from {start_time_sec} to {end_time_sec} seconds...")
        record_process = record_bag(output_bag)

        # Records for the specified duration
        time.sleep(record_duration)

        # Stops the recording process for this segment
        print(f"Stopping recording for {output_bag}...")
        record_process.terminate()

    # Stops the playback process after all segments are recorded
    print("Stopping the bag file playback...")
    play_process.terminate()

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
            segments = config['segments']
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    split_bag(input_bag, segments)

