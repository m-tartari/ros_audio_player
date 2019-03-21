# ros_audio_player
a simple audio player package for ros.

## Installation

This package uses pygame mixer to reproduce the audio files. It can be installed using:
```
sudo pip install pygame 
```
This repository can be cloned using
```
git clone https://github.com/m-tartari/ros_audio_player.git
```

## Use
A sample launch file named pub_sub.launch is present in the package. and can be run using:
```
roslaunch ros_audio_player pub_sub.launch
```
It will launch the player.py (main component of this package) and a publisher node (used only for testing and understanding the package).
