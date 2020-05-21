#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 21:12:21 2020

@author: gururaj
"""

from impfuncs import *
states=np.array(["India",'Maharastra', "Delhi",
     'Gujarat','Rajasthan',"West Bengal",'Madhya Pradesh'])

clrs=['#008000','#C0C0C0', '#FFC0CB', '#FF0000', '#D2691E',
     '#aafbff', '#0000FF', '#9400D3','#306998','#f4c430','#00563f',"#FFFF00","#ACDDDE","#FF4500","#FFFA8D"]

from itertools import cycle
lines = ["-","--","-.",":"]
linecycler = cycle(lines)
colorcycler=cycle(clrs)
start_day=23
end_day=68
dfs=populate_dfs()    
dts=getDates(start_day,end_day)

for state in states:
    
    arr=load_Data(dfs=dfs,start_day=start_day,day_max=end_day,state=state)
    closed=column(arr,2)-column(arr,5)
    dead_percent_closed=(column(arr,4)/closed)*100
    if state=="India":
        plt.plot(column(arr,0),dead_percent_closed,markersize=12,marker="*",linewidth=4,color=next(colorcycler),label=state)
    else:
        plt.plot(column(arr,0),dead_percent_closed,markersize=5,marker="o",linewidth=1,color=next(colorcycler),label=state)
    
plt.xticks(range(0,end_day-start_day,3),dts[range(0,end_day-start_day,3)])

plt.xticks()
plt.ylabel("Dead % among closed cases")
plt.grid(True)
plt.legend(frameon=False)
plt.title("Fraction of deceased in closed cases of each state\n data upto "+dts[end_day-start_day-1])
plt.show()