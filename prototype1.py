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
     cv2.imshow(string,thresh)
     imgg, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     shapelist2 = list()
     cx1 = list()
     cy1 = list()
     if len(contours) > 0:
       n1 = len(contours)
       for i in range(0,n1):
          cnt1 = contours[i]
          M1 = cv2.moments(cnt1)
          if M1['m00']!= 0:
           cx1.append(int(M1['m10']/M1['m00']))
           cy1.append(int(M1['m01']/M1['m00']))

          approx = cv2.approxPolyDP(cnt1,0.01*cv2.arcLength(cnt1,True),True)
          if len(approx)==3:
           print "TRiangle"
          elif len(approx)==4:
           print "square"
          elif len(approx)>=15:
           print "circle"




       





    

  

# pred2=[20,255,255]
# pred1=[0,100,100]
# cx2,cy2,n = color_recog(pred1,pred2)
pblue2=[130,255,255]
pblue1=[75,50,50]
color_recog(pblue1,pblue2,img,'string1')


# for j in range (0,n):
#  cv2.putText(img,"Blue",(cx2[j]+10,cy2[j]+40),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
# j=0
# pgreen2=[69,255,110]
# pgreen1=[60,0,50]
# color_recog(pgreen1,pgreen2,img,'thre1')
# # for j in range (0,n):
# #  cv2.putText(img,"Green",(cx2[j]+10,cy2[j]+40),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)
# j=0
# pred1 = [0,100,100]
# pred2 = [20,255,255]
# color_recog(pred1,pred2,img,'str2')
# for j in range (0,n):
#  cv2.putText(img,"Red",(cx2[j]+10,cy2[j]+40),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1)


#cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()











