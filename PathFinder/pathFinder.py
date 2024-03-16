from ultralytics import YOLO, utils, models

import torch
import cv2


# Folder Paths
testImageFolder = "path/to/your/images/folder"  # Folder containing images
imageFolder = "path/to/your/images/folder"  # Folder containing images
weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/best.pt"  # Path to your YOLOv8 weights file
outputFolder = "path/to/output/folder"  # Folder to save output images
outputTestFolder = "path/to/output/folder"  # Optional: Folder to save output images
img='/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/test3.jpg'

def detectPathsOnImage(imgPath):
    """Detects paths on an image and displays it with bounding boxes in a resized window."""
    model = YOLO(weightsPath)
    results = model.predict(imgPath)
    print(results)
    result = results[0]

    img = cv2.imread(imgPath)

    # Set desired window size (replace with your preferred width and height)
    window_width = 800
    window_height = 600
    cv2.namedWindow("Image with Paths", cv2.WINDOW_NORMAL)  # Enable window resizing
    cv2.resizeWindow("Image with Paths", window_width, window_height)

    for box in result.boxes:
        x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]  # Convert to integers for cv2
        label = f"{result.names[box.cls[0].item()]}: {round(box.conf[0].item(), 2)}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green bounding box
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Label above box

    cv2.imshow("Image with Paths", img)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()

detectPathsOnImage(img)
