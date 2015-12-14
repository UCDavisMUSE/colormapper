import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# This is a phantom used for detecting the difference between
# nonnegative least squares and least squares unmixing

image = np.zeros((3, 9, 3), dtype=np.uint8)
image[:,0:3,:] = [255, 255, 255]
image[:,3:6,:] = [  0,   0, 255]
image[:,6:9,:] = [255, 255,   0]

plt.imshow(image, interpolation = "nearest")
plt.xticks([]), plt.yticks([])
plt.show()

image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
cv2.imwrite("testImages/Unmix Phantom.png",image)
