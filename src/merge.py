import sys
import math
import cv2
import numpy as np
import random
import config
from Fragment import *
from transform import *
from Image import *
# requires transform.py



def getMergedFragment(A,B,startA,endA,startB,endB,flag):
	# print "WE ARE HERE"
	# print "startA = ",startA,"endA = ",endA,"startB = ",startB,"endB = ",endB
	print "\nIMAGES IN A = ",len(A.images)
	print "\nIMAGES IN B = ",len(B.images)
	T = getTransformationMatirxFromFragment(B,A,startB,endB,startA,endA,config.FRAGMENT)
	if(T is None):
		return None
	
# 	print T
	dummy1,sizeA,dummy2 = A.points.shape
	dummy1,sizeB,dummy2 = B.points.shape

	if(flag == config.ENHANCEMODE):
		startA,endA,startB,endB = findProperStartAndEndPoint(A,B,startA,endA,startB,endB,T)

	Xnumpy = np.empty([1,sizeA+sizeB+2,2],np.int)
	X = Xnumpy[0]
	contourA = A.points[0]
	contourB = B.points[0]

	j = 0
	if(endA > startA and endB > startB):
		# print "FIRST CASE"
		for i in range(0,startA+1):
			X[j] = contourA[i]
			j = j+1
		for i in range(startB-1,-1,-1):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(sizeB-1,endB-1,-1):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(endA+1,sizeA):
			X[j] = contourA[i]
			j = j+1
	if(endA > startA and endB < startB):
		# print "2nd CASE"
		for i in range(0,startA):
			X[j] = contourA[i]
			j = j+1
		for i in range(startB,sizeB):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(0,endB):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(endA,sizeA):
			X[j] = contourA[i]
			j = j+1
	if(endA < startA and endB > startB):
		# print "3rd CASE"
		for i in range(0,endA+1):
			X[j] = contourA[i]
			j = j+1
		for i in range(endB+1,sizeB):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(0,startB):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(startA,sizeA):
			X[j] = contourA[i]
			j = j+1
	if(endA < startA and endB < startB):
		# print "4th CASE"
		for i in range(0,endA):
			X[j] = contourA[i]
			j = j+1
		for i in range(endB-1,-1,-1):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(sizeB-1,startB,-1):
			P = getTransformedPoint(T,contourB[i])
			X[j] = P
			j = j + 1
		for i in range(startA,sizeA):
			X[j] = contourA[i]
			j = j+1
	# now j is the number of points on the new contour
	
	F = Fragment()
	F.points = np.empty([1,j,2],np.int)
	for i in range(0,j):
		F.points[0][i] = X[i]
	F.images = []
	
	for i in range(0,len(A.images)):
		image = Image()
		image.name = A.images[i].name
		image.transform_matrix = A.images[i].transform_matrix
		print "\nMatrix ",i," (A)","\n"
		print image.transform_matrix
		F.images.append(image)

	for i in range(0,len(B.images)):
		image = Image()
		image.name = B.images[i].name
		image.transform_matrix = T * ( B.images[i].transform_matrix )
		print "\nMatrix ",i," (B)","\n"
		print image.transform_matrix
		F.images.append(image)
	print "\nIMAGES IN F = ",len(F.images)
	return F

def N12Frag(As):
	A = Fragment()
	sizeA = len(As.points)
	A.points = np.empty([1,sizeA,2],np.int)
	for i in range(0,sizeA):
		A.points[0][i] = As.points[i]
	A.turning_angles = As.turning_angles
	A.images = As.images
	return A
	

#def getMergedFragment(As,Bs,startA,endA,startB,endB,flag,convert):
#	
#	A = N12Frag(As)
#	B = N12Frag(Bs)
#	
#	X =  getMergedFragment1(A,B,startA,endA,startB,endB,flag)
#	
#	return X
#

def getBoundingPointSofFragment(A):
	X = A.points[0]
	dummy1,sizeA,dummy2 = A.points.shape

	leftMost = X[0]
	rightMost = X[0]
	upMost = X[0]
	downMost = X[0]

	for i in range(0,sizeA):
		if(X[i][0] < leftMost[0]):
			leftMost = X[i]
		if(X[i][0] > rightMost[0]):
			rightMost = X[i]
		if(X[i][1] < downMost[1]):
			downMost = X[i]
		if(X[i][1] > upMost[1]):
			upMost = X[i]
	return leftMost,rightMost,upMost,downMost

def getDimension(leftMost,rightMost,upMost,downMost):
	# (leftMost,rightMost,upMost,downMost)
	print "UPMOST = ",upMost[1]," DOWNMOST = ",downMost[1]
	height = int(math.fabs(upMost[1]-downMost[1]))
	width = int(math.fabs(leftMost[0]-rightMost[0]))
	print "HEIGHT WITHOUT MARGIN = ",height
	print "WIDTH WITHOUT MARGIN = ",width
	return (height+config.MARGIN*2),(width+config.MARGIN*2)

def getFinalTranslationMatrix(leftMost,rightMost,upMost,downMost):
	tx = 0
	ty = 0
	if(leftMost[0]<=0):

		tx = (int(math.fabs(leftMost[0])) + config.MARGIN)
	else:
		tx = config.MARGIN - leftMost[0]
	if(downMost[1]<=0):
		ty = (int(math.fabs(downMost[1])) + config.MARGIN)
	else:
		ty = config.MARGIN - downMost[1]

	return getSampleTransformationMatrix(0,tx,ty)

def combineAndAddImages(A,height,width,final_name):
	# code to blindly create a recombined image
	image = np.zeros((height,width,3),np.uint8)
	# print "We are here !"

	# M = np.float32([[1,0,100],[0,1,50]])
	# dst = cv2.warpAffine(img,M,(cols,rows))
	for i in range(0,len(A.images)):
		img_i = cv2.imread(A.images[i].name)
		print img_i.shape
		rows,cols,channel = img_i.shape
		T = threeD_to_TwoD_Affine(A.images[i].transform_matrix)
		print("*************************")
		print (A.images[i].name)
		print T
		print("**************************")
		affinedImage = cv2.warpAffine(img_i,T,(width,height))
		affinedname = "affine_"+str(i+1)+".png"
		# cv2.imwrite(affinedname, affinedImage)
		# cv2.imshow(affinedname,affinedImage)
		# waitForESC()
		print "\nStarting Addition\n"
		image = cv2.addWeighted(image,1,affinedImage,1,0)
		# image = addImage(image,affinedImage)
		print "\nEnding Addition\n"	
	# cv2.imshow(final_name,image)
	cv2.imwrite(final_name, image)
	#waitForESC()
	
	return image

def createFinalImage(A,final_name):
	print "\nIN create FINAL IMAGE\n"
	leftMost,rightMost,upMost,downMost = getBoundingPointSofFragment(A)
	print "\nLEFTMOST = ",leftMost," RIGHTMOST = ",rightMost," UPMOST = ",upMost," DOWNMOST = ",downMost
	height,width = getDimension(leftMost,rightMost,upMost,downMost)

	print "\nOPTIMAL HEIGHT = ",height,"WIDTH = ",width

	T = getFinalTranslationMatrix(leftMost,rightMost,upMost,downMost)
	print T
	for i in range(0,len(A.images)):
		A.images[i].transform_matrix = T * A.images[i].transform_matrix

	return combineAndAddImages(A,height,width,final_name)
'''
def displayContour(imgname,contour,height,width):
	img = np.zeros((height,width,1),np.uint8)
	cv2.drawContours(img,contour,-1,255,1)
	cv2.imshow(imgname,img)
	return'''


