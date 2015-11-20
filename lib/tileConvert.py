import numpy as np
import math
import cv2
import cPickle
import os
import tempfile
import matplotlib.pyplot as plt
import colormappingMethods
import time

start = time.time()
# Specify image tile size (height, width)
tileSize = (1024, 1024) 

# Colormapper Filename
colormapperFilename = "../tmp/default.colormapper"

# Read colormapper settings and compute affine transformation
try:
    f = open(colormapperFilename, 'r')
    (inputColors, outputColors) = cPickle.load(f)
except cPickle.UnpicklingError:
    print("Could not read colormapper file!")

inputColorMatrix = np.zeros((3, len(inputColors)))
outputColorMatrix = np.zeros((3, len(outputColors)))

for color in range(len(inputColors)):
    inputColorMatrix[:, color] = inputColors[color]

for color in range(len(outputColors)):
    outputColorMatrix[:, color] = outputColors[color]

(A, c) = colormappingMethods.learnAffineColorspaceMap(inputColorMatrix, outputColorMatrix)

# Image filename
imageFilename = "../tmp/rescued 20000_stitch.jpg"
#imageFilename = "NL tissue-esophagus-151131624-2.jpg"

# Read in the image
image = cv2.imread(imageFilename)

# Split filename into parts for temporary use
(imageFilename, fileExtension) = os.path.splitext(imageFilename)
(imageDirectory, imageFilename) = os.path.split(imageFilename)
#print(imageDirectory, imageFilename, fileExtension)

# Create a temporary directory in which to save files
#temporaryDirectory = tempfile.mkdtemp()
temporaryDirectory = "/Users/zac/Desktop/temp"
os.mkdir(temporaryDirectory)
print(temporaryDirectory)

(height, width, colors) = image.shape

heightTiles = int(math.floor(1.0*height/tileSize[0]))
widthTiles = int(math.floor(1.0*width/tileSize[1]))

heightRemainder = height % tileSize[0]
widthRemainder = width % tileSize[1]

for widthTile in range(widthTiles + 1):
    for heightTile in range(heightTiles + 1):

    
        if heightTile < heightTiles and widthTile < widthTiles:
            subImage = image[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                         widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:]
        elif heightTile < heightTiles and widthTile == widthTiles and widthRemainder != 0:
            subImage = image[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                         widthTile*tileSize[1]:,:]
        elif heightTile == heightTiles and widthTile < widthTiles and heightRemainder != 0:
            subImage = image[heightTile*tileSize[0]:, 
                         widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:]
        elif heightTile == heightTiles and widthTile == widthTiles and widthRemainder != 0 and heightRemainder !=0:
            subImage = image[heightTile*tileSize[0]:, 
                         widthTile*tileSize[1]:,:]
        
        subImageFilename = imageFilename + " - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        cv2.imwrite(temporaryFilename, subImage)

for widthTile in range(widthTiles + 1):
    for heightTile in range(heightTiles + 1):
        subImageFilename = imageFilename + " - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        subImage = cv2.imread(temporaryFilename)
        
        # Convert
        subImage = cv2.cvtColor(subImage,cv2.COLOR_BGR2RGB)
        subImage = colormappingMethods.applyAffineColorspaceMap(subImage,A,c)
        subImage = cv2.cvtColor(subImage,cv2.COLOR_RGB2BGR)

        # Save converted image
        subImageFilename = imageFilename + " - Converted - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        cv2.imwrite(temporaryFilename, subImage)

# Stich together converted image 
newImage = np.zeros((height, width, colors), np.uint8)
 
for widthTile in range(widthTiles + 1):
    for heightTile in range(heightTiles + 1):
        subImageFilename = imageFilename + " - Converted - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        subImage = cv2.imread(temporaryFilename)
    
        if heightTile < heightTiles and widthTile < widthTiles:
            newImage[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                         widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:] = subImage
        elif heightTile < heightTiles and widthTile == widthTiles and widthRemainder != 0:
            newImage[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                         widthTile*tileSize[1]:,:] = subImage
        elif heightTile == heightTiles and widthTile < widthTiles and heightRemainder != 0:
            newImage[heightTile*tileSize[0]:, 
                         widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:] = subImage
        elif heightTile == heightTiles and widthTile == widthTiles and widthRemainder != 0 and heightRemainder !=0:
            newImage[heightTile*tileSize[0]:, 
                         widthTile*tileSize[1]:,:] = subImage

newImageFilename = imageFilename + " - Converted.png"
newFilename = os.path.join(imageDirectory, newImageFilename)                          
cv2.imwrite(newFilename, newImage)

# Clean up temporary directory
for widthTile in range(widthTiles + 1):
    for heightTile in range(heightTiles + 1):
        subImageFilename = imageFilename + " - Converted - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        os.remove(temporaryFilename)
        
        subImageFilename = imageFilename + " - (" + str(heightTile) + ", " + str(widthTile) + ").png"                 
        temporaryFilename = os.path.join(temporaryDirectory,subImageFilename)
        os.remove(temporaryFilename)
        
os.rmdir(temporaryDirectory)
end = time.time()
print("Time Elapsed: " + str(end-start))
        
        




