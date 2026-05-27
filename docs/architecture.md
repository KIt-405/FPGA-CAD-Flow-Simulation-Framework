# FPGA CAD Flow Architecture & Internal APIs

This document outlines the internal data structures, algorithmic pipeline, and inter-process communication schema used in the FPGA CAD Flow Simulation Framework.

## 1. High-Level Pipeline Architecture

The framework is divided into a high-performance C++ core for algorithmic processing and a Python suite for diagnostics. The pipeline executes in three distinct phases:

1. **Front-End (AST Generation):** A Recursive-Descent parser reads RTL-style Boolean logic and constructs an Abstract Syntax Tree (AST), ensuring operator precedence (`NOT` > `AND` > `OR`).
2. **Middle-End (Optimization):** The AST is transformed into a Directed Acyclic Graph (DAG) for Common Subexpression Elimination (CSE). Optimization passes (constant propagation, dead logic elimination) run over the DAG.
3. **Back-End (Physical Routing):** The optimized logic is mapped to physical pins. The PathFinder algorithm (Negotiated Congestion) routes nets across a simulated Island-Style FPGA fabric.

---

## 2. Core Data Structures (C++)

### 2.1 Routing Resource Graph (RRG)
The physical FPGA fabric is represented as a directed graph.
* **Nodes:** Represent configurable logic block (CLB) pins, connection blocks, or routing wire segments.
* **Edges:** Represent programmable switch boxes (pass transistors).
* **State:** Each node tracks its legal `capacity` and its current `occupancy`. 

### 2.2 Negotiated Congestion Cost Model
Routing relies on the PathFinder algorithm, utilizing an A* search heuristic. The cost to use a specific wire segment (Node $n$) is calculated dynamically per iteration:

$$Cost_n = BaseCost_n \times h_n \times p_n$$

* **$BaseCost_n$**: Intrinsic delay of the wire (default 1.0).
* **$p_n$ (Present Congestion):** Scales linearly with `occupancy - capacity` if the wire is currently overused. Resets to 1.0 if legal.
* **$h_n$ (Historical Congestion):** Increases incrementally every iteration a wire remains congested. Never resets. Acts as a memory mechanism to force nets to route around chronic bottlenecks.

---

## 3. Inter-Process Communication (JSON Schema)

To decouple the C++ engine from the visualization and analytics tools, all physical routing states are dumped to a standardized JSON file. 

**Any modifications to the C++ router or Python visualization tools MUST strictly adhere to this schema.**

### 3.1 JSON Schema Definition

```json
{
  "grid_size": <int>,           // The dimensions of the N x N FPGA fabric
  "channel_capacity": <int>,    // Maximum legal nets allowed per wire segment
  "nets": [                     // Array of all routed signals
    {
      "id": <int>,              // Unique identifier for the net
      "path": [                 // Ordered list of [x, y] coordinates defining the route
        [<x_start>, <y_start>],
        [<x_step1>, <y_step1>],
        ...
        [<x_end>, <y_end>]
      ]
    }
  ]
}
