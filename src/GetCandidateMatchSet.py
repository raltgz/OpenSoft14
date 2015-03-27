import Matchset
from SmithWaterman import *
from transform import *

#to do list: CompareContour function as implemented by srini
def GetCandidateMatchSet(F,iter):
    W = len(F)
    print str(W) + "matchset"
    MatchList = []
    temp_match=[]
    avg_score = 0
    
    Max=None
    for i in range(0,W):
        Max = None
        for j in range(i,W):
            if i!=j:
                m = CompareContour(F[i],F[j],iter)
                #def isMatchPossible(A,B,startA,endA,startB,endB):
                
                if Max is None or m.score>Max.score:
                    if isMatchPossible(m.fragment_1,m.fragment_2,m.match_1_start,m.match_1_end,m.match_2_start,m.match_2_end):
                        m.i=i
                        m.j=j
                        print m.score
                        #temp_match.append(m)
                        Max=m
        if Max is not None and len(Max.match_1.points[0])>10:
            temp_match.append(Max)   
    
    
    temp_match.sort(key=lambda x: (x.score), reverse=True)
    frags=[]
    for match in temp_match:
        #if(match.i not in frags and match.j not in frags):
            MatchList.append(match)
            frags.append(match.i)
            frags.append(match.j)
            
    return MatchList
