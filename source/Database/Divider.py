import os
import json
import numpy as np
import time

import matplotlib.pyplot as plt

try:
    import cv2
except:
    import sys
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
    import cv2

jsonFile = 'labels.json'

xhistory = [] #fjernes
yhistory = [] #fjernes

def createNegativeSamples(image_index,dead_eggs_in_images):
    img_counter = 0
    counter = 0
    for image_id in dead_eggs_in_images:
        img_counter = img_counter+1 #fjernes
        #henter orginalbilde
        img = cv2.imread("Source/"+image_index[image_id].split("/")[-1], cv2.IMREAD_GRAYSCALE)
        shape = img.shape
        print(len(dead_eggs_in_images[image_id]))
        time.sleep(5)
        for _ in dead_eggs_in_images[image_id]:
            while(True):
                check = 1
                x = round(np.random.random()*shape[1])
                y = round(np.random.random()*shape[0])
                for box in dead_eggs_in_images[image_id]:
                    #bbox er [x,y,xlen,ylen]
                    #print("x: %d, y: %d, box[0]: %d\n" %(x,y,box[0]))
                    if x+search_size[0] > shape[1] or y+search_size[1] > shape[0]:
                        check = 0
                        break

                    #sjekker om x og y treffer inni en tideligere definert eggboks
                    if ((x > box[0] and x < box[0]+box[2]) or (x+search_size[0] > box[0] and x+search_size[0] < box[0]+box[2])):
                        if ((y > box[1] and y < box[1]+box[3]) or (y+search_size[1] > box[1] and y+search_size[1] < box[1]+box[3])):
                            check = 0
                            break

                if check == 1:
                    #crop img er [ystart:yend,xstart:xend]
                    crop_img = img[y:y+search_size[1], x:x+search_size[0]]
                    if counter%10==0:
                        cv2.imwrite('Test/Negative/'+ str(counter) +'.png',crop_img)
                    if counter%10<=3:
                        cv2.imwrite('Validate/Negative/'+ str(counter) +'.png',crop_img)
                    else:
                        cv2.imwrite('Train/Negative/'+ str(counter) +'.png',crop_img)
                    counter = counter + 1
                    if img_counter == 1: #fjernes
                        xhistory.append(x)
                        yhistory.append(y)
                    break
    print("Total negatives created: %d" % (counter))


#load labels from file
with open(jsonFile) as f:
    data = json.load(f)

# check and create folders
paths = ["./Test","./Test/DeadEggs","./Test/Negative","./Train","./Train/DeadEggs","./Train/Negative","Validate","Validate/DeadEggs","Validate/Negative"]
for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)

print("loaded image labels")

image_index = {}

search_size = (20,20)
dead_eggs_in_images = {}

for i in data['images']:
    path = i['path'].split("/")[-1]
    image_index[i['id']] = path


print("sorted image paths")

count = 0;
for annotation in data['annotations']:
    try:
        #henter data
        box = annotation['bbox']
        #data er floats, så mapper de til ints
        box = list( map(int, box) )
        image_id = annotation['image_id']
        #henter orginalbilde
        img = cv2.imread("Source/"+image_index[image_id], cv2.IMREAD_GRAYSCALE)
        #bbox er [x,y,xlen,ylen]
        #crop img er [ystart,yend,xstart,xend]
        crop_img = img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        #lagrer klipt bilde
        if count%10==0:
            cv2.imwrite('Test/DeadEggs/'+ str(annotation['id']) +'.png',crop_img)
        elif count%10<=3:
            cv2.imwrite('Validate/DeadEggs/'+ str(annotation['id']) +'.png',crop_img)
        else:
            cv2.imwrite('Train/DeadEggs/'+ str(annotation['id']) +'.png',crop_img)
        count = count + 1
        #lagrer positive treff i spesifikke bilder
        if image_id in dead_eggs_in_images:
            dead_eggs_in_images[image_id].append(box)
        else:
            dead_eggs_in_images[image_id]=[box]

    except Exception as e:
        print("\n\n Error in generating positive images \n")
        raise(e)

print("created positive images")
createNegativeSamples(image_index,dead_eggs_in_images)


plt.scatter(xhistory, yhistory)
plt.savefig('./negativeSpread.png')
