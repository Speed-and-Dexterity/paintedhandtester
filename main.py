import cv2
import numpy as np
import time
middle = ["middle", (0,0,100),(30,40,140)] # works pretty wel
pinky = ["pinky",(20,75,120),(70,180,170)]
yellow = [(20,240,250),(10,255,255)]
dot_colors = [middle,pinky] 
    
img = cv2.imread('glovehands.jpg')   
# apply medianBlur to smooth image before threshholding
blur= cv2.medianBlur(img, 7) # smooth image by 7x7 pixels, may need to adjust a bit
fingerpoints = {}
def drawfinger(image, joints):
    joints.sort(key=lambda l:l[0])
    myjoints = []
    for i in joints:
        pass
    #term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
    #skel = cv2.kmeans(joints,4, None,term_crit, 10, 0)
    prevx, prevy = [0,0]
    for x,y in gamer:
        cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 255), -1)
        cv2.line(output, (x,y),(prevx,prevy),(255,0,0),8)
        prevx = x
        prevy = y
  #  cv2.imshow("g", image)
    cv2.waitKey()
    return image
input_source = "glovevid.mp4"
cap = cv2.VideoCapture(input_source)
hasFrame, frame = cap.read()

frameWidth = frame.shape[1]
frameHeight = frame.shape[0]

aspect_ratio = frameWidth/frameHeight

inHeight = 368
inWidth = int(((aspect_ratio*inHeight)*8)//8)

vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

k = 0
while 1:
    k+=1
    t = time.time()
    hasFrame, frame = cap.read()
    frameCopy = np.copy(frame)
    if not hasFrame:
        cv2.waitKey()
        break
    print("forward = {}".format(time.time() - t))

    for finger, lower, upper in dot_colors:
        output = frame
        blur= cv2.medianBlur(output, 7)
        mask = cv2.inRange(output,lower,upper) 

        circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=20,param2=8,
                                minRadius=0,maxRadius=60)    
        index = 0
        dupes = []
        if circles is not None:
         #   print(len(circles[0]))
            for i in circles[0]:
                if index == len(circles[0]) - 1 | index == len(circles[0]):
                    continue 
                for item in range(2):
                    #time.sleep(1)
                  #  print("first: " + str(circles[0][index][item]) + " second : " + str(circles[0][index - 1][item]) + " " +  str(item))
                    if (circles[0][index][item] + 200 > circles[0][index - 1][item])&(circles[0][index][item] - 200 < circles[0][index - 1][item]):
                     #   print("AAAA")
                        dupes.append(index)
                    # circles = np.delete(circles, index,1)
                        continue
                index += 1
            # convert the (x, y) coordinates and radius of the circles to integers
            #print(circles)
            circles = np.delete(circles,dupes,1)
        #    print(circles)
            circles = np.round(circles[0, :]).astype("int")
            index = 0
            # loop over the (x, y) coordinates and radius of the circles
            # for (x, y, r) in circles:
            #     # draw the circle in the output image, 
            #     #   then draw a rectangle corresponding to the center of the circle
            #     cv2.circle(output, (x, y), r, (255, 0, 255), 2)
            #     cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 255), -1)

            #     index = index + 1
            #     #print str(index) + " : " + str(r) + ", (x,y) = " + str(x) + ', ' + str(y)
            fingerpoints[finger] = [[g[0],g[1]] for g in circles]
            gamer = fingerpoints[finger]
            frame = drawfinger(output,gamer)
            vid_writer.write(frame)

vid_writer.release()
