import cv2
import numpy as np
from sklearn.cluster import KMeans
cap = cv2.VideoCapture("nygiants.mp4")
red = ["red", (0,0,20),(20,20,100)] # works pretty wel
white = ["white",(90,90,90),(150,170,170)]
hasFrame, frame = cap.read()
vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

while(1):
    _, frame = cap.read()
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
   # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = frame
    lower_red = red[1]
    upper_red = red[2]
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask= mask)
   # print([i[0] for i in frame])
    #print(res[0])
  #  print(frame.shape)
 #   cv2.imshow('frame',frame)
   # break
 #   cv2.imshow('res',res)
    # kmeans = KMeans(n_clusters=6, init='k-means++', max_iter=300, n_init=10, random_state=0).fit(mask)#[i for i in mask if i[0] == 255])
    # print(kmeans.cluster_centers_)
    
    # for i in range(len(kmeans.cluster_centers_)):
    #     #print(kmeans.cluster_centers_)
    #     start_point = (int(kmeans.cluster_centers_[:,0][i]-5),int(kmeans.cluster_centers_[:,1][i]-5))
    #  #   print(start_point)
    #     end_point = (int(kmeans.cluster_centers_[:,0][i]+5),int(kmeans.cluster_centers_[:,1][i]+5))
    #    # cv2.rectangle(frame,(0,0),(100,100),(0,0,0),-1)
    #     img = cv2.rectangle(frame, start_point,end_point, (0,0,255),-1)
  #  cv2.imshow('mask',mask)\
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours] 
    contour_sizes.sort(reverse=True, key=lambda  x: x[0])
    gaming = contour_sizes[:6]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    for i in gaming:         
      x,y,w,h = cv2.boundingRect(i[1])
      cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

# Draw contours:
    cv2.imshow("gamer",frame)
    vid_writer.write(frame)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
vid_writer.release()
cv2.destroyAllWindows()
cap.release()