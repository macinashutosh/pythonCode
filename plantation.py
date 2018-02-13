import cv2
import numpy as np
import os

def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
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
    # while True:
    #     cv2.imshow('frame',image)
    #     # cv2.imshow('Frame', final_overlay)

    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break

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

    # while True:
    #     cv2.imshow('frame',image)
    #     # cv2.imshow('Frame', final_overlay)

    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break


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
    # while True:
    #     cv2.imshow('frame',image)
    #     # cv2.imshow('Frame', final_overlay)

    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break
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
    # while True:
    #     cv2.imshow('frame',image)
    #     # cv2.imshow('Frame', final_overlay)

    #     if cv2.waitKey(25) & 0xFF == ord('q'):
    #         break
image = cv2.imread("Plantation.png", -1)
overlay_image = cv2.imread("Seedlings/carnation.png",-1)

number_of_times = 4
size_of_flower = 40
flower_spacing = 40
hillside(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for hillside size_of_flower = 40 flower_Spacing = 40
berns(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for berns size_of_flower = 40 flower_Spacing = 40
size_of_flower = 30
flower_spacing = 30
cliff(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for cliff size_of_flower = 30 flower_Spacing = 30
size_of_flower = 30
flower_spacing = 25
plane(image,overlay_image,size_of_flower,number_of_times,flower_spacing)#for plane size_of_flower = 30 flower_Spacing = 25
while True:
        cv2.imshow('frame',image)
        # cv2.imshow('Frame', final_overlay)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
# img_x = image.shape[1]
# img_y = image.shape[0]
# print img_x
# print img_y
# count_x = 20
# count_y = 20
# while count_x < img_x:
#     cv2.line(image, (count_x, 0), (count_x, img_y), (255, 0, 0), 1, 1)
#     count_x = count_x + 20
# while count_y < img_y:
#     cv2.line(image, (0, count_y), (img_x, count_y), (255, 0, 0), 1, 1)
#     count_y = count_y + 20
# image[1:40,1:40] = [255,255,255]
# print image[1:100,1:200,0]
# x,y,w,h = cv2.boundingRect(image[1:40,1:40])
# final_overlay = cv2.resize(overlay_image,(40,40), interpolation = cv2.INTER_CUBIC)
# image[260:300,340:380] = blend_transparent(image[260:300,340:380],final_overlay)

# x,y,w,h = cv2.boundingRect(cont)
# diff = 0
# diff = w - len(frame[y:y+w,x:x+h,:])
# # print len(frame[y:y+w,x:x+h,:])
# overlay_image1g = cv2.resize(imgg,(h,w-diff), interpolation = cv2.INTER_CUBIC)
# frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:],overlay_image1g)