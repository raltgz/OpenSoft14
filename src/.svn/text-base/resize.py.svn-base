
import cv2
import cv
import numpy as np
from config import *

HEIGHTMAX = 300.0
WIDTHMAX = 300.0

def isResizeNeeded(imglist):
	# returns true if resize
	maxheight = 0
	maxwidth = 0
	flag = False
	for i in range(0,len(imglist)):
		color_img=cv2.imread(imglist[i])
		height,width,channel = color_img.shape
		if(height > maxheight):
			maxheight = height
		if(width > maxwidth):
			maxwidth = width
	if((maxheight > HEIGHTMAX) or (maxwidth > WIDTHMAX)):
		flag = True
	scaleheight = HEIGHTMAX/(maxheight * 1.0)
	scalewidth = WIDTHMAX/(maxwidth * 1.0)

	return flag,min(scalewidth,scaleheight)
def getResizeMatrix(scale):
	T = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0]])
	T[0,0] = scale
	T[0,1] = 0
	T[0,2] = 0
	T[1,0] = 0
	T[1,1] = scale
	T[1,2] = 0
	return T

def resizeImage(imagename,newimgname,scale):
	T = getResizeMatrix(scale)
	img_i = cv2.imread(imagename)
	height,width,channel = img_i.shape
	height = int(height * scale)
	width = int(width * scale)
	affinedImage = cv2.warpAffine(img_i,T,(width,height))
	cv2.imwrite(newimgname, affinedImage)
	return

def resizeAllIfNeeded(imglist):
	resizeFlag,scale = isResizeNeeded(imglist)
	if(resizeFlag == False):
		return imglist
	newimglist = []
	for i in range(0,len(imglist)):
		newname = "resized_"+str(i+1)+".png"
		newimglist.append(newname)
		resizeImage(imglist[i],newname,scale)
	return newimglist

def printAspectRatio(imgname):
	color_img=cv2.imread(imgname)
	height,width,channel = color_img.shape
	return (height*1.0) / (width * 1.0)


def test():
	imglist = []

	imglist.append("test_new_7/scan0001.jpg")
	imglist.append("test_new_7/scan0002.jpg")
	imglist.append("test_new_7/scan0003.jpg")
	imglist.append("test_new_7/scan0004.jpg")
	imglist.append("test_new_7/scan0005.jpg")

	print imglist
	for i in range(0,len(imglist)):
		print "ASPECT [",i+1,"] = ",printAspectRatio(imglist[i])

	imglist = resizeAllIfNeeded(imglist)

	for i in range(0,len(imglist)):
		print "ASPECT [",i+1,"] = ",printAspectRatio(imglist[i])

	print imglist

	return

# if __name__ == "__main__":
#     main()