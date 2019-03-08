#! /usr/bin/env python

# Python libraries
import os
from pygame import mixer

# ROS libraries
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool


class player(object):

    def __init__(self):
        # Start node
        rospy.init_node("player")
        rospy.on_shutdown(self.shutdown)

        self.file_path_param = "~file_path"
        self.file_extention_param = "~file_extension"
        self.default_file_param = "~default_file"
        self.no_file_param = "~no_file"

        # you may need to change publisher destination depending on what you run
        self.sub_ = rospy.Subscriber("chatter", String, self.callback)
        self.pub_ = rospy.Publisher('busy', Bool, queue_size=1)

        if rospy.has_param(self.file_path_param):
            self.file_path = rospy.get_param(self.file_path_param)
            rospy.loginfo("Loaded costum file path: " + self.file_path)
        else:
            self.file_path = "/home/michele/ros/src/Voice_Controlled_Mobile_Robot/control_bot/voice_commands/"
            rospy.loginfo("Loaded the default file path")

        if rospy.has_param(self.file_extention_param):
            self.file_extention = rospy.get_param(self.file_extention_param)
            rospy.loginfo("Loaded the costum file extension: " +
                          self.file_extention)
        else:
            self.file_extention = ".wav"
            rospy.loginfo("Loaded the default file extension .wav")

        if rospy.has_param(self.file_path_param):
            self.default_file = rospy.get_param(self.default_file_param)
            rospy.loginfo("Loaded the costum default file: "+self.default_file)
        else:
            # "I want to say something but I don't know what is it"
            self.default_file = "I want to say something but I don't know what is it"
            rospy.loginfo("Loaded the default default file: " +
                          self.default_file)

        if rospy.has_param(self.no_file_param):
            self.no_file = rospy.get_param(self.no_file_param)
            rospy.loginfo("Loaded the costum no-file: '"+self.no_file)
        else:
            self.no_file = "none"
            rospy.loginfo("Loaded the default 'none' no-file")

        self.busy = False
        self.new_file = ''
        self.start_player()

    def start_player(self):
        mixer.init()
        rospy.loginfo("busy initializing player")

        last_played = ''

        # Main loop
        rate = rospy.Rate(10)
        rospy.loginfo("Spinning at 10Hz")
        while not rospy.is_shutdown():
            self.busy = False
            rospy.loginfo(
                "Audio player ready, new file: '"+self.new_file+"' last file played: '"+last_played+"' extension:" + self.file_extention)
            # check if the command has been played
            if ((self.new_file != last_played) & (self.new_file != self.no_file)):
                last_played = self.new_file
                rospy.loginfo("File different from previous\n")
                file_full_name = self.file_path+self.new_file+self.file_extention

                # check if it exist, else select a default file to play
                if os.path.isfile(file_full_name):
                    rospy.loginfo("Audio file found\n")
                else:
                    file_full_name = self.file_path+self.default_file+self.file_extention
                    rospy.loginfo("Audio file not found\n")

                # load and play file
                print(self.file_extention)
                print(file_full_name)
                s = mixer.Sound(file_full_name)
                rospy.loginfo("Audio file loaded\n")
                # mixer.Sound.play(s)
                s.play(loops=0, maxtime=0, fade_ms=0)
                rospy.loginfo("Audio file played\n")
                # wait for file to finish
                while mixer.get_busy():
                    # pygame.time.Clock().tick(10)
                    rospy.loginfo("Playing audio file\n")
                    self.busy = True
                    self.publish_result()
            self.publish_result()
            rate.sleep()

        mixer.quit()

    def callback(self, msg):
        self.new_file = msg.data
        rospy.loginfo("Received new file:"+msg.data)

    def publish_result(self):
        self.pub_.publish(self.busy)

    def shutdown(self):
        # message executed after Ctrl+C is pressed
        rospy.loginfo("Stopping mp3_player node")


if __name__ == "__main__":
    start = player()
