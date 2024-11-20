import numpy as np

def position_calculator(camera_matrix, bounding_box, drone_gps, altitude, pitch_angle):
    """
    Calculate the GPS coordinates of an object detected by a UAV using a monocular camera.
    
    Parameters:
    - camera_matrix: Intrinsic camera matrix (3x3 numpy array).
    - bounding_box: Tuple (xmin, ymin, xmax, ymax) from YOLO detection.
    - drone_gps: Tuple (latitude, longitude) of the drone's GPS.
    - altitude: Current altitude of the drone (in meters).
    - pitch_angle: Camera pitch angle in degrees.

    Returns:
    - Tuple (latitude, longitude) of the detected object.
    """
    # Extract bounding box details
    xmin, ymin, xmax, ymax = bounding_box
    
    # Calculate foot coordinates (xf, yf)
    xf = 0.5 * (xmin + xmax)
    yf = ymax

    # Normalize image coordinates
    fx, fy, cx, cy = camera_matrix[0, 0], camera_matrix[1, 1], camera_matrix[0, 2], camera_matrix[1, 2]
    xn = (xf - cx) / fx
    yn = (yf - cy) / fy

    # Calculate depth of the principal point
    zp = altitude / np.cos(np.radians(pitch_angle))

    # Calculate 3D camera coordinates
    xc = xn * zp
    yc = yn * zp
    zc = zp

    # Rotate camera coordinates to body frame
    xc_body = xc * np.cos(np.radians(pitch_angle)) + zc * np.sin(np.radians(pitch_angle))
    zc_body = -xc * np.sin(np.radians(pitch_angle)) + zc * np.cos(np.radians(pitch_angle))
    
    # Convert to ENU coordinates
    enu_x = xc_body
    enu_y = yc
    enu_z = zc_body

    # Calculate bearing and distance
    distance = np.sqrt(enu_x**2 + enu_y**2)
    bearing = np.arctan2(enu_x, enu_y)

    # Convert ENU to GPS corrections
    R = 6378137  # Radius of Earth in meters
    dlat = distance * np.cos(bearing) / R
    dlon = distance * np.sin(bearing) / (R * np.cos(np.radians(drone_gps[0])))

    # Calculate final GPS coordinates
    obj_lat = drone_gps[0] + np.degrees(dlat)
    obj_lon = drone_gps[1] + np.degrees(dlon)

    return obj_lat, obj_lon

# Example usage
camera_matrix = np.array([[1000, 0, 320],
                          [0, 1000, 240],
                          [0, 0, 1]])

bounding_box = (50, 150, 200, 300)  # Example YOLO bounding box
drone_gps = (12.9866, 77.6693)  # Example GPS location
altitude = 100  # Drone altitude in meters
pitch_angle = 10  # Camera pitch angle in degrees

object_gps = position_calculator(camera_matrix, bounding_box, drone_gps, altitude, pitch_angle)
print("Object GPS Coordinates:", object_gps)
