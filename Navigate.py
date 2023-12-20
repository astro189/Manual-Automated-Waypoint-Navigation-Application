import numpy as np
from PathFinder import send_coords, Show_Path
from SendRequest import sendRequest
import cv2 as cv
import time

coords,aruco_center=send_coords()
path_to_travel=coords[0]

path_to_travel.pop(0)

start=aruco_center


avg_speed=28

path_request=[]


def calc_time(dist):
    return round(dist/avg_speed,2)
i=0

left_value=0.28
right_value=0.28
prev=None
last=""

for x,y in path_to_travel:
    if i==0:
        if abs(x-start[0])>=1.5:
            if x>start[0]:
                path_request.append(['R',right_value])
                t=calc_time(abs(x-start[0]))
                path_request.append(['F',t])
            else:
                path_request.append(['L',left_value])
                t=calc_time(abs(x-start[0]))
                path_request.append(['F',t])
            last='x'

        elif abs(y-start[1])>=1.5:
            t=calc_time(abs(y-start[1]))
            path_request.append(['F',t])
            last='y'

    else:
        if abs(x-prev[0])>=1.5:
            if last=='x':
                t=calc_time(abs(x-prev[0]))
                path_request.append(['F',t])
                last='x'

            elif last=='y':
                if x>prev[0]:
                    path_request.append(['R',right_value])
                    t=calc_time(abs(x-prev[0]))
                    path_request.append(['F',t])
                    last='x'

                
                else:
                    path_request.append(['L',left_value])
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
                    path_request.append(['R',right_value])
                    t=calc_time(abs(y-prev[1]))
                    path_request.append(['F',t])
                    last='y'
                
                else:
                    path_request.append(['L',left_value])
                    t=calc_time(abs(y-prev[1]))
                    path_request.append(['F',t])
                    last='y'
    i+=1
    prev=(x,y)

final_path=[]
sum_forward=0
for x,t in path_request:
    if x=="F":
        sum_forward+=t
    else:
        final_path.append(['F',round(sum_forward,2)])
        if x=='L':
            final_path.append([x,left_value])
            sum_forward=0
        else:
            final_path.append([x,right_value])
            sum_forward=0
final_path.append(['F',round(sum_forward-5,2)])
Show_Path(path_request,track=True)

i=0
for path in final_path:
    x=sendRequest(path[0],path[1])



