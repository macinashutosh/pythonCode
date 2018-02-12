from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
# Motor1A = 33
# Motor1B = 35
# Motor1E = 37
# Motor2A = 36
# Motor2B = 38
# Motor2E = 40

def getCentre(crop_img):
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(15,15),0)
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    img, contours, hierarchy = cv2.findContours(thresh, 1, cv2.CHAIN_APPROX_SIMPLE)
    cx = -1
    cy = -1
    if (len(contours)>1):
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
    sensitivity = 8
    if(abs(cx1-cx2) > sensitivity and cx1 > cx2):
        diff1 = right
    elif(abs(cx1-cx2) > sensitivity and cx1 < cx2):
        diff1 = left
    if(cx1 < 0):
        if previousDecision1 == left:
            diff1 = right
        else:
            diff1 = left
    if(cx2 < 0):
        if previousDecision1 == left:
            diff2 = right
        else:
            diff2 = left

    if(abs(cx2-cx3) > sensitivity and cx2 > cx3):
        diff2 = right
    elif(abs(cx2-cx3) > sensitivity and cx2 < cx3):
        diff2 = left

    if(abs(cx3-cx4) > sensitivity and cx3 > cx4):
        diff3 = right
    elif(abs(cx3-cx4) > sensitivity and cx3 < cx4):
        diff3 = left

    if(abs(cx4-cx5) > sensitivity and cx4 > cx5):
        diff4 = right
    elif(abs(cx4-cx5) > sensitivity and cx4 < cx5):
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
    if centreCount > leftCount and centreCount > rightCount:
        return centre,diff1,diff2
    elif leftCount > rightCount and leftCount > centreCount:
        return left,diff1,diff2
    elif rightCount > leftCount and rightCount > centreCount:
        return right,diff1,diff2
    elif diff1 == left and diff2 == left:
        return left,diff1,diff2
    elif diff1 == right and diff2 == right:
        return right,diff1,diff2
    else:
        return centre,diff1,diff2
def turn_left():
    GPIO.output(Motor1A,1)
    GPIO.output(Motor1B,1)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,1)
    #GPIO.output(Motor2E,1)
    print "turn left"
def turn_right():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,1)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,1)
    GPIO.output(Motor2B,1)
    #GPIO.output(Motor2E,1)
    print "turn right"
def go_straight():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,1)
    #GPIO.output(Motor1E,1)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,1)
    #GPIO.output(Motor2E,1)
    print "go straight"
def motor_stop():
    GPIO.output(Motor1A,0)
    GPIO.output(Motor1B,0)
    GPIO.output(Motor2A,0)
    GPIO.output(Motor2B,0)




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

speedb.start(25)#left motor
speeda.start(25)#right motor
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
left = -1
centre = 0
right = 1

previousDecision1 = centre
previousDecision2 = centre
decisionArr = [centre]
decisionItr = 0
i = 30
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if i > 0:
        i= i - 1
        time.sleep(0.1)
    else:
        image = frame.array
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

        decision , previousDecision1 , previousDecision2 =  getDecision(cx1,cx2,cx3,cx4,cx5,previousDecision1,previousDecision2)  
        decisionArr.append(decision)

        if decisionArr[decisionItr] == centre:
            go_straight()
        elif decisionArr[decisionItr] == left:
            turn_left()
        elif decisionArr[decisionItr] == right:
            turn_right()
        time.sleep(delay_time)
        decisionItr = decisionItr + 1;
        motor_stop()    
    
    
    rawCapture.truncate(0)
    #cv2.imshow('frame',image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    
    # while True:
    # #cv2.imshow('frame',image)
    #     cv2.putText(crop_img1,'CX:'+str(cx1), (15,30),font,1,(0,0,255),2)
    #     cv2.putText(crop_img1,'CY: '+str(cy1),(15,70),font,1,(0,0,255),2)
    #     cv2.putText(crop_img2,'CX:'+str(cx2), (15,30),font,1,(0,0,255),2)
    #     cv2.putText(crop_img2,'CY: '+str(cy2),(15,70),font,1,(0,0,255),2)
    #     cv2.putText(crop_img3,'CX:'+str(cx3), (15,30),font,1,(0,0,255),2)
    #     cv2.putText(crop_img3,'CY: '+str(cy3),(15,70),font,1,(0,0,255),2)
    #     cv2.putText(crop_img4,'CX:'+str(cx4), (15,30),font,1,(0,0,255),2)
    #     cv2.putText(crop_img4,'CY: '+str(cy4),(15,70),font,1,(0,0,255),2)
    #     cv2.putText(crop_img5,'CX:'+str(cx5), (15,30),font,1,(0,0,255),2)
    #     cv2.putText(crop_img5,'CY: '+str(cy5),(15,70),font,1,(0,0,255),2)
    #     cv2.imshow('Frame',image)
    #     # cv2.imshow('Frame 1',crop_img1)
    #     # cv2.imshow('Frame 2',crop_img2)
    #     # cv2.imshow('Frame 3',crop_img3)
    #     # cv2.imshow('Frame 4',crop_img4)
    #     # cv2.imshow('Frame 5',crop_img5)
    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break                    
     
GPIO.cleanup()