#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 07:55:21 2020

@author: gururaj
"""

from impfuncs import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
fig = make_subplots(rows=1, cols=1,subplot_titles=["Doubling Days"])
fig=go.Figure()

import matplotlib.pyplot as plt


start_day=25
end_day=63

dfs=populate_dfs()    


#fig,(ax1,ax2,ax3)=plt.subplots(nrows=2,ncols=1,sharex=True)
type="cases"
state="Tamilnadu"
states=["India","Tamilnadu","Maharastra","West Bengal","Gujarat","Rajasthan"]

for state in states:
    color=next(colorcycler)
    arr=load_Data(dfs,state=state,day_max=end_day)
    cases=column(arr,2)
    recovery=column(arr,3)
    dead=column(arr,4)
    active=column(arr,5)
    cases_diff=np.diff(cases)
    recovery_diff=np.diff(recovery)
    dead_diff=np.diff(dead)
    active_diff=np.diff(active)
    
    cases_ddays=[get_doubling_s(cases_diff[i-1]/cases[i-1]) for i in range(start_day,end_day)]
    recovery_ddays=[get_doubling_s(recovery_diff[i-1]/recovery[i-1]) for i in range(start_day,end_day)]
    dead_ddays=[get_doubling_s(dead_diff[i-1]/dead[i-1]) for i in range(start_day,end_day)]
    active_ddays=[get_doubling_s(active_diff[i-1]/active[i-1]) for i in range(start_day,end_day)]
    
    cases_rate=[cases_diff[i-1]*100/cases[i-1] for i in range(start_day,end_day)]
    recovery_rate=[recovery_diff[i-1]*100/recovery[i-1] for i in range(start_day,end_day)]
    dead_rate=[dead_diff[i-1]*100/dead[i-1] for i in range(start_day,end_day)]
    active_rate=[active_diff[i-1]*100/active[i-1] for i in range(start_day,end_day)]
    
    
    x=column(arr,1)[range(start_day,end_day)]
    if type=="dead":    
        y1=dead[range(start_day,end_day)]
        y2=dead_diff[range(start_day-1,end_day-1)]
        y3=dead_ddays
        y4=dead_rate
    if type=="active":    
        y1=active[range(start_day,end_day)]
        y2=active_diff[range(start_day-1,end_day-1)]
        y3=active_ddays
        y4=active_rate
    if type=="cases":
        y1=cases[range(start_day,end_day)]
        y2=cases_diff[range(start_day-1,end_day-1)]
        y3=cases_ddays
        y4=cases_rate
    if type=="recovery":    
        y1=recovery[range(start_day,end_day)]
        y2=recovery_diff[range(start_day-1,end_day-1)]
        y3=recovery_ddays
        y4=recovery_rate
    #p1=go.Scatter(x=x,y=y1,name=state+" Cummulative",marker={'color': color,'line':dict(width=2)},mode="lines+markers")
    #p2=go.Bar(x=x,y=y2,name=state+" Daily Addition",marker={'color': color})
    p3=go.Scatter(x=x,y=y3,name=state,marker={'color': color,'line':dict(width=2)},mode="lines+markers",line_shape='spline')
    p4=go.Scatter(x=x,y=y4,name=state,marker={'color': color},mode="lines+markers",line_shape='spline')
    #fig.append_trace(p1,row=1,col=1)
    #fig.append_trace(p2,row=2,col=1)
    fig.add_trace(p3)
    #fig.append_trace(p4,row=2,col=1)
title="Doubling days for "+type+"."
fig.update_layout(height=400, width=900, title_text=title.title())
fig.write_html('index.html', auto_open=True)
