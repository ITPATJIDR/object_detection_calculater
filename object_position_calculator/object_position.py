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
from coordinate_calculator import CoordinateCalculator2
from newCalculator import newCoordinateCalculator

sio = socketio.Client()
lat, lng, heading, altitude, pitch, fov_h, fov_v = None, None, None, None, None, None, None

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
    global lat, lng, heading, altitude, pitch, fov_h, fov_v
    lat = data.get("lat")
    lng = data.get("lng")
    heading = data.get("heading")
    altitude = data.get("altitude")
    pitch = data.get("pitch")
    fov_v = data.get("fov_vertical")
    fov_h = data.get("fov_horizontal")
    
    print(f'[{room}] Received data to yolo: {data}')
    
    # do anything from this for calculation of estimation 
    return lat, lng, heading, altitude, pitch, fov_h, fov_v



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
        print(lat, lng, heading, altitude, pitch, fov_v)
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
            image_width, image_height = 640, 640  # Image resolution
            x, y = detected

            # Define the size of the bounding box (example: width=50, height=50)
            width, height = 50, 50
            top_left = (x - width // 2, y - height // 2)
            bottom_right = (x + width // 2, y + height // 2)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)  # Green color, thickness=2
            text_position = (top_left[0], top_left[1] - 40)  # Position the text above the top-left corner
            cv2.putText(image, f"Position", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            
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

            
            # #Output the calculated results
            # print("=== CoordinateCalculator Results ===")
            # print(f"Ground Coordinates of G: ({lat}, {lng})")
            # print(f"New Coordinates of P: ({x_new:.6f}, {y_new:.6f})")
            # print(f"Distance in Pixels: {distance_pf_pixels:.2f} px")
            # print(f"Distance in Meters: {distance_pf_meters:.2f} m")
            # print(f"Bearing from Image Center: {bearing_from_center:.2f} degrees")
            # print(f"New Coordinates of F: ({xf_new:.6f}, {yf_new:.6f})")
            
            # calculator2 = CoordinateCalculator2(
            #     angle=pitch,
            #     bearing=heading,
            #     height=altitude,
            #     gps_x=lat,
            #     gps_y=lng,
            #     image_width=image_width,
            #     image_height=image_height,
            #     detected_x=x,
            #     detected_y=y,
            #     fov=fov_h
            # )

            # #Perform the main calculation
            # results = calculator2.calculate()

            # # Output the calculated results
            
            # print(f"CoordinateCalculator Results1")
            # print(f"Ground Coordinates of G: {results['Ground Coordinates of G']}")
            # print(f"New Coordinates of P: {results['New Coordinates of P']}")
            # print(f"Distance in Pixels: {results['Distance in Pixels']:.2f} px")
            # print(f"Distance in Meters: {results['Distance in Meters']:.2f} m")
            # print(f"Bearing from Image Center: {results['Delta Bearing']:.2f} degrees")
            # print(f"New Coordinates of F: {results['New Coordinates of F']}")
            # print("\n")
            calculator = newCoordinateCalculator(
                angle=pitch,                # มุมกล้อง
                height=altitude,              # ความสูงของกล้อง (เมตร)
                gps_lat=lat,       # ละติจูดจุด G
                gps_lon=lng,      # ลองจิจูดจุด G
                image_width=image_width,         # ความกว้างของภาพ
                image_height=image_height,        # ความสูงของภาพ
                detected_x=x,          # พิกัด X ของจุด F ในภาพ
                detected_y=y,          # พิกัด Y ของจุด F ในภาพ
                fov =fov_h,
                bearing=heading
            )
            
            results2 = calculator.calculate_coordinates()
            print("Calculation Results2:")
            print(f"GPS Latitude, Longitude: {calculator.gps_lat}, {calculator.gps_lon}")
            print(f"1. Principle Distance (P): {results2['principle_distance']:.2f} meters")
            print(f"2. Horizontal Distance (d): {results2['horizontal_distance']:.2f} meters")
            print(f"3. Coordinates of Point P: Latitude {results2['coordinates_p'][0]:.15f}, Longitude {results2['coordinates_p'][1]:.15f}")
            print(f"4. Coordinates of Point F: Latitude {results2['coordinates_f'][0]:.15f}, Longitude {results2['coordinates_f'][1]:.15f}")
            print(f"5. Distance between G and F: {results2['distance_gf']:.2f} meters")
            print(f"6. Bearing Offset to Point F: {results2['bearing_offset']:.2f} degrees")
            
            text_position_1 = (top_left[0], top_left[1] - 10)  # Position the text above the top-left corner
            cv2.putText(image, f"({results2['coordinates_f'][0]:.15f}, {results2['coordinates_f'][1]:.15f})", text_position_1, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            text_position = (top_left[0], bottom_right[1] + 20)  # Position the text below the bottom-right corner
            cv2.putText(image, f"5. Distance between G and F: {results2['distance_gf']:.2f} meters", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        
        SAVE_DETECTION_FOLDER = 'detected_images'
        detect_image = SAVE_DETECTION_FOLDER + "/" +"dectect_image_" + timestamp + ".png"
        cv2.imshow("Image with Bounding Boxes", image)
        cv2.imwrite(detect_image, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        image = cv2.imread(detect_image)
        success, encoded_image = cv2.imencode('.png', image)

        if success:
            # Convert the encoded buffer to a bytes array
            image_bytes = encoded_image.tobytes()
            print(f"Image converted to bytes array: {image_bytes[:20]}...")  # Display first 20 bytes as a sample
        else:
            print("Error encoding image.")
        
        
# Connect to the server
server_url = "http://10.109.68.49:8000"
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

