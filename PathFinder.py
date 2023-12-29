import cv2
from cv2 import aruco
import numpy as np
import os
from queue import PriorityQueue
from Get_world_coords import Get_World_Coords
import time




img = cv2.imread(r'C:\Users\Shirshak\Desktop\Robotics Summer Project\Photos\Final_Map1.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray,255,255)
print("Generating Map:\n")
print("------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

#FOR DETECTING ARUCO MARKERS

def findArucoMarkers(img):

    marker_dict=aruco.Dictionary_get(aruco.DICT_4X4_1000)

    parameters_marker=aruco.DetectorParameters_create()

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    marker_corner,marker_IDs,reject=aruco.detectMarkers(gray,marker_dict,parameters=parameters_marker) #Detecting markers

    if marker_corner: #Giving condition
        for id,corners in zip(marker_IDs,marker_corner):
            cv2.polylines(img,[corners.astype(np.int32)],True,(0,255,0),2,cv2.LINE_AA)
            corners=corners.reshape(4,2)
            corners=corners.astype(int)
            top_right=corners[0].ravel()
            cv2.putText(img,f"id:{id[0]}",top_right,cv2.FONT_HERSHEY_TRIPLEX,0.05,(0,0,255),thickness=1)
            
            peri = cv2.arcLength(corners,True)
            epsi = 0.2*peri
            approx = cv2.approxPolyDP(corners,epsi,True)
            x, y, w, h = cv2.boundingRect(approx)
            k=int(corners[0][0])
            p=int(corners[0][1])
            if corners[0][0]-k>=.5:
                x+=1
            if corners[0][1]-p>=.5:
                y+=1

    return [(x,y+1),marker_IDs,((x+1+(w//2)),y+1+(h//2))]

coord_aruco,arucoFound,aruco_center = findArucoMarkers(img)

#DEFINING A CLASS WITH ALL NECESSTIES FOR EACH CELL 

class Spot:
    def __init__(self, x, y, w, h, id):
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.id=id
        self.neighbors=[]
        self.centre=(x+w/2,y+h/2)
        self.edge_score=1
        

#FOR GETTING ALL THE CONTOURS
minContours = []

total = 0

contours, _ = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


def getContours(img):
    b=0
    val={}
    c=[]
    i=0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >50:
            perimeter = cv2.arcLength(contour,True)
            epsilon = 0.1*perimeter
            approx = cv2.approxPolyDP(contour,epsilon,True)
            x, y, w, h = cv2.boundingRect(approx)
           
            cv2.putText(img, str(i), (x + (w//2),y + (h//2)), cv2.FONT_HERSHEY_TRIPLEX,1, (255,0,0), 2, cv2.FILLED)
            minContours.append(approx)
            c.append((x,y))
            i = i+1
    
        val[i]=contour
        
        
    i=0
    for l in c:
        if coord_aruco==l:
            b=i
        i+=1
    
    # print("THE TOTAL NO. OF NODES ARE")
    global total
    total = i
    return val,b

#MAIN

path,begin=getContours(img)
# begin=70


#DEPENDENCIES AND VARIBLES
id = 0
spots = []


w_all = []
h_all = []

w_sum = 0
h_sum = 0


#GETTING THE X AND Y COORDINATES ALONG WITH THE HEIGHT AND WIDTH OF EACH CELL
for cnt in minContours:
    x, y, w, h = cv2.boundingRect(cnt)
    w_all.append(w)
    h_all.append(h)
    spots.append(Spot(x,y,w,h,id))

    id = id + 1

def PathCost(current,neighbor):
    Turn_Cost=0
    if current==neighbor:
        Turn_Cost=0
    elif current=="F" or current=="B":
        if neighbor=="L" or neighbor=="R":Turn_Cost=500
        else: Turn_Cost=1000

    elif current=="L" or current=="R":
        if neighbor=="F" or neighbor=="B":Turn_Cost=500
        else: Turn_Cost=1000
    
    return Turn_Cost+116


for w in w_all:
    w_sum = w_sum + w

for h in h_all:
    h_sum = h_sum + h

w_av = w_sum/total
h_av = h_sum/total
j=0
for spot in spots:
    i = 0
    if j%4==0:
        print("#",end="")
    for cnt in minContours:
        if(cv2.pointPolygonTest(cnt, (spot.centre[0] + w_av, spot.centre[1]), False)==1):
            spot.neighbors.append((i,'R'))
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] - w_av, spot.centre[1]), False)==1):
            spot.neighbors.append((i,'L'))
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] , spot.centre[1] + h_av), False)==1):
            spot.neighbors.append((i,'B'))
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] , spot.centre[1] - h_av), False)==1):
            spot.neighbors.append((i,'F'))

        i += 1
    j+=1

corner=None

for spot in spots:
    if len(spot.neighbors)<4:
        spot.edge_score=1000
        
        corner=True
    else:
        if corner==True:
            spot.edge_score=500
            
        corner=False
imgedge = cv2.resize(img, (1500,800))

Map = cv2.resize(img, (1500,800))

cv2.imshow('Map',Map)
cv2.waitKey(0)

last=int(input("\n\nEnter Final Point:"))

start = spots[begin]
end = spots[last]
hue = []
for spot in spots:
    hue.append( abs(spot.centre[0]-end.centre[0]) + abs(spot.centre[1]-end.centre[1]) )

count = 0
open_set = PriorityQueue()
open_set.put( (0, count, (begin, 'F'))) #f_score, count(for tie breaking if 2 have same f_score), spot_id) 
came_from = {begin:None}
g_score = {spot: float("inf") for spot in range(0,i+1)}
g_score[begin] = 0
f_score = {spot: float("inf") for spot in range(0,i+1)}
f_score[begin] = abs(spots[0].centre[0]-spots[last].centre[0]) + abs(spots[0].centre[1]-spots[last].centre[1])

open_set_hash = {begin}
weight=1.5

expanded_nodes=0
while not open_set.empty():
    node = open_set.get()[2]
    current=node[0]
    current_direction=node[1]
    expanded_nodes+=1
    cv2.rectangle(img,(spots[current].x,spots[current].y),(spots[current].x+spots[current].w,spots[current].y+spots[current].h),
                      (0,255,0),thickness=cv2.FILLED)
    open_set_hash.remove(current)

    if current == last:
        break
    
    for neighbor in spots[current].neighbors :

        temp_g_score = g_score[current] + PathCost(current_direction,neighbor[1])

        if temp_g_score < g_score[neighbor[0]]:
            came_from[neighbor[0]] = current
            g_score[neighbor[0]] = temp_g_score
            
            if temp_g_score<hue[neighbor[0]]:
                f_score[neighbor[0]] =temp_g_score + hue[neighbor[0]] + spots[neighbor[0]].edge_score
            else:
                f_score[neighbor[0]] =(temp_g_score + (2*weight-1)*hue[neighbor[0]])/weight + spots[neighbor[0]].edge_score
            
            if neighbor[0] not in open_set_hash:
                count = count + 1
                open_set.put((f_score[neighbor[0]], count, (neighbor[0],neighbor[1])))
                open_set_hash.add(neighbor[0])

path_to_Traverse=[]

def print_path(img):
    nodes=[]
    current=last
    while came_from[current]!=None:
        nodes.append(came_from[current])
        current=came_from[current]
    for node in nodes:
        cv2.rectangle(img,(spots[node].x,spots[node].y),(spots[node].x+spots[node].w,spots[node].y+spots[node].h),
                      (255,0,0),thickness=cv2.FILLED)
        path_to_Traverse.append([(spots[node].x+w//2),(spots[node].y+h//2)])
        

print_path(img)
path_to_Traverse.append(aruco_center)
real_path=Get_World_Coords(path_to_Traverse)

def send_coords():
    center=real_path[0][len(real_path[0])-1]
    del list(real_path[0])[-1]
    real_path_new=real_path.tolist()
    return real_path_new,center

def Show_Path(time,show_map=False,track=False):
    if show_map:
        cv2.imshow('Map', Map)
        cv2.waitKey(0)
    if track:
        Track(time)

def Track(time):
    add=0
    net_time=[]
    for t in time:
        if t[0]=="R" or t[0]=="L":
            add=t[1]
            continue
        else:
            t[1]+=add+0.42
            add=0
        net_time.append(t)
    for coords,t in zip(path_to_Traverse,net_time):
            t[1]=t[1]*1000
            imgFinal=cv2.circle(img,(coords[0],coords[1]),30,(255,0,0),thickness=cv2.FILLED)
            imgFinal = cv2.resize(imgFinal, (1500,800))
            cv2.imshow('Tracked', imgFinal)
            cv2.waitKey(int(t[1]))



imgFinal = cv2.resize(img, (1500,800))

if __name__=="__main__":
    print(real_path)
    cv2.imwrite(r'Photos/output.png',imgFinal)
    cv2.imshow('Contour Detection', imgFinal)
    cv2.waitKey(0)
