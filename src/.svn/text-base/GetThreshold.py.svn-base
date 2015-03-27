import cv2

def getThreshold(im_name):
    img = cv2.imread(im_name,0)
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    max_val = hist[0]
    max_idx = 0 
    for i in range(0,len(hist)):
        if hist[i] > max_val:
            max_val = hist[i]
            max_idx = i
    return max_idx

# print getThreshold("2.png")