#include "route/pathfinder.hpp"
#include <iostream>
#include <cassert>
#include <vector>

void test_single_net_routing() {
    std::cout << "[Test] Running test_single_net_routing..." << std::endl;
    init_routing_grid(4, 1); // 4x4 grid, 1 net per track max

    std::vector<Net> nets = {
        {1, 0, 15, {}} // Route from top-left (0) to bottom-right (15)
    };

    bool success = run_pathfinder(nets, 10, 4);
    
    assert(success == true);
    assert(!nets[0].routed_path.empty());
    assert(nets[0].routed_path.front() == 0);
    assert(nets[0].routed_path.back() == 15);
}

void test_negotiated_congestion() {
    std::cout << "[Test] Running test_negotiated_congestion..." << std::endl;
    init_routing_grid(3, 1); // 3x3 grid, STRICT capacity of 1

    // Intentionally create a scenario where shortest paths cross
    std::vector<Net> nets = {
        {1, 0, 2, {}}, // Top row: left to right
        {2, 1, 7, {}}  // Middle column: top to bottom (will collide at node 1)
    };

    // The router should take a few iterations to increase the cost of the center node
    // and eventually detour one of the nets to achieve 0 congestion.
    bool success = run_pathfinder(nets, 20, 3);
    
    assert(success == true);
    
    // Verify no node is over capacity after routing
    for (const auto& pair : routing_grid) {
        assert(pair.second.occupancy <= pair.second.capacity);
    }
}

void test_unroutable_design() {
    std::cout << "[Test] Running test_unroutable_design..." << std::endl;
    init_routing_grid(2, 1); // 2x2 grid, capacity 1

    // Cram too many nets into a tiny fabric so it mathematically cannot succeed
    std::vector<Net> nets = {
        {1, 0, 3, {}},
        {2, 1, 2, {}},
        {3, 0, 2, {}}
    };

    bool success = run_pathfinder(nets, 5, 2);
    
    // We EXPECT this to fail because the hardware capacity is exceeded
    assert(success == false);
}

int main() {
    std::cout << "========================================" << std::endl;
    std::cout << "  Starting Back-End PathFinder Tests    " << std::endl;
    std::cout << "========================================" << std::endl;

    test_single_net_routing();
    test_negotiated_congestion();
    test_unroutable_design();

    std::cout << "\n[SUCCESS] All PathFinder Router tests passed!" << std::endl;
    return 0;
}
