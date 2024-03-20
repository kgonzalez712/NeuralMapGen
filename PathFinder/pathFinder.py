from ultralytics import YOLO, utils, models

import torch
import cv2
import os

#Class Types
classType = {
  '0': "Closed Path",
  '1': "Semi Open Path",
  '2': "Open Path"
}

# Folder Paths
testImageFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages/"  # Folder containing images
imageFolder = "path/to/your/images/folder"  # Folder containing images
weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/bestTS4.pt"  # Path to your YOLOv8 weights file
outputFolder = "path/to/output/folder"  # Folder to save output images
outputTestFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/outputTest"  # Optional: Folder to save output images
img='/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages/test2.jpg'

def getClassType(number):
  #Returns the string associated with the number, or None if not found.
  return classType.get(number)

def decimal_to_percent(decimal):
  #Converts a decimal number to a percentage string.
  return str(decimal * 100) + "%"

def calculate_center(coordinates):
  """
  Calculates the center point of a rectangle given its corner coordinates.

  Args:
      coordinates: A list or array containing the x1, y1, x2, y2 coordinates
                   of the rectangle in the order [x1, y1, x2, y2].

  Returns:
      A list containing the center coordinates (x_center, y_center).
  """

  if len(coordinates) != 4:
    raise ValueError("Invalid number of coordinates. Expected 4 (x1, y1, x2, y2).")

  x1, y1, x2, y2 = coordinates
  x_center = (x1 + x2) / 2
  y_center = (y1 + y2) / 2
  return [round(x_center), round(y_center)]

def detectPathsOnImage(imgPath):
    #Detects paths on an image and displays it with bounding boxes.
    model = YOLO(weightsPath)
    results = model.predict(imgPath)
    
    result = results[0]
    box = result.boxes[0]
    img = cv2.imread(imgPath)

    # Set desired window size (replace with your preferred width and height)
    window_width = 800
    window_height = 600
    cv2.namedWindow("Image with Paths", cv2.WINDOW_NORMAL)  # Enable window resizing
    cv2.resizeWindow("Image with Paths", window_width, window_height)

    for box in result.boxes:
        class_id = getClassType(result.names[box.cls[0].item()])
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = decimal_to_percent(float(round(box.conf[0].item(), 2)))
        print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Center:", calculate_center(cords))
        print("Probability:", conf)
        x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]  # Convert to integers for cv2
        label = f"{result.names[box.cls[0].item()]}: {round(box.conf[0].item(), 2)}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green bounding box
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)  # Label above box
        print("---")


    # Save modified image
    outputPath = f"{outputTestFolder}/modified_{os.path.basename(imgPath)}"
    cv2.imwrite(outputPath, img)
    print(f"Image saved to: {outputPath}")

# Process all images in the folder (optional)
for filename in os.listdir(testImageFolder):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Check for image extensions
        full_path = os.path.join(testImageFolder, filename)
        detectPathsOnImage(full_path)

# Or process a specific image (replace with your image path)
# detectPathsOnImage("/path/to/your/specific/image.jpg")

detectPathsOnImage(img)
