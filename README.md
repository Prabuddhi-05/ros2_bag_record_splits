# Split multiple ROS2 bag files by time segments

## Overview
- This script automatically splits multiple ROS2 bag files into smaller time-based segments.
- It plays each bag file and records defined segments into new bags using a YAML config file. 

## Requirements
- **Python 3** (Install dependencies with `pip install PyYAML`)
- **ROS2** (for `ros2 bag play/record`)

## Usage
1. **Edit the YAML configuration** as given below.
```bash
bags:
  - input_bag: "/path/to/bag1"
    segments:
      - output_bag: "/path/to/segment1"
        start_time: 10
        end_time: 20
      - output_bag: "/path/to/segment2"
        start_time: 30
        end_time: 40

  - input_bag: "/path/to/bag2"
    segments:
      - output_bag: "/path/to/segment3"
        start_time: 5
        end_time: 15
```
### What to Change in the YAML:
- **Change `/path/to/bag1` and `/path/to/bag2`** to the actual paths of your original ROS2 bag files.
- **Update `/path/to/segmentX`** to the desired output location for each split segment.
- **Modify `start_time` and `end_time`** to define where each segment starts and stops.

2. **Run the script**:
   ```bash
   python3 record_splits.py config.yaml
   ```
   
3. New bag files appear at the specified paths.
