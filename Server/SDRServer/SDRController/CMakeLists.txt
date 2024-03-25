cmake_minimum_required(VERSION 3.5)

project(SDRController VERSION 0.1 LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


add_library(SDRController SHARED
    SDRController.h
    SDRController.cpp
)


find_package(Qt6 REQUIRED COMPONENTS Core Network)

# set(rtlsdr_DIR "${PROJECT_SOURCE_DIR}/rtlsdr/cmake")
# find_package(rtlsdr REQUIRED)

# if(rtlsdr_FOUND)
#     target_include_directories(SDRController PRIVATE ${rtlsdr_INCLUDE_DIRS})
#     target_link_libraries(SDRController PRIVATE ${rtlsdr_LIBRARIES})
# endif()

# target_include_directories(SDRController PRIVATE rtl-sdr/include)
# include_directories(rtl-sdr)
######################
#include_directories("${PROJECT_SOURCE_DIR}/rtlsdr/include")

#add_subdirectory(rtlsdr)
###############################
# find_library(LIBUSB_LIBRARY
#              NAMES usb-1.0
#              PATHS /lib /usr/lib /usr/local/lib)


# target_link_libraries(SDRController ${LIBUSB_LIBRARY})
#####################################

target_link_libraries(SDRController Qt6::Core Qt6::Network)
