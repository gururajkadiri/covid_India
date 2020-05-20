#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 07:55:21 2020

@author: gururaj
"""

from impfuncs import *

start_day=17
end_day=60

dfs=populate_dfs()    
state="Tamilnadu"
arr=load_Data(dfs,state=state,day_max=end_day)
cases=column(arr,2)
recovery=column(arr,3)
dead=column(arr,4)
active=column(arr,5)
cases_diff=np.diff(cases)
recovery_diff=np.diff(recovery)
dead_diff=np.diff(dead)
active_diff=np.diff(active)

cases_doubling=[get_doubling_s(cases_diff[i-1]/cases[i-1]) for i in range(start_day,end_day)]
recovery_doubling=[get_doubling_s(recovery_diff[i-1]/recovery[i-1]) for i in range(start_day,end_day)]
dead_doubling=[get_doubling_s(dead_diff[i-1]/dead[i-1]) for i in range(start_day,end_day)]
active_doubling=[get_doubling_s(active_diff[i-1]/active[i-1]) for i in range(start_day,end_day)]

plt.plot(column(arr,1)[range(start_day,end_day)],cases_doubling,markersize=8,marker="*",linewidth=3,color="blue",label="Cases")
plt.plot(column(arr,1)[range(start_day,end_day)],recovery_doubling,markersize=8,marker="o",linewidth=3,color="green",label="Recovery")
plt.plot(column(arr,1)[range(start_day,end_day)],dead_doubling,markersize=8,marker="d",linewidth=3,color="red",label="Death")
#plt.plot(column(arr,1)[range(start_day,end_day)],active_doubling,markersize=8,marker="D",linewidth=3,color="yellow",label="Active")
    
    

plt.xticks(range(0,end_day-start_day,4))
plt.xlabel("Date",weight='bold')
plt.ylabel("Days",weight='bold')
plt.grid()
plt.legend(frameon=False,loc=0)
plt.title("Covid-19 Doubling days of "+ state)
from matplotlib import rc
rc('font', weight='bold',size=12)
plt.show()
