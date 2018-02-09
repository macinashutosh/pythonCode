import cv2
import numpy as np
import os

cx1 = 0
cx2 = 0 
cx3 = 0
cy1 = 0
cy2 = 0
cy3 = 0
image = cv2.imread("ninty.jpeg", -1)
# print image.length
crop_img1 = image[0:210,0:640]
crop_img2 = image[210:430,0:640]
crop_img3 = image[430:640,0:640]
font = cv2.FONT_HERSHEY_SIMPLEX

gray = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(15,15),0)
ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
img, contoursLeft, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
# len(contoursLeft)
gray2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)
blur2 = cv2.GaussianBlur(gray2,(15,15),0)
ret2,thresh2 = cv2.threshold(blur2,60,255,cv2.THRESH_BINARY_INV)
img2, contoursCentre, hierarchy2 = cv2.findContours(thresh2, 1, cv2.CHAIN_APPROX_SIMPLE)
# len(contoursCentre)
gray3 = cv2.cvtColor(crop_img3, cv2.COLOR_BGR2GRAY)
blur3 = cv2.GaussianBlur(gray3,(15,15),0)
ret3,thresh3 = cv2.threshold(blur3,60,255,cv2.THRESH_BINARY_INV)
img3, contoursRight, hierarchy3 = cv2.findContours(thresh3, 1, cv2.CHAIN_APPROX_SIMPLE)

# Setup SimpleBlobDetector parameters.
if (len(contoursLeft)):
    c1 = max(contoursLeft, key=cv2.contourArea)
    M1 = cv2.moments(c1)
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])
    cv2.line(crop_img1,(cx1,0),(cx1,720),(255,0,0),1)
    cv2.line(crop_img1,(0,cy1),(1280,cy1),(255,0,0),1)
    cv2.drawContours(crop_img1, c1, -1, (0,255,0), 1)

if (len(contoursCentre)):
    c2 = max(contoursCentre, key=cv2.contourArea)
    M2 = cv2.moments(c2)
    cx2 = int(M2['m10']/M2['m00'])
    cy2 = int(M2['m01']/M2['m00'])
    cv2.line(crop_img2,(cx2,0),(cx2,720),(255,0,0),1)
    cv2.line(crop_img2,(0,cy2),(1280,cy2),(255,0,0),1)
    cv2.drawContours(crop_img2, c2, -1, (0,255,0), 1)

if (len(contoursRight)):
    c3 = max(contoursRight, key=cv2.contourArea)
    M3= cv2.moments(c3)
    cx3 = int(M3['m10']/M3['m00'])
    cy3 = int(M3['m01']/M3['m00'])
    cv2.line(crop_img3,(cx3,0),(cx3,720),(255,0,0),1)
    cv2.line(crop_img3,(0,cy3),(1280,cy3),(255,0,0),1)
    cv2.drawContours(crop_img3, c3, -1, (0,255,0), 1)


# edges = cv2.Canny(img,10,150,apertureSize = 3)
 
# # This returns an array of r and theta values
# lines = cv2.HoughLines(edges,1,np.pi/180, 110)
 
# # The below for loop runs till r and theta values 
# # are in the range of the 2d array
# for line in lines:
# 	for r,theta in line:
     
# 		# Stores the value of cos(theta) in a
# 		a = np.cos(theta)

# 		# Stores the value of sin(theta) in b
# 		b = np.sin(theta)
		 
# 		# x0 stores the value rcos(theta)
# 		x0 = a*r
		 
# 		# y0 stores the value rsin(theta)
# 		y0 = b*r
		 
# 		# x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
# 		x1 = int(x0 + 1000*(-b))
		 
# 		# y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
# 		y1 = int(y0 + 1000*(a))

# 		# x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
# 		x2 = int(x0 - 1000*(-b))
		 
# 		# y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
# 		y2 = int(y0 - 1000*(a))
		 
# 		# cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
# 		# (0,0,255) denotes the colour of the line to be 
# 		#drawn. In this case, it is red. 
# 		cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)

while True:
    #cv2.imshow('frame',image)
    cv2.putText(crop_img1,'CX:'+str(cx1), (15,30),font,1,(0,0,255),2)
    cv2.putText(crop_img1,'CY: '+str(cy1),(15,70),font,1,(0,0,255),2)
    cv2.putText(crop_img2,'CX:'+str(cx2), (15,30),font,1,(0,0,255),2)
    cv2.putText(crop_img2,'CY: '+str(cy2),(15,70),font,1,(0,0,255),2)
    cv2.putText(crop_img3,'CX:'+str(cx3), (15,30),font,1,(0,0,255),2)
    cv2.putText(crop_img3,'CY: '+str(cy3),(15,70),font,1,(0,0,255),2)
    cv2.imshow('Frame',image)
    cv2.imshow('Frame 1',crop_img1)
    cv2.imshow('Frame 2',crop_img2)
    cv2.imshow('Frame 3',crop_img3)
    if cv2.waitKey(25) & 0xFF == ord('q'):
    	break