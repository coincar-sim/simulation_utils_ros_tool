#!/usr/bin/env python

# ROS Dependencies
import roslib
import rospy
import tf
import tf2_ros
import geometry_msgs.msg

# Regular Python Dependencies
import pyproj


stb = None
static_transform = None


def get_zone(lon, lat):
    if 56 <= lat < 64 and 3 <= lon < 12:
        return 32
    if 72 <= lat < 84 and 0 <= lon < 42:
        if lon < 9:
            return 31
        elif lon < 21:
            return 33
        elif lon < 33:
            return 35
        return 37
    return int((lon + 180) / 6) + 1


def ll2xy(lat, lon):
    zone_ = get_zone(lon, lat)
    p = pyproj.Proj(proj='utm', zone=zone_, ellps='WGS84')
    [x, y] = p(lon, lat, errcheck=True)
    return [x, y]


def timer_callback(event):
    global stb, static_transform
    static_transform.header.stamp = rospy.Time.now()
    stb.sendTransform(static_transform)


if __name__ == '__main__':

    rospy.init_node( 'static_utm_tf_publisher' )

    child_lat = rospy.get_param("~child_lat")
    child_lon = rospy.get_param("~child_lon")

    tf_frame_id_utm_base = rospy.get_param("~tf_frame_id_utm_base")
    tf_frame_id_child = rospy.get_param("~tf_frame_id_child")

    pub_frequ = rospy.get_param("~publishing_frequency")

    stb = tf2_ros.TransformBroadcaster()

    static_transform = geometry_msgs.msg.TransformStamped()
    static_transform.header.stamp = rospy.Time.now()
    static_transform.header.frame_id = tf_frame_id_utm_base
    static_transform.child_frame_id = tf_frame_id_child
    [utm_x, utm_y] = ll2xy(child_lat, child_lon)
    static_transform.transform.translation.x = utm_x
    static_transform.transform.translation.y = utm_y
    static_transform.transform.translation.z = 0.0
    q = tf.transformations.quaternion_from_euler(0, 0, 0)
    static_transform.transform.rotation.x = q[0]
    static_transform.transform.rotation.y = q[1]
    static_transform.transform.rotation.z = q[2]
    static_transform.transform.rotation.w = q[3]

    rospy.Timer(rospy.Duration(1./float(pub_frequ)), timer_callback)

    rospy.spin()
