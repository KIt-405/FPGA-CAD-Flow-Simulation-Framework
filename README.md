# FPGA-CAD-Flow-Simulation-Framework

A custom, end-to-end Electronic Design Automation (EDA) simulation framework designed to mimic industrial FPGA toolchains (e.g., Xilinx Vivado, VTR). This project bridges computer science compiler theory and physical silicon architecture, encompassing RTL parsing, logic optimization, and congestion-aware physical routing.

##  What Does This System Actually Do?

When you write software for a standard computer, a compiler translates your code into instructions for a fixed CPU. But when you write code for an **FPGA (Field Programmable Gate Array)**, there is no fixed CPU—you are programming the *physical hardware itself*. 

An EDA toolchain is the massive software engine responsible for figuring out how to wire millions of microscopic logic gates together to build a custom chip. This framework simulates that exact industrial pipeline from scratch:

1. **Reads the Blueprint (Front-End):** It takes raw logical equations (e.g., `Y = (A AND B) OR C`) and constructs a mathematical tree (AST) that the computer can understand.
2. **Optimizes the Logic (Middle-End):** It trims the fat. If a signal is calculated but never used, or if a Boolean expression is unnecessarily complex, the framework simplifies the math to save physical space on the silicon.
3. **Wires It Up (Back-End Routing):** It takes the optimized logic gates and figures out how to physically run wires across a grid (the FPGA fabric). It uses advanced pathfinding algorithms to ensure thousands of wires reach their destinations without colliding or causing traffic jams (congestion).

In short: **It is a software engine that converts abstract math into a physically routable silicon layout.**

##  Core Features

* **Recursive-Descent Parser:** Constructs Abstract Syntax Trees (ASTs) from RTL-style Boolean logic expressions, featuring strict syntax validation and operator precedence handling.
* **Middle-End Optimization:** Converts ASTs into Directed Acyclic Graphs (DAGs) for topological dependency modeling. Implements constant propagation, dead logic elimination, and Boolean simplification passes.
* **Congestion-Aware Routing (PathFinder):** Models an Island-Style FPGA fabric (Configurable Logic Blocks, Connection Blocks, Switch Boxes) using a Routing Resource Graph (RRG). Utilizes Negotiated Congestion (A* search with historical/present cost inflation) to resolve wire-sharing conflicts.
* **Python Visualization Suite:** Decodes C++ routing states into interactive graphical plots, highlighting physical wire layout, CLB utilization, and routing capacity bottlenecks.

## Repository Architecture

FPGA-CAD-Flow-Simulation-Framework/
├── .gitignore               
├── README.md                
├── CMakeLists.txt           
├── requirements.txt         
│
├── include/                 
│   └── route/
│       ├── rrg_node.hpp
│       └── pathfinder.hpp
│
├── src/                     
│   ├── main.cpp
│   └── route/
│       └── pathfinder.cpp
│
├── python/                  
│   ├── requirements.txt
│   ├── visualize_grid.py
│   └── parse_metrics.py
│
├── tests/                   
│   ├── test_parser.cpp
│   └── test_router.cpp
│
├── data/                    
│   ├── inputs/              
│   └── outputs/             
│
└── docs/                    
    └── architecture.md
