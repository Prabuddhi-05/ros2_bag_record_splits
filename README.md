# Split multiple ROS2 bag files by time segments

## Overview
- This script automatically splits multiple ROS2 bag files into smaller time-based segments.
- It plays each bag file and records defined segments into new bags using a YAML config file. 

## Requirements
- **Python 3** (Install dependencies with `pip install PyYAML`)
- **ROS2** (for `ros2 bag play/record`)

## Usage
1. **Edit the output directory in record_splits.py**
  ```
  SAVE_DIR = "splitted_bags"  # Folder where split bags are stored
  ```
   
3. **Edit the YAML configuration** as given below.
```bash
bags:
  - "/path/to/bag1":
      - [start_time, end_time, "segment.bag"]
      - [start_time, end_time, "segment.bag"]
  - "/path/to/bag2":
      - [start_time, end_time, "segment.bag"]
```
### What to change in the YAML config file:
- **Update `/path/to/bag1` and `/path/to/bag2`** to the actual paths of your original ROS2 bag files.
- **Modify `start_time` and `end_time`** to define where each segment starts and stops.
- **Note:** name of the splited bags should be unique. This code will do it for you if you use any duplicated names for splited bags.

3. **Run the script**:
   ```bash
   python3 record_splits.py config.yaml
   ```
   
4. New bag files will appear at the specified paths.
