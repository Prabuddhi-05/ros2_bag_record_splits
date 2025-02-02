# Split multiple ROS2 bag files by time segments

## Overview
- [x] This script automatically splits multiple ROS2 bag files into smaller time-based segments.
- [x] It plays each bag file and records defined segments into new bags using a YAML config file. 

## Requirements
- **Python 3** (Install dependencies with `pip install PyYAML`)
- **ROS2 installed & sourced** (for `ros2 bag play/record`)

## Usage
1. **Edit the YAML configuration** (see example below).
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
3. **Run the script**:
   ```bash
   python3 split_bags.py config.yaml
   ```
