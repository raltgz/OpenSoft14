from Matchset import *
from Neighbour import *
from area import *

a1 = 0.25

#to do list : make GetOverLappingArea and GetArea functions
def GetNeighbourhood(M):
    N = len(M)
    G_list = [None for x in range(0,N)]
    for i in range(0,N):
        G_list[i]=[]
        for j in range(0,N):
                if i==j:
                    Neighbour_object = Neighbour()
                    Neighbour_object.M = M[j]
                    G_list[i].append(Neighbour_object)
                else:
                    if (M[i].fragment_1 == M[j].fragment_1) or (M[i].fragment_1 == M[j].fragment_2)or(M[i].fragment_2 == M[j].fragment_1)or(M[i].fragment_2 == M[j].fragment_2) :
                        area1 = GetOverLappingArea(M[i],M[j])
                        #area1=1
                        area2 = GetArea(M[i])
                        #area2=1
                        area_ratio = area1/area2
                        if area_ratio<a1 :
                            gamma_t = 1 - ((area_ratio)*(area_ratio))
                        else :
                            gamma_t = - (area_ratio)
                        Neighbour_object = Neighbour()
                        Neighbour_object.M = M[j]
                        Neighbour_object.gamma = gamma_t
                        G_list[i].append(Neighbour_object)
                    else:
                        Neighbour_object = Neighbour()
                        Neighbour_object.M = M[j]
                        G_list[i].append(Neighbour_object)
    return G_list