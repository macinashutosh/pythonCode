# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np
 
# Reading the required image in 
# which operations are to be done. 
# Make sure that the image is in the same 
# directory in which this python program is
img = cv2.imread('right.jpeg')
 
# Convert the img to grayscale
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(15,15),0)
ret2,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
img2, contoursCentre, hierarchy2 = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
# Apply edge detection method on the image
edges = cv2.Canny(img2,10,150,apertureSize = 3)
 
# This returns an array of r and theta values
lines = cv2.HoughLines(edges,1,np.pi/180, 90)
 
# The below for loop runs till r and theta values 
# are in the range of the 2d array
for line in lines:
	for r,theta in line:
     
		# Stores the value of cos(theta) in a
		a = np.cos(theta)

		# Stores the value of sin(theta) in b
		b = np.sin(theta)
		 
		# x0 stores the value rcos(theta)
		x0 = a*r
		 
		# y0 stores the value rsin(theta)
		y0 = b*r
		 
		# x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
		x1 = int(x0 + 1000*(-b))
		 
		# y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
		y1 = int(y0 + 1000*(a))

		# x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
		x2 = int(x0 - 1000*(-b))
		 
		# y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
		y2 = int(y0 - 1000*(a))
		 
		# cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
		# (0,0,255) denotes the colour of the line to be 
		#drawn. In this case, it is red. 
		cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)
 
# All the changes made in the input image are finally
# written on a new image houghlines.jpg
# cv2.imwrite('houghlines3.jpg', img)
while True:
	cv2.imshow("gray",gray)
	cv2.imshow("edges",edges)
	cv2.imshow("image1",img)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break
