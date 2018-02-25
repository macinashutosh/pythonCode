from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

plantation_image=cv2.imread('plant.png', -1) 
global plantation_image
cv2.imshow('image',plantation_image)
cv2.waitKey(0)
time.sleep(1)
blue = 22
GPIO.setup(blue,GPIO.OUT)
green = 12
GPIO.setup(green,GPIO.OUT)
red = 16
GPIO.setup(red,GPIO.OUT)

def blend_transparent(face_img, overlay_t_img):
    overlay_img = overlay_t_img[:,:,:3] 
    overlay_mask = overlay_t_img[:,:,3:] 
    background_mask = 255 - overlay_mask
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0)) 
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def hillside(overlay_image,size,kitni_baar,spacing=30):
    global plantation_image
    img_x = 260
    img_y = 340
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
    
def berns(overlay_image,size,kitni_baar,spacing=30):
    global plantation_image
    img_x = 190
    img_y = 140
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    if(kitni_baar <= 2):
        while i < kitni_baar:
            plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
    else:
        while i < 2:
            plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
            img_x = img_x+10
        img_x = img_x + 10
        img_y = img_y - 40
        count = 0
        i=0
        while i < kitni_baar-2:
            plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
            img_x = img_x+10
          
def cliff(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    global plantation_image
    img_x = 170
    img_y = 260
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
    
def plane(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    global plantation_image
    img_x = 170
    img_y = 520
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        plantation_image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(plantation_image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
        img_x = img_x + 5

def blueBlink():
    global blue
    GPIO.output(blue,1)
    time.sleep(1)
    GPIO.output(blue,0)
    time.sleep(1)
def greenBlink():
    global green
    GPIO.output(green,1)
    time.sleep(1)
    GPIO.output(green,0)
    time.sleep(1)
def redBlink():
    global red
    GPIO.output(red,1)
    time.sleep(1)
    GPIO.output(red,0)
    time.sleep(1)
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

speeda = GPIO.PWM(Motor1E,100)
speedb = GPIO.PWM(Motor2E,100)


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

def get_area(crop_img):
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
 area = 0
 if len(contours) > 0:
  c = max(contours, key=cv2.contourArea)
  M = cv2.moments(c)
  #print cv2.contourArea(c)
  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])
  #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
  #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
  #cv2.drawContours(crop_img,contours, -1, (0,255,0), 1)
  area =  cv2.contourArea(c)
 print area
 return area 

camera = PiCamera()
camera.resolution = (160, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(160, 600))
time.sleep(1)

def motion_function(speed,size_value,zone):
  rawCapture.truncate(0)
  delay_time = 0.1
  if zone == 4 or zone == 3:
   delay_time = 0.05
  else :
   delay_time = 0.07
  speedb.start(speed)#left motor
  speeda.start(speed)#right motor
  current_dec = 0 #1 for Right -1 for Left 0 for c
  i = 5
  byeByeCameraError = 5
  count = -1
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

   
   image = frame.array
   crop_img = image[0:120, 0:160]
   crop_img1 = image[120:240,0:160]
   crop_img2 = image[240:360,0:160]
   crop_img3 = image[360:480,0:160]
   crop_img4 = image[480:600,0:160]

   if byeByeCameraError > 0:
     byeByeCameraError = byeByeCameraError -1
   else:
     if(get_area(image)>size_value):
      if count < 0:
        print "zone_marker_aagya"
        if zone == 2 or zone == 4:
          turn_right()
          time.sleep(0.4)
        else:
          go_straight()
          time.sleep(0.2)
        print "aage_badgya"
        motor_stop()
        time.sleep(1.5)   
        break
      count = count - 1
      # Convert to grayscale
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
   #delay_time = 0.05
   final_contours = contours1
   if len(contours2)>0:
    final_contours = contours2
   elif len(contours3)>0:
    final_contours = contours3
   elif len(contours4)>0:
    if zone == 4 or zone == 3:
     final_contours = contours4
    else:
     final_contours = []
    
    
   if len(contours) > 0:
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    #print cv2.contourArea(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
    cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

    cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

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
      else:
       go_straight()
    time.sleep(delay_time)
    motor_stop()
   elif len(final_contours) > 0:
    c = max(final_contours, key=cv2.contourArea)
    M = cv2.moments(c)
    #print cv2.contourArea(c)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
    cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)

    cv2.drawContours(crop_img,final_contours, -1, (0,255,0), 1)

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
       else:
        go_straight()
       
      if cx<0:
       motor_stop()
       print "jaddoooooo"
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
   rawCapture.truncate(0)


def blink_led(color,kitni_baar):
  i=0
  if color == "red":
    while i < kitni_baar:
      redBlink()
      i=i+1
  elif color == "blue":
    while i<kitni_baar:
      blueBlink()
      i=i+1
  elif color == "green":
    while i< kitni_baar:
      greenBlink()
      i=i+1

print "##########Zone 1###########"
motion_function(80,81000,1)
blink_led("blue",2)
overlay_image = cv2.imread("Seedlings/tulipblue.png",-1)
hillside(overlay_image,40,2,30)

print "##########Zone 2###########"
motion_function(80,88000,2)
blink_led("red",3)
overlay_image = cv2.imread("Seedlings/carnation.png",-1)
berns(overlay_image,40,3,30)


print "##########Zone 3###########"
motion_function(70,84000,3)
blink_led("red",2)
overlay_image = cv2.imread("Seedlings/tulipred.png",-1)
cliff(overlay_image,40,2,30)


print "##########Zone 4###########"
motion_function(60,83000,4)
blink_led("green",4)
overlay_image = cv2.imread("Seedlings/sunflower.png",-1)
plane(overlay_image,40,4,30)


print "##########End Zone###########"
motion_function(60,84000,5)
i=0
while i< 50:
 turn_right()
 time.sleep(0.1)
 motor_stop()
 time.sleep(0.1)
 turn_left()
 time.sleep(0.1)
 motor_stop()
 time.sleep(0.1)
 i=i+1
#motion_function(60,83000,6)
cv2.imwrite('answer.png', plantation_image)
blink_led("blue",2)
blink_led("red",3)
blink_led("red",2)
blink_led("green",4)

GPIO.cleanup()