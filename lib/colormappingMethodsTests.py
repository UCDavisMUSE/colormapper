import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from colormappingMethods import *
# This script tests the colormapping methods in colormappingMethods.py

# First Test

X = np.array([ [  0, 134, 130],
               [  0, 168,  81],
               [  0, 242,  66] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

start = time.time()
(A, c) = learnAffineColorspaceMap(X,Y)
end = time.time()
print("Learn Affine Colorspace Map Time: " + str(end-start))

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
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

plt.imshow(image, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()

start = time.time()
newImage = applyAffineColorspaceMap(image,A,c)
end = time.time()
print("Apply Affine Colorspace Map Time: " + str(end-start))

plt.imshow(newImage, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()


# Second Test

X = np.array([ [  0, 228, 244],
               [  0, 250, 205],
               [  0, 166, 100] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

start = time.time()
(A, c) = learnAffineColorspaceMap(X,Y)
end = time.time()
print("Learn Affine Colorspace Map Time: " + str(end-start))


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
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

plt.imshow(image, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()

start = time.time()
newImage = applyAffineColorspaceMap(image,A,c)
end = time.time()
print("Apply Affine Colorspace Map Time: " + str(end-start))

plt.imshow(newImage, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()

# Third Test

X = np.array([ [  0, 134, 130],
               [  0, 168,  81],
               [  0, 242,  66] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

start = time.time()
(A, c) = learnLogisticColorspaceMap(X,Y)
end = time.time()
print("Learn Logistic Colorspace Map Time: " + str(end-start))

print(A)
print(c)
print(255/(1 + np.exp(-(np.dot(A,X) + np.dot(c,np.ones((1,3),float))))))

image = cv2.imread("testImages/AVG_Stack-9.jpg") 
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

plt.imshow(image, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()

start = time.time()
newImage = applyLogisticColorspaceMap(image,A,c)
end = time.time()
print("Apply Logistic Colorspace Map Time: " + str(end-start))

plt.imshow(newImage, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()


# Fourth Test

X = np.array([ [  0, 228, 244],
               [  0, 250, 205],
               [  0, 166, 100] ])
               
Y = np.array([ [255,  70, 230],
               [255,  30, 160],
               [255, 150, 200] ])

start = time.time()
(A, c) = learnLogisticColorspaceMap(X,Y)
end = time.time()
print("Learn Logistic Colorspace Map Time: " + str(end-start))


print(A)
print(c)
print(255/(1 + np.exp(-(np.dot(A,X) + np.dot(c,np.ones((1,3),float))))))

image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

plt.imshow(image, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()

start = time.time()
newImage = applyLogisticColorspaceMap(image,A,c)
end = time.time()
print("Apply Logistic Colorspace Map Time: " + str(end-start))

plt.imshow(newImage, interpolation = "bicubic")
plt.xticks([]), plt.yticks([])
plt.show()



