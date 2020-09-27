import cv2
import numpy as np
cap = cv2.VideoCapture("croppednygiants.mp4")
red = ["red", (0,0,20),(20,20,100)] # works pretty wel
white = ["white",(70,40,50),(150,170,170)]
hasFrame, frame = cap.read()
vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))
redfingernames = ["RPinky","RMiddle","RThumb","LThumb","RMiddle","RPinky"]
whitefingernames = ["LRing","LPointer","LPointer","LRing"]
fingiedata = []

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