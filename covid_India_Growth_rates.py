#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 16:54:16 2020

@author: gururaj
"""

import numpy as np
import pandas as pd
import pandas as pd
import sys
from scipy import optimize
import matplotlib.pyplot as plt
from impfuncs import *
import datetime

start_day=30
end_day=75

start_date=datetime.datetime.strptime("14-Mar-20", "%d-%b-%y")
start_date=start_date+datetime.timedelta(days=start_day)

df=pd.read_csv("state_wise_daily.csv",na_values='-')
df["Date"]=pd.to_datetime(df["Date"])
df=df[df["Date"]>=start_date]
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

def plot_Data(start_day=0,day_max=50,state="TT"):
    arr=[]
    for index in range(day_max-start_day):
        recovered=df2_recovered[state].loc[start_day*3+3*index+1]
        dead=df2_dead[state].loc[start_day*3+3*index+2]
        cases=df2_cases[state].loc[start_day*3+3*index]
        active=cases-(dead+recovered)
        date=df_cases["Date"].loc[start_day*3+3*index]
        arr.append([index,cases,recovered,dead,active])
    return(arr)


dts=[]
for i in range(0,end_day):
     dt=start_date+datetime.timedelta(days=i)
     dts.append(datetime.datetime.strftime(dt,"%d-%b"))
dts=np.array(dts)
arr=plot_Data(start_day=start_day,day_max=54,state="MH")
x_pts=column(arr,0)
x_ext_pts=range(0,end_day)
y_cases=column(arr,1)

[x0_cases, r_cases,ini_cases], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,1), p0=(0, 1.0,column(arr,1)[0]),method="lm")
[x0_recovered, r_recovered,ini_recovered], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,2), p0=(0, 1.0,column(arr,2)[0]),method="lm")
[x0_dead, r_dead,ini_dead], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,3), p0=(0, 1.0,column(arr,3)[0]),method="lm")
[x0_active, r_active,ini_active], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,4), p0=(0, 1.0,column(arr,4)[0]),method="lm")


fitted_cases = exp_growth(x_ext_pts, x0_cases, r_cases,ini_cases)
fitted_recovered = exp_growth(x_ext_pts, x0_recovered, r_recovered,ini_recovered)
fitted_dead = exp_growth(x_ext_pts, x0_dead, r_dead,ini_dead)
fitted_active = exp_growth(x_ext_pts, x0_active, r_active,ini_active)


fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(nrows=2,ncols=2,sharex=True)
ax1.semilogy(x_pts, column(arr,1), 'bo')
ax1.semilogy(fitted_cases, 'b-')
ax1.set_title("Cases")
ax2.semilogy(x_pts, column(arr,2), 'go')
ax2.semilogy(fitted_recovered, 'g-')
ax2.set_title("Recovered")
ax3.semilogy(x_pts, column(arr,3), 'ro')
ax3.semilogy(fitted_dead, 'r-')
ax3.set_title("dead")
ax4.semilogy(x_pts, column(arr,4), 'ko')
ax4.semilogy(fitted_active, 'k-')
ax4.set_title("Active")

ax1.set_xticks(range(0,75,6))
ax1.set_xticklabels(dts[range(0,75,6)],rotation=90)
ax3.set_xticks(range(0,75,6))
ax3.set_xticklabels(dts[range(0,75,6)],rotation=90)
plt.text(5,5,"Gururaj is a good boy")

#plt.tick_params(axis='both', which='minor', labelsize=2)
ax1.grid()
ax2.grid()
ax3.grid()
ax4.grid()

plt.xticks(rotation=90)
#plt.title("Data fitted upto "+str(dts[0])+" and extrapolated upto "+str(dts[len(dts)-1]))
plt.show()

print("Fitting data from "+dts[0])
print("Growth Parameters:\n")
print("Cases rate:"+str(r_cases))
print("Recovery rate:"+str(r_recovered))
print("Dead rate:"+str(r_dead))
print("Active rate:"+str(r_active))


t=20

printStats(arr, dts, t)
printPredictions(fitted_cases,fitted_recovered,fitted_dead,fitted_active,dts,t)