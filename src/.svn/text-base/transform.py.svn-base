import sys
import math
import cv2
import numpy as np
import random
import config
from Fragment import *

def displayContour_transform(imgname,contour,height,width):
	img = np.zeros((height,width,1),np.uint8)
	cv2.drawContours(img,contour,-1,255,1)
	cv2.imshow(imgname,img)
	return

def displayPartOfFragment(imgname,A,startA,endA,height,width):
	partSize = int(math.fabs(startA - endA))+1
	dummy1,sizeA,dummy2 = A.points.shape
	print "\n*** sizeA = ",sizeA,"startA = ",startA," End = ",endA," PartSize = ",partSize
	X = np.empty([1,partSize,2],np.int)
	if(startA<endA):
		j = 0
		for i in range(startA,endA+1):
			X[0][j] = A.points[0][i]
			j = j + 1
	if(startA>endA):
		j = 0
		for i in range(startA,endA-1,-1):
			X[0][j] = A.points[0][i]
			j = j + 1
	#displayContour_transform(imgname,X,height,width)
	return

def waitForESC():
	k=cv2.waitKey(0)
	if(k==27):
		cv2.destroyAllWindows()
	return

def getDistance(X,Y):
	dist = (X[0] - Y[0])*(X[0] - Y[0]) + (X[1] - Y[1])*(X[1] - Y[1])
	return math.sqrt(dist)

def iround(x):
	# """iround(number) -> integer
	# Round a number to the nearest integer."""
	return int(round(x) - .5) + (x > 0)

def getTransformedPoint(T,P):
	# tested
	X = np.matrix([[0],[0],[1]])
	X[0] = P[0]
	X[1] = P[1]
	# print X
	Y = T * X
	# print Y
	if((Y[2]-1)>.000001):
		print "WARNING:Value!=1 in 3rd homogeneous dimension"
	Y[2] = 1
	Q =  np.squeeze(np.asarray(Y))
	Q = [iround(Q[0]),iround(Q[1])]
	# print P," ---> ",Q
	return Q


def twoD_to_ThreeD_Affine(T):
	# tested
	A = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
	A[0,0] = T[0,0]
	A[0,1] = T[0,1]
	A[0,2] = T[0,2]
	A[1,0] = T[1,0]
	A[1,1] = T[1,1]
	A[1,2] = T[1,2]
	A[2,0] = 0.0
	A[2,1] = 0.0
	A[2,2] = 1.0
	return A

def threeD_to_TwoD_Affine(T):
	# tested
	A = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0]])
	A[0,0] = T[0,0]
	A[0,1] = T[0,1]
	A[0,2] = T[0,2]
	A[1,0] = T[1,0]
	A[1,1] = T[1,1]
	A[1,2] = T[1,2]
	return A

def getSampleTransformationMatrix(theta,tx,ty):
	Rot = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
	Tran = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

	Tran[0,0] = Tran[1,1] = Tran[2,2] = 1
	Tran[0,2] = tx
	Tran[1,2] = ty

	Rot[0,0] = math.cos(theta)
	Rot[0,1] = math.sin(theta)
	Rot[1,0] = -1.0 * math.sin(theta)
	Rot[1,1] = math.cos(theta)
	Rot[2,2] = 1.0

	return Tran * Rot

def getTransformationMatrixFromArray(A,B):
	# A,B both have to be numpy array
	# they must contain same number of points say n
	# so shape of A,B = [1,n,2]
	# returns a 3*3 np.matrix and a success flag(=1->OH yeah , 0 ->:())
	T = cv2.estimateRigidTransform(A,B,False)
	#T2 = cv2.estimateRigidTransform(A,B,False)
	#T=(T1+T2)/2
	dummy1,sizeA,dummy2 = A.shape
	dummy1,sizeB,dummy2 = B.shape
	X = np.empty([2,max(sizeA,sizeB),2])
	X[0] = A
	X[1] = B
	# print X
	z =random.randint(0,10000)
	if(T is None):
		# waitForESC()
		textA = "FAILED_CHECK_A"+str(z)
		textB = "FAILED_CHECK_B"+str(z)
		#displayContour_transform(textA,A,700,700)
		#displayContour_transform(textB,B,700,700)
		return None
	textA = "SUCCESS_CHECK_A"+str(z)
	textB = "SUCCESS_CHECK_B"+str(z)
	
	'''r1 = math.sqrt(T[0,0] * T[0,0] + T[0,1]*T[0,1])
	T[0,0] =T[0,0]/r1
	T[0,1] =T[0,1]/r1
	r2 = math.sqrt(T[1,0] * T[1,0] + T[1,1]*T[1,1])
	T[1,0] =T[1,0]/r2
	T[1,1] =T[1,1]/r2'''
	
	#displayContour_transform(textA,A,700,700)
	#displayContour_transform(textB,B,700,700)
	return twoD_to_ThreeD_Affine(T)

def getTransformationMatrixFromFragment_3pairs(A,B,startA,endA,startB,endB):
	T  = None

	A3 = np.empty([1,3,2],np.int)
	B3 = np.empty([1,3,2],np.int)
	# print A.shape," ",startA," ",endA
	A3[0][0] = A[startA]
	A3[0][2] = A[endA]
	B3[0][0] = B[startB]
	B3[0][2] = B[endB]
	
	middleA = (startA + endA)/2
	middleB = (startB + endB)/2
	
	A3[0][1] = A[middleA]
	B3[0][1] = B[middleB]


	T = cv2.estimateRigidTransform(A3,B3,False)
	#print T
	if(T is not None):
		r1 = math.sqrt(T[0,0] * T[0,0] + T[0,1]*T[0,1])
		T[0,0] =T[0,0]/r1
		T[0,1] =T[0,1]/r1
		r2 = math.sqrt(T[1,0] * T[1,0] + T[1,1]*T[1,1])
		T[1,0] =T[1,0]/r2
		T[1,1] =T[1,1]/r2
		return twoD_to_ThreeD_Affine(T) 
	print "WE are in shit !"
	print "*********************"
	# print A3,B3
	# def displayContour(imgname,contour,height,width):
	img = np.zeros((800,800,1),np.uint8)
	contour = np.empty([2,3,2],np.int)
	contour[0] = A3
	contour[1] = B3
	# cv2.drawContours(img,contour,-1,255,1)
	# cv2.imshow("Contours",img)
	# k=cv2.waitKey(0)
	# if(k==27):
	# 	cv2.destroyAllWindows()
	
	# return
	print "*********************"
	# i = (endA-middleA)
	# while(T is None):
		
	# return twoD_to_ThreeD_Affine(T)
	return None
def getIdentitymatrix():
	T = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
	for i in range(0,3):
		for j in range(0,3):
			T[i,j] = 0.0
		T[i,i] = 1.0
	return T
def getTransformationMatrixFrom_3_pairs(A,B,startA,middleA,endA,startB,middleB,endB):
	A3 = np.empty([1,3,2],np.int)
	B3 = np.empty([1,3,2],np.int)

	A3[0][1] = A.points[0][1]
	A3[0][2] = A.points[0][2]
	A3[0][3] = A.points[0][3]

	B3[0][1] = B.points[0][1]
	B3[0][2] = B.points[0][2]
	B3[0][3] = B.points[0][3]

	return cv2.estimateRigidTransform(A3,B3,False)

def getTransformationMatrixFromFragment_Always_Success(A,B,startA,endA,startB,endB,type):
	# T = getTransformationMatirxFromFragment(A,B,startA,endA,startB,endB,type)
	# print "***************** we are here ********************"
	# print T
	# if(T is None):
	print "************** Warning : Optimal Rigid Transformation was not successfull !!"
	if(type == config.CONTOUR):
		return getTransformationMatrixFromFragment_3pairs(A,B,startA,endA,startB,endB)
	else:
		return getTransformationMatrixFromFragment_3pairs(A.points[0],B.points[0],startA,endA,startB,endB)

def transformCountour(C,T,flag):
	# Tested for numpy array
	# transforms the contour C with transformation matrix 
	# changes are applied on C,,, no new contour is created
	# C is assumed in this shape [1,n,2] ... where n is the number of points
	# on the contour
	if(flag == config.NORMALNUMPY):
		(dummy1,n,dummy2) = C.shape
		for i in range(0,n):
			C[0][i] = getTransformedPoint(T,C[0][i])
		return
	if(flag == config.NUMPY_SHAPE_N_2):
		(n,dummy2) = C.shape
		for i in range(0,n):
			C[i] = getTransformedPoint(T,C[i])
		return


def reservoirSample(A,B,n,k):
	# tested
	# reservoir sampling without sorting n = A.size k = B.size
	# print "IN RESERVOIR n = ",n,"k=",k
	for i in range(0,k):
		B[i] = A[i]
	for i in range(k,n):
		j = random.randint(1,i)
		if(j < k):
			B[j] = A[i]
	return

def selectNfromM(A,B,n,k):
	separation = (n*1.0)/(k*1.0)
	# print "\nseparation = ",separation
	index = 0
	for i in range(0,k):
		if(index>=n):
			index = n-1
		B[i] = A[index]
		nextIndex = separation * i
		if(nextIndex == index):
			nextIndex = nextIndex + 1
		index = nextIndex
	return

def getTransformationMatirxFromFragment(A,B,startA,endA,startB,endB,type):
	# MAY FAIL if transformation is not feasible entirely or all the points are on straight line need to resolve
	# Here A and B are Fragments
	# startA and endA are points on A and same for B
	# B have to be moved such that startB --> startA endB --> endB
	# na = |endA - startA|+1 nb = |endB - startB|+1
	# if na!=nb we will do a reservoir sampling on the larger one
	# to make both the contours of the same size say n
	# next numpy arrays of shape (1,n,2) are created and the transformation is computed
	na = int(math.fabs(startA - endA))
	nb = int(math.fabs(startB - endB))
	n = min(na,nb)
	m = max(na,nb)
	
#	if(m!=n):
#		print "\n **************** m = ",m," n = ",n,"   INTRODUCING RANDOMNESS ********\n"

# 	print "in getTransformationFromFragmetn m = ",m," n = ",n,"startA = ",startA,"endA = ",endA,"startB = ",startB,"endB = ",endB


	X = np.empty([1,na+1,2],np.int)
	Y = np.empty([1,nb+1,2],np.int)
	Z = np.empty([1,n+1,2],np.int)

	reservoir = np.arange(m)
	sample = np.arange(n)
	
	reservoirSample(reservoir,sample,m,n)
	sample.sort()

	#selectNfromM(reservoir,sample,m,n)

	if(endA>startA):
		# print A.shape
		# print X.shape
		j = 0
		for i in range(startA,endA+1):
			
			# print A[0][i]
			if(type == config.CONTOUR):
				X[0][j] = A[i]
			if(type == config.FRAGMENT):
				X[0][j] = A.points[0][i]
			j = j + 1
	else:
		j = 0
		for i in range(startA,endA-1,-1):
			if(type == config.CONTOUR):
				X[0][j] = A[i]
			if(type == config.FRAGMENT):
				X[0][j] = A.points[0][i]
			j = j + 1
	if(endB>startB):
		j = 0
		for i in range(startB,endB+1):
			if(type == config.CONTOUR):
				Y[0][j] = B[i]
			if(type == config.FRAGMENT):
				Y[0][j] = B.points[0][i]
			j = j + 1
	else:
		j = 0
		for i in range(startB,endB-1,-1):
			if(type == config.CONTOUR):
				Y[0][j] = B[i]
			if(type == config.FRAGMENT):
				Y[0][j] = B.points[0][i]
			j = j + 1
	
	if(na>nb and startA<endA):
		for i in range(0,n):
			Z[0][i] = X[0][sample[i]]
		X = Z
	if(na>nb and startA>endA):
		for i in range(n-1,-1,-1):
			Z[0][i] = X[0][sample[i]]
		X = Z
	if(na<nb and startB<endB):
		for i in range(0,n):
			Z[0][i] = Y[0][sample[i]]
		Y = Z
	if(na<nb and startB>endB):
		for i in range(n-1,-1,-1):
			Z[0][i] = Y[0][sample[i]]
		Y = Z
	T = getTransformationMatrixFromArray(X,Y)
	if(T is None):
		return getTransformationMatrixFromFragment_Always_Success(A,B,startA,endA,startB,endB,type)
	else:
		return T

def getRandom(a,b):
	# gives a rondom numeber between a,b
	# always succeeds
	if(a == b):
		print "Warning random number in empty interval asked !!\n"
		return a
	if(a<b):
		return random.randint(a,b)
	return random.randint(b,a)

def getTransformedFragment(A,T):
	if(T == None):
		return None
	B = Fragment()
	(dummy1,sizeA,dummy2) = A.points.shape
	B.points = np.empty([1,sizeA,2],np.int)
	B.images = 0
	B.turning_angles = 0
	for i in range(0,sizeA):
		B.points[0][i] = A.points[0][i]
	transformCountour(B.points,T,config.NORMALNUMPY)
	return B

def findProperStartAndEndPoint(A,B,startA,endA,startB,endB,T):
	# TEST PASSED
	contourA = A.points[0]
	contourB = B.points[0]
	dummy1,sizeA,dummy2 = A.points.shape
	dummy1,sizeB,dummy2 = B.points.shape
	if(endA > startA and endB > startB):
		while(True):
			distStart = getDistance(contourA[startA],getTransformedPoint(T,contourB[startB]))
			if(distStart > config.MAXPIXELSEPARATION or startA == 0 or startB == 0):
				break
			startA = startA-1
			startB = startB-1
		while(True):
			distEnd = getDistance(contourA[endA],getTransformedPoint(T,contourB[endB]))
			if(distEnd > config.MAXPIXELSEPARATION or endA == sizeA-1 or endB == sizeB-1):
				break
			endA = endA+1
			endB = endB+1
		return startA,endA,startB,endB
	if(endA > startA and endB < startB):
		while(True):
			distStart = getDistance(contourA[startA],getTransformedPoint(T,contourB[startB]))
			if(distStart > config.MAXPIXELSEPARATION or startA == 0 or startB == sizeB-1):
				break
			startA = startA-1
			startB = startB+1
		while(True):
			distEnd = getDistance(contourA[endA],getTransformedPoint(T,contourB[endB]))
			if(distEnd > config.MAXPIXELSEPARATION or endA == sizeA-1 or endB == 0):
				break
			endA = endA+1
			endB = endB-1
		return startA,endA,startB,endB
	if(endA < startA and endB > startB):
		while(True):
			distStart = getDistance(contourA[startA],getTransformedPoint(T,contourB[startB]))
			if(distStart > config.MAXPIXELSEPARATION or startA == sizeA-1 or startB == 0):
				break
			startA=startA+1
			startB=startB-1
		while(True):
			distEnd = getDistance(contourA[endA],getTransformedPoint(T,contourB[endB]))
			if(distEnd > config.MAXPIXELSEPARATION or endA == 0 or endB == sizeB-1):
				break
			endA = endA-1
			endB = endB+1
		return startA,endA,startB,endB
	if(endA < startA and endB < startB):
		while(True):
			distStart = getDistance(contourA[startA],getTransformedPoint(T,contourB[startB]))
			if(distStart > config.MAXPIXELSEPARATION or startA == sizeA-1 or startB == sizeB-1):
				break
			startA = startA+1
			startB = startB+1
		while(True):
			distEnd = getDistance(contourA[endA],getTransformedPoint(T,contourB[endB]))
			if(distEnd > config.MAXPIXELSEPARATION or endA == 0 or endB == 0):
				break
			endA = endA-1
			endB = endB-1
		return startA,endA,startB,endB

def isMatchPossible(A,B,startA,endA,startB,endB):
	T = getTransformationMatirxFromFragment(B,A,startB,endB,startA,endA,config.FRAGMENT)
	if(T is None):
		print "Incompatable MatchSet Found ... requesting removal"
		return False
	return True