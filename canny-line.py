import cv2
import numpy as np
import os

left = -1
centre = 0
right = 1


def getCentre(crop_img):
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(15,15),0)
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    img, contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
    cx = 0
    cy = 0
    if (len(contours)):
        c1 = max(contours, key=cv2.contourArea)
        M1 = cv2.moments(c1)
        cx = int(M1['m10']/M1['m00'])
        cy = int(M1['m01']/M1['m00'])
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(crop_img, c1, -1, (0,255,0), 1)
    return cx,cy



def getDecision(cx1,cx2,cx3,cx4,cx5,prev1,prev2):

    diff1 = centre
    diff2 = centre
    diff3 = centre
    diff4 = centre
    centreCount = 0
    leftCount = 0
    rightCount = 0
    if(abs(cx1-cx2) > 15 and cx1 > cx2):
        diff1 = right
    elif(abs(cx1-cx2) > 15 and cx1 < cx2):
        diff1 = left

    if(abs(cx2-cx3) > 15 and cx2 > cx3):
        diff2 = right
    elif(abs(cx2-cx3) > 15 and cx2 < cx3):
        diff2 = left

    if(abs(cx3-cx4) > 15 and cx3 > cx4):
        diff3 = right
    elif(abs(cx3-cx4) > 15 and cx3 < cx4):
        diff3 = left

    if(abs(cx4-cx5) > 15 and cx4 > cx5):
        diff4 = right
    elif(abs(cx4-cx5) > 15 and cx4 < cx5):
        diff4 = left

    arr = []
    arr.append(diff1)
    arr.append(diff2)
    arr.append(diff3)
    arr.append(diff4)
    arr.append(prev1)
    arr.append(prev2)
    for diff in arr:
        if(diff == centre):
            centreCount = centreCount + 1
        if(diff == left):
            leftCount = leftCount + 1
        if(diff == right):
            rightCount = rightCount + 1
    print leftCount
    print rightCount
    print centre    
    if centreCount > leftCount and centreCount > rightCount:
        return centre,diff1,diff2
    elif leftCount > rightCount and leftCount > centreCount:
        return left,diff1,diff2
    else:
        return right,diff1,diff2
image = cv2.imread("left.jpeg", -1)
# print image.length
crop_img1 = image[0:128,0:640]
crop_img2 = image[128:256,0:640]
crop_img3 = image[256:384,0:640]
crop_img4 = image[384:512,0:640]
crop_img5 = image[512:640,0:640]
font = cv2.FONT_HERSHEY_SIMPLEX
cx1,cy1 = getCentre(crop_img1)
cx2,cy2 = getCentre(crop_img2)
cx3,cy3 = getCentre(crop_img3)
cx4,cy4 = getCentre(crop_img4)
cx5,cy5 = getCentre(crop_img5)
# edges = cv2.Canny(img,10,150,apertureSize = 3)

decision , previousDecision1 , previousDecision2 =  getDecision(cx1,cx2,cx3,cx4,cx5,-1,-1)  

print decision
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
    cv2.putText(crop_img4,'CX:'+str(cx4), (15,30),font,1,(0,0,255),2)
    cv2.putText(crop_img4,'CY: '+str(cy4),(15,70),font,1,(0,0,255),2)
    cv2.putText(crop_img5,'CX:'+str(cx5), (15,30),font,1,(0,0,255),2)
    cv2.putText(crop_img5,'CY: '+str(cy5),(15,70),font,1,(0,0,255),2)
    cv2.imshow('Frame',image)
    # cv2.imshow('Frame 1',crop_img1)
    # cv2.imshow('Frame 2',crop_img2)
    # cv2.imshow('Frame 3',crop_img3)
    # cv2.imshow('Frame 4',crop_img4)
    # cv2.imshow('Frame 5',crop_img5)
    if cv2.waitKey(25) & 0xFF == ord('q'):
    	break