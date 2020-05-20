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

df_Cases=pd.read_csv("confirmed.csv",na_values='-')
df_Cases.rename(columns={'TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan"},inplace=True)

df_Deaths=pd.read_csv("deceased.csv",na_values='-')
df_Deaths.rename(columns={'TN':'Tamilnadu','TG':'Telangana','MH':"Maharastra","KL":"Kerala","DL":"Delhi","GJ":"Gujarat","RJ":"Rajasthan"},inplace=True)


df2d=df2d.cumsum(axis=0)
df2d.fillna(0,inplace=True)


def draw_curve(date):
    states=np.array(['Tamilnadu','Telangana','Maharastra','Kerala','Delhi','Gujarat','Rajasthan'])
    ax.clear()
    for state in states:
        cases=df2[states].loc[index]
        deaths=df2d[deaths].loc[index]
        ax.margins(0, 0.01)
        ax.grid(which='major', axis='x', linestyle='-')
    
animator = animation.FuncAnimation(fig, draw_barchart, frames=range(0, 28),interval=500,repeat=False)
HTML(animator.to_jshtml()) 
animator.save('animation.gif', writer='imagemagick', fps=2)