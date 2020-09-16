import cv2
import numpy as np
import time
middle = [(0,0,105),(30,40,140)] # works pretty wel
green = [(0,90,100),(120,200,260)]
yellow = [(0,240,250),(10,255,255)]
dot_colors = [middle] #, green, yellow]
    
img = cv2.imread('gam.jpg')   
# apply medianBlur to smooth image before threshholding
blur= cv2.medianBlur(img, 7) # smooth image by 7x7 pixels, may need to adjust a bit

for lower, upper in dot_colors:
    output = img.copy()
    # apply threshhold color to white (255,255, 255) and the rest to black(0,0,0)
    mask = cv2.inRange(blur,lower,upper) 

    circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=20,param2=8,
                               minRadius=0,maxRadius=60)    
    index = 1
    dupes = []
    if circles is not None:
        print(len(circles[0]))
        for i in circles[0]:
            if index == len(circles[0]) - 1 | index == len(circles[0]):
                continue 
            for item in range(2):
                #time.sleep(1)
                print("first: " + str(circles[0][index][item]) + " second : " + str(circles[0][index - 1][item]) + " " +  str(item))
                if (circles[0][index][item] + 200 > circles[0][index - 1][item])&(circles[0][index][item] - 200 < circles[0][index - 1][item]):
                    print("AAAA")
                    dupes.append(index)
                  # circles = np.delete(circles, index,1)
                    continue
            index += 1
        # convert the (x, y) coordinates and radius of the circles to integers
        #print(circles)
        circles = np.delete(circles,dupes,1)
        print(circles)
        circles = np.round(circles[0, :]).astype("int")
        index = 0
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, 
            #   then draw a rectangle corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (255, 0, 255), 2)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 255), -1)

            index = index + 1
            #print str(index) + " : " + str(r) + ", (x,y) = " + str(x) + ', ' + str(y)
        cv2.imshow("gamer",output)
        cv2.waitKey()
        print("No. of circles detected =" + str(index))