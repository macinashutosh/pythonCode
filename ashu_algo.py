from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 33
Motor1B = 35
Motor1E = 37
Motor2A = 36
Motor2B = 38
Motor2E = 40

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)


# speeda = GPIO.PWM(Motor1E,100)
# speedb = GPIO.PWM(Motor2E,100)

# speedb.start(25)#left motor
# speeda.start(25)#right motor
GPIO.output(Motor1A,0)
GPIO.output(Motor1B,0)
GPIO.output(Motor2A,0)
GPIO.output(Motor2B,0)

delay_time = 0.3
thicknessAllowance = 20
camera = PiCamera()
camera.resolution = (640, 640)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 640))

time.sleep(1)
font = cv2.FONT_HERSHEY_SIMPLEX
def turn_left():
 GPIO.output(Motor1A,1)
 GPIO.output(Motor1B,1)
 GPIO.output(Motor2A,0)
 GPIO.output(Motor2B,1)
 print "turn left"
def turn_right():
 GPIO.output(Motor1A,0)
 GPIO.output(Motor1B,1)
 GPIO.output(Motor2A,1)
 GPIO.output(Motor2B,1)
 print "turn right"
def go_straight():
 GPIO.output(Motor1A,0)
 GPIO.output(Motor1B,1)
 GPIO.output(Motor2A,0)
 GPIO.output(Motor2B,1)
 print "go straight"
def motor_stop():
 GPIO.output(Motor1A,0)
 GPIO.output(Motor1B,0)
 GPIO.output(Motor2A,0)
 GPIO.output(Motor2B,0) 
decision = "straight"
prev_decision = ""
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    image = frame.array
    # crop_img = image[0:680, 80:520]
    # gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray,(15,15),0)
    # ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    #edges = cv2.Canny(thresh,100,200)
    # img, contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
    crop_img = image[150:640, 0:210]
    crop_img2 = image[150:640,210:430]
    crop_img3 = image[150:640,430:640]
    # print len(image)
    # print len(image[0])
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
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
    img3, contoursRight, hierarchy3 = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
    # len(contoursRight)
    
    widthCenter = 0
    if(len(contoursCentre) > 0):
      c = max(contoursCentre, key=cv2.contourArea)
      x,y,w,h = cv2.boundingRect(c)
      widthCenter = w
    if (len(contoursLeft) > 0):
      c = max(contoursLeft, key=cv2.contourArea)
      x,y,w,h = cv2.boundingRect(c)
      if(w > widthCenter - thicknessAllowance && w < widthCenter + thicknessAllowance):
        decision = "left"
    elif (len(contoursRight) > 0):
      c = max(contoursRight, key=cv2.contourArea)
      x,y,w,h = cv2.boundingRect(c)
      if(w > widthCenter - thicknessAllowance && w < widthCenter + thicknessAllowance):
        decision = "right"
    else :
        decision = "straight"

    if (decision == "left"):
      if not prev_decision == "left":
        turn_left()
    elif (decision == "right"):
      if not prev_decision == "right":
        turn_right()
    else :
      if not prev_decision == "straight": 
        go_straight()
    time.sleep(delay_time)
    prev_decision = decision
    # if len(contours) > 0:
    #  c = max(contours, key=cv2.contourArea)
    #  #print cv2.contourArea(c)
    #  M = cv2.moments(c)
    #  cx = int(M['m10']/M['m00'])
    #  cy = int(M['m01']/M['m00'])
     #cv2.line(crop_img,(cx,0),(cx,240),(255,0,0),1)
     #cv2.line(crop_img,(0,cy),(320,cy),(255,0,0),1)
     #cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
GPIO.cleanup()