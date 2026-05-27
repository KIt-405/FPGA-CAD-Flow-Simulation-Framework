#pragma once
#include <vector>
#include <unordered_map>
#include "route/rrg_node.hpp" // Link to the data structures

// The Global Routing Graph representing the entire FPGA fabric
// (Extern tells the compiler: "This variable exists, but it is initialized in the .cpp file")
extern std::unordered_map<int, RRGNode> routing_grid;

/**
 * Initializes a blank Island-Style FPGA routing fabric.
 * Generates CLBs, Switch Boxes, and sets wire capacities.
 */
void init_routing_grid(int grid_size, int channel_capacity);

/**
 * Attempts to find the cheapest path for a single net using A* Search.
 * Costs are dynamically inflated based on current congestion.
 */
bool route_net(Net& net);

/**
 * The core Negotiated Congestion (PathFinder) execution loop.
 * Iteratively rips up and reroutes nets while increasing historical penalties (h_n)
 * until all congestion shorts are resolved or max_iterations is hit.
 */
bool run_pathfinder(std::vector<Net>& nets, int max_iterations);
