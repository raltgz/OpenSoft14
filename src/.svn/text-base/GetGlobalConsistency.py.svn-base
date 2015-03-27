'''
author: subham
'''
from Matchset import *
import math
from config import *

 
A3 = 0.5
w = 0.4
delta = 0.1   
beta = 1.5 
alpha1 = 0.1
alpha2 = 50
alpha = alpha1 * alpha2
lamda = 0.001
C_list = []

def CheckConvergence(C):
    global maxC, minC
    if(len(C_list) == 0):
        C_list.append(C)
        maxC = C
        minC = C
        return False
    if(len(C_list)<5):
        C_list.append(C)
        if(C < minC):
            minC = C
        if(C > maxC):
            maxC = C
        return False
    maxC = C
    minC = C
    for k in range(0,len(C_list)-1):
        C_list[k] = C_list[k+1]
        if(C_list[k] > maxC):
            maxC = C_list[k]
        if(C_list[k] < minC):
            minC = C_list[k]
    C_list[4] = C
    if ((maxC - minC)<C_THRESHOLD):
        return True
    else:
        return False

def GetGlobalConsistency(M,G):
    N = len(M)
#     print N
    if(N == 0):
        return
    x = []
    u = []
    C = []
    v = []
    max_score = min_score = M[0].score
    for k in range(0,N):
        if(M[k].score > max_score):
            max_score = M[k].score
        if(M[k].score < min_score):
            min_score = M[k].score
    for k in range(0,N):
        if(max_score == min_score):
            x.append(1)
        else:
            value = A3 - (M[k].score - min_score)/(max_score - min_score)*w
            print value
            x.append(value)
    rho = 0.1
    for k in range(0,N):
        u.append(GetU(G[k], x))
        C.append(u[k] * x[k])
    ctr = 0
    while True:
        ctr = ctr + 1
        print "Iteration: " + str(ctr)
        v = []
        for k in range(0,N):
            v.append(GetV(G, x, k))
        mag = 0
        for k in range(0,N):
            mag = mag + v[k]*v[k]
#        mag = lambda v: math.sqrt(sum(i**2 for i in x))
        mag = math.sqrt(mag)
        v = [q/mag for q in v]
        print v
        for k in range(0,N):
            x[k] = x[k] + rho * v[k]
        for k in range(0,N):
            if x[k] > 1:
                x[k] = 1
            if x[k] < 0:
                x[k] = 0
        print x
        C_Temp = []
        for k in range(0,N):
            u[k] = GetU(G[k], x)
            C_Temp.append(u[k] * x[k])
        print "C=" + str(C)
        if sum(C_Temp) > sum(C):
            rho = rho + delta
        C = C_Temp
        if CheckConvergence(sum(C)):
            break
    return x   
        
def GetU(G_List, x):
    sum1 = 0
    sum2 = 0
    L = len(G_List)
#     print "*"
#     print G_List
    for i in range(0,L):
        sum1 = sum1 + (x[i]*(G_List[i].gamma))
        sum2 = sum2 + math.exp(alpha2*(x[i] - G_List[i].gamma - beta))
    return (sum1 - alpha1*sum2)

def GetV(G,x,i):
    L = len(G[i])
    sum1 = 0
    sum2 = 0
#     print L
#     print len(x)
    for j in range(0,L):
        
        sum1 = sum1 + (G[i][j].gamma + G[j][i].gamma) * x[j] - alpha1*math.exp(alpha2*(x[j]-G[i][j].gamma-beta))
        sum2 = sum2 + lamda * alpha * (x[j] * math.exp(alpha2*(x[i]-G[j][i].gamma-beta)))
#        print("Sum1")
#        print(sum1)
#        print("Sum2")
#        print(sum2)
#        #print((G[i][j].gamma + G[j][i].gamma) * x[j])
        
    return sum1 - sum2
