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
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

fig, ax = plt.subplots(figsize=(15, 8))
colors = dict(zip(
    ['Tamilnadu', 'Telangana', 'Maharastra', 'Kerala',
     'Delhi', 'Gujarat', 'Rajasthan'],
    ['#adb0ff', '#ffb3ff', '#90d595', '#e48381',
     '#aafbff', '#f7bb5f', '#eafb50']))

df=pd.read_csv("confirmed.csv",na_values='-')
df.rename(columns={'TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan"},inplace=True)

df_Deaths=pd.read_csv("deceased.csv",na_values='-')
df_Deaths.rename(columns={'TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan"},inplace=True)


df2=df.loc[:,df.columns[1:]]
df2=df2.cumsum(axis=0)
df2.fillna(0,inplace=True)


def draw_barchart(index):
    states=np.array(['Tamilnadu','Telangana','Maharastra','Kerala','Delhi','Gujarat','Rajasthan'])
    ax.clear()
    cases=df2[states].loc[index]
    sort=np.argsort(cases).to_list()
    states=states[sort]
    cases=cases[sort]
    date=df["date"].loc[index]
    for i, (value, name) in enumerate(zip(cases, states)):
        
        ax.text(value+1, i,     int(value),           ha='left',size=15)
        ax.text(value, i,     name,            ha='right',size=15)
    ax.barh(states,cases,color=[colors[state] for state in states])
    ax.text(1, 0.4, "Date: "+str(date), transform=ax.transAxes, color='#777777', size=25, ha='right', weight=800)
    ax.text(0, 1.06, 'Cases', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    plt.box(False)
    
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(0, 28),interval=500,repeat=False)
HTML(animator.to_jshtml()) 
animator.save('animation.gif', writer='imagemagick', fps=2)