#pragma once
#include <vector>

// Represents a signal that needs to be routed from a Source pin to a Sink pin
struct Net {
    int id;
    int source_node_id;
    int sink_node_id;
    
    // The final sequence of RRG Node IDs chosen by the router
    std::vector<int> routed_path; 
};

// Represents a single wire segment, Switch Box pin, or CLB pin in the FPGA
struct RRGNode {
    int id;
    
    // Routing costs for Negotiated Congestion (PathFinder algorithm)
    double base_cost = 1.0; 
    double pres_fac = 1.0;  // Present congestion penalty (p_n)
    double hist_fac = 1.0;  // Historical congestion penalty (h_n)
    
    // Congestion tracking
    int capacity = 1;       // How many nets can legally share this wire? 
    int occupancy = 0;      // How many nets are currently trying to use this wire?
    
    // Adjacency list: IDs of nodes we can reach through programmable switches
    std::vector<int> edges; 
};
