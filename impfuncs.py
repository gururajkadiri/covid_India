#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 18:23:44 2020

@author: gururaj
"""

from scipy import optimize
from matplotlib import pylab as plt
import numpy as np
import pdb
from numpy import log
import pandas as pd
import datetime
import io 
import itertools

import urllib.request
url = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
urllib.request.urlretrieve(url,"state_wise_daily.csv")


states=np.array(["India",'Tamilnadu', 'Maharastra', 'Kerala',
     'Delhi', 'Telangana',"JK",'Gujarat',"Bihar", 'Rajasthan','Andhra Pradesh',"West Bengal","Punjab","Uttar Pradesh","Karnataka",'Madhya Pradesh'])
states=np.array(["India",'Maharastra', 
     'Tamilnadu','Rajasthan',"Telangana",'Madhya Pradesh'])

clrs=['#008000','#0000FF', "#FFFF00", '#FF0000', '#D2691E',
     '#00563f','#C0C0C0','#aafbff', '#9400D3','#306998','#f4c430','#FFC0CB',"#ACDDDE","#FF4500","#FFFA8D"]

 

colorcycler=itertools.cycle(clrs)




population={"Tamilnadu":77841267,"Maharastra":123144223,"Kerala":35699443,
            "Delhi":18710922,"Telangana":39362732,"JK":13606320,
            "Gujarat":3872399,"Bihar":124799926,"Rajasthan":8622934,
            "Andhra Pradesh":11628099,"West Bengal":24981474,"Punjab":30141373,
            "Uttar Pradesh":237882725,"Karnataka":67562686,
            "Madhya Pradesh":85358965,"India":1371360350}

def getDates(start_day,end_day):
    start_date=datetime.datetime.strptime("14-Mar-20", "%d-%b-%y")
    start_date=start_date+datetime.timedelta(days=start_day)
    dts=[]
    for i in range(0,end_day):
        dt=start_date+datetime.timedelta(days=i)
        dts.append(datetime.datetime.strftime(dt,"%d-%b"))
    dts=np.array(dts)
    return(dts)



def populate_dfs():
    
    df=pd.read_csv("state_wise_daily.csv",na_values='-')
    df.rename(columns={'AP':'Andhra Pradesh','TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan","MP":"Madhya Pradesh","UP":"Uttar Pradesh","WB":"West Bengal","PB":"Punjab","JK":"JK","BR":"Bihar","KA":"Karnataka","TT":"India"},inplace=True)
    df_cases=df[df["Status"]=="Confirmed"]
    df_dead=df[df["Status"]=="Deceased"]
    df_recovered=df[df["Status"]=="Recovered"]
    return([df,df_cases,df_recovered,df_dead])
    
    
    


def load_Data(dfs,start_day=0,day_max=57,state="India"):
    
    start_date=datetime.datetime.strptime("14-Mar-20", "%d-%b-%y")
    start_date=start_date+datetime.timedelta(days=start_day)
    dts=getDates(start_day,day_max)
    [df,df_cases,df_recovered,df_dead]=dfs
    df["Date"]=pd.to_datetime(df["Date"])
    #df=df[df["Date"]>=start_date]
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
    df2_cases=df2_cases[df["Date"]>=start_date]
    df2_recovered=df2_recovered[df["Date"]>=start_date]
    df2_dead=df2_dead[df["Date"]>=start_date]
    arr=[]
    i=0
    for index in range(day_max-start_day):
        recovered=df2_recovered[state].loc[start_day*3+3*index+1]
        dead=df2_dead[state].loc[start_day*3+3*index+2]
        cases=df2_cases[state].loc[start_day*3+3*index]
        active=cases-(dead+recovered)
        dt=dts[i]
        arr.append([index,dt,cases,recovered,dead,active])
        i=i+1
    return(arr)


def column(arr,i):
  return(np.array([row[i] for row in arr]))

def exp_growth_guru(t, x0, r,delta):
    return x0 * ((1 + r) ** t)+delta

def exp_growth(t, x0, r):
    return x0 * ((1 + r) ** t)


def printStats(arr,dts,t):
    print("\nOn Day "+str(t)+" Date:"+dts[t]+"\n")
    print("Total Cases: "+str(column(arr,2)[t]))
    print("Recovered Cases: "+str(column(arr,3)[t]))
    print("Dead Cases: "+str(column(arr,4)[t]))
    print("Active Cases: "+str(column(arr,5)[t]))
    
def printPredictions(fitted_cases,fitted_recovered,fitted_dead,fitted_active,dts,t):
    print("\n Fitting On Day "+str(t)+" Date:"+dts[t]+"\n")
    print("Total Cases: "+str(int(round(fitted_cases[t]))))
    print("Recovered Cases: "+str(int(round(fitted_recovered[t]))))
    print("Dead Cases: "+str(int(round(fitted_dead[t]))))
    print("Active Cases: "+str(int(round((fitted_active[t])))))
    
    
    

def exp_growth_s(t, x0, r):
    return x0 * ((1 + r) ** t)


def get_doubling_s(r):
    return(log(2)/log(1+r))


def get_doubling(t,r,x0,ini):
    t_new=log(x0/ini+2*(1+r)**t)/log(1+r)
    return(t_new)
