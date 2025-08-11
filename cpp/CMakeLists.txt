cmake_minimum_required(VERSION 3.10)
project(unitree_dds_wrapper)

include_directories(
  /usr/local/include/ddscxx
  /usr/local/include/iceoryx/v2.0.2
  include
)

link_libraries(unitree_sdk2 ddsc ddscxx rt pthread fmt)
link_libraries(unitree_idl fmt)

add_executable(go2_print_state examples/go2/print_state.cpp)
add_executable(go2_low_level_control examples/go2/low_level_control.cpp)
add_executable(g1_test_dds examples/g1/test_dds.cpp)
add_executable(client examples/dds/client.cpp)

# test
add_executable(test_dds examples/test_dds.cpp)