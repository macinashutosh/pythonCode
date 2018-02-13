import cv2
import numpy as np
import time

img_name = "image6.png"
img = cv2.imread(img_name,1)
dic={"cr":"assorted.png","tr":"carnation.png","sr":"gerber.png","cg":"hibiscusred.png","tg":"marigold.png","sg":"hydrangeablue.png","cb":"hydrangeayellow.png","tb":"lilac.png","sb":"lily.png"}
def color_recog(p1,p2,img2,string):
     hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
     lower = np.array(p1)
     upper = np.array(p2)
     mask  = cv2.inRange(hsv, lower, upper)
     ret,thresh = cv2.threshold(mask,125,255,0)
     cv2.imshow("thresh",thresh)
     imgg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
     t=0
     c=0
     s=0
     if len(contours) > 0:
       n1 = len(contours)
       for i in range(0,n1):
        if cv2.contourArea(contours[i]) >=1200:
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
       
def detect_markers():
  pblue2=[130,255,255]
  pblue1=[75,50,50]
  tb,cb,sb=color_recog(pblue1,pblue2,img,'string1')
  pgreen2=[69,255,110]
  pgreen1=[60,0,50]
  tg,cg,sg=color_recog(pgreen1,pgreen2,img,'thre1')
  pred1 = [0,100,100]
  pred2 = [20,255,255]
  tr,cr,sr=color_recog(pred1,pred2,img,'str2')
  markers={"tr":tr,"tg":tg,"tb":tb,"sr":sr,"sg":sg,"sb":sb,"cr":cr,"cg":cg,"cb":cb}
  print markers


def blend_transparent(face_img, overlay_t_img):
    overlay_img = overlay_t_img[:,:,:3] 
    overlay_mask = overlay_t_img[:,:,3:] 
    background_mask = 255 - overlay_mask
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0)) 
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def hillside(image,overlay_image,size,kitni_baar,spacing=30):
    img_x = 260
    img_y = 340
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
def berns(image,overlay_image,size,kitni_baar,spacing=30):
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
def cliff(image,overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
    img_x = 170
    img_y = 260
    final_overlay = cv2.resize(overlay_image,(size,size), interpolation = cv2.INTER_CUBIC)
    count = 0
    i=0
    while i<kitni_baar:
        image[img_x:img_x+size,img_y+count:img_y+count+size] = blend_transparent(image[img_x:img_x+size,img_y+count:img_y+count+size],final_overlay)
        i = i + 1
        count = count+spacing
def plane(image,overlay_image,size,kitni_baar,spacing=30):#size of the flower should be small as it is far
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
image = cv2.imread("horizontal.jpg", -1)
overlay_image = cv2.imread("carnation.png",-1)

# number_of_times = 4
# size_of_flower = 40
# flower_spacing = 40
hillside(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for hillside size_of_flower = 40 flower_Spacing = 40
# berns(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for berns size_of_flower = 40 flower_Spacing = 40
# size_of_flower = 30
# flower_spacing = 30
# cliff(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for cliff size_of_flower = 30 flower_Spacing = 30
# size_of_flower = 30
# flower_spacing = 25
# plane(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for plane size_of_flower = 30 flower_Spacing = 25
detect_markers()
cv2.waitKey(0)
cv2.destroyAllWindows()











