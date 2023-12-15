import cv2
from cv2 import aruco
import numpy as np
import os
from queue import PriorityQueue
from Get_world_coords import Get_World_Coords
import time




img = cv2.imread(r'C:\Users\Shirshak\Desktop\MAWNA\Photos\Final_Map1.png')
# print(img.shape)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgCanny = cv2.Canny(imgGray,255,255)

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
    # print(marker_corner[0][0][0][0],marker_corner[0][0][0][1])

    return [(x,y+1),marker_IDs,((x+1+(w//2)),y+1+(h//2))]

coord_aruco,arucoFound,aruco_center = findArucoMarkers(img)
# print(coord_aruco)

#DEFINING A CLASS WITH ALL NECESSTIES FOR EACH CELL 

class Spot:
	def __init__(self, x, y, w, h, id):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.id = id
		self.neighbors = []
		self.centre = (x+w/2, y+h/2)


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
            # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            # cv2.circle(img,(x,y),3,(0,0,255),thickness=-1)
            cv2.putText(img, str(i), (x + (w//2),y + (h//2)), cv2.FONT_HERSHEY_TRIPLEX,1, (255,0,0), 2, cv2.FILLED)
            minContours.append(approx)
            c.append((x,y))
            # if i==325:
            #     print(x,y)
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

def h(cell1,cell2):
    x1,y1=cell1  

    x2,y2=cell2   

    return abs(x1-x2)+abs(y1-y2) #


for w in w_all:
    w_sum = w_sum + w

for h in h_all:
    h_sum = h_sum + h

w_av = w_sum/total
h_av = h_sum/total
for spot in spots:
    i = 0
    for cnt in minContours:
        if(cv2.pointPolygonTest(cnt, (spot.centre[0] + w_av, spot.centre[1]), False)==1):
            spot.neighbors.append(i)
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] - w_av, spot.centre[1]), False)==1):
            spot.neighbors.append(i)
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] , spot.centre[1] + h_av), False)==1):
            spot.neighbors.append(i)
        elif(cv2.pointPolygonTest(cnt, (spot.centre[0] , spot.centre[1] - h_av), False)==1):
            spot.neighbors.append(i)
        i += 1

# for spot in spots:
#     print(spot.neighbors)
Map = cv2.resize(img, (1500,800))
# Map = cv2.resize(img, (1300,640))

cv2.imshow('Map',Map)
cv2.waitKey(0)

# start=int(input("Enter starting point"))
last=int(input("Enter Final Point:"))

start = spots[begin]
end = spots[last]
hue = []
for spot in spots:
    hue.append( abs(spot.centre[0]-end.centre[0]) + abs(spot.centre[1]-end.centre[1]) )

count = 0
open_set = PriorityQueue()
open_set.put( (0, count, begin) ) #f_score, count(for tie breaking if 2 have same f_score), spot_id) 
came_from = {}
g_score = {spot: float("inf") for spot in range(0,i+1)}
g_score[begin] = 0
f_score = {spot: float("inf") for spot in range(0,i+1)}
f_score[begin] = abs(spots[0].centre[0]-spots[last].centre[0]) + abs(spots[0].centre[1]-spots[last].centre[1])


open_set_hash = {begin}

while not open_set.empty():
    current = open_set.get()[2]
    
    open_set_hash.remove(current)

    if current == last:
        break
    
    for neighbor in spots[current].neighbors :
        if neighbor in came_from:continue
        temp_g_score = g_score[current] + 45


        if temp_g_score < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = temp_g_score
            f_score[neighbor] = temp_g_score + hue[neighbor]

            if neighbor not in open_set_hash:
                count = count + 1
                open_set.put( (f_score[neighbor], count, neighbor) )
                open_set_hash.add(neighbor)
# print(came_from)
                
imgFinal = cv2.resize(img, (1500,800))
path_to_Traverse=[]
def print_path(img):

    list1=[]
    for i in came_from:
        # print(i)
        list1.append(came_from[i])
    coords = []
   
    [coords.append(x) for x in list1 if x not in coords]
    j=0
    
    for coord in coords:
        cv2.rectangle(img,(spots[coord].x,spots[coord].y),(spots[coord].x+spots[coord].w,spots[coord].y+spots[coord].h),
                      (0,255,0),thickness=cv2.FILLED)
        path_to_Traverse.append([(spots[coord].x+w//2),(spots[coord].y+h//2)])
        # imgFinal = cv2.resize(img, (1500,800))
        # cv2.circle(img,((spots[coord].x+w//2),(spots[coord].y+h//2)),30,(255,0,0),thickness=cv2.FILLED)
        # cv2.imshow('Contour Detection', imgFinal)
        # cv2.waitKey(0)
        # imgFinal = cv2.resize(img, (1500,800))
        # cv2.imshow('Contour Detection', imgFinal)
        # cv2.waitKey(0)
    # for i in path:
    #     if i==coords[j]:
    #         perimeter = cv2.arcLength(path[i+1],True)
    #         epsilon = 0.02*perimeter
    #         approx = cv2.approxPolyDP(path[i+1],epsilon,True)
    #         x, y, w, h = cv2.boundingRect(approx)
    #         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),thickness=cv2.FILLED)
    #         path_to_Traverse.append([(x+w//2),(y+h//2)])
    #         imgFinal = cv2.resize(img, (1500,800))
    #         cv2.imshow('Contour Detection', imgFinal)
    #         cv2.waitKey(0)

    #         # cv2.circle(img,((x+w//2),(y+h//2)),30,(255,0,0),thickness=cv2.FILLED)
    #         j+=1
    #     if j==len(coords)-1:
    #         break

        
print_path(img)
path_to_Traverse.append(aruco_center)
real_path=Get_World_Coords(path_to_Traverse)

def send_coords():
    center=real_path[0][len(real_path[0])-1]
    del list(real_path[0])[-1]
    real_path_new=real_path.tolist()
    return real_path_new,center

def Show_Path(show_map=False):
    if show_map:
        cv2.imshow('Map', Map)
        cv2.waitKey(0)
    else:
        cv2.imshow('Path', imgFinal)
        cv2.waitKey(0)



def track(y):
    # for x,y in zip(path,path_to_Traverse):
    imgFinal = cv2.resize(img, (1500,800))
    cv2.circle(imgFinal,(path_to_Traverse[y][0],path_to_Traverse[y][1]),30,(255,0,0),thickness=cv2.FILLED)
    cv2.imshow('Contour Detection', imgFinal)
    cv2.waitKey(0)
# cv2.circle(img,aruco_center,30,(255,0,0),cv2.FILLED)


# imgFinal = cv2.resize(img, (2000,1000))

if __name__=="__main__":
    print(real_path)
    # cv2.imwrite(r'Photos/output.png',imgFinal)
    cv2.imshow('Contour Detection', imgFinal)
    cv2.waitKey(10000000)
