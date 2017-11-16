#!/usr/bin/env python

# ROS Dependencies
import roslib
import rospy
import sensor_msgs.msg

publisher = None
nav_sat_msg = None


def timer_callback(event):
    global publisher, nav_sat_msg
    nav_sat_msg.header.stamp = rospy.Time.now()
    publisher.publish(nav_sat_msg)


if __name__ == '__main__':

    rospy.init_node( 'static_nav_sat_fix_publisher' )

    frame_lat = rospy.get_param("~frame_lat")
    frame_lon = rospy.get_param("~frame_lon")
    frame_alt = rospy.get_param("~frame_alt")

    tf_frame_id = rospy.get_param("~tf_frame_id")
    # from http://docs.ros.org/api/sensor_msgs/html/msg/NavSatFix.html
    # header.frame_id is the frame of reference reported by the satellite
    #        receiver, usually the location of the antenna.  This is a
    #        Euclidean frame relative to the vehicle, not a reference
    #        ellipsoid.
    # -> here, frame_id is the frame that originates in upper lat lon
    #    [lat,lon]_{WGS84} <-> [0,0]_{frame_id}
    # -> a tf transformation from mercator_base to frame_id has to be published
    #    separately

    pub_frequ = rospy.get_param("~publishing_frequency")

    nav_sat_fix_topic = rospy.get_param("~nav_sat_fix_topic")
    publisher = rospy.Publisher( nav_sat_fix_topic, sensor_msgs.msg.NavSatFix, queue_size=6 )

    nav_sat_msg = sensor_msgs.msg.NavSatFix()
    nav_sat_msg.header.stamp = rospy.Time.now()
    nav_sat_msg.header.frame_id = tf_frame_id
    nav_sat_msg.status.status = -1
    nav_sat_msg.status.service = 1
    nav_sat_msg.latitude = frame_lat
    nav_sat_msg.longitude = frame_lon
    nav_sat_msg.altitude = frame_alt
    nav_sat_msg.position_covariance_type = 0

    rospy.Timer(rospy.Duration(1./float(pub_frequ)), timer_callback)

    rospy.spin()
