'''
* Team Id : <Team Id>
* Author List : Vivek Sood, Jaideep Singh, Ashutosh Singhal, Ayush Mallik
* Filename: submissionCode.py
* Theme: Planter Bot
* Functions: blueBlink, greenBlink,blend_transparent, hillside, berns,cliff, plane,turn_right, turn_left, go_straight, 
             motor_stop, turn_extreme_left, turn_extreme_right,shape_recog, color_recog, get_area, get_contours, motion_function, 
             click_a_pick 
* Global Variables: blue, green , red, image, camera
'''

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)


#This is the plantation image on which the seedlings have to be overlaid at the end of the run
image=cv2.imread('plant.png',-1) 
cv2.imshow('image',image)
cv2.waitKey(0)

#This dictionary contain the realtion between the color marker and the seedling images that needs to be overlaid
dic={"cr":"assorted.png","tr":"carnation.png","sr":"gerber.png","cg":"hibiscusred.png","tg":"marigold.png","sg":"hydrangeablue.png","cb":"hydrangeayellow.png","tb":"lilac.png","sb":"lily.png"}
color_list = {"tr":"red","sr":"red","cr":"red","tb":"blue","sb":"blue","cb":"blue","tg":"green","sg":"green","cg":"green"}

Motor1A = 29 #GPIO pin number for M+ of motor encoder for the Right Motor
Motor1B = 31 #GPIO pin number for M- of motor encoder for the Rigth Motor
Motor1E = 35 #GPIO pin number for Enable of motor encoder for the Right Motor
Motor2A = 38 #GPIO pin number for M+ of motor encoder for the Left Motor
Motor2B = 32 #GPIO pin number for M- of motor encoder for the Left Motor
Motor2E = 40 #GPIO pin number for Enable of motor encoder for the Left Motor

#The following section is used to set the GPIO pins of the Raspberry Pi as Outputs, Which will be the inputs to the 
#L298n motor Encoder
GPIO.setup(Motor1A,GPIO.OUT) 
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)

#The speed of the motor can be controlled by controlling the duty cycle of the Enable input of the Motor Encoder
#The duty cycle is produced using sqaure waves with varying on and off time.
#The duty cycle is changed using Pulse Width Modulation
#The idea is to control the duty cycle thereby reducing the average potential over an entire cycle to our desired value.
#Let us say that the duty cycle of the enable input is 25% and Vmax = 12Volts. Then the average given to motors is 25% of 12V, i.e 3V
#Since the speed of the motor is dependant upon the voltage supplied to the motor we control the speed of the motor.
#The frequency of the PWM square waves is set to be 100 Hz
#The motors are initially given a duty cycle of 100% making them use the entire battery power
speeda = GPIO.PWM(Motor1E,100)
speedb = GPIO.PWM(Motor2E,100)
speedb.start(100)
speeda.start(100)
#The motor should initially be at rest. Therefore the input to the motor is zero
GPIO.output(Motor1A,0)
GPIO.output(Motor1B,0)
GPIO.output(Motor2A,0)
GPIO.output(Motor2B,0)


blue = 22 #GPIO pin number that is connected to the BLUE pin of the RGB LED
GPIO.setup(blue,GPIO.OUT) # This GPIO is set as an output to control the RGB LED
green = 12 #GPIO pin number that is connected to the GREEN pin of the RGB LED
GPIO.setup(green,GPIO.OUT) # This GPIO is set as an output to control the RGB LED
red = 16 #GPIO pin number that is connected to the RED pin of the RGB LED
GPIO.setup(red,GPIO.OUT) # This GPIO is set as an output to control the RGB LED


 
# an object with the name of 'camera' has been created to use in-built functions of the PiCamera library to capture and record frames by 
#referencing this object 
camera = PiCamera()
#The camera resolution , or pixel length x width of the image is set to 608 x 608
camera.resolution = (608, 608)
#The framerate of the camerra defines how many frames can be captured at most by the camera in 1s. Here set to 32
camera.framerate = 32
#We wish to capture the image in the form of an array where the value of the pixel is stored in the RGB format.
rawCapture = PiRGBArray(camera, size=(600, 600))

'''
*Function Name : blueBlink
*Input : None
*Output : Does not return any value. This function is used to blink the LED 
*Logic : The LED is switched On for 1 second and then switched off for 1 second
*Example Call : blueBlink()
'''
def blueBlink():
    global blue
    #The Blue pin of the RGB LED is turned on
    GPIO.output(blue,1)
    time.sleep(1)
    # The Blue pin of the RGB LED is turned off
    GPIO.output(blue,0)
    time.sleep(1)


'''
*Function Name : greenBlink
*Input : None
*Output : Does not return any value. This function is used to blink the LED 
*Logic : The LED is switched On for 1 second and then switched off for 1 second
*Example Call : greenBlink()
'''
def greenBlink():
    global green
    # The Green pin of the RGB LED is turned on
    GPIO.output(blue,1)
    time.sleep(1)
    # The Green pin of the RGB LED is turned off
    GPIO.output(blue,0)
    time.sleep(1)


'''
*Function Name : redBlink
*Input : None
*Output : Does not return any value. This function is used to blink the LED 
*Logic : The LED is switched On for 1 second and then switched off for 1 second
*Example Call : redBlink()
'''
def redBlink():
    global red
    # The Red pin of the RGB LED is turned on
    GPIO.output(red,1)
    time.sleep(1)
    # The Red pin of the RGB LED is turned off
    GPIO.output(red,0)
    time.sleep(1)
    
'''
*Function Name : blend_transparent
*Input : main image on which the seedling is to be superimposed, seedling image
*Output : The pixel values in the form of a list that are to be altered on the main image
*Logic : 
'''
def blend_transparent(face_img, overlay_t_img):
    overlay_img = overlay_t_img[:,:,:3] 
    overlay_mask = overlay_t_img[:,:,3:] 
    background_mask = 255 - overlay_mask
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0)) 
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

'''
*Function Name : hillside
*Input : The seedling image which has to be overlaid, the size of the seedling image, the no. of markers detected, and the spave between two images
*Output : Overlays the seedling images on the plantation image
*Logic : It is first necessary to identify and choose an appropriate starting pixel value, where this Zone starts. The images will start being 
         stacked from this point. The seedling image is resized so that they do not overlap once overlaid. We have to then use the blend transparent 
         function to find the altered values of the image pixel such that the image is superimposed properly. We need to iterate this procedure for n number of times
         where n is the no. of images that need to superimposed,giving a spce of 30 pixels between two adjacent images
'''
def hillside(overlay_image,size,kitni_baar,spacing=30):
    global image
    #Starting Pixel of image overlay
    img_x = 260
    img_y = 340
    #Resized seedling image
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    
    count = 0 # This variable is used to keep a record of the number of images so that the pixel value of the next image may be given appropriate spacing 
    
    i=0 #Iterating variable

    while i<kitni_baar:
        #The pixel values of the Plantation image that need to be altered are received from the blend transparent function and are substituted 
        #with correct indexing
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        #This variable increases after every iteration to keep track of the already superimposed images
        i = i + 1
        #The starting pixel of each seedling image needs to be updated after overlaying each image. 
        #The starting Pixel of the next image must be the previous starting value+padding 
        #This variable keeps track of that padding required and provides the starting pixel for each Seedling image
        count = count+spacing
  
'''
*Function Name : Berns
*Input : The seedling image which has to be overlaid, the size of the seedling image, the no. of markers detected, and the spave between two images
*Output : Overlays the seedling images on the plantation image
*Logic : It is first necessary to identify and choose an appropriate starting pixel value, where this Zone starts. The images will start being 
         stacked from this point. The seedling image is resized so that they do not overlap once overlaid. We have to then use the blend transparent 
         function to find the altered values of the image pixel such that the image is superimposed properly. We need to iterate this procedure for n number of times
         where n is the no. of images that need to superimposed,giving a spce of 30 pixels between two adjacent images
'''
def berns(overlay_image,size,kitni_baar,spacing=30):
    global image
    #Starting Pixel of image overlay
    img_x = 190
    img_y = 140
    #Resized seedling image
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0 # This variable is used to keep a record of the number of images so that the pixel value of the next image may be given appropriate spacing 
    i=0 # iterating Variable
    # Now the images in the berns section cannot be placed in a line if the no. of images exceed 2.
    #If the number of images is less than 2 we proceed as discussed earlier
    if(kitni_baar <= 2):
        while i < kitni_baar:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
    else:
        #When the no. of images exceed 2, we first place the first two images as it is
        while i < 2:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            count = count+spacing
            img_x = img_x+10
        #Then the starting pixel values of the next images value are changed as follows:
        img_x = img_x + 10
        img_y = img_y - 40
        count = 0
        i=0
        while i < kitni_baar-2:
            image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
            i = i + 1
            #For the exceeding images the y spacing and the x spacing are both changed to avoid overlapping
            count = count+spacing
            img_x = img_x+10
  
'''
*Function Name : Cliff
*Input : The seedling image which has to be overlaid, the size of the seedling image, the no. of markers detected, and the spave between two images
*Output : Overlays the seedling images on the plantation image
*Logic : 
'''       
def cliff(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    # The procedure for overlaying the images is exactly the same as discussed for the hillside zone
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
    
'''
*Function Name : Plane
*Input : The seedling image which has to be overlaid, the size of the seedling image, the no. of markers detected, and the spave between two images
*Output : Overlays the seedling images on the plantation image
*Logic : 
'''
def plane(overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
   # The procedure for overlaying the images is exactly the same as discussed for the hillside zone
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


'''
*Function Name : turn_right
*Input : None
*Output : Turns the right wheel off and Turns the left wheel on so that the robot moves in the right direction
*Logic : Differential Drive Mechansim - Only keeping the left wheel on turns the Robot in the right Direction
*Example Call : turn_right()
''' 
def turn_right():
    #Right Motor is given Input 0 to stop rotation
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    #Left Motor is given Input 1 to move in forward direction, turning the Robot Right
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
    
'''
*Function Name : turn_left
*Input : None
*Output : Turns the right wheel on and Turns the left wheel off so that the robot moves in the left Direction
*Logic : Differential Drive Mechansim - Only keeping the right wheel on turns the Robot in the left Direction
*Example Call : turn_right()
'''
def turn_left():
    #Right Motor is given Input 1 to move in forward direction, turning the Robot Left
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #Left Motor is given input 0 to stop  rotation
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)

'''
*Function Name : go_straight
*Input : None
*Output : Moves the Robot in the forward direction
*Logic : Turns the left wheel and the right wheel fowrard simultaneously in the same direction, moving the robot forward
*Example Call : go_straight()
'''
def go_straight():
    #Both Motors are given input 1 to make the Robot move Forward
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
   

'''
*Function Name : motor_stop
*Input : None
*Output : Stops the motor where it stands
*Logic : The input to the motor encoder is made zero for both the left and the right wheels
*Example Call : motor_stop()
'''
def motor_stop():
    #Both Motors are given input 0 to make the Robot Stop
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)

'''
*Function Name : turn_extreme_left
*Input : None
*Output : Turns the right wheel in the forward direction and Turns the left wheel in the reverse direction so that the robot moves in the left direction
*Logic : During sharp turns it is better to reverse the polarity of one motor so that the turning angle becomes sharper.
*Example Call : turn_extreme_left()
'''
def turn_extreme_left():
    #The right wheel moves in clockwise rotation
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,0)
    #The left wheel moves in counter clockwise rotation
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,1)
    

'''
*Function Name : turn_extreme_right
*Input : None
*Output : Turns the right wheel in the revesre direction and Turns the left wheel in the forward direction so that the robot moves in the right direction
*Logic : During sharp turns it is better to reverse the polarity of one motor so that the turning angle becomes sharper.
*Example Call : turn_extrme_right()
'''
def turn_extreme_right():
    #The right wheel moves in counter clockwise rotation
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,1)
    #The left wheel moves in clockwise rotation
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,0)
   

'''
*Function Name : shape_recog
*Input : Takes the threshold values of the particular color, which it will detect the shapes for
*Output : Returns the number of the shapes detectd in the following order triangles,circles,squares
*Logic : The image is first thresholded. It is thresholded such that we are left with only that part of the image that lies in the color range tha we have currently
         selected. Then the contours of the image are found. The contours are then approximated such that we find tthe no. of line segemnts that a shape makes
         This is done using the ApproxPolyDP function. If the number of line seg,emts formed = 3, the shape is assumed to be a triangle. If the No. of line segments 
         are 4 then the shape is assumed to be a square. Otherwise the shape must be a circle
'''
def shape_recog(p1,p2,img2,string):
     #The image format of the array is converted from BGR to HSV so that color detection can be done more accurately
     hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
     #The lower and upper range of the respective colour is made into a numpy array
     lower = np.array(p1)
     upper = np.array(p2)
     #Only those vlaues which lie within our range remain in the image. Rest are given binary 0 value.
     mask  = cv2.inRange(hsv, lower, upper)
     #This image is thresholded for finding the contours.
     ret,thresh = cv2.threshold(mask,125,255,0)
     imgg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     #Temporary value of the number of shapes detected. initialised as zero
     t=0
     c=0
     s=0
     #If contours exist then proceed
     if len(contours) > 0:
       n1 = len(contours)
       #Iterate through each shape with it's list of contours
       for i in range(0,n1):
        #Contours with area smaller than this value are to be neglected as they may be some erroneous shadows.
        if cv2.contourArea(contours[i]) >=1000:
          cnt1 = contours[i]
          #Approximate those contours that lie on an arc and give the no. of vertices as the result
          approx = cv2.approxPolyDP(cnt1,0.04*cv2.arcLength(cnt1,True),True)
          #Triangle should have 3 vertices
          if len(approx)==3:
           t=t+1 
          #Square should have 4 vertices
          elif len(approx)==4:
           s=s+1
          #Else it ought to be a circle    
          else:
           c=c+1
     return t,c,s      
       
'''
*Function Name :  color_recog
*Input : The image of the color markers aroung the Zone indictaor
*Output : Returns a list of the number of shapes and their respective colours
*Logic : We know that the RGB values of various colors lie within a range defined by it's upper bound and lower bound. Hence we have 3 possible ranges 
         for red, green and blue. The image is first thresholded using the range of the blue color. This is done by passing the values of the threshold to the 
         shape recogniton function. the shape recognition function returns alist of the shapes if there are any shapes of the colour currently under inspection
         The threshold values are then changed and the entire process is repeated for all the three ranges. The final result is a list of the color markers
         with their colours and their shapes.
'''
def color_recog(img):

 #The HSV upper and Lower bound of the blue colour are given
 pblue2=[130,255,255]
 pblue1=[75,50,50]
 #This boundary is given to the shape recognition function for appropriate thresholding
 tb,cb,sb=shape_recog(pblue1,pblue2,img,'string1')
 #The Blue LED should blink as many times as there are blue objects
 
 #The same process is followed for finding green markers
 pgreen2=[69,255,110]
 pgreen1=[60,0,50]
 tg,cg,sg=shape_recog(pgreen1,pgreen2,img,'thre1')
 # The same process is followed for finding red markers
 pred1 = [0,100,100]
 pred2 = [20,255,255]
 tr,cr,sr=shape_recog(pred1,pred2,img,'str2')
 #A combined list of all the markers with their colour and shape is returned
 markers={"tr":tr,"tg":tg,"tb":tb,"sr":sr,"sg":sg,"sb":sb,"tr":cr,"cg":cg,"cb":cb}
 return markers

'''
*Function Name :  get_area
*Input : The cropped image or the ROI
*Output : Returns the area of the contour of the black path
*Logic : We first convert the color of the image from BGR to Grayscale. We remove the Grid lines by blurring the image using Gaussian Blur. 
         The image is then thresholded so that the white space in te image acquires binary 0 vlaue and the black area acquires binary balue 255.
         Thsi will allow the contours to be detected clearly. In case multiple contours are detected we consider only the contour with maximum area
         and return this value
'''
def get_area(crop_img):
  #Convert the image to Grayscale Image
 gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
 #Convert the image to Grayscale Image
 blur = cv2.GaussianBlur(gray,(5,5),0)
 # The pixels with grayscale value greater than 60 are given value 255 and the rest are reduced to zero
 ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
 # Erode and dilate to remove accidental line detections
 mask = cv2.erode(thresh1, None, iterations=2)
 mask = cv2.dilate(mask, None, iterations=2)
 # Find the contours of the frame
 img, contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
 #Find the maximum contour
 area = 0
 if len(contours) > 0: 
   c = max(contours, key=cv2.contourArea)
   #Find the centre of the maximum contour
   M = cv2.moments(c)
   #Find The area of this contour
   area =  cv2.contourArea(c)
   #Return this value
 print area 
 return area 

'''
*Function Name :  get_contours
*Input : The cropped Image or the ROI
*Output : Returns a list of the contours of the black path for the line follower
*Logic :  We first convert the color of the image from BGR to Grayscale. We remove the Grid lines by blurring the image using Gaussian Blur. 
         The image is then thresholded so that the white space in te image acquires binary 0 vlaue and the black area acquires binary balue 255.
         Thsi will allow the contours to be detected clearly. We then return this contour array
'''
def get_contours(crop_img):#Used for contour detection
  #Convert the image to Grayscale Image
  gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

  #Blur the grid lines 
  blur = cv2.GaussianBlur(gray,(5,5),0)

  # Color thresholding same as in get_area function
  ret,thresh1 = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

  # Erode and dilate to remove accidental line detections
  mask = cv2.erode(thresh1, None, iterations=2)
  mask = cv2.dilate(mask, None, iterations=2)

  # Find the contours of the frame
  img, contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

  return contours
  
'''
*Function Name : motion_function
*Input : Speed at which you wish the robot to traverse, and a delay with which the robot will stop afetr detecting the Zone Indicator
*Output : None
*Logic : The Robot captures a frame using the Picamera and inspects the frame by dividing it into 5 different areas or Regions Of Interests(ROI)
         The Five regions of interset divides the entire image into 5 rows.
         Each row is selected starting from the top and processed to find if there is any black line on which the robot is to traverse 
         present or not. And hence find the contours
         If the centre of the contour does lies within the Central region of the ROI then the bot moves forward
         However if the centre does not lie in the central region then a decision is made based upon the position of the centre
         If the centre lies towards the right of the centyral region the bot is made to turn right and the same paradigm for the left turn
         In case there is no contour present in the Top most ROI then the next ROI or the second row of the Image is considred for line detection
         This continues until a contour is found.
         The Zone is indicated by keeping track of the area of the Contour. We know that area of the Zone Indicator would be larger than the area of the Path.
         Using this property a threshold value is set, which when exceeded indicates that a Zone INdicator has been found

*Example Call : motion_function(40,0.2)
'''
def motion_funtion(speed,delay_time=0.1):
  global camera
  current_dec = 0 #1 for Right -1 for Left 0 
  i = 5
  count = 1
  zone_count = 0
  byeByeCameraError = 10
  rawCapture.truncate(0)
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
        if current_dec == -1:
         turn_left()
        elif current_dec == 1:
         turn_right()
        time.sleep(0.4)
        motor_stop()
        time.sleep(0.5)    
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

'''
*Function Name : click_a_pic
*Input : None
*Output : Returns the list of various color markers with their shapes present in the Image clicked around the Zone Indiactor
*Logic : camera.capture takes an image using the raspberry picam and stores it in the file specified in given format. This image is given to 
the color recognition function which also further uses the shape recognition function that processes and returns the list of Color Markers
*Example Call : click_a_pic()
'''
def click_a_pic():
  #Use the camera object to capture an image of the Zone Markers
  camera.capture('snapshot.png')
  #Read the captured image from the file
  detect = cv2.imread('snapshot.png')
  #Provide this image to the color and shape detection function and transfer control back while calling this function
  answer  =  color_recog(detect)
  return answer


hills1={} #Empty List created where the list of the colour markers for the Hills Zone will be stored
berns1={} #Empty List created where the list of the colour markers for the Berns Zone will be stored
cliff1={} #Empty List created where the list of the colour markers for the Cliffs Zone will be stored
plains1={} #Empty List created where the list of the colour markers for the Plains Zone will be stored
endLED=[] #Empty List for LED Pattern Storage to display in the end
motion_funtion(80,0.08)#zone1

#Once the Zone Indicator is found the motion_function breaks. We then process the current frame of the PiCam for the Color Markers.
#The First zone is te Hillside Hence any Markers found in this region are to be consequently shown by overlaying appropriate seedlings in this region 
hill1 = click_a_pic()
#THe list Hill1 contains all the markers detected in this Zone, hence is traversed to select one marker at a time to overlay the image on the Plantation image
for key in hills1:
  print "hills"
  if not hills[key] == '':
    string = "./Seedling"+key
    overlay_image = cv2.imread(string,-1)
    endLED.append([color_list[key],hills1[key]])
    blink_led(color_list[key],hills1[key])
    hillside(overlay_image,40,hills1[key],40)

#The robot then moves onto the next Zone to repeat the same process. The Berns are the second zone in the track
motion_funtion(60,0.07)#zone2
#This function breaks once the Zone Indicator is found
#The same process as discussed earlier is used to overlay the images according to the Markers in this region
berns1 = click_a_pic()
for key in berns1:
  print "berns"
  if not berns1[key] == '':
    string = "./Seedling"+key
    overlay_image = cv2.imread(string,-1)
    blink_led(color_list[key],berns1[key])
    endLED.append([color_list[key],berns1[key]])
    overlay_image = cv2.imread("lilac.png",-1)
    berns(overlay_image,40,berns1[key],40)
#The robot then continues onto the next Zone which is the Cliff
motion_funtion(70,0.1)#zone3
#This function breaks once the Zone Indicator is found
#The same process as discussed earlier is used to overlay the images according to the Markers in this region
cliff1 = click_a_pic()
for key in cliff1:
  print "cliff"
  if not cliff1[key] == '':
    string = "./Seedling"+key
    overlay_image = cv2.imread(string,-1)
    endLED.append([color_list[key],cliff1[key]])
    blink_led(color_list[key],cliff1[key])
    cliff(overlay_image,40,cliff1[key],40)
#The robot then continues onto the next Zone which is the Plains
motion_funtion(60,0.05)#zone4
#This function breaks once the Zone Indicator is found
#The same process as discussed earlier is used to overlay the images according to the Markers in this region
plains1 = click_a_pic()
for key in plains1:
  print "plain"
  if not plains1[key] == '':
    endLED.append([color_list[key],plains1[key]])
    blink_led(color_list[key],plains1[key])
    string = "./Seedling"+key
    overlay_image = cv2.imread(string,-1)
    plain(overlay_image,40,plains1[key],40)
#The entire path has been traversed

motion_funtion(90,0.1)
motion_funtion(80,0.1)
#The final image with all the seedlings overlaid according to the color markers is then stored
cv2.imwrite('answer.png', image) 
#To Run The LEDs at the end of the code
for i in endLED:
    blink_led(endLED[i][0],endLED[i][1]) 
#Reserved or Used GPIO pins are cleared
GPIO.cleanup()
