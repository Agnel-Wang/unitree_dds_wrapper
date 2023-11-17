cmake_minimum_required(VERSION 3.10)
project(unitree_dds_wrapper)

include_directories(
  /usr/local/include/ddscxx
  /usr/local/include/iceoryx/v2.0.2
  /usr/local/include/common/dds
  include
)

link_libraries(unitree_sdk2 ddsc ddscxx rt pthread)

add_executable(go2_print_state examples/go2/print_state.cpp)
add_executable(go2_low_level_control examples/go2/low_level_control.cpp)


# Custom message
option(BUILD_CUSTOM_MESSAGE "Build custom message" OFF)
if (BUILD_CUSTOM_MESSAGE)
  include_directories(${PROJECT_SOURCE_DIR}/idl/include)
  link_directories(${PROJECT_SOURCE_DIR}/idl/lib)
  link_libraries(custom_idl_cpp)
  add_executable(custom_message examples/custom/custom_message.cpp)
endif()