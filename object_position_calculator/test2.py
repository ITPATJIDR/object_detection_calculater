import base64
import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO
import socketio
import time
import os

# Assuming you have a socketio instance
sio = socketio.Client()

class YOLOTracker:
    def __init__(self, model_path="yolo11n.pt", save_dir="./detected_images"):
        """
        Initialize the YOLO Tracker with a model path and save directory for detected images.

        :param model_path: Path to the YOLO model file.
        :param save_dir: Directory to save the detected images.
        """
        # Load the YOLO model
        self.model = YOLO(model_path)
        self.track_history = defaultdict(lambda: [])
        self.save_dir = save_dir

        # Create the save directory if it doesn't exist
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def process_image(self, image_byte_array):
        """
        Convert the byte array to an OpenCV frame and display it.

        :param image_byte_array: Image data as byte array.
        :return: OpenCV frame (image).
        """
        # Convert the byte array to a base64 string
        image_base64 = base64.b64encode(bytes(image_byte_array)).decode('utf-8')

        # Decode the base64 image into an OpenCV image
        img_data = base64.b64decode(image_base64)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(image_byte_array, cv2.IMREAD_COLOR)

        if frame is None:
            print("Error: Could not decode image")
            return None

        # Display the image
        cv2.imshow("Captured Image", frame)

        # Wait for a small delay (e.g., 1 ms) and close after a set period (e.g., 3 seconds)
        cv2.waitKey(1)
        time.sleep(3)  # Adding a delay of 3 seconds before closing

        # Close the window after waiting
        cv2.destroyAllWindows()

        return frame

    def encode_image_to_base64(self, frame):
        """
        Encode an OpenCV frame into a base64 string.

        :param frame: The OpenCV frame to encode.
        :return: Base64-encoded string of the image.
        """
        _, buffer = cv2.imencode('.jpg', frame)
        return base64.b64encode(buffer).decode("utf-8")

    def detect_objects(self, frame):
        """
        Perform object detection using YOLO on the frame.

        :param frame: The OpenCV frame to process.
        :return: Detection results.
        """
        # Perform detection using YOLO
        results = self.model(frame)
        return results

    def save_detection_results(self, results, frame):
        """
        Save the frame with detection results to the specified directory.

        :param results: YOLO detection results.
        :param frame: The original frame to save.
        :return: None
        """
        # Access the detection boxes and other information
        boxes = results[0].boxes  # results[0] is the first image in the batch (can be adjusted)

        # Loop through the detected boxes and draw bounding boxes
        for box in boxes:
            x_min, y_min, x_max, y_max = box.xyxy[0].tolist()  # Get the bounding box coordinates
            conf = box.conf[0].item()  # Get the confidence score
            cls = box.cls[0].item()  # Get the class ID
            label = results.names[int(cls)]  # Get class label

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (int(x_min), int(y_min)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the frame with bounding boxes to the custom directory
        output_path = os.path.join(self.save_dir, "output_image.jpg")
        cv2.imwrite(output_path, frame)  # Save the image with bounding boxes
        print(f"Image saved to: {output_path}")

    def send_detections(self, results):
        """
        Send the detection results over a Socket.IO connection.

        :param results: YOLO detection results.
        :return: None
        """
        sio.emit('detections', {'results': str(results)})

# Initialize the YOLO tracker
tracker = YOLOTracker(model_path="yolo11n.pt", save_dir="./detected_images")

# Simulated byte array (e.g., received from a socket or file)
with open("./received_images/received_image.png", "rb") as img_file:
    image_byte_array = img_file.read()

# Process the image
frame = tracker.process_image(image_byte_array)

# Perform YOLO detection if the frame was processed successfully
if frame is not None:
    results = tracker.detect_objects(frame)  # Perform detection using YOLO
    print("Detection Results:", results)

    # Save the detection results
    tracker.save_detection_results(results, frame)

    # Optionally send results over socket
    tracker.send_detections(results)
