#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 16:54:16 2020

@author: gururaj
"""

import numpy as np
import pandas as pd
import os 
import glob
import sys
import cv2
import matplotlib.pyplot as plt
img = np.zeros((1000,1000,3), np.uint8)
cv2.rectangle(img,(0,0),(1000,1000),(255,255,255),-1)

    
def makeAnimationNew(title,filename="",wd="",extension="png",loop=True,delay=20):
     import imageio
     if len(filename)==0:
         filename=title
     print("Readying animation...", end=' ')
     import webbrowser
     if len(wd)==0:
            cwd = os.getcwd()
     else:
            #cwd=os.getcwd()+"/"+wd
             cwd=wd
     files=glob.glob(cwd+"/"+title+"@*."+extension)
     files.sort(key=os.path.getmtime)
     #files=[cwd+"/"+"b_"+str(i)+".jpeg" for i in range(37)]
     images=[]
     for file in files:
         images.append(imageio.imread(file))
     imageio.mimsave(filename+".gif", images,duration=0.25,loop=1)
     
     webbrowser.open_new("file://"+cwd+"/"+filename+".gif")
     print("done.")
     
def removePngs(title):
    print("Deleting pngs and gifs...", end=' ')
    command='rm -rf '+title+"@*.png "
    os.system(command)
    command='rm -rf '+title+".gif "
    os.system(command)
    print("done.")

def plotCircle(radius,angle,clr):
    global img
    center_coordinates = (350, 350)
    thickness=10
    color2=(126,126,126)
    color=(int(clr[0]),int(clr[1]),int(clr[2]))
    if angle>0:
        cv2.ellipse(img, center_coordinates,(radius,radius),0,0,angle,color=color,thickness=thickness)
    if angle<360:
        cv2.ellipse(img, center_coordinates,(radius,radius),0,angle,endAngle=360,color=tuple(color),thickness=thickness//4)
    
  

states=np.array(['Tamilnadu', 'Maharastra', 'Kerala',
     'Delhi', 'Telangana',"JK",'Gujarat',"Bihar", 'Rajasthan','Andhra Pradesh',"West Bengal","Punjab","Uttar Pradesh","Karnataka",'Madhya Pradesh'])
#states=np.array(['Tamilnadu',"Delhi","Madhya Pradesh","Telangana","Rajasthan"])
#states=np.array(['Tamilnadu',"Maharastra"])
cmap = plt.get_cmap('tab20', len(states))
colors=[]
for i in range(len(states)):
    color=[int(j*255) for j in cmap(i)[0:3]]
    colors.append(tuple(color))
colors=np.array(colors)

for i in range(len(states)):
    color=colors[i]
    
    
df=pd.read_csv("state_wise_daily.csv",na_values='-')
df.rename(columns={'AP':'Andhra Pradesh','TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan","MP":"Madhya Pradesh","UP":"Uttar Pradesh","WB":"West Bengal","PB":"Punjab","JK":"JK","BR":"Bihar","KA":"Karnataka"},inplace=True)
df_cases=df[df["Status"]=="Confirmed"]
df_dead=df[df["Status"]=="Deceased"]
df_recovered=df[df["Status"]=="Recovered"]

df2_cases=df_cases.loc[:,df.columns[1:]]
df2_cases=df2_cases.cumsum(axis=0)
df2_cases.fillna(0,inplace=True)

df2_dead=df_dead.loc[:,df.columns[1:]]
df2_dead=df2_dead.cumsum(axis=0)
df2_dead.fillna(0,inplace=True)

df2_recovered=df_recovered.loc[:,df.columns[1:]]
df2_recovered=df2_recovered.cumsum(axis=0)
df2_recovered.fillna(0,inplace=True)

def draw_rings(index,canvas=(300,300)):
    global img
    print("Doing "+str(index))
    global states
    global colors
    dead=df2_dead[states].loc[3*index+2]
    cases=df2_cases[states].loc[3*index]
    recovered=df2_recovered[states].loc[3*index+1]
    closed=(dead+recovered)
    angles=np.divide(recovered*360,closed)
    angles[np.isnan(angles)]=0
    closed_percent=np.divide(closed,cases)
    sort=np.argsort(closed).to_list()
    
    date=df["Date"].loc[index]
    #states=states[sort]
    #closed=closed[sort]
    #angles=angles[sort]
    #colors=colors[sort]
    
    for i in range(len(states)):
        radius=int(closed[i]*400/cases[i])
        #print(closed[i])
        angle=int(angles[i])
        state=states[i]
        color=colors[i]
        plotCircle(radius,angle,clr=color)
        clr=(int(color[0]),int(color[1]),int(color[2]))
        cv2.rectangle(img,(800,30*i),(825,30*i+25),color=clr,thickness=-1)
    cv2.imwrite("rings@"+str(index)+".png",img)
    cv2.rectangle(img,(0,0),(1000,1000),(255,255,255),-1)
    




for index in range(10,50):
    draw_rings(index)
    
makeAnimationNew("rings")