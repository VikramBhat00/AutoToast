import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import math

import models

DISPLAY = False #Set this to true to display intermediate CV steps

ct = 0


def init_camera():
    vcap  = cv2.VideoCapture(1)

    # Adjust camera lighting
    ramp_frames = 30
    for i in range(ramp_frames):
        temp = vcap.read()



    return vcap



def close_camera(capture):

    cv2.destroyAllWindows()
    capture.release()

#Get the done-ness of a piece of toast 
#Using Computer Vision

def get_doneness(vcap):

    global ct

    #Get Image From Camera
    
    ret, image = vcap.read()

    if DISPLAY:
        cv2.imshow("original picture", image)
        cv2.waitKey(0)
    cv2.imwrite("images/" + str(ct) + ".jpg", image)

    #Threshold Image to get the region that's been marked off with blue tape

    hsvImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #Convert to HSV : H 0- 179, S: 0-255 , V: 0-255
    hsvImgBlur = cv2.blur(hsvImg, (3, 3)) #Blur

                            # H    S   V
    RED_MIN_high = np.array([160, 100, 80])
    RED_MAX_high = np.array([179, 255, 255])
    RED_MIN_low = np.array([0, 100, 80])
    RED_MAX_low = np.array([10, 255, 255])


    frame_threshed_red_high = cv2.inRange(hsvImg, RED_MIN_high, RED_MAX_high)
    frame_threshed_red_low = cv2.inRange(hsvImg, RED_MIN_low, RED_MAX_low)

    frame_threshed_red = frame_threshed_red_low+frame_threshed_red_high
    frame_threshed_red = cv2.blur(frame_threshed_red, (5,5))

    ret, thresh = cv2.threshold(frame_threshed_red, 127,255,cv2.THRESH_BINARY) #Turn into binary image 

    kernel = np.ones((9, 9), np.uint8)
    thresh = cv2.erode(thresh, kernel) 

    if DISPLAY:
        cv2.imshow("Red Threshold", thresh)
        cv2.waitKey(0)

    #Find Contour
    contour_mask = np.zeros(image.shape, dtype='uint8') #Create mask for contour

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in range(len(contours)):
        #print(cv2.contourArea(contours[c]))
        if cv2.contourArea(contours[c]) >= 10000: #Get only big thing
            cv2.drawContours(contour_mask, contours, c, color=(255, 255, 255), thickness=cv2.FILLED)
            break

    #c = contours[0] #GET FIRST (ONLY?) Contour 

    if DISPLAY:
        cv2.imshow("Raw Contours", contour_mask)
        cv2.waitKey(0)

    #Turn Contour Mask into Binary Image from RGB
    ret,contour_mask = cv2.threshold(contour_mask,127,255,cv2.THRESH_BINARY)
    contour_mask = contour_mask[:,:,0] #make 1 channel

    mask_size = np.sum(contour_mask != 0) #Number white pixels
    #print("Mask Size: ", mask_size)
    if DISPLAY:
        cv2.imshow("Contour Mask", contour_mask)
        cv2.waitKey(0)


    #Now we have a mask to overlay on original image to get just bread

    #Want to get the average grayscale pixel value for the bread region - will tell us how 'done' it is


    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #make image grayscale
    # print(gray_img)
    #print(gray_img.shape)
    #print(contour_mask.shape)
    masked_img = cv2.bitwise_and(gray_img, contour_mask)
    #print(masked_img)
    if DISPLAY:
        cv2.imshow("Masked Gray Image", masked_img)
        cv2.waitKey(0)

    #Average Grayscale value of bread
    avg = np.sum(masked_img) / mask_size
    #print("Average Value: ", avg)
    #Display avg grayscale color:
    disp = np.ones((100,100))
    disp[:,:] = avg/255
    # print(avg)
    # print(disp)

    if DISPLAY:
        cv2.imshow("Average Toast Color (Grayscale)", disp)
        cv2.waitKey(0)

    ct += 1

    cv2.imshow("Average Toast Color (Grayscale)", image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        return

    return avg

#get_doneness()



# c = init_camera()
# get_doneness(c)
# close_camera(c)