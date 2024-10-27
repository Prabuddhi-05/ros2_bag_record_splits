import subprocess
import time
import sys
import yaml

# Plays the entire bag file from the beginning
def play_bag(input_bagfile):
    play_cmd = ["ros2", "bag", "play", input_bagfile]
    return subprocess.Popen(play_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Records all topics to the specified output bag file
def record_bag(output_bagfile):
    record_cmd = ["ros2", "bag", "record", "-a", "-o", output_bagfile]
    return subprocess.Popen(record_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def split_bag(input_bag, segments):
    # Start playing the bag file from the beginning
    print(f"Playing the bag file {input_bag} from the beginning")
    play_process = play_bag(input_bag)
    playback_start_time = time.time()  # Record the start time of playback

    # Process each segment in the configuration
    for segment in segments:
        start_time_sec = segment['start_time']
        end_time_sec = segment['end_time']
        output_bag = segment['output_bag']

        # Validate start and end times
        if end_time_sec <= start_time_sec:
            print(f"Error: End time must be greater than start time for {output_bag}. Skipping segment.")
            continue

        # Calculate the recording duration for this segment
        record_duration = end_time_sec - start_time_sec
        print(f"Segment for {output_bag} has a duration of {record_duration:.2f} seconds.")

        # Calculate the wait time until this segment's start
        time_to_wait = start_time_sec - (time.time() - playback_start_time)
        if time_to_wait > 0:
            print(f"Waiting {time_to_wait:.2f} seconds to start recording {output_bag}")
            time.sleep(time_to_wait)

        # Start recording for the segment
        print(f"Recording segment to {output_bag} from {start_time_sec} to {end_time_sec} seconds")
        record_process = record_bag(output_bag)

        # Record for the specified duration
        time.sleep(record_duration)

        # Stop the recording process
        print(f"Stopping the recording for {output_bag}")
        print("........................................")
        record_process.terminate()

    # Stop playback once all segments have been recorded
    print("Stopping the bag file playback")
    play_process.terminate()
    print("All segments recorded and playback completed.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    # Load the configuration from the YAML file
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            input_bag = config['input_bag']
            segments = config['segments']
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    split_bag(input_bag, segments)
