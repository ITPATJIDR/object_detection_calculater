from ultralytics import YOLO
import time
import cv2

if __name__ == '__main__':
    # Load the YOLO model
    model = YOLO("best.pt")
    
    # Define image path
    path1 = rf"received_images\freefire_2567-11-05_16-35-14.png"
    
    # Read the frame from the image
    frame = cv2.imread(path1)

    if frame is None:
        print("Frame image not found")
        exit()

    # Perform the object detection
    result = model.predict(frame, show=True, stream=False)

    # Extract the bounding boxes from the first result in the list
    boxes = result[0].boxes.xyxy  # Bounding box coordinates (x_min, y_min, x_max, y_max)
    
    # Extract the center coordinates of each bounding box
    for box in boxes:
        x_min, y_min, x_max, y_max = box
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        print(f"Detected object at coordinates: x = {center_x}, y = {center_y}")

    # Display the result in fullscreen
    cv2.namedWindow("Object Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Object Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Draw the bounding boxes on the frame
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Show the frame with bounding boxes
    cv2.imshow("Object Detection", frame)

    # Wait for a key press to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
