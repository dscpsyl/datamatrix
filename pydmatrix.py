from pylibdmtx.pylibdmtx import decode, encode
import cv2
import numpy as np
import sys
import time
import os
from PIL import Image
####################################################################################################

def readingDecode():  
    
     
    #* empty function to pass to 
    def empty(a):
        pass

    #* Draws out shape Info
    def shapeInfo(approx, cntArea):
        global square, upperLeft, upperRight, lowerLeft, lowerRight
        x, y, w, h, = cv2.boundingRect(approx)
        points = str(len(approx))
        cv2.rectangle(frameContour, (x,y), (x+w, y+h), (0,255,0), 3)
        upperLeft = [y, x]
        lowerLeft = [y+h, x]
        upperRight = [y, x+w]
        lowerRight = [y+h, x+w]
        
        cv2.putText(frameContour, "Points: " + points, (x+w+20, y+h+20), cv2.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 3)
        cv2.putText(frameContour, "Area: " + str(cntArea), (x+w+20, y+h+45), cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,0), 3)
        try:
            cv2.putText(frameContour, "Shape: " + shapeDict[len(approx)], (x+w+20, y+60), cv2.FONT_HERSHEY_COMPLEX, .7, (0,255,0), 3)
            if shapeDict[len(approx)] == "Circle":
                if debug == True:
                    print("Found a circle at [" + str(x) + "," + str(y) + "]")
                circle = True
            if shapeDict[len(approx)] == "Square":
                if debug == True:
                    print("Found a square at [" + str(x) + "," + str(y) + "]")
                square = True
                return square
            if shapeDict[len(approx)] == "Triangle":
                if debug == True:
                    print("Found a triangle at [" + str(x) + "," + str(y) + "]")
                triangle = True
        except KeyError as e:
            print("No classified shapes found...: " + str(len(approx)))

    #*detects contours 
    def getContours(frame, frameContour, frameThresh):
        global square
        contours, hierarchy = cv2.findContours(frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) 
        
        square = False
        
        for cnt in contours:
            cntArea = cv2.contourArea(cnt)
            areaThresh = cv2.getTrackbarPos("AreaThresh", parametersWindowName)
            if cntArea > areaThresh:
                ##### ?Displays contours
                cv2.drawContours(frameContour, contours, -1, (255,0,255), 3) 
                parami = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * parami, True)
                
                
                ##### ?Displays information
                try: 
                    shapeInfo(approx, cntArea)
                except:
                    print("shapeInfo Error")

    #*Reads, Transforms, and Writes Image | Then Finally Calls Decode function
    def processWrite(square, frameThresh, frameCanny, flipRequired):
        global counter
        if square == True:
            counter = counter + 1
            print("counter is at: " + str(counter))
            if counter > 200:
                try:  
                    rows,cols = frameCanny.shape
                    cornerPoints = np.float32([[upperLeft[1],upperLeft[0]],[upperRight[1],upperRight[0]],[lowerLeft[1],lowerLeft[0]],[lowerRight[1],lowerRight[0]]])
                    docEdge = np.float32([[0,0],[rows,0],[0,rows],[rows,rows]])
                    Matrix = cv2.getPerspectiveTransform(cornerPoints,docEdge)
                    frameCrop = cv2.warpPerspective(frameThresh,Matrix,(cols,rows))
                    if flipRequired == True:
                        frameCrop = cv2.flip(frameCrop, 1)
                
                    cv2.imwrite("frame.jpg", frameCrop)
                    time.sleep(1)
                except Exception as e:
                    print("Something went wrong with the image cropping: " + str(e))
                try:
                    processDecode()
                except Exception as e:
                    print("Decoding Error: " + str(e))
                sys.exit(0)
        if square == False:
            counter = 0

    #*Function to decode
    def processDecode():
        img = cv2.imread("frame.jpg")
        result = decode(img)
        strResult = str(result[0]).split("'")
        print(strResult[1])
        
        counter = 0
        os.remove("frame.jpg")

    #* Confirms whether the image needs to be fliped in the end due to the camera
    def flip():
        a = input("Does your camera need to be fliped? (y,n): ")
        if a == "y":
            flipRequired = True
        elif a == "n":
            flipRequired = False
        else:
            print("That is not a valid input. Please Try Again...")
            flip()

    upperLeft = None
    lowerLeft = None
    upperRight = None
    lowerRight = None

    shapeDict = { 2: "Circle", 8: "Circle", 9: "Circle", 4: "Square", 3: "Triangle", 5: "Triangle", 6: "Triangle" }
    debug = True
    counter = 0
    flipRequired = None

    ##### ?stacks images for debugging    
    def stackImages(scale,imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range ( 0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor= np.hstack(imgArray)
            ver = hor
        return ver

     
    flip() 
    inputCam = cv2.VideoCapture(0)           
        
    ##### ?create sliders 
    parametersWindowName = "Parameters"
    cv2.namedWindow(parametersWindowName)
    cv2.resizeWindow(parametersWindowName, 720, 480)
    cv2.createTrackbar("Threshold1", parametersWindowName, 50, 255, empty)
    cv2.createTrackbar("Threshold2", parametersWindowName, 150, 255, empty)
    cv2.createTrackbar("AreaThresh", parametersWindowName, 15000, 99999, empty)
    cv2.createTrackbar("Threshold3", parametersWindowName, 170, 255, empty)
    cv2.createTrackbar("Threshold4", parametersWindowName, 255, 255, empty)

        
    ##### ?Shows image process
    while True :
        #* Reads input 
        ret, frame = inputCam.read()
        #* Flips it right way around
        frame = cv2.flip(frame, 1)
        #* gathers trackign bar positions for threshold values 
        threshold1 = cv2.getTrackbarPos("Threshold1", parametersWindowName)
        threshold2 = cv2.getTrackbarPos("Threshold2", parametersWindowName)
        threshold3 = cv2.getTrackbarPos("Threshold3", parametersWindowName)
        threshold4 = cv2.getTrackbarPos("Threshold4", parametersWindowName)
        
        #* Tries to process and operate on image
        try:
            #* Basic Processing
            frameBlur = cv2.GaussianBlur(frame, (7,7), 1)
            frameGray = cv2.cvtColor(frameBlur, cv2.COLOR_BGR2GRAY)
            frameCanny = cv2.Canny(frameGray, threshold1, threshold2)
            ret, frameThresh = cv2.threshold(frameGray, threshold3, threshold4, cv2.THRESH_BINARY)
            #* Dialiation 
            kernel = np.ones((4,4))
            frameDial = cv2.dilate(frameCanny, kernel, iterations=1)
            
            #* Finds contours 
            frameContour = frame.copy()
            getContours(frameDial, frameContour, frameThresh)
            
            processWrite(square, frameThresh, frameCanny, flipRequired)
                
        except Exception as e:
            print("Something went wrong with image processing...: " + str(e))
            
        
        
        #* Stacks and shows the image
        imgStack = stackImages(0.3,([frame, frameThresh, frameContour]))
        cv2.imshow('video', imgStack)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #TODO: out = cv2.imwrite(outputName, frame)
            sys.exit(0)

def writtingEncode():
    data = input("What would you like to encode?: ")
    saveName = input("What would you like to save the image as? : ")
    encoded = encode(data)
    img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)
    img.save(saveName + ".png")
    print("Encoded image is saved at the dir of this script.")
    sys.exit(0)

####################################################################################################

def initPrompt():
    whatToDo = input("Would you like to read a Data Matrix or Create one? (r/c): ")
    if whatToDo == "r":
        readingDecode()
    elif whatToDo == "c":
        writtingEncode()
    else:
        print("That is not a valid option. Please try again...")
        initPrompt

if __name__ == "__main__":
    menu = True
    while menu:
        initPrompt()
    print("Do you want to do compute another data matrix?")
    again = input("Press 'y' to compute again or any other key to exit: ")
    menu = False
    if again == "y":
        menu = True