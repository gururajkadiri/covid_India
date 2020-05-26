#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 07:55:21 2020

@author: gururaj
"""

from impfuncs import *
from plotly.subplots import make_subplots
import plotly.graph_objects as go
fig = make_subplots(rows=4, cols=1,shared_xaxes=True, 
                    vertical_spacing=0.02)
#fig=go.Figure()

import matplotlib.pyplot as plt


start_day=25
end_day=68

dfs=populate_dfs()    


#fig,(ax1,ax2,ax3)=plt.subplots(nrows=2,ncols=1,sharex=True)
state="India"

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
y_dead=dead[range(start_day,end_day)]
y_dead_diff=dead_diff[range(start_day-1,end_day-1)]
y_dead_ddays=dead_ddays
y_dead_rate=dead_rate
y_active=active[range(start_day,end_day)]
y_active_diff=active_diff[range(start_day-1,end_day-1)]
y_active_ddays=active_ddays
y_active_rate=active_rate
y_cases=cases[range(start_day,end_day)]
y_cases_diff=cases_diff[range(start_day-1,end_day-1)]
y_cases_ddays=cases_ddays
y_cases_rate=cases_rate
y_recovery=recovery[range(start_day,end_day)]
y_recovery_diff=recovery_diff[range(start_day-1,end_day-1)]
y_recovery_ddays=recovery_ddays
y_recovery_rate=recovery_rate

p_cases=go.Scatter(x=x,y=y_cases,name="Cases",marker={'color': "blue",'line':dict(width=2)},mode="lines+markers")
p_recovery=go.Scatter(x=x,y=y_recovery,name="Recovered",marker={'color': "green",'line':dict(width=2)},mode="lines+markers")
p_dead=go.Scatter(x=x,y=y_dead,name="Dead",marker={'color': "red",'line':dict(width=2)},mode="lines+markers")
p_active=go.Scatter(x=x,y=y_active,name="Active",marker={'color': "black",'line':dict(width=2)},mode="lines+markers")

p_cases_diff=go.Bar(x=x,y=y_cases_diff,name="Daily cases",marker={'color': "blue"})
p_recovery_diff=go.Bar(x=x,y=y_recovery_diff,name="Daily recovered",marker={'color': "green"})
p_dead_diff=go.Bar(x=x,y=y_dead_diff,name="Daily deaths",marker={'color': "red"})
p_active_diff=go.Bar(x=x,y=y_active_diff,name="Daily active",marker={'color': "black"})

p_cases_ddays=go.Scatter(x=x,y=y_cases_ddays,name="cases doubling days" ,marker={'color': "blue",'line':dict(width=2)},mode="lines+markers")
p_recovery_ddays=go.Scatter(x=x,y=y_recovery_ddays,name="Recovered doubling days",marker={'color': "green",'line':dict(width=2)},mode="lines+markers")
p_dead_ddays=go.Scatter(x=x,y=y_dead_ddays,name="Dead doubling days",marker={'color': "red",'line':dict(width=2)},mode="lines+markers")
p_active_ddays=go.Scatter(x=x,y=y_active_ddays,name="Active doubling days",marker={'color': "black",'line':dict(width=2)},mode="lines+markers")

p_cases_rate=go.Scatter(x=x,y=y_cases_rate,name="Cases inc rate",marker={'color': "blue",'line':dict(width=2)},mode="lines+markers")
p_recovery_rate=go.Scatter(x=x,y=y_recovery_rate,name="Recovery inc rate",marker={'color': "green",'line':dict(width=2)},mode="lines+markers")
p_dead_rate=go.Scatter(x=x,y=y_dead_rate,name="Death inc rate",marker={'color': "red",'line':dict(width=2)},mode="lines+markers")
p_active_rate=go.Scatter(x=x,y=y_active_rate,name="Active inc rate",marker={'color': "black",'line':dict(width=2)},mode="lines+markers")


fig.append_trace(p_cases,row=1,col=1)
fig.append_trace(p_recovery,row=1,col=1)
fig.append_trace(p_dead,row=1,col=1)
fig.append_trace(p_active,row=1,col=1)

fig.append_trace(p_cases_diff,row=2,col=1)
fig.append_trace(p_recovery_diff,row=2,col=1)
fig.append_trace(p_dead_diff,row=2,col=1)
fig.append_trace(p_active_diff,row=2,col=1)

fig.append_trace(p_cases_rate,row=3,col=1)
fig.append_trace(p_recovery_rate,row=3,col=1)
fig.append_trace(p_dead_rate,row=3,col=1)
fig.append_trace(p_active_rate,row=3,col=1)

fig.append_trace(p_cases_ddays,row=4,col=1)
fig.append_trace(p_recovery_ddays,row=4,col=1)
fig.append_trace(p_dead_ddays,row=4,col=1)
fig.append_trace(p_active_ddays,row=4,col=1)


fig.update_layout(height=900, width=900,title="Consolidated plots for "+state)
fig.update_yaxes(title_text="Cummulative", row=1, col=1)
fig.update_yaxes(title_text="Daily Addition", row=2, col=1)
fig.update_yaxes(title_text="Daily Addition %", row=3, col=1)
fig.update_yaxes(title_text="Doubling days", row=4, col=1)
fig.write_html('index.html', auto_open=True)
