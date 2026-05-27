#include "route/pathfinder.hpp"
#include <iostream>
#include <queue>
#include <cmath>
#include <algorithm>
#include <limits>

// Define the global routing graph declared in the header
std::unordered_map<int, RRGNode> routing_grid;

// Helper: Calculate Manhattan distance for A* Heuristic
double manhattan_distance(int node_a, int node_b, int grid_size) {
    int x1 = node_a % grid_size;
    int y1 = node_a / grid_size;
    int x2 = node_b % grid_size;
    int y2 = node_b / grid_size;
    return std::abs(x1 - x2) + std::abs(y1 - y2);
}

void init_routing_grid(int grid_size, int channel_capacity) {
    routing_grid.clear();

    // 1. Generate Nodes (A simple 2D mesh grid representing Switch Boxes/Wire Segments)
    for (int y = 0; y < grid_size; ++y) {
        for (int x = 0; x < grid_size; ++x) {
            int id = y * grid_size + x;
            RRGNode node;
            node.id = id;
            node.capacity = channel_capacity;
            node.occupancy = 0;
            node.base_cost = 1.0;
            node.pres_fac = 1.0;
            node.hist_fac = 1.0;
            
            // Connect to neighbors (North, South, East, West) to build the fabric
            if (x > 0) node.edges.push_back(y * grid_size + (x - 1)); // West
            if (x < grid_size - 1) node.edges.push_back(y * grid_size + (x + 1)); // East
            if (y > 0) node.edges.push_back((y - 1) * grid_size + x); // North
            if (y < grid_size - 1) node.edges.push_back((y + 1) * grid_size + x); // South

            routing_grid[id] = node;
        }
    }
    std::cout << "[Grid] Initialized " << grid_size << "x" << grid_size 
              << " FPGA fabric with capacity " << channel_capacity << " per track.\n";
}

// Priority Queue element for A* Search
struct PQElement {
    int node_id;
    double cost_from_start;
    double estimated_total_cost; // cost_from_start + heuristic
    int parent_id; 

    bool operator>(const PQElement& other) const {
        return estimated_total_cost > other.estimated_total_cost;
    }
};

bool route_net(Net& net, int grid_size) {
    std::priority_queue<PQElement, std::vector<PQElement>, std::greater<PQElement>> pq;
    std::unordered_map<int, double> min_cost_to_reach;
    std::unordered_map<int, int> came_from; 

    pq.push({net.source_node_id, 0.0, 0.0, -1});
    min_cost_to_reach[net.source_node_id] = 0.0;

    while (!pq.empty()) {
        auto current = pq.top();
        pq.pop();

        // Target reached! Backtrack to reconstruct the path
        if (current.node_id == net.sink_node_id) {
            int curr_trace = current.node_id;
            while (curr_trace != -1) {
                net.routed_path.
