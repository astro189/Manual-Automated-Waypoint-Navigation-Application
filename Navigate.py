import numpy as np
from PathFinder_Final import send_coords, Show_Path, track
from SendRequest import sendRequest
import cv2 as cv
import time

# Initiate=int(input("Initiate Map (YES/NO):"))
coords,aruco_center=send_coords()

# path_to_travel=[[100.59462 , 105.989586],
#   [100.625   ,  93.7066  ],
#   [100.625    , 81.46701 ],
#   [ 91.78385  , 81.510414],
#   [ 83.03385  , 81.510414]]

# start=[ 74.22309  , 81.33681 ]
path_to_travel=coords[0]
# print(coords[0])
path_to_travel.pop(0)

# path_to_travel.reverse()
start=aruco_center


avg_speed=17

path_request=[]
# print(path_to_travel)

# def GUI(Show_Map=False):
#     if Show_Map:
#         Show_Path(show_map=True)

# GUI(True)   

def calc_time(dist):
    return round(dist/avg_speed,2)
i=0
# print(start)
prev=None
last=""
for x,y in path_to_travel:
    # print(x,y)
    if i==0:
        # print(x-start[0],y-start[1])
        if abs(x-start[0])>=1.5:
            # t=calc_time(abs(x-start[0]))
            if x>start[0]:
                path_request.append(['R',0.65])
                t=calc_time(abs(x-start[0]))
                path_request.append(['F',t])
            else:
                path_request.append(['L',0.75])
                t=calc_time(abs(x-start[0]))
                path_request.append(['F',t])
            last='x'

        elif abs(y-start[1])>=1.5:
            t=calc_time(abs(y-start[1]))
            path_request.append(['F',t])
            last='y'
            # if y<start[1]:
            #     t=calc_time(abs(y-start[1]))
            #     path_request.append(['F',t])
            #     t=calc_time(abs(y-start[1]))
            #     path_request.append(['F',t-0.14])
            #     last='y'

            # elif y>start[1]:
            #     path_request.append(['R',0.30])
            #     t=calc_time(abs(y-start[1]))
            #     path_request.append(['F',t-0.14])
            #     last='y'

    else:
        if abs(x-prev[0])>=1.5:
            if last=='x':
                t=calc_time(abs(x-prev[0]))
                path_request.append(['F',t])
                last='x'

            elif last=='y':
                if x>prev[0]:
                    path_request.append(['R',0.65])
                    t=calc_time(abs(x-prev[0]))
                    path_request.append(['F',t])
                    last='x'

                
                else:
                    path_request.append(['L',0.75])
                    t=calc_time(abs(x-prev[0]))
                    path_request.append(['F',t])
                    last='x'
            
        elif abs(y-prev[1])>=1.5:
            if last=='y':
                t=calc_time(abs(y-prev[1]))
                path_request.append(['F',t])
                last='y'

            elif  last=='x':
                if y>prev[1]:
                    path_request.append(['R',0.65])
                    t=calc_time(abs(y-prev[1]))
                    path_request.append(['F',t])
                    last='y'
                
                else:
                    path_request.append(['L',0.75])
                    t=calc_time(abs(y-prev[1]))
                    path_request.append(['F',t])
                    last='y'
    i+=1
    prev=(x,y)
# print(path_request)

# for i,value in enumerate(path_request):
#     track(i)
#     time.sleep(value[1])

final_path=[]
sum_forward=0
for x,t in path_request:
    if x=="F":
        sum_forward+=t
    else:
        final_path.append(['F',round(sum_forward,2)])
        if x=='L':
            final_path.append([x,0.77])
            sum_forward=0
        else:
            final_path.append([x,0.65])
            sum_forward=0
final_path.append(['F',round(sum_forward,2)])
print(final_path)
# Show_Path()

i=0
for path in path_request:
    x=sendRequest(path[0],path[1])
    if x:
        track(i)
    i+=1


