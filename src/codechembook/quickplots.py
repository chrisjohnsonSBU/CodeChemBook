# -*- coding: utf-8 -*-
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#
# 1d plots
#
    
def quickXY(x = None, y = None, xlabel = None, ylabel = None, template = "simple_white", mode = "lines", show = "png"):
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

#this is a wrapper for quickXY, in case people want to use quickxy
def quickxy(x = None, y = None, xlabel = None, ylabel = None, template = "simple_white", mode = "lines", show = "png"):
    return quickXY(x = x, y = y, xlabel = xlabel, ylabel = ylabel, template = template, mode = mode, show = show)


def quickGrid(x = None, y = None, ncols = None, nrows = None, template = "simple_white"):
    # first make sure that we have lists of lists... 
    # so this first section makes sure that, if we get a single list, we put it in a list
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
    
    # now, create a grid
    if ncols == None and nrows == None:
        ncols = int(np.sqrt(len(xplot))) # number of colums is equal to the truncated square root of the 
        nrows = math.ceil(len(xplot)/ncols) # number of rows we will need
    elif ncols != None and nrows != None:
        if ncols*nrows < len(xplot):
            raise "ncols*nrows is not large enough"
    elif ncols != None:
        nrows = math.ceil(len(xplot)/ncols)
    else:
        ncols = math.ceil(len(xplot)/nrows)
    
    gplot = make_subplots(rows = nrows, cols = ncols)
    for i, xi in enumerate(xplot):
        trace = go.Scatter(x = xplot[i], y = yplot[i])
        
        # find the row and column number we are on
        row = int(i/ncols) + 1
        col = (i+1)%ncols
        
        #add the trace to those
        gplot.add_trace(trace, row = row, col = col)
    
    gplot.update_layout(template = template)
    return gplot



