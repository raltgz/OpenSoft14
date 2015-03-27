import os
import cv2
import numpy as np
import math
from SmithWaterman import *
from GetCandidateMatchSet import *
from merge import *
from transform import *
from GetMergedImage import *
from Fragment import *
from config import *
from Image import *
from transform import *
import random
from GetThreshold import *

resultList = []
tempnames=[]

def test(I_List):
    for i in range(1,7):
        I_List.append("test8/"+str(i)+".jpg")
    return

def execute(I_List, countdown):
    resultList = []
#     I_List = resizeAllIfNeeded(I_List) # ONLY THIS IS ADDED TO RESIZE
    n_img=len(I_List)-1
#     print "****" + str(I_List[0])
    
    THRESHOLD = getThreshold(I_List[0]) - 2
    I_List.pop(0)
    print I_List
    image=[None for i in range(0,n_img)]
    corrected=[None for i in range(0,n_img)]
    kernel = np.ones((1,1),np.uint8)
    contours=[[] for i in range(0,n_img)]
    new_contours=[None for i in range(0,n_img)]
    contour_img=[None for i in range(0,n_img)]
    cont=[None for i in range(0,n_img)]
    turning=[[] for i in range(0,n_img)]
    turn_pts=[[] for i in range(0,n_img)]
    
    F=[]
    

    for i in range(0,n_img):
        imgname = I_List[i]

        imname=imgname[:-4]+str(i)+"temp"
        print(imname)
        image[i]=cv2.imread(imgname,0)
        
        #image[i]=cv2.resize(image[i],(0,0),image[i],0.5,0.5,cv2.INTER_AREA)
        
        color_img=cv2.imread(imgname,1)
        #color_img=cv2.resize(color_img,(0,0),image[i],0.5,0.5,cv2.INTER_AREA)
        
        #image[i]=cv2.GaussianBlur(image[i],(5,5),1)
        print("hell")
        image[i]=cv2.GaussianBlur(image[i],(5,5),1)
        print("helllllo")
        #Image Thresholding
        ret,threshold = cv2.threshold(image[i],THRESHOLD,255,cv2.THRESH_BINARY_INV)
        height,width= image[i].shape[:2]
        src2=np.zeros((height,width,3),np.uint8)
        corrected[i]=cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        open=cv2.morphologyEx(corrected[i], cv2.MORPH_OPEN, kernel)
        iii=cv2.bitwise_and(color_img,color_img,mask=open)
        
        
        #ret,threshold = cv2.threshold(image[i],THRESHOLD,255,cv2.THRESH_BINARY_INV)
        #height,width= image[i].shape[:2]
        # Drawing Contours
        #open=cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
        #corrected[i]=cv2.morphologyEx(threshold, cv2.MORPH_CLOSE, kernel)
        
        
        if ACCURACY == 1:
            param = cv2.CHAIN_APPROX_TC89_KCOS
        if ACCURACY == 2:
            param = cv2.CHAIN_APPROX_SIMPLE
        if ACCURACY == 3:
            param = cv2.CHAIN_APPROX_NONE
        new_contours[i], hierarchy = cv2.findContours(corrected[i],cv2.RETR_EXTERNAL,param)
        
        
    #     cv2.imshow("Image"+str(i),iii)
        color_img=None
        tempname="TEMP/"+str(i)+str(random.randint(0,100))+".png"
        tempnames.append(tempname)
        cv2.imwrite(tempname,iii)
        #exit()
        # cv2.waitKey(0)
        
        
        # cont1=np.zeros((1000,1000),np.uint8)
        # cv2.drawContours(cont1,new_contours[i],-1,255,1)
        # cv2.imshow("Contour",cont1)
        
        height,width= image[i].shape[:2]
        contour_img[i]=np.zeros((height,width,1), np.uint8)
        
        #displayContour("Cont1",new_contours[i])
        
        #print(new_contours[i])
        for cnt in new_contours[i]:
            if cv2.contourArea(cnt)>MIN_AREA:
                #displayContour("Contq"+str(cv2.contourArea(cnt)),[cnt])
                contours[i].extend(cnt)
        
        
        #contours[i]=contours[i][::1]    
        #contours[i]=cv2.approxPolyDP(new_contours[i][0],2,True)
        
        #contours[i]=[cnt for cnt in contours[i] if cv2.contourArea(cnt)>50000]
        if(len(contours[i])>C_LIMIT):
            contours[i]=contours[i][::int(len(contours[i])/C_LIMIT)]
    
        for num in range(NPOINTS,len(contours[i])-NPOINTS):
            vector1=(contours[i][num-NPOINTS][0]-contours[i][num][0])
            vector2=(contours[i][num+NPOINTS][0]-contours[i][num][0])
            
            #print(vector1)
            
            cos=(vector1[0]*vector2[0]+vector1[1]*vector2[1])/(math.sqrt((math.pow(vector1[0],2)+math.pow(vector1[1],2))*(math.pow(vector2[0],2)+math.pow(vector2[1],2))))
            turn=round(math.acos(cos),100)
            #print(turn)
            #if abs(turn)>=(10*3.14/180) and (abs(turn)<=(170*3.14/180) or abs(turn)>=(190*3.14/180)):
            turning[i].append(turn)
            turn_pts[i].append(contours[i][num])                
            
        
        frag=Fragment()
        frag.turning_angles=turning[i]
        frag.points=contours[i]
        frag.images = []
    #     image_ = Image()
    #     image_.name = "i"+str(i)+".jpeg"
    #     image_.transform_matrix= getIdentitymatrix()
    #     frag.images.append(image_)
    #     print "\nInit Matrix :\n"
    #     print frag.images[0].transform_matrix
        image_ = Image()
        image_.name = tempname
        image_.transform_matrix= getIdentitymatrix()
        frag.images.append(image_)
        print "\nInit Matrix :\n"
        print frag.images[0].transform_matrix
        F.append(frag)
        # print F.ima
        
        
        
        # cv2.drawContours(contour_img[i], contours[i], -1, 255, 1)
        # cv2.imshow('contour_image'+str(i),contour_img[i])
    
    FragmentList=GetMergedImage(F,countdown)
    
    print("Hello")
    
    cont3=np.zeros((1000,1000),np.uint8)
    
    # print(get1N2(FragmentList[0].points))
    
    # quit()
    
    for i in range(0,len(FragmentList)):
    #     cv2.drawContours(cont3,get1N2(FragmentList[i].points),-1,255,1)
    #     cv2.imshow("Output" + str(i),cont3)
        final_name = "FINAL"+str(i+1)+".png"
        # FragmentList[i]
        FragmentList[i].points = get1N2(FragmentList[i].points)
        createFinalImage(FragmentList[i],final_name)
        resultList.append(final_name)
    
    
    for name in tempnames:
        try:
            os.remove(name)
        except:
            pass
    #D=GetCandidateMatchSet(F)
    
    
    k=cv2.waitKey(0)
    if(k==27):
        cv2.destroyAllWindows()

    return resultList


def testss():
    I_List = []
    test(I_List)
    print len(I_List)
    execute(I_List)

    return

#testss()