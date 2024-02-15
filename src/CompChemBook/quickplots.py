# -*- coding: utf-8 -*-
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def quickPlot(x = None, y = None, xlabel = None, ylabel = None, template = "simple_white", mode = "lines", show = "png"):
    if type(x[0]) != np.ndarray and type(x[0]) != list: # then x is not an array or list
        xplot = [x]
    else:
        try: 
            xplot = x # if already an array of arrays, then just keep it
        except:
            raise "You need to supply a list or array of floats or ints"
    if type(y[0]) != np.ndarray and type(y[0]) != list: # then y is not an array or list
        yplot = [y]
    else:
        try: 
            yplot = y # if already an array of arrays, then just keep it
        except:
            raise "You need to supply a list or array of floats or ints"
    
    #next, let us ensure we can iterate through x and y together
    if len(xplot) == 1:
        xplot = [xplot[0]]*len(yplot)
    elif len(xplot) != len(yplot):
        raise "your x values should be a list of length equal to y values, or a list of 1"
    
    # start the plotting
    qplot = make_subplots()
    
    
    for xi,yi in zip(xplot, yplot):
        if len(xi) != len(yi):
            raise "you do not have the same number of x and y points!"
        points = go.Scatter(x=xi, y = yi, mode = mode)
        qplot.add_trace(points)
    
    qplot.update_xaxes(title = xlabel)
    qplot.update_yaxes(title = ylabel)
    qplot.update_layout(template = template)
    if show != False:
        qplot.show(show)
    return qplot

def quickPlot2():
    return