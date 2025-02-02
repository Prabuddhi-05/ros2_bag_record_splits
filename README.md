# Split Multiple ROS2 Bag Files by Time Segments

## Overview
This script automates splitting multiple ROS2 bag files into smaller time-based segments.  
Controlled via a YAML config, it plays each bag file and records defined segments into new bags.

## Requirements
- **Python 3** (Install dependencies with `pip install PyYAML`)
- **ROS2 installed & sourced** (for `ros2 bag play/record`)

## Usage
1. **Edit the YAML configuration** (see example below).
2. **Run the script**:
   ```bash
   python split_bags.py config.yaml
