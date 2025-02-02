import os
import subprocess
import time
import sys
import yaml

SAVE_DIR = "splitted_bags"  # Folder where split bags are stored

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)


def generate_unique_filename(output_bag):
    """
    Checks if a bag file with the given name already exists in SAVE_DIR.
    If it exists, appends a numerical suffix to make it unique.
    """
    base_name, ext = os.path.splitext(output_bag)  # Extract name and extension
    unique_name = output_bag
    counter = 1

    while os.path.exists(os.path.join(SAVE_DIR, unique_name)):
        unique_name = f"{base_name}_{counter}{ext}"
        counter += 1

    return unique_name


def play_bag(input_bagfile):
    play_cmd = ["ros2", "bag", "play", input_bagfile]
    return subprocess.Popen(play_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def record_bag(output_bagfile):
    output_path = os.path.join(SAVE_DIR, output_bagfile)
    record_cmd = ["ros2", "bag", "record", "-a", "-o", output_path]
    return subprocess.Popen(record_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def split_bag(input_bag, segments):
    print(f"Playing the bag file {input_bag} from the beginning.")
    play_process = play_bag(input_bag)
    playback_start_time = time.time()

    for segment in segments:
        start_time_sec = segment["start_time"]
        end_time_sec = segment["end_time"]
        output_bag = segment["output_bag"]

        # Validate times
        if end_time_sec <= start_time_sec:
            print(f"Error: End time ({end_time_sec}) must be greater than start time ({start_time_sec}) "
                  f"for {output_bag}. Skipping segment.")
            continue

        record_duration = end_time_sec - start_time_sec
        print(f"\nSegment for {output_bag} will last {record_duration:.2f} seconds.")

        # Ensure unique output bag name
        unique_output_bag = generate_unique_filename(output_bag)
        print(f"Saving segment as: {unique_output_bag}")

        # Wait until start time
        time_to_wait = start_time_sec - (time.time() - playback_start_time)
        if time_to_wait > 0:
            print(f"Waiting {time_to_wait:.2f} seconds to start recording {unique_output_bag}...")
            time.sleep(time_to_wait)

        # Start recording
        print(f"Recording segment to {unique_output_bag} from {start_time_sec} to {end_time_sec} seconds.")
        record_process = record_bag(unique_output_bag)

        # Record for the required duration
        time.sleep(record_duration)

        # Stop recording
        print(f"Stopping the recording for {unique_output_bag}.")
        record_process.terminate()
        print("------------------------------------------------")

    # Stop playback after all segments are recorded
    print(f"Stopping playback for {input_bag}.")
    play_process.terminate()
    print("All segments recorded for this bag.\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python split_bags.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    # Load configuration from YAML file
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

    bags_list = config.get("bags", [])

    if not bags_list:
        print("No bags found in the configuration.")
        sys.exit(1)

    for bag_entry in bags_list:
        for input_bag, segments in bag_entry.items():
            if not segments:
                print(f"No segments defined for {input_bag}. Skipping.")
                continue

            formatted_segments = [
                {"start_time": seg[0], "end_time": seg[1], "output_bag": seg[2]}
                for seg in segments
            ]

            split_bag(input_bag, formatted_segments)

    print("Finished processing all bags.")


if __name__ == "__main__":
    main()
