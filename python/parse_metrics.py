import sys
import json
from collections import Counter
import matplotlib.pyplot as plt

def analyze_metrics(json_filepath):
    """
    Parses the routing state output from the C++ CAD engine and calculates
    key EDA metrics such as total wirelength, critical path length, and congestion.
    """
    print(f"Loading routing metrics from: {json_filepath}\n")
    
    try:
        with open(json_filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {json_filepath}")
        sys.exit(1)

    grid_size = data.get("grid_size", 0)
    channel_capacity = data.get("channel_capacity", 1)
    nets = data.get("nets", [])
    
    total_nets = len(nets)
    if total_nets == 0:
        print("No nets found in the routing state.")
        return

    # 1. Calculate Wirelengths
    wirelengths = []
    wire_usage = Counter()

    for net in nets:
        path = net.get("path", [])
        # Wirelength is the number of segments (nodes - 1)
        length = len(path) - 1 if len(path) > 0 else 0
        wirelengths.append(length)

        # Track usage for congestion metrics
        for i in range(len(path) - 1):
            seg_start = tuple(path[i])
            seg_end = tuple(path[i+1])
            # Sort the tuple so (A,B) and (B,A) map to the same physical wire segment
            segment = tuple(sorted([seg_start, seg_end]))
            wire_usage[segment] += 1

    # 2. Derive Statistical Metrics
    total_wirelength = sum(wirelengths)
    max_wirelength = max(wirelengths) if wirelengths else 0
    avg_wirelength = total_wirelength / total_nets if total_nets else 0

    # 3. Derive Congestion Metrics
    total_segments_used = len(wire_usage)
    over_capacity_segments = sum(1 for count in wire_usage.values() if count > channel_capacity)
    peak_congestion = max(wire_usage.values()) if wire_usage else 0
