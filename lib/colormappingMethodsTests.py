import numpy as np
import cv2
from colormappingMethods import *
# This script tests the colormapping methods in colormappingMethods.py

# First Test

X = np.array([ [  0, 134, 130],
               [  0, 168,  81],
               [  0, 242,  66] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

(A, c) = learnAffineColorspaceMap(X,Y)

print(A)
print(c)
print(np.dot(A,X) + np.dot(c,np.ones((1,3),float)))

# MATLAB Output:
# A =
#     0.3658   -0.2483   -0.7947
#    -0.2259   -0.3559   -0.5576
#    -0.2162   -0.1750   -0.1927
# 
# c =
# 
#   255.0000
#   255.0000
#   255.0000

image = cv2.imread("testImages/AVG_Stack-9.jpg") 
cv2.imshow("Image",image) # the window title will be "image"
k = cv2.waitKey(0) & 0xFF # Mask the return of waitKey
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows() #closes all windows

image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

newImage = applyAffineColorspaceMap(image,A,c)

newImage = cv2.cvtColor(newImage, cv2.COLOR_RGB2BGR)

cv2.imshow("image",newImage) # the window title will be "image"
k = cv2.waitKey(0) & 0xFF # Mask the return of waitKey
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows() #closes all windows


# Second Test

X = np.array([ [  0, 228, 244],
               [  0, 250, 205],
               [  0, 166, 100] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

(A, c) = learnAffineColorspaceMap(X,Y)

print(A)
print(c)
print(np.dot(A,X) + np.dot(c,np.ones((1,3),float)))

# MATLAB Output:
# A =
#     1.1795   -0.7234   -1.6451
#     0.7324   -0.6907   -1.3212
#     0.2258   -0.2911   -0.5044
# 
# 
# c =
#   255.0000
#   255.0000
#   255.0000

image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
cv2.imshow("Image",image) # the window title will be "image"
k = cv2.waitKey(0) & 0xFF # Mask the return of waitKey
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows() #closes all windows

image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

newImage = applyAffineColorspaceMap(image,A,c)

newImage = cv2.cvtColor(newImage, cv2.COLOR_RGB2BGR)

cv2.imshow("image",newImage) # the window title will be "image"
k = cv2.waitKey(0) & 0xFF # Mask the return of waitKey
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows() #closes all windows
