cmake_minimum_required(VERSION 3.10)
project(unitree_dds_wrapper)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")

include_directories(
  /usr/local/include/ddscxx
  /usr/local/include/iceoryx/v2.0.2
  /usr/local/include/common/dds
  include
)

link_libraries(unitree_sdk2 ddsc ddscxx rt pthread)

add_executable(go2_print_state examples/go2/print_state.cpp)
add_executable(go2_low_level_control examples/go2/low_level_control.cpp)