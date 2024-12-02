import math

class PixelToMeterConverter:
    def __init__(self, height, fov, image_width, image_height):
        """
        Initialize the converter with camera properties.
        
        :param height: Altitude of the camera in meters
        :param fov: Horizontal field of view in degrees
        :param image_width: Width of the image in pixels
        :param image_height: Height of the image in pixels
        """
        self.height = height
        self.fov = fov
        self.image_width = image_width
        self.image_height = image_height

    def pixels_to_meters(self, x_pixels, y_pixels):
        """
        Convert pixel coordinates to real-world distances in meters.
        
        :param x_pixels: X coordinate in pixels
        :param y_pixels: Y coordinate in pixels
        :return: Tuple (x_meters, y_meters) representing distances in meters
        """
        # Calculate pixel-to-meter ratios for horizontal and vertical axes
        pixel_scale_x = (self.height * math.tan(math.radians(self.fov) / 2)) / (self.image_width / 2)
        pixel_scale_y = (self.height * math.tan(math.radians(self.fov) / 2)) / (self.image_height / 2)
        
        # Convert pixel coordinates to meters
        x_meters = x_pixels * pixel_scale_x
        y_meters = y_pixels * pixel_scale_y
        return x_meters, y_meters

# Example Usage
if __name__ == "__main__":
    height = 50  # Camera height in meters
    fov = 90  # Field of view in degrees
    image_width = 1920  # Image width in pixels
    image_height = 1080  # Image height in pixels
    x_pixels = 691  # X coordinate in pixels
    y_pixels = 1228  # Y coordinate in pixels

    converter = PixelToMeterConverter(height, fov, image_width, image_height)
    x_meters, y_meters = converter.pixels_to_meters(x_pixels, y_pixels)
    
    print(f"X distance in meters: {x_meters:.2f}")
    print(f"Y distance in meters: {y_meters:.2f}")
