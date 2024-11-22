from calculate2 import CoordinateCalculator2
from calculate import CoordinateCalculator
angle = 30  # degrees
bearing = 45  # degrees
height = 25  # meters
gps_x, gps_y = 50.0, 100.0  # Coordinates
image_width, image_height = 640, 640  # Image dimensions
detected_x, detected_y = 219.15426635742188, 439.4124755859375  # Detected point
fov = 90  # Field of View in degrees (used by CoordinateCalculator2)
pixel_to_meter_ratio = 0.01  # Fixed ratio for CoordinateCalculator

# Calculator 2
calculator2 = CoordinateCalculator2(
    angle=angle, bearing=bearing, height=height, gps_x=gps_x, gps_y=gps_y,
    fov=fov, image_width=image_width, image_height=image_height,
    detected_x=detected_x, detected_y=detected_y
)
results2 = calculator2.calculate()

# Calculator 1
calculator1 = CoordinateCalculator(
    angle_deg=angle, bearing_deg=bearing, height=height,
    gps_lat=gps_x, gps_lng=gps_y, image_size=(image_width, image_height),
    detected_x=detected_x, detected_y=detected_y, pixel_to_meter_ratio=pixel_to_meter_ratio
)
results1 = calculator1.main()

# Compare results
print("=== CoordinateCalculator2 Results ===")
for key, value in results2.items():
    print(f"{key}: {value}")

print("\n=== CoordinateCalculator Results ===")
for key, value in results1.items():
    print(f"{key}: {value}")
