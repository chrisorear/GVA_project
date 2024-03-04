#finds all .jpg files in a specified folder

import os
from os import listdir

#change path for different folders
path = "/Users/chrisorear/Downloads/OneDrive_1_1-22-2024"
img_list = []
file_list = os.listdir(path)
for i in range(len(file_list)): #the range argument lets me iterate through integers
    if (file_list[i].endswith(".jpg")):
        img_list.append(file_list[i]) #append function appends to end of list
print(img_list)
#edge detection 

import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import pandas as pd

#reads in image as grayscale, gaussian blurs it to reduce noise, edge detection with Canny function 
images = []
blurred_images = []
edge_images = []
for img in img_list:
    images.append(cv2.imread(path+'/'+img, cv2.IMREAD_GRAYSCALE))
for img in images:  
    blurred_images.append(cv2.GaussianBlur(img,(5,5),0))
for img in blurred_images:
    edge_images.append(cv2.Canny(img,3,20))

#plot original and edge image
for i in range(len(edge_images)):
    plt.subplot(121), plt.imshow(images[i], cmap ='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edge_images[i],cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.figure()

#reads in image as grayscale, gaussian blurs it to reduce noise, edge detection with Canny function 
image = cv2.imread(path+'/'+img_list[1], cv2.IMREAD_GRAYSCALE)
blurred_image = cv2.GaussianBlur(image,(3,3),0)
edge_image = cv2.Canny(blurred_image,3,12)

#plot original and edge image
plt.subplot(121), plt.imshow(image, cmap ='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edge_image,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

contours, _ = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image_copy = image.copy()
image_copy = cv2.cvtColor(image_copy, cv2.COLOR_GRAY2BGR)
cv2.drawContours(image_copy,contours,-1, (0,0,255), 3)
print(len(contours), "objects were found in this image.")

#plt.figure()
#plt.imshow(image_copy)
#plt.show()

cv2.imshow("contoured image", image_copy)
cv2.waitKey(0)

