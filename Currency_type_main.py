from PIL import ImageGrab,Image
import cv2
import numpy as np
import uuid
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import gc
from pynput.keyboard import Key, Listener 

from functools import partial
import time


def predict_image(img,model,currency_model):

    predict_results = model.predict(img)
    predict_currency_results = currency_model(img)
    results = []
    currency_results = [np.argmax(i) for i in predict_currency_results]
    for i in predict_results:
        if np.argmax(i) + 1 == 21:
             results.append(0)
        else:

            results.append(np.argmax(i)+1)
    c = 0
    list_of_totals = []
    while c<2:
        currency_results = np.array(currency_results)
        indexs = np.where(currency_results == c)
        total = 0
        for i in indexs[0]:
            total += results[i]

        list_of_totals.append(total)
        c+=1
    del img
    return list_of_totals
    
def get_screen(x1,y1,x2,y2):
        
        cap = ImageGrab.grab(bbox=(x1,y1,x2,y2))
        return cap
        

    
def get_distance(x1,y1,x2,y2):
    return (x2-x1,y2-y1)
def get_segment_distance(segments_x,segments_y,x1,y1,x2,y2):
    dist = get_distance(x1,y1,x2,y2)
    dist_of_segs_x = dist[0]/segments_x
    dist_of_segs_y = dist[1]/segments_y
    return (dist_of_segs_x,dist_of_segs_y)

def make_segment_list(segments_x,segments_y,x1,y1,x2,y2):
    seg_dist = get_segment_distance(segments_x,segments_y,x1,y1,x2,y2)
    counter = 0
    segment_x_list = []
    segment_y_list = []
    for i in range(segments_x):
        segment_x_list.append((counter,counter+seg_dist[0]))
        counter+= seg_dist[0]
    counter=0
    for i in range(segments_y):
        segment_y_list.append((counter,counter+seg_dist[1]))
        counter+= seg_dist[1]
    new_list = []
   
    for x in segment_x_list:
        for y in segment_y_list:
            new_list.append([x[0],y[0],x[1],y[1]])  
    return new_list

def run_model(x1,y1,x2,y2,model,currency_model,key):
    if key == Key.page_up:
        segments_x = 12
        segments_y = 5

        segs = make_segment_list(segments_x,segments_y,x1,y1,x2,y2)
    

        img = get_screen(x1,y1,x2,y2)
        imgs = []
        for i in segs:
            cropped_x1,cropped_y1,cropped_x2,cropped_y2 = i
            rectangle = (cropped_x1,cropped_y1,cropped_x2,cropped_y2)
            cropped_im = img.crop(rectangle)
            img_to_array = tf.keras.utils.img_to_array(cropped_im)
            resize = tf.image.resize(img_to_array,(256,256))
            resize = resize/255.0
            cropped_im.close()
            imgs.append(resize)

            cropped_im.close()
        img.close()

        del cropped_im
        del img
        del resize

        imgs = np.array(imgs)
        list_of_predicts= predict_image(imgs,model,currency_model)
        del imgs
        message = "Chaos {}, Divines: {}".format(list_of_predicts[0],list_of_predicts[1])
        filedir = 'src/total.txt'
        with open(filedir,'w+') as f:
            f.write(message)
        gc.collect()
        # keys = ['Chaos','Divine','Fusings','Other']
        # converted = [keys[i] for i in list_of_predicts]
        # print(converted)
        # print("Chaos {}, Divines: {}, Fusings: {}, Other: {}".format(list_of_predicts.count(0),list_of_predicts.count(1),list_of_predicts.count(2),list_of_predicts.count(3)))
def main():
    currency_model_save_path = 'ModelCheckpoints\checkpoint-CURRENCY-05-0.01.hdf5'
    model_save_path = 'ModelCheckpoints\checkpoint-11-0.00.hdf5'
    model = tf.keras.models.load_model(model_save_path)
    currency_model = tf.keras.models.load_model(currency_model_save_path)
    runtime = partial(run_model,1698, 786,2539, 1134,model,currency_model)
    # run_model(1698, 786,2539, 1134,model,currency_model,"abc")
    while 1:
        time.sleep(0.0050) #this is here so u dont lag
        with Listener(on_press=runtime) as listener:
            listener.join()
        gc.collect()


main()

