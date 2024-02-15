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

def quickBin(x, limits = None, nbins = None, width = None):
    '''
    Accepts a collection of numbers that can be coerced into a numpy array, and bins these numbers. 
    If none of keyword arguments are specified, this results in a Freeman-Diaconis binning.
    
    Parameters
    ----------
    x : collection of numbers
        must be coercable into numpy arrays
    limits : float, optional
        the upper and lower limits of the binning. The default is None, which means it will be determined by the limits of the data.
    nbins : int, optional
        the number of bins that are desired. If a float is provided, then it will be converted to an int. The default is None, which means this is automatically determined.
    width : float, optional
        the width of the bins. The default is None, which means it will be automatically determined.

    Returns
    -------
    list
        DESCRIPTION.

    '''
    try:
        x = np.array(x)
    except:
        raise("the data need to be in a form that can be converted to a numpy array")
    # we need to start by finding the limits and the bin width
    
    # we can start by getting the iqr, which might prove useful for formatting as well
    q75, q25 = np.percentile(x, [75,25]) # find the places for the inner quartile
    iqr = q75 - q25 # calculate the inner quartile range
    
    
    # first thing: make sure we have a range to work with...
    if limits == None: # then set the limis as the min and max of x
        limits = [min(x), max(x)]
        
    if nbins != None and width != None:
        raise("Specify either the number of bins, or the bin width, but not both.")
    
    # check to see if the width of the bins was specified...
    if width == None and nbins == None: # then use the Freedman-Diaconis method to calculate bins
        width = 2*iqr*len(x)**(-1/3)
    
    if nbins != None and width == None: # use the number of bins to determine the width
        width = abs(limits[1] - limits[0]) / int(nbins)
    
    # the only other option is that width was directly specified.... 
    # so now we are ready to go...
    
    # Define the bin edges using numpy's arange function
    bin_edges = np.arange(limits[0], limits[1] + width, width)
    
    # Use numpy's histogram function to bin the data, using the bin edges we have calculated
    bin_counts, _ = np.histogram(x, bins=bin_edges)
    
    # Calculate the bin centers by averaging each pair of consecutive edges
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    
    return [bin_centers, bin_counts]


def quickHist(x, xlabel = None, ylabel = None, limits = None, nbins = None, width = None, mode = "counts", buffer = 0.05, template = "simple_white"):
    # we will want the iqr for calculating the buffer space on the plot
    q75, q25 = np.percentile(x, [75,25]) # find the places for the inner quartile
    iqr = q75 - q25 # calculate the inner quartile range
    
    bin_centers, bin_counts = quickBin(x, limits = limits, nbins = nbins, width = width)
    
    # now we can plot a bar chart that looks like a histogram...
    hist = make_subplots()
    if mode == "counts":
        bars = go.Bar(x = bin_centers, y = bin_counts)
        hist.update_yaxes(title = "counts")
    if mode == "freq": # we are doing frequency
        bars = go.Bar(x = bin_centers, y = bin_counts/np.sum(x))
        hist.update_yaxes(title = "frequency")
    
    hist.add_trace(bars)
    hist.update_traces(marker = dict(line = dict(width = 1, color = "black")))
    
    hist.update_xaxes(title = xlabel, range = [min(bin_centers) - buffer*iqr, max(bin_centers) + buffer*iqr])
    
    hist.update_layout(bargap = 0, template = template)
    hist.show("png")
    return(hist)

