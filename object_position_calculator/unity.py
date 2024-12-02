import math
import json

# Constants
EARTH_RADIUS = 6371000  # Radius of Earth in meters

# Function to convert degrees to radians
def to_radians(degrees):
    return degrees * math.pi / 180.0

# Function to calculate the 2D distance using Haversine formula
def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitudes and longitudes from degrees to radians
    phi1 = to_radians(lat1)
    phi2 = to_radians(lat2)
    delta_phi = to_radians(lat2 - lat1)
    delta_lambda = to_radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in meters
    return EARTH_RADIUS * c

# Function to calculate 3D distance if height is known for both points
def euclidean_distance(lat1, lon1, h1, lat2, lon2, h2):
    # Convert lat/lon to radians and then to XYZ coordinates
    x1, y1, z1 = lat_lon_to_xyz(lat1, lon1, h1)
    x2, y2, z2 = lat_lon_to_xyz(lat2, lon2, h2)
    
    # Euclidean distance formula
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Convert latitude, longitude, and height to XYZ coordinates
def lat_lon_to_xyz(lat, lon, h):
    # Earth's radius in meters
    R = EARTH_RADIUS + h
    phi = to_radians(lat)
    lambda_ = to_radians(lon)
    
    # Convert to XYZ coordinates
    x = R * math.cos(phi) * math.cos(lambda_)
    y = R * math.cos(phi) * math.sin(lambda_)
    z = R * math.sin(phi)
    
    return x, y, z