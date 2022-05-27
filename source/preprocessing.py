import numpy as np
import cv2
from math import sqrt

def generateEggSuggestions(img,testState=0):
    """
    Generates suggestionboxses for where the CNN should look for eggs
    requires unprosessed loaded image as parameter, optional testState = 1 to show images
    Returns x-position, y-position, width ,height
    """
    def generator(return_list):
        for returns in return_list:
            yield returns

    # Use threshhold to remove background
    (retval,thresh) = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
    boundingBoxes = eggFinder(thresh)
    return generator(boundingBoxes)
    if testState == 1:
        # show the output image
        cv2.imshow("output", thresh)
        cv2.imshow("original image", img)
        cv2.waitKey(0)

    #manual edge to generate images for rapport
    if testState==1:
        blur = cv2.GaussianBlur(thresh,(5,5),0)
        cv2.imshow('smoothed', thresh)
        cv2.waitKey(0)


    #find edges
    edge_detected_image = cv2.Canny(thresh, 75, 200)

    if testState==1:
        cv2.imshow('Edge', edge_detected_image)
        cv2.waitKey(0)

    #find contours
    contours,_ = cv2.findContours(edge_detected_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boundingBox_list = []
    for box in contours:
        x,y,w,h = cv2.boundingRect(box)
        boundingBox_list.append((x,y,w,h))
        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    array = np.asarray(boundingBox_list,dtype=np.int)


    # initialize the list of picked indexes
    pick = []

    # grab the values of the bounding boxes
    x = array[:,0]
    y = array[:,1]
    w = array[:,2]
    h = array[:,3]

    # find the area, sort by area
    area = w*h
    idas = np.argsort(area)

    #keep looping while some indexes still remains
    while len(idas) > 0:
        #choose and keep the biggest area
        last = len(idas) - 1
        i = idas[last]
        pick.append(i)

        # do placement checks
        xc1 = np.maximum(0, x[idas[:last]] - x[i])
        yc1 = np.maximum(0, y[idas[:last]] - y[i])
        xc2 = np.maximum(0, x[i] + w[i] - x[idas[:last]] - w[idas[:last]])
        yc2 = np.maximum(0, y[i] + h[i] - y[idas[:last]] - h[idas[:last]])

        #set the results together
        check = xc1*xc2*yc1*yc2

        # delete all indexes from the index list that matches the check
        idas = np.delete(idas, np.concatenate(([last],
            np.where(check > 0)[0])))

    #Overlap is now reduced as much as possible, pick is sorted in smallest to largest area.
    # now is the time to erode away some of the areas
    # do this first single threaded, then move on to multiprocessing (if cv2 only uses one core)


    #need to sort out the sections that needs extra work
    size_limit = 2000
    divider = np.where(area[pick] > 2000)[0][-1] #lists the indexes of boxes with area over size_limit
    further_work = pick[0:divider + 1]
    pick = pick[divider+1:]

    boundingBoxes = array[pick] #these are certified "good"
    boundingBoxes = boundingBoxes.tolist()

    divided_boundingBoxes = []
    for index in further_work:
        #do the separation before adding it to the list
        box = boundingBox_list[index]
        cutVal = box
        cutout = thresh[box[1]:box[1]+box[3],box[0]:box[0]+box[2]]

        # defining kernel size to use
        kernel = np.ones((3,3),np.uint8)

        opening = cv2.morphologyEx(cutout,cv2.MORPH_OPEN,kernel, iterations = 2)
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,0.3*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)

        # repeat edge detection
        edge_detected_image = cv2.Canny(sure_fg, 75, 200)
        contours,_ = cv2.findContours(edge_detected_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # add to new list
        for box in contours:
            x,y,w,h = cv2.boundingRect(box)
            divided_boundingBoxes.append((x+cutVal[0],y+cutVal[1],w,h))

    # combine the two lists
    boundingBoxes = boundingBoxes + divided_boundingBoxes

    if testState == 1:
        for box in boundingBoxes:
            cv2.rectangle(img,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,255,0),2)
        cv2.imshow('Objects Detected',img)
        cv2.waitKey(0)
        print("teststate")
        return 1
    else:
        boundingBoxes = eggFinder(thresh)
        return generator(boundingBoxes)

def eggFinder(imgThresh, eggSize=28):

    # defining kernel size to use
    kernel = np.ones((3,3),np.uint8)

    eggs = []
    flag = 10

    opening = cv2.morphologyEx(imgThresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    # print("\n\n")
    # print(cv2.THRESH_BINARY)
    # print("verdi")
    # print(dist_transform.max())
    # print(dist_transform.size)
    # ret, sure_fg = cv2.threshold(dist_transform,8,255,cv2.THRESH_BINARY)
    # cv2.imshow('dist',dist_transform)
    # cv2.imshow('original',imgThresh)
    # cv2.imshow('test',sure_fg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # return -1

    while flag > 2 :
        # if flag == 0:
        #     flag = flag +1
        #     opening = cv2.morphologyEx(imgThresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        # else:
        #     opening = cv2.morphologyEx(sure_fg,cv2.MORPH_OPEN,kernel, iterations = 2)
        # Finding sure foreground area

        flag = flag -1
        ret, sure_fg = cv2.threshold(dist_transform,flag/10*dist_transform.max(),255,cv2.THRESH_BINARY)
        sure_fg = np.uint8(sure_fg)

        # cv2.imshow('Erotion iteration %d' %(10-flag),sure_fg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # repeat edge detection
        edge_detected_image = cv2.Canny(sure_fg, 75, 200)
        contours,_ = cv2.findContours(edge_detected_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        templist=[]
        # add to new list
        for box in contours:
            x,y,w,h = cv2.boundingRect(box)
            if h*w<eggSize*eggSize:
                templist.append((x,y,w,h))
            #eggs.append((x+cutVal[0],y+cutVal[1],w,h))
        #print(templist)
        if len(templist) == 0:
            continue
        if len(eggs) == 0:
            eggs.append(templist[0])
        for box in templist:
            centerX = box[0]+box[2]/2
            centerY = box[1]+box[3]/2
            for egg in eggs:
                ecenterX = egg[0]+egg[2]/2
                ecenterY = egg[1]+egg[3]/2
                distanceX = ecenterX-centerX
                distanceY = ecenterY-centerY
                if sqrt(distanceX**2 + distanceY**2) < 10:
                    continue
                #got to expand the image so it corresponds with a egg
                new_egg = [box[x] for x in range(0,4)]
                if new_egg[2] < eggSize:
                    new_egg[0] = new_egg[0] - (eggSize-new_egg[2])/2
                    new_egg[2] = eggSize
                if new_egg[3] < eggSize:
                    new_egg[1] = new_egg[1] - (eggSize-new_egg[3])/2
                    new_egg[3] = eggSize
                eggs.append(new_egg)
                break

        # clone = imgThresh.copy()
        # ret,thresh1 = cv2.threshold(clone,-1,255,cv2.THRESH_BINARY)
        # for box in templist:
        #     cv2.rectangle(thresh1,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,0,0),2)
        # cv2.imshow('Objects Detected 3',thresh1)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if flag == 1:
            break

    array = np.asarray(eggs,dtype=np.int)


    # initialize the list of picked indexes
    pick = []

    # grab the values of the bounding boxes
    x = array[:,0]
    y = array[:,1]
    w = array[:,2]
    h = array[:,3]

    # find the area, sort by area
    area = w*h
    idas = np.argsort(area)

    #keep looping while some indexes still remains
    while len(idas) > 0:
        #choose and keep the biggest area
        last = len(idas) - 1
        i = idas[last]
        pick.append(i)

        # do placement checks
        xc1 = np.maximum(0, x[idas[:last]] - x[i] +1)
        yc1 = np.maximum(0, y[idas[:last]] - y[i] +1)
        xc2 = np.maximum(0, x[i] + w[i] - x[idas[:last]] - w[idas[:last]]+1)
        yc2 = np.maximum(0, y[i] + h[i] - y[idas[:last]] - h[idas[:last]]+1)

        #set the results together
        check = xc1*xc2*yc1*yc2

        # delete all indexes from the index list that matches the check
        idas = np.delete(idas, np.concatenate(([last],
            np.where(check > 0)[0])))
    eggs = array[pick].tolist()


    if 1:
        array = np.asarray(eggs,dtype=np.int)

        # initialize the list of picked indexes
        pick = []

        # grab the values of the bounding boxes
        x = array[:,0]
        y = array[:,1]
        w = array[:,2]
        h = array[:,3]

        # find the area, sort by area
        area = w*h
        idas = np.argsort(area)

        #keep looping while some indexes still remains
        while len(idas) > 0:
            #choose and keep the biggest area
            last = len(idas) - 1
            i = idas[last]
            pick.append(i)

            # do placement checks
            x1 = np.minimum(0,np.absolute(x[idas[:last]]-x[i])-5)
            y1 = np.minimum(0,np.absolute(y[idas[:last]]-y[i])-5)

            #set the results together
            check = x1*y1

            # delete all indexes from the index list that matches the check
            idas = np.delete(idas, np.concatenate(([last],
                np.where(check != 0)[0])))

        eggs = array[pick].tolist()

    return eggs
