import os
from ultralytics import YOLO
import cv2


#Class Types
classType = {
  '0': "Closed Path",
  '1': "Semi Open Path",
  '2': "Open Path"
}

class PathFinder:
    def __init__(self, weigthsPath, imagesPath, outputPath):
        """
        Initializes the PathDetector object.

        Args:
            weights_path (str): Path to the YOLO model weights file.
            images_folder (str): Path to the folder containing images.
            output_folder (str): Path to the folder for saving modified images.
            class_types (dict): Dictionary mapping class IDs to human-readable names.
        """
        self.weightsPath = weigthsPath
        self.imagesFolder = imagesPath
        self.outputFolder = outputPath
        self.model = YOLO(self.weightsPath)  # Load the model once for efficiency

    def getClassType(self,number):
      #Returns the string associated with the number, or None if not found.
      return classType.get(number)
    
    def decimalToPercent(self,decimal):
      #Converts a decimal number to a percentage string.
      return str(decimal * 100) + "%"
    
    def calculateCenter(self,coordinates):
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
    
    def detectPathsInFolder(self):
      #Detects paths on images within a folder and saves modified images with bounding boxes.
      imageList = [[1]]
      imageId = currentId = 1
      pathId = 1
      pictures = sorted(os.listdir(self.imagesFolder))
      pathList = []
      print(pictures)
      for filename in pictures:
          if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG")  or filename.endswith(".JPG"):  # Check for image extensions
              full_path = os.path.join(self.imagesFolder, filename)
              print("Analizing image " + filename)
              results = self.model.predict(full_path)  # Predict on each image
              result = results[0]
              img = cv2.imread(full_path)
                        # Check if the filename starts with the current image ID
              print(str(imageId))
              if filename.startswith(str(imageId)):
                  print("aqi")
                  imageId = currentId
              else:
                  pathList = []
                  imageId += 1
                  imageList.append([imageId])
              if(len(result.boxes) > 0):
                for box in result.boxes:
                    print("boxy box")
                    classId = self.getClassType(result.names[box.cls[0].item()])
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = self.decimalToPercent(float(round(box.conf[0].item(), 2)))
                    pathList.append(list((pathId,classId,self.calculateCenter(cords),conf)))
                    x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]
                    label = f"{classId} PathId:{pathId}"
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 230, 0), 2)
                    cv2.putText(img, label, (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 230, 0), 2)
                    pathId += 1
                    imageList[imageId-1].append(sorted(pathList,key=lambda x: x[2][0]))
              elif(len(pathList)!=0):
                pass
              else:
                imageList[imageId-1].append([])
              #Save modified image
              output = f"{self.outputFolder}/modified_{os.path.basename(full_path)}"
              cv2.imwrite(output, img)


              #print(f"\n Image saved to: {output}")
      #return imageList
      print(imageList)


#test Code
#Folder Paths
weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/bestTS4.pt"
imagesFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages"
outputFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/outputTest"
a = PathFinder(weightsPath, imagesFolder, outputFolder)
list = a.detectPathsInFolder()
# print(" ------------- ")
# print("Final output below \n")
# print("Results list: \n")
# print(list)
# print("\nImages list: \n")
# print(list[0]) # lista de imagenes
# print("\nImage id: \n")
# print(list[0][0]) # id de imagen
# print("\nPaths on image: \n")
# print(list[0][1]) # paths en la  imagen
# print("\nPath detail: \n")
# print(list[0][1][0]) # camino
# print("\nPath id: \n")
# print(list[0][1][0][0]) # coordenadas del camino
# print("\nPath type: \n")
# print(list[0][1][0][1]) # coordenadas del camino
# print("\nPath center: \n")
# print(list[0][1][0][2]) # coordenadas del camino


# # print(" ------------- ")
