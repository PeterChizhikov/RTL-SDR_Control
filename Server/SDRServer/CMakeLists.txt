cmake_minimum_required(VERSION 3.14)

project(SDRServer LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


find_package(Qt6 REQUIRED COMPONENTS Core Network)


add_executable(SDRServer
  main.cpp
  MainProcessor.h
  MainProcessor.cpp
)
target_link_libraries(SDRServer Qt6::Core  TcpServerProcessor Qt6::Network)

target_include_directories(SDRServer PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/TcpServerProcessor)



add_subdirectory(./TcpServerProcessor)
