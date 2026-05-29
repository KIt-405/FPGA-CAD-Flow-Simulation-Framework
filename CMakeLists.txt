cmake_minimum_required(VERSION 3.15)

project(FPGACADFlow VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${CMAKE_SOURCE_DIR}/include)

set(SOURCE_FILES
    src/main.cpp
    src/parse/ast_parser.cpp
    src/route/pathfinder.cpp
)

add_executable(fpga_engine ${SOURCE_FILES})


enable_testing()

add_executable(test_parser tests/test_parser.cpp src/parse/ast_parser.cpp)
add_test(NAME ParserTest COMMAND test_parser)

add_executable(test_router tests/test_router.cpp src/route/pathfinder.cpp)
add_test(NAME RouterTest COMMAND test_router)
