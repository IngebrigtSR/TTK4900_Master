import numpy as np
from cv2 import cv2
from preprocessing import generateEggSuggestions
from cnn import *
import multiprocessing
#from ximea import xiapi





class detector():

    def __init__(self):
        ### Settings ###
        print("init start")
        self.wind_row, self.wind_col = 28,28 # search area size
        self.IMG_SIZE = 10 # dimensions of the input image

        #initialise prosesses and queues
        self.queue = multiprocessing.Queue()
        self.results = multiprocessing.Queue()

        numProcs  = 3
        self.events = [ multiprocessing.Event() for i in range(0,numProcs) ]
        self.imgQueues = [ multiprocessing.Queue() for i in range(0,numProcs) ]
        self.workers = [  multiprocessing.Process(target=self.predictor, args=(self.queue, self.results, self.events[i], self.imgQueues[i]),daemon=True) for i in range(0,numProcs)]
        for process in self.workers:
            process.start()

        self.cam = cv2.VideoCapture()
        print("init done")


    def cameraInit():
        print('Opening first camera...')
        self.cam.open_device()

        #settings
        self.cam.set_exposure(10000)
        print('Exposure was set to %i us' %cam.get_exposure())

        #create instance of Image to store image data and metadata
        self.img = xiapi.Image()

    def cameraShutdown():
        #stop communication
        self.cam.close_device()
        print("Camera shut down")

    def cameraCapture():
        ### Capture an image and return it as numpy array ###
        self.cam.start_acquisition()
        self.cam.get_image(img)
        data = self.img.get_image_data_numpy()
        self.cam.stop_acquisition()
        return(data)


    def doPredictions(self, image,area =[0,1280-1,0,1024-1], show=0):
        ### This handles the predictions, with a configurable search area ###
        #image is [y,x]
        print(image.shape)
        self.resized = image[area[2]:area[3],area[0]:area[1]]/255
        for que in self.imgQueues:
            que.put(self.resized)
        for event in self.events:
            event.set()


        #testing purposes
        if show:
            clone = resized.copy()

        counter = 0
        print("main good")
        #generate suggested areas
        hitBoxes = []
        for (xSuggested,ySuggested,width,height) in generateEggSuggestions(image[area[2]:area[3],area[0]:area[1]]):
            for(x,y,window) in subSlidingWindow(image[area[2]:area[3],area[0]:area[1]], 3, (self.wind_row,self.wind_col), xSuggested, ySuggested, width, height):
                self.queue.put((x,y))
                counter += 1


        while counter > 0:
            hitBoxes.append(self.results.get())
            counter -= 1


        #sort out the good predtictions
        array = np.asarray(hitBoxes,dtype=np.float32)
        x = array[:,4]
        array = array[ np.where(x < 0.1)[0]]

        #add values so it consists with area to search
        array[:,0] = array[:,0]+area[0]
        array[:,1] = array[:,1]+area[2]

        hitBoxes = array.tolist()


        picks = boxReduction_faster(hitBoxes,0.5)

        if show:
            for box in picks:
                cv2.rectangle(clone, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 2)
            cv2.imshow("CNN detected", clone)
            cv2.waitKey(0)
        return picks


    def predictor(self,queue,result,event,imgQueue):
        ### The predictor thread, runs the CNN from the queue inputs from main ###
        #initialise
        print("starting")
        import cv2
        import numpy as np
        from tensorflow import lite
        interpreter = lite.Interpreter(model_path='converted_model_0_10.tflite')
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print("started")

        while True:

            x,y = queue.get()

            if event.is_set():
                resized = imgQueue.get()
                event.clear()

            p_img = cv2.resize(resized[y:y+self.wind_row,x:x+self.wind_col],(self.IMG_SIZE,self.IMG_SIZE))
            p_img = np.reshape(p_img,[-1,self.IMG_SIZE,self.IMG_SIZE,1])
            p_img = np.array(p_img, dtype=np.float32)

            interpreter.set_tensor(input_details[0]['index'], p_img)
            interpreter.invoke()
            prediction = interpreter.get_tensor(output_details[0]['index'])[0]

            result.put((x,y,self.wind_row,self.wind_col,prediction[0]))


    def findCenter(self,img,list):
        ### Finds the center of the roe ###
        found_center = []
        (retval,thresh) = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
        # defining kernel size to use
        kernel = np.ones((3,3),np.uint8)
        offset = 2
        for index in list:

            cutout = thresh[index[1]+offset:index[1]+index[3]-offset,index[0]+offset:index[0]+index[2]-offset]
            opening = cv2.morphologyEx(cutout,cv2.MORPH_OPEN,kernel, iterations = 2)
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)


            val = 0
            contours = [0,0]
            while len(contours) > 1 and val < 0.9:
                val += 0.1
                ret, sure_fg = cv2.threshold(dist_transform,val*dist_transform.max(),255,cv2.THRESH_BINARY)
                sure_fg = np.uint8(sure_fg)

                edge_detected_image = cv2.Canny(sure_fg, 75, 200)
                contours,_ = cv2.findContours(edge_detected_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) < 1:
                val -= 0.1
                ret, sure_fg = cv2.threshold(dist_transform,val*dist_transform.max(),255,cv2.THRESH_BINARY)
                sure_fg = np.uint8(sure_fg)

                edge_detected_image = cv2.Canny(sure_fg, 75, 200)
                contours,_ = cv2.findContours(edge_detected_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            val = 100
            for cont in contours:
                x,y,w,h = cv2.boundingRect(cont)
                if abs(x-self.wind_row/2)+abs(y-self.wind_col/2) < val:
                    val = abs(x-self.wind_row/2)+abs(y-self.wind_col/2)
                    ans = (x,y,w,h)
            found_center.append((int(index[0]+x+w/2),int(index[1]+y+h/2)))
        return found_center



    def distanceFromPixels(self,img,centerList,h):
        ### Finds the distance in cm given a list of placements and distance, cartesian coordinates ###

        # Settings for the current camera
        f = 12.5*10**(-3)
        plen = 5.3*10**(-6)

        # uses the image shape
        imgx = img.shape[0]
        imgy = img.shape[1]

        #finds the distances
        distanceList = []
        for box in centerList:
            xdif = abs(box[0]-imgx/2)
            ydif = abs(box[1]-imgy/2)
            x = xdif*plen*h/f
            y = ydif*plen*h/f
            distanceList.append(x,y)
        return distanceList






if __name__ == '__main__':

    ### Load image
    img = cv2.imread('./test.png', cv2.IMREAD_GRAYSCALE)

    test = detector()
    #results = test.doPredictions(img,area=[800,1280,800,1024])
    results = test.doPredictions(img)
    midten = test.findCenter(img,results)

    print(results[0:10])
    # for box in results[0:10]:
    #     cv2.rectangle(img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (0, 255, 0), 1)
    for dot in midten:
        cv2.circle(img,(dot[0],dot[1]),1,(0,255,0),2)
    cv2.imshow("CNN detected", img)
    cv2.waitKey(0)
