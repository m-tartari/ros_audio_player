cmake_minimum_required(VERSION 2.8.3)
project(ros_audio_player)

find_package(catkin REQUIRED)
catkin_package(DEPENDS)

install(PROGRAMS scripts/player.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})