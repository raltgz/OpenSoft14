from numpy import array,ones,linalg
# from pylab import plot,show
import math

def getregression(A_list):
    xi = []
    yi = []
    N = len(A_list)
    for k in range(0,N):
        xi.append(A_list[k][0])
        yi.append(A_list[k][1])
    xi = array(xi)
    yi = array(yi)
    A = array([ xi, ones(N)])
    
    # linearly generated sequence
    w = linalg.lstsq(A.T,yi)[0] # obtaining the parameters
     
    # plotting the line
    line = w[0]*xi+w[1] # regression line
#     plot(xi,line,'r-',xi,yi,'o')
#     show()
     
    m = w[0]
    c = w[1]
    sum1 = 0
#     if m > 100 or m < -100 :
#         for i in range(0,N):
#             pr = abs(x[i] + (c/m))
#             sum1 = sum1 + pr*pr
#     else:
    for i in range(0,N):
        pr = (abs(yi[i] - m*xi[i] - c))/math.sqrt(1 + m*m)
        #print pr
        sum1 = sum1 + pr*pr
    sd = math.sqrt(sum1/len(xi))
    return sd

#A_list = [[1,1],[2,2],[4,4],[10,15],[-2,15],[4,-20]]
#print getregression(A_list)


    