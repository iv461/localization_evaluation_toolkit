import pandas as pd
import numpy as np
import sys
import rosbag2_py
from scipy.spatial.transform import Rotation as R

from rcl_interfaces.msg import Log
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


def read_ros2bag(bag_file, param):

    bag_path = str(bag_file)
    storage_options = rosbag2_py.StorageOptions(uri=bag_path, storage_id=param.bag_id)
    converter_options = rosbag2_py.ConverterOptions(input_serialization_format=param.bag_format, output_serialization_format=param.bag_format)

    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)
    topic_types = reader.get_all_topics_and_types()

    type_map = {topic_types[i].name: topic_types[i].type for i in range(len(topic_types))}

    storage_filter = rosbag2_py.StorageFilter(topics=[param.topic])
    reader.set_filter(storage_filter)

    i = 0
    while reader.has_next():
        (topic, data, t) = reader.read_next()
        msg_type = get_message(type_map[topic])
        msg = deserialize_message(data, msg_type)
        
        param.df_temp.at[i, "time"] = (msg.header.stamp.sec)+(msg.header.stamp.nanosec) / 10**9
        param.df_temp.at[i, "x"] = msg.pose.pose.position.x
        param.df_temp.at[i, "y"] = msg.pose.pose.position.y
        param.df_temp.at[i, "z"] = msg.pose.pose.position.z
        q_temp = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        e_temp = R.from_quat([q_temp[0], q_temp[1], q_temp[2], q_temp[3]])
        param.df_temp.at[i, "roll"] = e_temp.as_euler("ZYX", degrees=False)[2]
        param.df_temp.at[i, "pitch"] = e_temp.as_euler("ZYX", degrees=False)[1]
        param.df_temp.at[i, "yaw"] = e_temp.as_euler("ZYX", degrees=False)[0]
        i += 1