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

image=cv2.imread("Plantation.png",-1) 
dic={"cr":"assorted.png","tr":"carnation.png","sr":"gerber.png","cg":"hibiscusred.png","tg":"marigold.png","sg":"hydrangeablue.png","cb":"hydrangeayellow.png","tb":"lilac.png","sb":"lily.png"}
dic2={"sr":"rosered.png","cr":"gerber.png","tr":"poinsettia.png","sb":"orchid.png","cb":"tulipblue.png","tb":"lilac.png","sg":"hibiscusyellow.png","cg":"lily.png","tg":"marigold.png"}
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

speedb.start(100)#left motor
speeda.start(100)#right motor
GPIO.output(Motor1A,0)
GPIO.output(Motor1B,0)
GPIO.output(Motor2A,0)
GPIO.output(Motor2B,0)

blue = 22
GPIO.setup(blue,GPIO.OUT)
green = 12
GPIO.setup(green,GPIO.OUT)
camera = PiCamera()
camera.resolution = (608, 608)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(600, 600))

def blueBlink():
    global blue
    GPIO.output(blue,1)
    time.sleep(1)
    GPIO.output(blue,0)
    time.sleep(1)
def greenBlink():
    global green
    GPIO.output(blue,1)
    time.sleep(1)
    GPIO.output(blue,0)
    time.sleep(1)
    
# funtions for image overlay
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
    global image
    img_x = 260
    img_y = 340
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
    
def berns(overlay_image,size,kitni_baar,spacing=30):
    global image
    img_x = 190
    img_y = 140
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    if(kitni_baar <= 2):
        while i < kitni_baar:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
    else:
        while i < 2:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
            img_x = img_x+10
        img_x = img_x + 10
        img_y = img_y - 40
        count = 0
        i=0
        while i < kitni_baar-2:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
            img_x = img_x+10
          
def cliff(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    global image
    img_x = 170
    img_y = 260
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
    
def plane(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    global image
    img_x = 170
    img_y = 520
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
        img_x = img_x + 5

#Motor Actions   
def turn_right():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    #print "turn right"
def turn_left():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    #print "turn left"
def go_straight():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    #GPIO.output(Motor2E,1)
    #print "go straight"
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
    #print "extreme left"
def turn_extreme_right():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,1)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    #print "extreme_right"
    #GPIO.output(Motor2E,1)


def shape_recog(p1,p2,img2,string):
     print 'shape_recog'
     hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
     lower = np.array(p1)
     upper = np.array(p2)
     mask  = cv2.inRange(hsv, lower, upper)
     ret,thresh = cv2.threshold(mask,125,255,0)
     imgg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     t=0
     c=0
     s=0
     if len(contours) > 0:
       n1 = len(contours)
       for i in range(0,n1):
        if cv2.contourArea(contours[i]) >=1000:
          cnt1 = contours[i]
          approx = cv2.approxPolyDP(cnt1,0.04*cv2.arcLength(cnt1,True),True)
          #print len(approx)
          if len(approx)==3:
           t=t+1 
           #print "TRiangle"
          elif len(approx)==4:
           s=s+1
           #print "square"
          else:
           c=c+1 
           #print "circle"
     return t,c,s      
       
def color_recog(img):

 print 'color_recog'
 pblue2=[130,255,255]
 pblue1=[75,50,50]
 tb,cb,sb=shape_recog(pblue1,pblue2,img,'string1')
 for i in range(tb) :
  blueBlink()
  

 pgreen2=[69,255,110]
 pgreen1=[60,0,50]
 tg,cg,sg=shape_recog(pgreen1,pgreen2,img,'thre1')

 pred1 = [0,100,100]
 pred2 = [20,255,255]
 tr,cr,sr=shape_recog(pred1,pred2,img,'str2')
 markers={"tr":tr,"tg":tg,"tb":tb,"sr":sr,"sg":sg,"sb":sb,"tr":cr,"cg":cg,"cb":cb}
 print markers
 return markers


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

def get_contours(crop_img):#Used for copntour detection
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

  return contours
  



def motion_funtion(speed,delay_time=0.1)
  global camera
  current_dec = 0 #1 for Right -1 for Left 0 
  i = 5
  count = 1
  zone_count = 0
  byeByeCameraError = 10
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   image_frame = frame.array
   crop_img = image_frame[0:120, 240:400]
   crop_img1 = image_frame[120:240, 240:400]
   crop_img2 = image_frame[240:360, 240:400]
   crop_img3 = image_frame[360:480, 240:400]
   crop_img4 = image_frame[480:600, 240:400]
   if byeByeCameraError > 0:
     byeByeCameraError = byeByeCameraError -1
   else:
     if(get_area(image_frame)>95000):
      if count < 0:
        print "zone_marker_aagya"
        time.sleep(1)
        print "abc"
        motor_stop()
        time.sleep(1)    
        break
      count = count - 1
   
   contours = get_contours(crop_img)
   contours1 = get_contours(crop_img1)
   contours2 = get_contours(crop_img2)
   contours3 = get_contours(crop_img3)
   contours4 = get_contours(crop_img1)
      # Find the biggest contour (if detected)
   #delay_time = 0.1#add this as an argument
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
    if cv2.contourArea(c) > 600 or i > 0:
      i = i -1
      if cx >= 120: #right
       offset_x = (cx-60)
       #print offset_x
       turn_right()
       current_dec = 1
      if cx < 120 and cx > 50:
       go_straight()
      if cx <= 50: #left
       offset_x = (60-(60-cx))
       turn_left()
       current_dec = -1
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
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    if cv2.contourArea(c) > 600 or i > 0:
      i = i -1
      if cx >= 120: #right
       offset_x = (cx-60)
       turn_extreme_right()
       current_dec = 1
      if cx <= 50: #left
       offset_x = (60-(60-cx))
       turn_extreme_left()
       current_dec = -1
      if cx >50 and cx < 120:
       if current_dec == -1:
        turn_left()
       elif current_dec == 1:
        turn_right()
    else:# when all the frame go out of ranger
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

#camera.start_preview()
def click_a_pic():
  camera.capture('snapshot.png')
  #camera.stop_preview()
  detect = cv2.imread('snapshot.png')
  return color_recog(detect)
hills1={}
berns1={}
cliff1={}
plains1={}
motion_funtion(100,0.1)#zone1
hill1 = click_a_pic()
for key in hills1:
  print "berns"
  overlay_image = cv2.imread("lilac.png",-1)
  hillside(overlay_image,40,hills1[key],40)

motion_funtion(100,0.1)#zone2
berns1 = click_a_pic()
for key in berns1:
  print "berns"
  overlay_image = cv2.imread("lilac.png",-1)
  berns(overlay_image,40,berns1[key],40)

motion_funtion(100,0.1)#zone3
cliff1 = click_a_pic()
for key in cliff1:
  print "berns"
  overlay_image = cv2.imread("lilac.png",-1)
  cliff(overlay_image,40,cliff1[key],40)

motion_funtion(100,0.1)#zone4
plains1 = click_a_pic()
for key in plains1:
  print "berns"
  overlay_image = cv2.imread("lilac.png",-1)
  plain(overlay_image,40,plains1[key],40)

cv2.imwrite('lun.png', image)  
         
GPIO.cleanup()
