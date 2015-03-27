from Fragment import *
from Matchset import *
from Neighbour import *
from GetCandidateMatchSet import GetCandidateMatchSet
from GetNeighbourhood import GetNeighbourhood
from GetGlobalConsistency import GetGlobalConsistency
from merge import getMergedFragment
from merge import * 
from SmithWaterman import *
from transform import *
#to do list : complete MergeFragment() function
def GetMergedImage(F,countdown):
    L = len(F)
    W = L #number of unmerged fragments
    iter=0
    while (W!=1):
        countdown.updatenumber(W)
        print W
#         print F 
       
        TF = []
        F1 = []
        F2 = []
        for k in range(0,W):
            F1.append(0)
            F2.append(0)
#         for i in range(0,W):
#             TF.append(F[i].turning_angles)
#         print "Before Candidate MatchSet"
        M=None
        M = GetCandidateMatchSet(F,iter)
        iter+=1
#         print "After Candidate MatchSet"
        N = len(M)
        if N == 0:
            break
        # for i in range(0,N):
        #     A = M[i]
        #     frag1 = A.fragment_1
        #     frag2 = A.fragment_2
        #     imagename1 = "Matchset_"+str(i+1)+"_fragment1"
        #     imagename2 = "Matchset_"+str(i+1)+"_fragment2"
        #     displayPartOfFragment(imagename1,A.fragment_1,A.match_1_start,A.match_1_end,700,700)
        #     displayPartOfFragment(imagename2,A.fragment_2,A.match_2_start,A.match_2_end,700,700)
        #     waitForESC()
        #     cv2.destroyAllWindows()
        #G_list = GetNeighbourhood(M)

#        print M
#        print G_list
#         print "After Nbr"
        #x = GetGlobalConsistency(M,G_list)
        #print x
#         print "After glob cons"
        
        print "N=" + str(len(M))
        for i in range(0,N):
            print("Merge")
            print (M[i].i)
            print (M[i].j)
            if 1:
                if F2[M[i].i] == 0 and F2[M[i].j] == 0:
                    try:
                        new_mergedfrag = getMergedFragment(M[i].fragment_1,M[i].fragment_2,M[i].match_1_start,M[i].match_1_end
                                                       ,M[i].match_2_start,M[i].match_2_end,1)
                        #displayContour("mergeFragment"+str(i)+"dsfsdf",new_mergedfrag.points)
                        img=createFinalImage(new_mergedfrag,"tempname.png")
                        contour=getContour(img)
                        new_mergedfrag.points=contour
                        displayContour("Merged",new_mergedfrag.points)
                        # print(new_mergedfrag.points)
                        TF.append(getTurning(getN2FrmN12(new_mergedfrag)))
                        
                        F2[M[i].i] = 1
                        F2[M[i].j] = 1
                        F[M[i].i] = None
                        F[M[i].j] = None
                    except:
                        pass
                # print(getList(M[i].fragment_1))
                
                # F.remove(F[M[i].i])
                # print F 
                # print M[i].j
                # if(M[i].j > M[i].i):
                #     F.remove(F[(M[i].j)-1])
                # else:
                #     F.remove(F[(M[i].j)])
                # F[M[i].i]=None
                # F[M[i].j]=None
#         print F1
        for k in range(0,W):
            if(F[k] is not None):
                TF.append(F[k])
                
         
        for i in range(0,len(TF)):
            frag=TF[i]
            #displayContour("Fragment"+str(i)+"dsfsdf",get1N2(frag.points))       
        
#        x=cv2.waitKey(0)
#        if(x==27):
#            cv2.destroyAllWindows()
#         Frag=[]
#         for x in F:
#             if x!=None:
#                 Frag.append(x)
#         F=Frag
        F = TF
        W = len(F)
        
    return F
            
                
                      
            