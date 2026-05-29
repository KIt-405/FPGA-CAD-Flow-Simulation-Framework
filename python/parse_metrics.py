import sys
import json
from collections import Counter
import matplotlib.pyplot as plt

def analyze_metrics(json_filepath):

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

    # 4. Print Terminal Report
    print("="*45)
    print("  FPGA CAD ROUTING METRICS REPORT")
    print("="*45)
    print(f"Fabric Size            : {grid_size}x{grid_size} CLBs")
    print(f"Total Nets Routed      : {total_nets}")
    print(f"Total Wirelength       : {total_wirelength} units")
    print(f"Average Wirelength     : {avg_wirelength:.2f} units")
    print(f"Critical Path (Max)    : {max_wirelength} units")
    print("-" * 45)
    print(f"Unique Grid Wires Used : {total_segments_used}")
    print(f"Target Track Capacity  : {channel_capacity}")
    print(f"Peak Wire Congestion   : {peak_congestion} nets/channel")
    print("-" * 45)
    
    if over_capacity_segments > 0:
        print(f"  ILLEGAL ROUTING: {over_capacity_segments} wire(s) over capacity!")
    else:
        print(" ROUTING FEASIBLE: 0 conflicts detected (100% Legal).")
    print("="*45)

    # 5. Visualize Wirelength Distribution
    plot_wirelength_histogram(wirelengths)

def plot_wirelength_histogram(wirelengths):

    plt.figure(figsize=(8, 5))
    
    
    min_len = min(wirelengths)
    max_len = max(wirelengths)
    bins = range(min_len, max_len + 2, 1)
    
    plt.hist(wirelengths, bins=bins, align='left', color='#4C72B0', edgecolor='black')
    
    plt.title("Net Wirelength Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Wirelength (Number of channel segments)", fontsize=11)
    plt.ylabel("Frequency (Number of Nets)", fontsize=11)
    
    plt.xticks(range(min_len, max_len + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_metrics.py <path_to_routing_state.json>")
        sys.exit(1)
        
    json_path = sys.argv[1]
    analyze_metrics(json_path)
