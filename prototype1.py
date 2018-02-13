import cv2
import numpy as np
import time

img_name = "image2.png"
img = cv2.imread(img_name,1)

def color_recog(p1,p2,img2,string):
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
          approx = cv2.approxPolyDP(cnt1,0.03*cv2.arcLength(cnt1,True),True)
          #print len(approx)
          if len(approx)==3:
           t=t+1 
           #print "TRiangle"
          elif len(approx)==4:
           s=s+1
           #print "square"
          elif len(approx)>=7:
           c=c+1 
           #print "circle"
     return t,c,s      
       
def detect_markers():
  pblue2=[100,255,255]
  pblue1=[75,50,50]
  tb,cb,sb=color_recog(pblue1,pblue2,img,'string1')

  pgreen2=[69,255,110]
  pgreen1=[60,0,50]
  tg,cg,sg=color_recog(pgreen1,pgreen2,img,'thre1')

  pred1 = [0,100,100]
  pred2 = [20,255,255]
  tr,cr,sr=color_recog(pred1,pred2,img,'str2')

  print "tr" +str(tr)
  print "tg" +str(tg)
  print "tb" +str(tb)
  print "cr" +str(cr)
  print "cg" +str(cg)
  print "cb" +str(cb)
  print "sr" +str(sr)
  print "sg" +str(sg)
  print "sb" +str(sb)



detect_markers()
cv2.waitKey(0)
cv2.destroyAllWindows()











