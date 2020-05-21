#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 16:54:16 2020

@author: gururaj
"""

import numpy as np

import pandas as pd
import sys
from scipy import optimize
import matplotlib.pyplot as plt
from impfuncs import *

start_day=30
end_day=75

dts=getDates(start_day,end_day)

x_ext_pts=range(0,end_day)
arr=load_Data(start_day=start_day,day_max=55,state="India")
x_pts=column(arr,0)
[x0_cases, r_cases], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,1), p0=(column(arr,1)[0], 0.1),method="lm")
[x0_recovered, r_recovered], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,2), p0=(column(arr,2)[0], 0.1),method="lm")
[x0_dead, r_dead], pcov  = optimize.curve_fit(exp_growth, x_pts, column(arr,3), p0=(column(arr,3)[0],0.1),method="lm")
    
fitted_cases = exp_growth(x_ext_pts, x0_cases, r_cases)
fitted_recovered = exp_growth(x_ext_pts, x0_recovered, r_recovered)
fitted_dead = exp_growth(x_ext_pts, x0_dead, r_dead)

fitted_active=[]
    
for i in range(len(fitted_cases)):
    act=fitted_cases[i]-(fitted_recovered[i]+fitted_dead[i])
    fitted_active.append(act)
    
    


plt.semilogy(x_pts, column(arr,1), 'bo',label="Data Cases")
plt.semilogy(fitted_cases, 'b-',label=" Fit Cases")

plt.semilogy(x_pts, column(arr,2), 'go',label=" Data Recovery")
plt.semilogy(fitted_recovered, 'g-',label=" Fit Recovery")

plt.semilogy(x_pts, column(arr,3), 'ro',label=" Data Deaths")
plt.semilogy(fitted_dead, 'r-',label=" Fit Deaths")

plt.semilogy(x_pts, column(arr,4), 'ko',label=" Data Active")
plt.semilogy(fitted_active, 'k-',label=" Fit Active")


plt.xticks(range(0,end_day,5),dts[range(0,end_day,5)])
plt.grid(True)
plt.xticks(rotation=90)
plt.legend(frameon=False)
plt.title("Covid data and projection for India \nFitted from "+dts[0]+" and extrapolated upto "+dts[len(dts)-1])
plt.tight_layout()

plt.show()

print("Fitting data from "+dts[0])
print("Growth Parameters:\n")
print("Cases rate:"+str(r_cases))
print("Recovery rate:"+str(r_recovered))
print("Dead rate:"+str(r_dead))



t=28

printStats(arr, dts, t)
printPredictions(fitted_cases,fitted_recovered,fitted_dead,fitted_active,dts,t)