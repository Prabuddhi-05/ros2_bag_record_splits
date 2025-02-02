import subprocess
import time
import sys
import yaml

# Plays the entire bag file from the beginning.
def play_bag(input_bagfile):
    play_cmd = ["ros2", "bag", "play", input_bagfile]
    return subprocess.Popen(play_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Records all topics to the specified output bag file.
def record_bag(output_bagfile):
    record_cmd = ["ros2", "bag", "record", "-a", "-o", output_bagfile]
    return subprocess.Popen(record_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Plays the given input_bag from the start and records multiple segments as defined.
def split_bag(input_bag, segments):
    # Starts playing the bag file from the beginning
    print(f"Playing the bag file {input_bag} from the beginning.")
    play_process = play_bag(input_bag)
    playback_start_time = time.time()  # Record the system time when playback starts

    # Processes each segment
    for segment in segments:
        start_time_sec = segment['start_time']
        end_time_sec = segment['end_time']
        output_bag = segment['output_bag']

        # Validates start and end times
        if end_time_sec <= start_time_sec:
            print(f"Error: End time ({end_time_sec}) must be greater than start time ({start_time_sec}) "
                  f"for {output_bag}. Skipping segment.")
            continue

        record_duration = end_time_sec - start_time_sec
        print(f"\nSegment for {output_bag} will last {record_duration:.2f} seconds.")

        # Calculates the wait time until this segment's start time
        time_to_wait = start_time_sec - (time.time() - playback_start_time)
        if time_to_wait > 0:
            print(f"Waiting {time_to_wait:.2f} seconds to start recording {output_bag}...")
            time.sleep(time_to_wait)

        # Starts recording
        print(f"Recording segment to {output_bag} from {start_time_sec} to {end_time_sec} seconds.")
        record_process = record_bag(output_bag)

        # Records for the required duration
        time.sleep(record_duration)

        # Stops recording
        print(f"Stopping the recording for {output_bag}.")
        record_process.terminate()
        print("------------------------------------------------")

    # After all segments for this bag are recorded, stops the playback
    print(f"Stopping playback for {input_bag}.")
    play_process.terminate()
    print("All segments recorded for this bag.\n")

def main():
    # Checks command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python split_bags.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    # Loads the configuration from the YAML file
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    # Retrieves the list of bags from the config
    bags_list = config.get('bags', [])
    if not bags_list:
        print("No bags found in the configuration.")
        sys.exit(1)

    # Processes each bag in the list
    for bag_entry in bags_list:
        input_bag = bag_entry.get('input_bag')
        segments = bag_entry.get('segments', [])

        if not input_bag:
            print("Skipping an entry because 'input_bag' is missing.")
            continue

        if not segments:
            print(f"No segments defined for {input_bag}. Skipping.")
            continue

        # Splits the current bag using the segments specified
        split_bag(input_bag, segments)

    print("Finished processing all bags.")

if __name__ == '__main__':
    main()

