cmake_minimum_required(VERSION 3.15)
project(Course-Work)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

set(SOURCES src/python/game_module.cpp src/game/game.cpp)
include_directories(src/game)

pybind11_add_module(game_module ${SOURCES})

target_include_directories(game_module PRIVATE ${CMAKE_SOURCE_DIR}/pybind11/include)


