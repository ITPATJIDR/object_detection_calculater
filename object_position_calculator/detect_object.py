import base64
import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
import socketio
import time
import os
from PIL import Image


class YOLOTracker:
    def __init__(self):
        # Load the YOLO model
        self.model = YOLO("best.pt")
    
    def process_image(self, image_filename):
        # Open and process the image
        frame = Image.open(image_filename)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # # Convert image to numpy array for YOLO
        # frame = np.array(image)

        # Perform object detection
        result = self.model.predict(frame, show=True, stream=False, conf=0.1)

        # Assuming we want to extract the center coordinates of detected objects
        boxes = result[0].boxes.xyxy  # Bounding box coordinates (x_min, y_min, x_max, y_max)

        # Simulate detected coordinates (replace with actual object detection results)
        detected_coordinates = []

        for box in boxes:
            x_min, y_min, x_max, y_max = box
            center_x = int((x_min + x_max) / 2)
            center_y = int((y_min + y_max) / 2)
            detected_coordinates.append((center_x, center_y))

        return detected_coordinates