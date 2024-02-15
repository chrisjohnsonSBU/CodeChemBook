# -*- coding: utf-8 -*-
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

#
# 1d plots
#
    
def quickXY(x = None, y = None, xlabel = None, ylabel = None, template = "simple_white", mode = "lines", show = "png"):
    """
    Quickly plot one xy trace in plotly.

    Optional Args:
        x (ndarray or list of ndarray): the x coordinates to plot
        y (ndarray or list of ndarray): the y coordinates to plot
        xlabel (string):                x axis title
        ylabel (string):                y axis title
        mode (string):                  plot using 'lines'(default) or 'markers'
        template (string):              which plotly template to use (default simple_white)
        show (string):                  output to Spyder plot window ('png') (default)
                                           or browser ('browser')
                                           or 'None' for no output
                    
    Returns:
        qplot (plotly figure object): the figure object created
    """
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
    
    qplot.update_xaxes(title = str(xlabel)) # cast as string to handle numeric values if passed
    qplot.update_yaxes(title = str(ylabel))
    
    # confirm that the specified template is one that we have
    if template not in pio.templates.keys():
        print('Invalid template specified, defaulting to simple_white.')
        template = 'simple_white'
    qplot.update_layout(template = template)
    
    # Plot the figure to the specified output
    if show in pio.renderers.keys():
        qplot.show(show)
    elif show == 'None':
        return qplot
    else:
        print("Enter 'png' to plot in Spyder or 'browser' for the browser.")
        print("Use 'None' to show nothing and return the figure object.")
    return qplot

#this is a wrapper for quickXY, in case people want to use quickxy
def quickxy(x = None, y = None, xlabel = None, ylabel = None, template = "simple_white", mode = "lines", show = "png"):
    return quickXY(x = x, y = y, xlabel = xlabel, ylabel = ylabel, template = template, mode = mode, show = show)
    