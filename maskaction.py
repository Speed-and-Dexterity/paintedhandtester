import cv2
import numpy as np
from sklearn.cluster import KMeans
cap = cv2.VideoCapture("croppednygiants.mp4")
red = ["red", (0,0,20),(20,20,100)] # works pretty wel
white = ["white",(70,40,50),(150,170,170)]
hasFrame, frame = cap.read()
vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))
redfingernames = ["RPinky","RMiddle","RThumb","LThumb","RMiddle","RPinky"]
whitefingernames = ["LRing","LPointer","LPointer","LRing"]
def getfingers(image, color):
    if color == "red":
      names = redfingernames
      lower = red[1]
      upper = red[2]
    else:
      names = whitefingernames
      lower = white[1]
      upper = white[2]
    nfingers = len(names)
    mask = cv2.inRange(image, lower, upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours] 
    contour_sizes.sort(reverse=True, key=lambda  x: x[0])
    fingers = contour_sizes[:nfingers]
    fingies = []
    for i in fingers:         
      # x,y,w,h = cv2.boundingRect(i[1])
      #x,y,w,h = cv2.minAreaRect(i[1])
      fingies.append(cv2.minAreaRect(i[1]))
    fingies.sort(key = lambda x: x[0])
    tick = 0

    for i in fingies:
      x,y,w = i
   #   cv2.putText(image, names[tick], (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
      #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
    #  rect = cv2.minAreaRect(i)
      box = cv2.boxPoints(i)
      box = np.int0(box)
      image = cv2.drawContours(image,[box],0,(0,0,255),2)

      tick += 1
    return image
while(1):
    _, frame = cap.read()
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    getfingers(frame,"red")
    getfingers(frame,"white")
    cv2.imshow("gamer",frame)
    vid_writer.write(frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
vid_writer.release()
cv2.destroyAllWindows()
cap.release()