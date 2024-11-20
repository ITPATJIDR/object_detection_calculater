import base64
import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
import socketio

# Assuming you have socketio instance
sio = socketio.Client()

class YOLOTracker:
    def __init__(self, model_path="yolo11n.pt"):
        # Load the YOLO model
        self.model = YOLO(model_path)
        self.track_history = defaultdict(lambda: [])

    def process_image(self, image_byte_array):
        # Convert the byte array to a base64 string
        image_base64 = base64.b64encode(bytes(image_byte_array)).decode('utf-8')
        
        # Decode the base64 image into an OpenCV image
        img_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("Error: Could not decode image")
            return None
        
        # Display the image
        cv2.imshow("Captured Image", frame)

        
        # Wait for a key press to close the window (use a small delay to update in real-time)
        cv2.waitKey(1)

        return frame  # Optionally return the frame if further processing is needed


    def encode_image_to_base64(self, frame):
        """Encode an OpenCV frame into a base64 string."""
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode("utf-8")

