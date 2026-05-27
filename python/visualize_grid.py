import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def visualize_fpga_routing(json_filepath):
    """
    Parses CAD flow outputs to render an island-style FPGA fabric,
    displaying CLBs, wire routing paths, and capacity bottlenecks.
    """
    print(f"Loading routing state from: {json_filepath}")
    
    try:
        with open(json_filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {json_filepath}")
        print("Please ensure you run the C++ fpga_engine first to generate the routing data.")
        sys.exit(1)

    grid_size = data.get("grid_size", 4)
    channel_capacity = data.get("channel_capacity", 1)
    nets = data.get("nets", [])

    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 1. Render Configurable Logic Blocks (CLBs)
    for x in range(grid_size):
        for y in range(grid_size):
            # CLBs occupy discrete coordinates; routing tracks run between them
            clb_rect = patches.Rectangle(
                (x + 0.15, y + 0.15), 0.7, 0.7, 
                edgecolor='#333333', facecolor='#E0E0E0', linewidth=1.5, zorder=2
            )
            ax.add_patch(clb_rect)
            ax.text(x + 0.5, y + 0.5, f"CLB\n({x},{y})", ha='center', va='center', fontsize=9, fontweight='bold')

    # 2. Track Wire Usage and Detect Over-Capacity (Congestion)
    wire_occupancy = {}
    for net in nets:
        path = net.get("path", [])
        for i in range(len(path) - 1):
            seg_start = tuple(path[i])
            seg_end = tuple(path[i+1])
            segment = tuple(sorted([seg_start, seg_end]))
            wire_occupancy[segment] = wire_occupancy.get(segment, 0) + 1

    # 3. Plot Wire Routing Paths
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for idx, net in enumerate(nets):
        path = net.get("path", [])
        if not path:
            continue
            
        # Offset coordinates slightly so overlapping non-congested paths don't perfectly hide each other
        offset = (idx * 0.05) - 0.05 
        x_coords = [p[0] + 0.5 + offset for p in path]
        y_coords = [p[1] + 0.5 + offset for p in path]
        
        color = colors[idx % len(colors)]
        
        # Draw the net's signal wire
        ax.plot(x_coords, y_coords, linewidth=3, color=color, alpha=0.8, zorder=3, label=f"Net {net['id']}")
        
        # Mark Source (Pin Input) and Sink (Pin Output)
        ax.scatter(x_coords[0], y_coords[0], marker='^', s=150, color='forestgreen', edgecolor='black', zorder=5)
        ax.scatter(x_coords[-1], y_coords[-1], marker='o', s=150, color='firebrick', edgecolor='black', zorder=5)

    # 4. Highlight Congestion Hotspots (Where occupancy exceeds channel capacity)
    for segment, occupancy in wire_occupancy.items():
        if occupancy > channel_capacity:
            p1, p2 = segment
            # Overlay a highly visible thick marker representing a short circuit
            ax.plot(
                [p1[0] + 0.5, p2[0] + 0.5], [p1[1] + 0.5, p2[1] + 0.5],
                color='crimson', linestyle='--', linewidth=6, zorder=4
            )
            # Add text indicator for the amount of illegal sharing
            mid_x = (p1[0] + p2[0]) / 2 + 0.5
            mid_y = (p1[1] + p2[1]) / 2 + 0.5
            ax.text(mid_x, mid_y, f"! {occupancy}/{channel_capacity}", color='white', 
                    fontsize=10, fontweight='bold', bbox=dict(facecolor='crimson', alpha=0.9, boxstyle='round,pad=0.3'))

    # Grid formatting adjustments
    ax.set_xlim(-0.5, grid_size + 0.5)
    ax.set_ylim(-0.5, grid_size + 0.5)
    ax.set_aspect('equal')
    ax.set_title(f"FPGA Routing Fabric (Capacity Boundary: {channel_capacity})", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Horizontal Routing Channels (X-Tracks)")
    ax.set_ylabel("Vertical Routing Channels (Y-Tracks)")
    
    # Configure grid lines to represent routing tracks
    ax.set_xticks(range(grid_size + 1))
    ax.set_yticks(range(grid_size + 1))
    ax.grid(True, which='major', color='#D3D3D3', linestyle='-', linewidth=1.5, zorder=1)
    
    # Move grid lines to align with the spaces between CLBs
    ax.set_xticks([x + 0.5 for x in range(grid_size)], minor=True)
    ax.set_yticks([y + 0.5 for y in range(grid_size)], minor=True)
    
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 visualize_grid.py <path_to_routing_state.json>")
        sys.exit(1)
        
    json_path = sys.argv[1]
    visualize_fpga_routing(json_path)
