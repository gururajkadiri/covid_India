#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 07:55:21 2020

@author: gururaj
"""

from impfuncs import *

start_day=15
end_day=58

dfs=populate_dfs()    
state="India"
arr=load_Data(dfs,state=state,day_max=end_day)
cases=column(arr,2)
recovery=column(arr,3)
dead=column(arr,4)
active=column(arr,5)
cases_diff=np.diff(cases)
recovery_diff=np.diff(recovery)
dead_diff=np.diff(dead)
active_diff=np.diff(active)


cases_rate=[cases_diff[i-1]/cases[i-1] for i in range(start_day,end_day)]
dead_rate=[dead_diff[i-1]/dead[i-1] for i in range(start_day,end_day)]
recovery_rate=[recovery_diff[i-1]/recovery[i-1] for i in range(start_day,end_day)]

ini_cases=10
ini_deaths=1
ini_recovery=1
cases=ini_cases
deaths=ini_deaths
recoveries=ini_recovery
arr=[]
arr.append([0,cases,deaths,recoveries])
for i in range(len(cases_rate)):
    cases=cases*(1+cases_rate[i])
    deaths=deaths*(1+dead_rate[i])
    recoveries=recoveries*(1+recovery_rate[i])
    arr.append([i+1,cases,deaths,recoveries])


plt.plot(column(arr,0),column(arr,1),markersize=4,marker="*",linewidth=3,color="blue",label="Cases")
plt.plot(column(arr,0),column(arr,2),markersize=4,marker="o",linewidth=3,color="red",label="Deaths")
#plt.plot(column(arr,0),column(arr,3),markersize=4,marker="o",linewidth=3,color="green",label="Recoveries")    
    


plt.xlabel("Day",weight='bold')
plt.ylabel("Counts",weight='bold')
plt.grid()
plt.legend(frameon=False,loc=0)
plt.title("Covid-19 with "+str(ini_cases)+" cases and "+str(ini_deaths)+" deaths on day 0, simulated with growth pattern of "+ state)
from matplotlib import rc
rc('font', weight='bold',size=12)
plt.show()
