cmake_minimum_required(VERSION 3.10)
project(unitree_dds_wrapper)

include_directories(
  /usr/local/include/ddscxx
  /usr/local/include/iceoryx/v2.0.2
  include
)

link_libraries(unitree_sdk2 ddsc ddscxx rt pthread)

link_directories(lib/${CMAKE_SYSTEM_PROCESSOR})
link_libraries(unitree_idl)

add_executable(go2_print_state examples/go2/print_state.cpp)
add_executable(go2_low_level_control examples/go2/low_level_control.cpp)

# test
add_executable(test_dds examples/test_dds.cpp)
