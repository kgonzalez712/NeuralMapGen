import os
from ultralytics import YOLO
import cv2
from logger import NMGLogger

#Class Types
classType = {
  '0': "Closed Path",
  '1': "Semi Open Path",
  '2': "Open Path"
}

class PathFinder:
    def __init__(self, weigthsPath, imagesPath, outputPath, logger:NMGLogger):
        """
        Args:
            weightsPath (str): Path to the YOLO model weights file.
            imagesFolder (str): Path to the folder containing images.
            outputFolder (str): Path to the folder for saving modified images.
            logger (NMGLogger): logger instance.
        """
        self.weightsPath = weigthsPath
        self.imagesFolder = imagesPath
        self.outputFolder = outputPath
        self.logger = logger
        self.model = YOLO(self.weightsPath)

    def getClassType(self,number):
      #Returns the string associated with the number, or None if not found.
      self.logger.log("Getting class for id: " +str(number))
      return classType.get(number)
    
    def decimalToPercent(self,decimal):
      #Converts a decimal number to a percentage string.
      return str(decimal * 100) + "%"
    
    def calculateCenter(self,coordinates):
      self.logger.log("Calculating center for coorditanes: " +str(coordinates))
      """
      Calculates the center point of a rectangle given its corner coordinates
      given a list or array containing the x1, y1, x2, y2 coordinates.
      Returns:
          A list containing the center coordinates (xCenter, yCenter).
      """

      if len(coordinates) != 4:
        raise ValueError("Invalid number of coordinates. Expected 4 (x1, y1, x2, y2).")

      x1, y1, x2, y2 = coordinates
      xCenter = (x1 + x2) / 2
      yCenter = (y1 + y2) / 2
      return [round(xCenter), round(yCenter)]
    
    def processImages(self, resultObj, paths, pathId,img,fullPath):
      #process Images to add the bounding box to a modified copy of the image.
      self.logger("---------- Started PathFinder subrutine: processImages ------")
      self.logger("processing image")
      for box in resultObj.boxes:
        self.logger('Getting image class type')
        classId = self.getClassType(resultObj.names[box.cls[0].item()])
        self.logger('Calculating box coordinates and center')
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = self.decimalToPercent(float(round(box.conf[0].item(), 2)))
        center = self.calculateCenter(cords)
        tempList = list((pathId,classId,center,conf))
        self.logger('Adding path to list'+ str(tempList))
        paths.append(tempList)
        x1, y1, x2, y2 = [int(x) for x in box.xyxy[0].tolist()]
        label = f"{classId}"
        self.logger("Adding bounding box to image")
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 230), 10)
        cv2.putText(img, label,(x1, y2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 5)
        #sorted(paths,key=lambda x: x[2][0])
      self.logger('Saving image selected output folder')
      output = f"{self.outputFolder}/modified_{os.path.basename(fullPath)}"
      self.logger('Successfully saved the modified Image')
      cv2.imwrite(output, img)
      self.logger('processImage subrutine completed! Returning paths')
      self.logger('Paths:'+str(paths))
      return paths


    
    def detectPathsInFolder(self):
      #Detects paths on images within a folder and saves modified images with bounding boxes.
      self.logger("---------- Started PathFinder subrutine: detectPathsInFolder ------")
      imageList = [[1]]
      imageId = 1
      pathId = 1
      pictures = sorted(os.listdir(self.imagesFolder))
      self.logger("Images from folder sorted by name following the standard")
      pathList = []
      self.logger("Detecting Paths...")
      for i, filename in enumerate(pictures):
          isLast = i == len(pictures) - 1
          matchesId = imageId == int(filename[:2])
          if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG")  or filename.endswith(".JPG"):  # Check for image extensions
              fullPath = os.path.join(self.imagesFolder, filename)
              self.logger("Predicting results on image:" + filename)
              results = self.model.predict(fullPath)
              result = results[0]
              lastElement = result
              img = cv2.imread(fullPath)
              if(matchesId):
                if(len(result.boxes)>0):
                  if(isLast):
                    break
                  else:
                    pathList = self.processImages(result,pathList,pathId,img,fullPath)
                    print(pathList)
                    pathId+=1    
                else:
                    pass  
              else:
                pathList = self.processImages(result,pathList,pathId,img,fullPath)
                self.logger("Adding results to imageList for image with id:" + str(imageId-1))
                imageList[imageId-1].append(pathList)
                pathList = []
                imageId+=1
                self.logger("Starting detection for image with id:" + str(imageId))
                imageList.append([imageId])
      if lastElement is not None:
        self.logger("Starting detection for the last image")
        if(len(lastElement.boxes)>0):
          pathList = self.processImages(result,pathList,pathId,img,fullPath)
          self.logger("Adding results to imageList for image with id:" + str(imageId-1))
          imageList[imageId-1].append(pathList)
        else:
          self.logger("Adding results to imageList for image with id:" + str(imageId-1))
          imageList[imageId-1].append(pathList)
          

      self.logger("Resulting ImageList:" + str(imageList))
      return imageList      

                
              



# test Code
# Folder Paths
# weightsPath = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/bestTS4.pt"
# imagesFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/testImages"
# outputFolder = "/Users/kgonzale/Documents/Resources/TEC/TFG/UrbanMapGen/PathFinder/outputTest"
# a = PathFinder(weightsPath, imagesFolder, outputFolder)
# list = a.detectPathsInFolder()
# print(" ------------- ")
# print("Final output below \n")
# print("Results list: \n")
# print(list)


