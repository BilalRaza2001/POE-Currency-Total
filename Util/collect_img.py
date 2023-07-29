# from pynput.mouse import Listener,Button, Controller

# Mouse = Controller()

# def get_postion_of_click(x,y,button,pressed):
#     print("{}, {}".format(x,y))

# with Listener(
#         on_click=get_postion_of_click) as listener:
#     listener.join()
# 1698, 786
# 1698, 786
# 2539, 1134
# 2539, 1134
from PIL import ImageGrab,Image
import cv2
import numpy as np
import uuid
import os


def save_image(img,seg):
    path = 'IMG'
    filename = "Blank ({}).png".format(str(seg))
    save_to_path = os.path.join(path,filename)
    img.save(save_to_path)
def get_screen(x1,y1,x2,y2,seg_no):
        cap = ImageGrab.grab(bbox=(x1,y1,x2,y2))
        save_image(cap,seg_no)

    
def get_distance(x1,y1,x2,y2):
    return (x2-x1,y2-y1)
def get_segment_distance(segments_x,segments_y,x1,y1,x2,y2):
    dist = get_distance(x1,y1,x2,y2)
    dist_of_segs_x = dist[0]/segments_x
    dist_of_segs_y = dist[1]/segments_y
    return (dist_of_segs_x,dist_of_segs_y)

def make_segment_list(segments_x,segments_y,x1,y1,x2,y2):
    seg_dist = get_segment_distance(segments_x,segments_y,x1,y1,x2,y2)
    counter = x1
    segment_x_list = []
    segment_y_list = []
    for i in range(segments_x):
        segment_x_list.append((counter,counter+seg_dist[0]))
        counter+= seg_dist[0]
    counter=y1
    for i in range(segments_y):
        segment_y_list.append((counter,counter+seg_dist[1]))
        counter+= seg_dist[1]
    new_list = []
   
    for x in segment_x_list:
        for y in segment_y_list:
            new_list.append([x[0],y[0],x[1],y[1]])  
    return new_list

def main(x1,y1,x2,y2):
    segments_x = 12
    segments_y = 5
    segs = make_segment_list(segments_x,segments_y,x1,y1,x2,y2)
    print(len(segs))
    print(segs[2])
    c = 60
    for i in segs:
        x1,y1,x2,y2 = i
        get_screen(x1,y1,x2,y2,c)
        c+= 1

main(1698, 786,2539, 1134)