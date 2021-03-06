from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#motor 1 is right
#motor 2 is left

#Left Forward
#GPIO.setup(40, GPIO.OUT)
#Right Forward
#GPIO.setup(35, GPIO.OUT)

#GPIO.output(40, GPIO.HIGH)
#GPIO.output(35, GPIO.HIGH)
Motor1A = 29
Motor1B = 31
Motor1E = 35
Motor2A = 38
Motor2B = 32
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

speeda = GPIO.PWM(Motor1E,45)
speedb = GPIO.PWM(Motor2E,45)

speedb.start(100)#left motor
speeda.start(100)#right motor
GPIO.output(Motor1A,0)
GPIO.output(Motor1B,0)
GPIO.output(Motor2A,0)
GPIO.output(Motor2B,0)

def turn_right():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    print "turn right"
def turn_left():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    print "turn left"
def go_straight():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    print "go straight"
def motor_stop():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)

def turn_extreme_left():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,1)
    #GPIO.output(Motor2E,1)
    print "extreme left"
def turn_extreme_right():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,1)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    print "extreme_right"
    #GPIO.output(Motor2E,1)

def get_contours(crop_img):
 gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
 blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

 # Find the contours of the frame
 img, contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 c = max(contours, key=cv2.contourArea)
 M = cv2.moments(c)
 #print cv2.contourArea(c)
 cx = int(M['m10']/M['m00'])
 cy = int(M['m01']/M['m00'])
 cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
 cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
 cv2.drawContours(crop_img,contours, -1, (0,255,0), 1)
 area =  cv2.contourArea(c)
 print area
 return area 
 
camera = PiCamera()
camera.resolution = (600, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(600, 600))
time.sleep(1)
current_dec = 0 #1 for Right -1 for Left 0 for c
i = 5
byeByeCameraError = 100
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
 image = frame.array
 crop_img = image[0:120, 240:400]
 crop_img1 = image[120:240, 240:400]
 crop_img2 = image[240:360, 240:400]
 crop_img3 = image[360:480, 240:400]
 crop_img4 = image[480:600, 240:400]
 if byeByeCameraError > 0:
   byeByeCameraError = byeByeCameraError -1
 else:
   if(get_contours(image)>140000):
    if count < 0:
      print "zone_marker_aagya"
      time.sleep(0.8)
      motor_stop()
      time.sleep(1)
      detect_markers(image,zone_count)    
      break
    count = count - 1    # Convert to grayscale
 gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
 blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
 img, contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 
 gray1 = cv2.cvtColor(crop_img1, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
 blur1 = cv2.GaussianBlur(gray1,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur1,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
 img, contours1, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

 gray = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
 blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
 img, contours2, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 
 gray = cv2.cvtColor(crop_img3, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
 blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
 img, contours3, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 
 gray = cv2.cvtColor(crop_img4, cv2.COLOR_BGR2GRAY)
 blur = cv2.GaussianBlur(gray,(5,5),0)

    # Color thresholding
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

    # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)

    # Find the contours of the frame
 img, contours4, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
    # Find the biggest contour (if detected)
 delay_time = 0.1
 final_contours = contours1
 img_to_draw = crop_img1
 if len(contours2)>0:
  final_contours = contours2
  img_to_draw = crop_img2
 elif len(contours3)>0:
  final_contours = contours3
  img_to_draw = crop_img3
 elif len(contours4)>0:
  final_contours = contours4
  img_to_draw = crop_img4
  
  
 if len(contours) > 0:
  c = max(contours, key=cv2.contourArea)
  M = cv2.moments(c)
  #print cv2.contourArea(c)
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])
  
  #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
  #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

  #cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

  print cx
  #print cy
  if cv2.contourArea(c) > 600 or i > 0:
    i = i -1
    if cx >= 120: #right
     offset_x = (cx-60)
     #print offset_x
     turn_right()
     current_dec = 1
     #GPIO.output(40, GPIO.HIGH)
     #GPIO.output(35, GPIO.LOW)
    if cx < 120 and cx > 50:
     go_straight()
     #GPIO.output(40, GPIO.LOW)
     #GPIO.output(35, GPIO.LOW)
    if cx <= 50: #left
     offset_x = (60-(60-cx))
     #print offset_x
     turn_left()
     current_dec = -1
     #GPIO.output(40, GPIO.LOW) 
     #GPIO.output(35, GPIO.HIGH)
  else:
    if current_dec == -1:
     turn_extreme_left()
    elif current_dec == 1:
     turn_extreme_right()
  time.sleep(delay_time)
  motor_stop()
 elif len(final_contours) > 0:
  c = max(final_contours, key=cv2.contourArea)
  M = cv2.moments(c)
  #print cv2.contourArea(c)
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])

  cv2.line(img_to_draw,(cx,0),(cx,720),(255,0,0),1)
  cv2.line(img_to_draw,(0,cy),(1280,cy),(255,0,0),1)

  cv2.drawContours(img_to_draw,final_contours, -1, (0,255,0), 1)

  print cx
  #print cy
  if cv2.contourArea(c) > 600 or i > 0:
    i = i -1
    if cx >= 120: #right
     offset_x = (cx-60)
     #print offset_x
     turn_extreme_right()
     current_dec = 1
     #GPIO.output(40, GPIO.HIGH)
     #GPIO.output(35, GPIO.LOW)
     #GPIO.output(40, GPIO.LOW)
     #GPIO.output(35, GPIO.LOW)
    if cx <= 50: #left
     offset_x = (60-(60-cx))
     #print offset_x
     turn_extreme_left()
     current_dec = -1
     #GPIO.output(40, GPIO.LOW) 
     #GPIO.output(35, GPIO.HIGH)
    if cx >50 and cx < 120:
     if current_dec == -1:
      turn_left()
     elif current_dec == 1:
      turn_right()
     
    #if cx<0:
     #motor_stop()
     #print "jaddoooooo"
  else:
    print "iski aukaat se bahar hai"
    if current_dec == -1:
     turn_extreme_left()
    elif current_dec == 1:
     turn_extreme_right()
  time.sleep(delay_time)
  motor_stop()
 else:
  if current_dec == -1:
   turn_extreme_left()
  elif current_dec == 1:
   turn_extreme_right()
  time.sleep(delay_time)
  motor_stop()
  #GPIO.output(40, GPIO.HIGH)
  #GPIO.output(35, GPIO.HIGH)
  

    #Display the resulting frame
 cv2.imshow('frame',image)
 #cv2.imshow('frame1',crop_img)
 #cv2.imshow('frame2',crop_img1)
 #cv2.imshow('frame3',crop_img2)
 #cv2.imshow('frame4',crop_img3)
 rawCapture.truncate(0)
 if cv2.waitKey(1) & 0xFF == ord('q'):
  break


        
GPIO.cleanup()
