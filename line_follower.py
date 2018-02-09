import cv2
import numpy as np
import os

image = cv2.imread("horizontal.jpg", -1)
# print image.length
crop_img = image[200:640, 0:210]
crop_img2 = image[200:640,210:430]
crop_img3 = image[150:640,430:640]
# print len(image)
# print len(image[0])
# gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray,(15,15),0)
# ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
# img, contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
# print len(contours)
gray2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)
blur2 = cv2.GaussianBlur(gray2,(15,15),0)
ret2,thresh2 = cv2.threshold(blur2,60,255,cv2.THRESH_BINARY_INV)
img2, contours2, hierarchy2 = cv2.findContours(thresh2, 1, cv2.CHAIN_APPROX_SIMPLE)
if(len(contours2)>0):
	x,y,w,h = cv2.boundingRect(contours2[0])
	print x,y,w,h
# print len(contours2)
# gray3 = cv2.cvtColor(crop_img3, cv2.COLOR_BGR2GRAY)
# blur3 = cv2.GaussianBlur(gray3,(15,15),0)
# ret3,thresh3 = cv2.threshold(blur3,60,255,cv2.THRESH_BINARY_INV)
# img3, contours3, hierarchy3 = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
# print len(contours3)
while True:
    cv2.imshow('frame',image)
    # cv2.imshow('Frame 1', img)
    cv2.imshow('Frame 2', img2)
    # cv2.imshow('Frame 3', img3)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break