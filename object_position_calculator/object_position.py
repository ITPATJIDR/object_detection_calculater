import socketio
import cv2
import numpy as np
import base64
from detect_object import YOLOTracker
import os
from datetime import datetime
import time
from PIL import Image
import io
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
# from calculate import CoordinateCalculator
from coordinate_calculator import CoordinateCalculator2
sio = socketio.Client()

lat, lng, heading, altitude, pitch, fov_h = None, None, None, None, None, None

def render_image_from_base64(base64_image):
    # image_data = base64.b64decode(base64_image)

    # # Convert bytes into a NumPy array
    # nparr = np.frombuffer(image_data, np.uint8)

    # # Decode the NumPy array into an OpenCV image
    # image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # # Display the image using OpenCV
    # cv2.imshow("Decoded Image", image)

    # # Wait for a key press and close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    ...


# Define event handlers
@sio.event
def connect():
    print("Connected to server!")
    # Example: Join a room upon connection
    room = "drone"
    sio.emit("join", {"room": room})
    print(f"Joined room: {room}")


@sio.event
def disconnect():
    print("Disconnected from server!")


# @sio.on("response_drone")
# def on_response_drone(data):
#     print(f"Drone response: {data}")


# @sio.on("response_user")
# def on_response_user(data):
#     print(f"User response: {data}")


@sio.on("response_geo_drone")
def data_to_yolo(data):
    room = data.get("room")
    # geo drone data
    global lat, lng, heading, altitude, pitch, fov_h
    lat = data.get("lat")
    lng = data.get("lng")
    heading = data.get("heading")
    altitude = data.get("altitude")
    pitch = data.get("pitch")
    fov_v = data.get("fov_vertical")
    fov_h = data.get("fov_horizontal")
    
    print(f'[{room}] Received data to yolo: {data}')
    
    # do anything from this for calculation of estimation 
    return lat, lng, heading, altitude, pitch, fov_h



@sio.on("captured_image")
def on_captured_image(data):

        # # Extract geospatial data
        # lat, lng, heading, altitude, pitch, fov_h = data_to_yolo(data)

        # Process image data
        image_byte_array = data.get("image_byte_array")
        if not image_byte_array:
            print("Error: No image byte array received.")
            return

        # Save the image locally
        SAVE_FOLDER = 'received_images'
        os.makedirs(SAVE_FOLDER, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_filename = os.path.join(SAVE_FOLDER, f'image_{timestamp}.png')

        image = Image.open(io.BytesIO(image_byte_array))
        image.save(image_filename)
        print(f"Image saved to {image_filename}")

        print("\n")
        print("Drone geo data")
        print(lat, lng, heading, altitude, pitch, fov_h)
        print("\n")
        
        # Run object detection
        tracker = YOLOTracker()
        detections = tracker.process_image(image_filename)
        
        print("\n")
        print("Detections", detections)
        print("\n")
        
        image = cv2.imread(image_filename)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Process each detection
        for detected in detections:
            image_width, image_height = 50, 50  # Image resolution
            x, y = detected

            # Define the size of the bounding box (example: width=50, height=50)
            width, height = 50, 50
            top_left = (x - width // 2, y - height // 2)
            bottom_right = (x + width // 2, y + height // 2)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Green color, thickness=2

            
            # Instantiate the CoordinateCalculator with necessary parameters
            # pixel_to_meter_ratio = 0.01  # Example ratio: 1 pixel = 0.01 meters
            # calculator = CoordinateCalculator(
            #     angle_deg=pitch,
            #     bearing_deg=heading,
            #     height=altitude,
            #     gps_lat=lat,
            #     gps_lng=lng,
            #     image_size=(image_width, image_height),
            #     detected_x=x,
            #     detected_y=y,
            #     pixel_to_meter_ratio=pixel_to_meter_ratio
            # )

            # x_new, y_new, distance_pf_pixels, distance_pf_meters, bearing_from_center, xf_new, yf_new = calculator.main()

            
            #Output the calculated results
            print("=== CoordinateCalculator Results ===")
            print(f"Ground Coordinates of G: ({lat}, {lng})")
            print(f"New Coordinates of P: ({x_new:.6f}, {y_new:.6f})")
            print(f"Distance in Pixels: {distance_pf_pixels:.2f} px")
            print(f"Distance in Meters: {distance_pf_meters:.2f} m")
            print(f"Bearing from Image Center: {bearing_from_center:.2f} degrees")
            print(f"New Coordinates of F: ({xf_new:.6f}, {yf_new:.6f})")
            
            calculator2 = CoordinateCalculator2(
                angle=pitch,
                bearing=heading,
                height=altitude,
                gps_x=lat,
                gps_y=lng,
                image_width=image_width,
                image_height=image_height,
                detected_x=x,
                detected_y=y,
                fov=fov_h
            )

            # Perform the main calculation
            results = calculator2.calculate()

            # Output the calculated results
            
            print(f"CoordinateCalculator Results")
            print(f"Ground Coordinates of G: {results['Ground Coordinates of G']}")
            print(f"New Coordinates of P: {results['New Coordinates of P']}")
            print(f"Distance in Pixels: {results['Distance in Pixels']:.2f} px")
            print(f"Distance in Meters: {results['Distance in Meters']:.2f} m")
            print(f"Bearing from Image Center: {results['Delta Bearing']:.2f} degrees")
            print(f"New Coordinates of F: {results['New Coordinates of F']}")
            print("\n")
            
        cv2.imshow("Image with Bounding Boxes", image)
        cv2.imwrite("test.png", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
# Connect to the server
server_url = "http://192.168.0.141:8000"
try:
    sio.connect(server_url)
    print(f"Connected to {server_url}")
except Exception as e:
    print(f"Failed to connect: {e}")

# Example: Sending messages to the server


def send_message_to_server(message="test message from yolo"):
    room = "drone"
    sio.emit("response_from_yolo", {"room": room, "message": message})
    print("Sent message to server.")


def send_drone_command(command, params=""):
    room = "drone"
    # example command
    # 1"
    # command: "goto_position"
    # params: "barn#2
    # 2"
    # command: "go_nearest"
    # params: "barn"
    # 3"
    # command: "capture_img"
    # params: ""
    sio.emit("send_command", {"room": room,
             "command": command, "params": params, "requester": "yolo"})
    print("Sent drone command.")

# Example: Send image bytes (base64 encoded)


def send_image(image_bytes):
    room = "drone"
    # Simulate image bytes (replace with actual data in real usage)
    image_bytes = b"example_image_bytes"
    sio.emit("send_image", {"room": room, "image_bytes": image_bytes})
    print("Sent image bytes.")


# Interact with the server
send_message_to_server("Hello, world from YOLO!")
send_drone_command("capture_img")
# send_image("test_image_bytes")

# Wait for interactions
sio.wait()

