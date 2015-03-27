import Polygon
import numpy as np
from Matchset import * 
from transform import *
from merge import *

OVERLAPTHRSH = 200


'''
def getTransformationMatirxFromFragment(A,B,startA,endA,startB,endB,type):

 def testtransformFragment():
     A # fragment you have
 
     X.shape = Y.shape = [1,n,2]
     At = transformFragment(A,TA)
    BT = transformFragment(B,TB)
      BT.points[0],AT.points[0]
     
     send D.points[0] to your function
'''

def GetOverLappingArea(Matchset1,Matchset2):
    A=Matchset1.fragment_1
    B_start=Matchset1.match_2_start
    B_end=Matchset1.match_2_end
    C_start=Matchset2.match_2_start
    C_end=Matchset2.match_2_end
    A_start=Matchset1.match_1_start
    A_end=Matchset1.match_1_end
    B=Matchset1.fragment_2
    C=Matchset2.fragment_2
    a_start=0
    a_end=0
    if Matchset1.fragment_1==Matchset2.fragment_1:
        B=Matchset1.fragment_2
        B_start=Matchset1.match_2_start
        B_end=Matchset1.match_2_end
        C=Matchset2.fragment_2
        C_start=Matchset2.match_2_start
        C_end=Matchset2.match_2_end
        A=Matchset1.fragment_1
        A_start=Matchset1.match_1_start
        A_end=Matchset1.match_1_end
        a_start=Matchset2.match_1_start
        a_end=Matchset2.match_1_end
    if Matchset1.fragment_2==Matchset2.fragment_1:
        B=Matchset1.fragment_1
        B_start=Matchset1.match_1_start
        B_end=Matchset1.match_1_end
        C=Matchset2.fragment_2
        C_start=Matchset2.match_2_start
        C_end=Matchset2.match_2_end
        A=Matchset1.fragment_2
        A_start=Matchset1.match_2_start
        A_end=Matchset1.match_2_end
        a_start=Matchset2.match_1_start
        a_end=Matchset2.match_1_end
    if Matchset1.fragment_1==Matchset2.fragment_2:
        B=Matchset1.fragment_2
        B_start=Matchset1.match_2_start
        B_end=Matchset1.match_2_end
        C=Matchset2.fragment_1
        C_start=Matchset2.match_1_start
        C_end=Matchset2.match_1_end
        A=Matchset1.fragment_1
        A_start=Matchset1.match_1_start
        A_end=Matchset1.match_1_end
        a_start=Matchset2.match_2_start
        a_end=Matchset2.match_2_end
    if Matchset1.fragment_2==Matchset2.fragment_2:
        B=Matchset1.fragment_1
        B_start=Matchset1.match_1_start
        B_end=Matchset1.match_1_end
        C=Matchset2.fragment_1
        C_start=Matchset2.match_1_start
        C_end=Matchset2.match_1_end
        A=Matchset1.fragment_2
        A_start=Matchset1.match_2_start
        A_end=Matchset1.match_2_end
        a_start=Matchset2.match_2_start
        a_end=Matchset2.match_2_end
    # waitForESC()
    cv2.destroyAllWindows()
    TB=getTransformationMatirxFromFragment(A.points[0],B.points[0],A_start,A_end,B_start,B_end,1)
    # waitForESC()
    if(TB == None):
        return 0
    # print "\nTEMP ******************\n"
    # Ttemp=getTransformationMatirxFromFragment(A.points[0],B.points[0],A_start,A_end,B_start,B_end,1)
    # print "Ttemp"
    # print Ttemp
    # waitForESC()
    # print "\nTC ******************\n"
    TC=getTransformationMatirxFromFragment(A.points[0],C.points[0],a_start,a_end,C_start,C_end,1)
    # waitForESC()
    if(TC == None):
        return 0
    print "\n******************\n"
    # if(TB is None):
    #     # **************** srini 
    #     # test here

    # if(TC is None):
    #     # **************** srini 
    #     # test here

    
    

    Bt=getTransformedFragment(B,TB)
    Ct=getTransformedFragment(C,TC)
    Polygon.setDataStyle(Polygon.STYLE_NUMPY)
    b_poly = Polygon.Polygon(Bt.points[0])
    c_poly = Polygon.Polygon(Ct.points[0])

    intersection_polygon=b_poly&c_poly

    area =  intersection_polygon.area()

    return area

def test_overlap():
    f=Fragment()
    f.points=np.empty([1,8,2],np.int)
    g=Fragment()
    g.points=np.empty([1,7,2],np.int)
    h=Fragment()
    h.points=np.empty([1,6,2],np.int)
    
    F=f.points[0]
    F[0]=[000,000]

    F[1]=[400,000]   
    F[2]=[400,100]
    F[3]=[300,100]
    
    F[4]=[300,200] 
    F[5]=[200,200]
    F[6]=[200,300]
    F[7]=[000,300]
    
    G=g.points[0]
    G[0]=[200,400]
    G[1]=[200,300]
    G[2]=[200,200]
    G[3]=[300,200]
    G[4]=[300,100]
    G[5]=[600,100]
    G[6]=[600,400]
    
    H=h.points[0]
    H[0]=[300,200]

    H[1]=[300,100]
    H[2]=[400,100]
    H[3]=[400,000]
    
    H[4]=[700,000]
    H[5]=[700,200]

    f_start=3
    f_end=5

    g_end=2
    g_start=4

    f_start1 = 1
    f_end1 = 3

    h_start = 3
    h_end = 1
 
    t1 = getTransformationMatirxFromFragment(f.points[0], g.points[0], f_start, f_end, g_start, g_end, 1)

    #     print "t1"
    #     print t1


    t2 = getTransformationMatirxFromFragment(f.points[0], h.points[0], f_start1, f_end1, h_start, h_end, 1)
    
    #     print "t2"
    #     print t2
 
    M1 = Matchset()
    M1.fragment_1 = f
    M1.fragment_2 = g 
    M1.match_1_start = f_start
    M1.match_1_end = f_end
    M1.match_2_end = g_end
    M1.match_2_start = g_start

    M2 = Matchset()
    M2.fragment_1 = f
    M2.fragment_2 = h
    M2.match_1_start = f_start1
    M2.match_1_end = f_end1
    M2.match_2_end = h_end
    M2.match_2_start = h_start

    #     print GetOverLappingArea(M1,M2)

    displayContour("F",f.points,600,900)
    displayContour("G",g.points,600,900)
    displayContour("H",h.points,600,900)

    waitForESC()
    return

    
def GetArea(M):
    A=M.fragment_1
    B=M.fragment_2

    poly_a=Polygon.Polygon(A.points[0])
    poly_b=Polygon.Polygon(B.points[0])

    return poly_a.area()+poly_b.area()

def getOverLapArea(A,B,startA,endA,startB,endB,TB):
    Bt=getTransformedFragment(B,TB)
    Polygon.setDataStyle(Polygon.STYLE_NUMPY)
    b_poly = Polygon.Polygon(Bt.points[0])
    a_poly = Polygon.Polygon(A.points[0])

    intersection_polygon=b_poly&a_poly

    area =  intersection_polygon.area()

    return area


def isMatchPossibleWithArea(A,B,startA,endA,startB,endB):
    T = getTransformationMatirxFromFragment(B,A,startB,endB,startA,endA,config.FRAGMENT)
    if(T is None):
        print "Incompatable MatchSet Found ... requesting removal"
        return False
    overlap = getOverLapArea(A,B,startA,endA,startB,endB,T)
    if(overlap > OVERLAPTHRSH):
        print "Incompatable MatchSet Found OVERLAP AREA = ",overlap," THRESHOLD = ",OVERLAPTHRSH,"... requesting removal"
        return False
    return True

if __name__=='__main__':
    test_overlap()
        
        