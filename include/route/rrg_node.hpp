#pragma once
#include <vector>

struct Net {
    int id;
    int source_node_id;
    int sink_node_id;
    
    std::vector<int> routed_path; 
};

struct RRGNode {
    int id;
    
    double base_cost = 1.0; 
    double pres_fac = 1.0;  // Present congestion penalty (p_n)
    double hist_fac = 1.0;  // Historical congestion penalty (h_n)
    
    int capacity = 1;       // How many nets can legally share this wire? 
    int occupancy = 0;      // How many nets are currently trying to use this wire?
    
    std::vector<int> edges; 
};
