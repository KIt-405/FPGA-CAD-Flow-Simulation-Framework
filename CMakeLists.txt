# Require a modern version of CMake
cmake_minimum_required(VERSION 3.15)

# Name your project and specify the language (C++)
project(FPGACADFlow VERSION 1.0.0 LANGUAGES CXX)

# Enforce modern C++17 standard (crucial for modern graph/auto features)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Tell the compiler where to find your .hpp header files
include_directories(${CMAKE_SOURCE_DIR}/include)

# Define the source files that need to be compiled for the main engine
set(SOURCE_FILES
    src/main.cpp
    src/parse/ast_parser.cpp
    src/route/pathfinder.cpp
)

# Create the final executable named 'fpga_engine'
add_executable(fpga_engine ${SOURCE_FILES})

# ---------------------------------------------------------
# Automated Testing Setup
# ---------------------------------------------------------
enable_testing()

# Compile the Parser tests (links the test file with the parser implementation)
add_executable(test_parser tests/test_parser.cpp src/parse/ast_parser.cpp)
add_test(NAME ParserTest COMMAND test_parser)

# Compile the Router tests (links the test file with the router implementation)
add_executable(test_router tests/test_router.cpp src/route/pathfinder.cpp)
add_test(NAME RouterTest COMMAND test_router)
