# Require a modern version of CMake
cmake_minimum_required(VERSION 3.15)

# Name your project and specify the language (C++)
project(FPGACADFlow VERSION 1.0.0 LANGUAGES CXX)

# Enforce modern C++17 standard (crucial for modern graph/auto features)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Tell the compiler where to find your .hpp header files
include_directories(${CMAKE_SOURCE_DIR}/include)

# Define the source files that need to be compiled
# As you build out the parser and optimizer, add their .cpp files here
set(SOURCE_FILES
    src/main.cpp
    src/route/pathfinder.cpp
)

# Create the final executable named 'fpga_engine'
add_executable(fpga_engine ${SOURCE_FILES})

# ---------------------------------------------------------
# Optional: Setup for automated testing later
# ---------------------------------------------------------
# enable_testing()
# add_executable(run_tests tests/test_router.cpp src/route/pathfinder.cpp)
# add_test(NAME RouterTest COMMAND run_tests)
