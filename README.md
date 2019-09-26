# Quadcopter with Image Processing system

Quadcopter with the mission of finding targets and performing autonomous
landings by flying based on the waypoints that have been set on the Mission Planner Ground Control
System (GCS). Quadcopter will look for targets using image processing systems.

The image processing system is created with a Raspberry PI and uses a 5 megapixel
camera module with a frame resolution of 1280x720 pixels. It uses the Python
programming language, OpenCV libraries and Dronekit-Python libraries. 

After thecamera successfully detects the object, the Raspberry Pi will send the command to
Pixhawk as a quadcopter controller to make landings on the target or base in the form
of red circles and have a size of 40 cm to 70 cm. With a flying altitude of 2 meters to
3 meters with a flying speed of 1 m/s to 5 m/s. 

After making the landing then the distance between the target center point with the quadcopter center point is measured.
Communication between Pixhawk and Raspberry Pi via the USB to Serial Interface
using the MAVlink protocol. As a result of image processing system detection, the
camera is able to detect the circles perfectly enough when converted to black and
white or image threshold. 

The camera is able to detect the target at a flying altitude of 2 meters to 3 meters at a speed of 1 m/s, but when the speed is adjusted to 5 m/s, the camera is only able to detect the target when the speed is 1 m/s to 3 m/s at an
altitude of 2 meters. At a flying altitude of 3 meters, the camera is only able to detect
at 1 m/s.
