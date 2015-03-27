import numpy as np
import math
import cv2

from Matchset import *
from Fragment import *
from config import *
from Image import *
from transform import *

# Parameters.. Some Optimization Required
space=SPACE
match=MATCH
mismatch=SPACE

#Global Storage Variables
isInitialized=False
scoreTable=None
sequence1=""
sequence2=""
traceBack=[]
traceBack1=[]

'''
class Cell:
    prevCell=None
    score=0
    row=0
    col=0
        
    def __init__(self,row=0,col=0,score=0):
        self.row=row
        self.col=col
        self.score=score
        
'''

#Cell Declaration Format 
#cell[row,col,score,prev_row,prev_col]
highScoreCell=[]
    


def getInitialScore(row,col):
   return 0

def getInitialPointer(row,col):
   return None


def initialize(length1,length2):
    global scoreTable,isInitialized,highScoreCell
    scoreTable = np.zeros((length1,length2,5),np.uint64) 
    for i in range(0,length1):
        for j in range(0,length2):
            scoreTable.itemset((i, j ,0),i)
            scoreTable.itemset((i, j ,1),j)    
    initializeScores(length1,length2);
    initializePointers(length1,length2);
    highScoreCell=np.zeros((5),np.uint64)

    isInitialized = True;

def initializeScores(length1,length2):
    global scoreTable
    for i in range(0,length1):
        for j in range(0,length2):
            scoreTable.itemset((i, j ,2),getInitialScore(i, j));
         

def initializePointers(length1,length2):
    global scoreTable
    for i in range(0,length1):
        for j in range(0,length2):
            scoreTable.itemset((i, j ,3),-1)
            scoreTable.itemset((i, j ,4),-1)


def fillInCell(row,col,cellAbove, cellToLeft, cellAboveLeft):
    global space,match,mismatch,scoreTable,sequence1,sequence2,highScoreCell
    rowSpaceScore = cellAbove.item(2) + space
    colSpaceScore = cellToLeft.item(2) + space
    matchOrMismatchScore = cellAboveLeft.item(2)
    if(abs(sequence1[row - 1] - sequence2[col - 1])<(ANGLEDIFF*3.14/180) and abs(sequence1[row - 1])>=(FLAT_THRESHOLD*3.14/180) and (abs(sequence1[row - 1])<=((180-FLAT_THRESHOLD)*3.14/180) or abs(sequence1[row - 1])>=((180+FLAT_THRESHOLD)*3.14/180))):
        matchOrMismatchScore += match;
    else:
        matchOrMismatchScore += mismatch;
        
    if(rowSpaceScore >= colSpaceScore):
        if(matchOrMismatchScore >= rowSpaceScore):
            if(matchOrMismatchScore > 0):
                #print(matchOrMismatchScore)
                scoreTable.itemset((row,col,2),matchOrMismatchScore);
                scoreTable.itemset((row,col,3),cellAboveLeft.item(0));
                scoreTable.itemset((row,col,4),cellAboveLeft[1]);
        else:
            if(rowSpaceScore > 0):
                scoreTable.itemset((row,col,2),rowSpaceScore);
                scoreTable.itemset((row,col,3),cellAbove.item(0));
                scoreTable.itemset((row,col,4),cellAbove.item(1));
    else:
        if(matchOrMismatchScore >= colSpaceScore):
            if(matchOrMismatchScore > 0):
                scoreTable.itemset((row,col,2),matchOrMismatchScore);
                scoreTable.itemset((row,col,3),cellAboveLeft.item(0));
                scoreTable.itemset((row,col,4),cellAboveLeft.item(1));
        else:
            if(colSpaceScore > 0):
                scoreTable.itemset((row,col,2),colSpaceScore);
                scoreTable.itemset((row,col,3),cellToLeft.item(0));
                scoreTable.itemset((row,col,4),cellToLeft.item(0));
    if(scoreTable.item(row,col,2) > highScoreCell.item(2)):
        highScoreCell = scoreTable[row][col];
        


def fillIn(length1,length2):
    for row in range(1,len(scoreTable)):
        for col in range(1,len(scoreTable[row])):
            currentCell = scoreTable[row][col]
            cellAbove = scoreTable[row - 1][col]
            cellToLeft = scoreTable[row][col - 1]
            cellAboveLeft = scoreTable[row - 1][col - 1]
            fillInCell(row,col, cellAbove, cellToLeft, cellAboveLeft);
            

def displayContour(name,contour):
    cont=np.zeros((1000,1000),np.uint8)
#     print(contour)
    cv2.drawContours(cont,contour,-1,255,1)
    cv2.imshow(name,cont)


def CompareContour(F1,F2):
    global sequence1,sequence2,scoreTable,traceBack,traceBack1
    sequence1=F1.turning_angles
    sequence2=F2.turning_angles[::-1]
    
    # print("sequence1")
    # print(sequence1)
    # print("sequence2")
    # print(sequence2)

    l1=len(sequence1)+1
    l2=len(sequence2)+1
    initialize(l1,l2)
    fillIn(l1,l2)
    
    start_end=getTraceback(F1.points,F2.points[::-1],F1.turning_angles,F2.turning_angles[::-1])
    match= Matchset()
    match_1=Fragment()
    match_2=Fragment()
    lt=len(traceBack)
    match_1.points=get1N2(traceBack)
    match_2.points=get1N2(traceBack1)
    
    FF1=Fragment()
    FF2=Fragment()
    
    
    FF1.points=get1N2(F1.points)
    FF1.turning_angles=F1.turning_angles
    FF2.points=get1N2(F2.points)
    FF2.turning_angles=F2.turning_angles

    FF1.images = []
    FF2.images = []



    for i in range(0,len(F1.images)):
        image = Image()
        image.name = F1.images[i].name
        image.transform_matrix = getIdentitymatrix() * F1.images[i].transform_matrix
        FF1.images.append(image)

    for i in range(0,len(F2.images)):
        image = Image()
        image.name = F2.images[i].name
        image.transform_matrix = getIdentitymatrix() * F2.images[i].transform_matrix
        FF2.images.append(image)
    
    
    match.fragment_1=FF1
    match.fragment_2=FF2
    match.match_1=match_1
    match.match_2=match_2
    match.score=highScoreCell[2]
    match.match_1_start=start_end[0]
    match.match_2_start=l2-start_end[1]+1
    match.match_1_end=start_end[2]
    match.match_2_end=l2-start_end[3]+1
    
    
    
    
    contour_img=np.zeros((1000,1000,1), np.uint8)
    contour_img1=np.zeros((1000,1000,1), np.uint8)
    
    #traceBack=cv2.approxPolyDP(traceBack,2,True)
    
    lt=len(traceBack1)
    #displayContour("TraceBack"+str(lt),traceBack)
    #displayContour("TraceBack1"+str(lt),traceBack1)

    #cv2.drawContours(contour_img, traceBack, -1, 255, 1)
    #cv2.drawContours(contour_img1, traceBack1, -1, 255, 1)
    
    #displayContour("Match1",traceBack)
    #displayContour("Match2",traceBack1)
    
    
    # cv2.imshow('IMPORTANT !!! :D',contour_img)
    # cv2.imshow('IMPORTANT2 !!! :D',contour_img1)
    
#     print("Length 1")
#     print(len(traceBack1))
#     print("Length 2")
#     print(len(traceBack))
#     


    contour_img=np.zeros((500,500),np.uint8)

    #cv2.drawContours(contour_img,np.array(traceBack),-1,255,1)

    return match
    
    
def get1N2(contour):
    size=len(contour)
    cont=np.empty([1,size,2],np.int)
    for j in range(0,size):
        cont[0][j] = contour[j]
    return cont


def getList(fragment):
    size=len(fragment.points[0])
    cont=[fragment.points[0][x] for x in range(0,size)]
    fragment.points=cont
    return fragment


def getTraceback(track,track1,s1,s2):
    global traceBack,traceBack1,highScoreCell,sequence1,sequence2,scoreTable
    traceBack=[]
    traceBack1=[]
    cell=highScoreCell
    print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAYYYYYYY")
    #print(sequence1)
    #print(highScoreCell.score)
    match_1=[]
    match_2=[]
    while(cell[2]!=0):
        row=int(cell[0]-1)
        col=int(cell[1]-1)
        print(row)
        print(col)
        if(row >=0 and col>=0):
            traceBack.append(track[row])
            traceBack1.append(track1[col])
            cell=scoreTable[cell[3]][cell[4]]
            match_1.append(sequence1[row])
            match_2.append(sequence2[col])
    print("MATCHESSSSSS")
    print(match_1)
    print(match_2)
    return [int(highScoreCell[0]),int(highScoreCell[1]),int(cell[0]),int(cell[1])]


def getTurning(fragment):
    contour=fragment.points
    turning=[]
    for num in range(3,len(contour)-3):
        vector1=(contour[num-3]-contour[num])
        vector2=(contour[num+3]-contour[num])
        
        cos=(vector1[0]*vector2[0]+vector1[1]*vector2[1])/(math.sqrt((math.pow(vector1[0],2)+math.pow(vector1[1],2))*(math.pow(vector2[0],2)+math.pow(vector2[1],2))))
        turn=round(math.acos(cos),100)
        
        turning.append(turn)
    fragment.turning_angles=turning
    return fragment
    