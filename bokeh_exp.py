#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 21:12:24 2020

@author: gururaj
"""

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import show, output_file

# create data
products = ['python', 'pypy', 'jython']
customers = ['Cust 1', 'Cust 2','Cust 3']
colours = ['red', 'blue','green']
data = {
    'products': products,
    'Cust 1': [200, 850, 400],
    'Cust 2': [600, 620, 550],
    'Cust 3': [400, 420, 440],
}


source = ColumnDataSource(data)
p = figure(y_range=products)

p.hbar_stack(customers, y='products', height=0.5, source=source, color=colours)

show(p)
#output_file("stacked.html")