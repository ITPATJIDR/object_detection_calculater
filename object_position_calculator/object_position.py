import socketio
import cv2
import numpy as np
import base64
from detect_object import YOLOTracker
import os

# Create a Socket.IO client instance
sio = socketio.Client()

def render_image_from_base64(base64_image):
    image_data = base64.b64decode(base64_image)

    # Convert bytes into a NumPy array
    nparr = np.frombuffer(image_data, np.uint8)

    # Decode the NumPy array into an OpenCV image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Display the image using OpenCV
    cv2.imshow("Decoded Image", image)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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

@sio.on("response")
def on_response(data):
    print(f"Response from server: {data}")

@sio.on("response_drone")
def on_response_drone(data):
    print(f"Drone response: {data}")

@sio.on("response_user")
def on_response_user(data):
    print(f"User response: {data}")


@sio.on("captured_image")
def on_captured_image(data):
    print("Captured image data received.")
    tracker = YOLOTracker()
    
    # Get the image byte array from the data
    image_byte_array = data.get("image_byte_array")
    
    if image_byte_array:
        print("Image byte array received.")
        
        # Convert the byte array to a NumPy array and then decode it into an image
        np_arr = np.frombuffer(image_byte_array, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is not None:
            # Define the folder to save images
            SAVE_FOLDER = 'received_images'
            os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure folder exists
            
            # Create a filename with a unique timestamp or index to avoid overwriting
            image_filename = os.path.join(SAVE_FOLDER, 'received_image.png')
            
            # Save the decoded image to the specified path
            cv2.imwrite(image_filename, frame)
            print(f"Image saved to {image_filename}")
            
            # Optionally, process the image using YOLO model
            annotated_frame = tracker.process_image(image_byte_array)
        else:
            print("Error: Could not decode image.")
    else:
        print("Error: No image byte array received.")


# Connect to the server
server_url = "http://10.109.68.49:8000"
try:
    sio.connect(server_url)
    print(f"Connected to {server_url}")
except Exception as e:
    print(f"Failed to connect: {e}")

# Example: Sending messages to the server
def send_message_to_server():
    room = "drone"
    message = "Hello from the client!"
    sio.emit("message_to_gpt", {"room": room, "message": message})
    print("Sent message to server.")

def send_drone_command():
    room = "drone"
    command = "takeoff"
    sio.emit("send_command", {"room": room, "command": command})
    print("Sent drone command.")

# Example: Send image bytes (base64 encoded)
def send_image():
    room = "drone"
    # Simulate image bytes (replace with actual data in real usage)
    image_bytes = b"example_image_bytes"
    sio.emit("send_image", {"room": room, "image_bytes": image_bytes})
    print("Sent image bytes.")

# Interact with the server
send_message_to_server()
send_drone_command()
send_image()

# Wait for interactions
sio.wait()
