# simulation_utils_ros_tool

Small nodes providing basic functionality for the simulation framework.

Consists of

#### static_utm_tf_publisher
* launched via `launch/static_utm_tf_publisher.launch`
* publishes a static tf, based on a UTM transformation
  * e.g. from `utm_base` (UTM Coordinate System) to `map_center`
    (local UTM Coordinate System, with origin (0,0) in the point
    (map_center_lat, map_center_lon) of `utm_base`)

#### static_nav_sat_fix_publisher
* launched via `launch/static_nav_sat_fix_publisher.launch`
* publishes a static nav sat fix
  * used e.g. for rviz satellite
  * provides the information that `map_center` (defined with the tf publisher above)
    has (lat,lon)-coordinates (map_center_lat, map_center_lon)

#### nav_sat_fix_launchfile_publisher
* launched via `launch/nav_sat_fix_launchfile_publisher.launch`
* publishes a static nav sat fix
* similar to `static_nav_sat_fix_publisher` but launchfile-only, using `rostopic pub`

#### pose_stamped_launchfile_publisher
* launched via `launch/pose_stamped_launchfile_publisher.launch`
* publishes a pose with stamp=0 (= ros::Time::now)

## Installation
* this package is part of the simulation framework
* see simulation_management_ros_tool for installation and more details

## Usage
* use these nodes in your framework setup as in `simulation_initialization_ros_tool`

## License
Contact the maintainer.
