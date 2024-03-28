cmake_minimum_required(VERSION 3.5)

project(UdpServerProcessor VERSION 0.1 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


add_library(UdpServerProcessor SHARED
    UdpServerProcessor.h
    UdpServerProcessor.cpp
)

find_package(Qt6 REQUIRED COMPONENTS Core Network)


target_link_libraries(UdpServerProcessor Qt6::Core Qt6::Network)

