import os
import configparser
from ultralytics import YOLO, utils, models
import cv2
import torch

#Config file
configFile = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/config.ini"

#Class Types
classType = {
  '0': "Closed Path",
  '1': "Semi Open Path",
  '2': "Open Path"
}

imageFolder = ""
weightsPath = ""
outputFolder = ""


def read_config(configFile):
    #Reads configuration parameters from a file.
    config = configparser.ConfigParser()
    config.read(configFile)
    imageFolder = config['DEFAULT']['imageFolder']
    weightsPath = config['DEFAULT']['weightsPath']
    outputFolder = config.get('DEFAULT', 'outputFolder', fallback='')
    


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

def detectPathsOnImagesInFolder(folderPath):
    """Detects paths on images within a folder and saves modified images with bounding boxes."""
    model = YOLO(weightsPath)  # Load the model once for efficiency

    for filename in os.listdir(folderPath):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Check for image extensions
            full_path = os.path.join(folderPath, filename)
            results = model.predict(full_path)  # Predict on each image
            result = results[0]

            img = cv2.imread(full_path)

            for box in result.boxes:
                class_id = getClassType(result.names[box.cls[0].item()])
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                conf = decimal_to_percent(float(round(box.conf[0].item(), 2)))
                print("Object type:", class_id)
                print("Coordinates:", cords)
                print("Center:", calculate_center(cords))
                print("Probability:", conf)
                x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]
                label = f"{result.names[box.cls[0].item()]}: {round(box.conf[0].item(), 2)}"
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                print("---")

            # Save modified image (replace with your desired output path)
            output_path = f"{outputFolder}/modified_{os.path.basename(full_path)}"
            cv2.imwrite(output_path, img)
            print(f"Image saved to: {output_path}")

# Or process a specific image (replace with your image path)
# detectPathsOnImage("/path/to/your/specific/image.jpg")
read_config(configFile)
detectPathsOnImagesInFolder(imageFolder)
