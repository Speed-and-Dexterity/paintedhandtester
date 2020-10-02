import cv2
import numpy as np
#keys spaced ~ 68px horizontally and 60px vertically, b key is at ~720,128
cap = cv2.VideoCapture("lightednygloves.mp4")
red = ["red", (30,30,170),(100,100,255)] # works pretty wel
white = ["white",(230,230,230),(255,255,255)]
hasFrame, frame = cap.read()
vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))
redfingernames = ["RPinky","RMiddle","RThumb","LThumb","RMiddle","RPinky"]
whitefingernames = ["LRing","LPointer","LPointer","LRing"]
fingiedata = []
def click_event(event, x, y, flags, params): 
    if event == cv2.EVENT_LBUTTONDOWN: 
        print(x, ' ', y) 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        cv2.putText(frame, str(x) + ',' +
                    str(y), (x,y), font, 
                    1, (255, 0, 0), 2) 
        cv2.imshow('image', frame) 
    if event==cv2.EVENT_RBUTTONDOWN: 
  
        # displaying the coordinates 
        # on the Shell 
        print(x, ' ', y) 
  
        # displaying the coordinates 
        # on the image window 
        font = cv2.FONT_HERSHEY_SIMPLEX 
        b = frame[y, x, 0] 
        g = frame[y, x, 1] 
        r = frame[y, x, 2] 
        cv2.putText(frame, str(b) + ',' +
                    str(g) + ',' + str(r), 
                    (x,y), font, 1, 
                    (255, 255, 0), 2) 
        cv2.imshow('image', frame) 
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
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours] 
    contour_sizes.sort(reverse=True, key=lambda  x: x[0])
    fingers = contour_sizes[:nfingers]
    fingies = []
    for i in fingers:         
      fingies.append(cv2.minAreaRect(i[1]))
    fingies.sort(key = lambda x: x[0])
    tick = 0
    fingieposes = []
    for i in fingies:
      box = cv2.boxPoints(i)
      box = np.int0(box)
      image = cv2.drawContours(image,[box],0,(0,0,255),2)
      box = sorted(box,reverse=True, key=lambda x:x[1])
      box = np.int0(box)[:2]
      tip = (int(abs(box[0][0] + box[1][0]) / 2),int(abs(box[0][1] + box[1][1]) / 2))
      fingieposes.append([tip,names[tick]])
      image = cv2.circle(image,tip,4,(0,0,255),4)
    #  break
      tick += 1
    return fingieposes
frameticker = 1
fps = cap.get(cv2.CAP_PROP_FPS)
while(1):
    _, frame = cap.read()
    try:
      frameWidth = frame.shape[1]
    except:
      break
    frameHeight = frame.shape[0]
   # cv2.imshow("clickme",frame)
    cv2.setMouseCallback("image", click_event)
   # cv2.waitKey(0)
    gam = getfingers(frame,"red")
    gamm = getfingers(frame,"white")
    fingiedata.append([frameticker/fps,gam + gamm])
    cv2.imshow("gamer",frame)
    vid_writer.write(frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    frameticker += 1
vid_writer.release()
cv2.destroyAllWindows()
cap.release()
with open('listfile.txt', 'w+') as filehandle:
  for gamer in fingiedata:
    filehandle.write('%s\n' % gamer)