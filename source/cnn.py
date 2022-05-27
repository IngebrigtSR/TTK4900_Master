from math import ceil
import numpy as np

### sliding window with suggestions ###

def subSlidingWindow(image, stepSize, windowSize, xSuggested, ySuggested, width, height):
    (yStart,yEnd) = boxCheck(image.shape[0], ySuggested, height, stepSize, 5, windowSize[1])
    for y in range(yStart, yEnd, stepSize):
        (xStart,xEnd) = boxCheck(image.shape[1], xSuggested, width, stepSize, 5, windowSize[0])
        for x in range(xStart, xEnd, stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def boxCheck(imageLength, boxStart, boxLength, stepSize, padding, windowLength):
    if boxStart-padding > 0:
        start = boxStart-padding
    else:
        start = 0
    if(ceil((boxLength+padding)/stepSize)*stepSize)+boxStart < imageLength:
        if int(ceil((boxLength+padding)/stepSize))*stepSize + boxStart - windowLength < boxStart:
            end = boxStart + padding
        else:
            end = int(ceil((boxLength+padding)/stepSize))*stepSize + boxStart - windowLength
    else:
        end = imageLength-windowLength
    return(start,end)

def boxReduction_faster(boxes, overlapThreshold, check=0):
    # transform to numpy array as floats because of divitions
    array = np.asarray(boxes, dtype=np.float)

    # initialize the list of picked indexes
    pick = []

    # grab the values of the bounding boxes
    x = array[:,0]
    y = array[:,1]
    w = array[:,2]
    h = array[:,3]
    p = array[:,4]

    # find the area, sort by prediction
    area = w*h
    idps = np.argsort(p)

    #keep looping while some indexes still remains
    while len(idps) > 0:
        #choose and keep the biggest area
        last = len(idps) - 1
        i = idps[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x[i], x[idps[:last]])
        yy1 = np.maximum(y[i], y[idps[:last]])
        xx2 = np.minimum(x[i] + w[i], x[idps[:last]] + w[idps[:last]])
        yy2 = np.minimum(y[i] + h[i], y[idps[:last]] + h[idps[:last]])

        # compute the width and height of the bounding box
        wc = np.maximum(0, xx2 - xx1 + 1)
        hc = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (wc * hc) / area[idps[:last]]

        # delete all indexes from the index list that have too mutch overlap
        idps = np.delete(idps, np.concatenate(([last],
            np.where(overlap > overlapThreshold)[0])))

    return array[pick].astype("int").tolist()
