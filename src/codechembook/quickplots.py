# -*- coding: utf-8 -*-
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import json

#
# 1d plots
#

def process_output(plot, output):
    # Plot the figure to the specified output
    if output in pio.renderers.keys():
        plot.show(output)
    elif output == "default":
        plot.show()
    elif output is None:
        pass # no need to do anything
    else:
        print("Enter 'png' to plot in Spyder or 'browser' for the browser.")
        print("Use 'None' to show nothing and return the figure object.")
    
    
def quickScatter(x = None, y = None, xlabel = None, ylabel = None, name = None, template = "simple_white", mode = None, output = "png"):
    """
    Quickly plot one xy trace in plotly.

    Optional Args:
        x (ndarray or list of ndarray): the x coordinates to plot
        y (ndarray or list of ndarray): the y coordinates to plot
        xlabel (string):                x axis title
        ylabel (string):                y axis title
        mode (string):                  plot using 'lines'(default) or 'markers'
        template (string):              which plotly template to use (default simple_white)
        show (string):                  output to Spyder plot window ('png', 'svg')
                                           or browser ('browser')
                                           or the 'normal' show behavior ('default')
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
    if name is None:
        name = ['' for x in xplot]
    for xi,yi,ni in zip(xplot, yplot, name):
        if len(xi) != len(yi):
            raise "you do not have the same number of x and y points!"
        if mode is None:
            points = go.Scatter(x=xi, y = yi, name = ni)
        elif "lines" in mode or "markers" in mode:
            points = go.Scatter(x=xi, y = yi, mode = mode, name = ni)
        else:
            raise "please enter either 'lines', 'markers', 'lines+markers', or None for mode"
        qplot.add_trace(points)
    
    qplot.update_xaxes(title = str(xlabel)) # cast as string to handle numeric values if passed
    qplot.update_yaxes(title = str(ylabel))
    
    # confirm that the specified template is one that we have
    if template not in pio.templates.keys():
        print('Invalid template specified, defaulting to simple_white.')
        template = 'simple_white'
    qplot.update_layout(template = template)
    
    process_output(qplot, output) # check to see how we should be outputting this plot
    
    return qplot



def quickGrid(x = None, labels = None, template = "simple_white", output = "png"):
    '''
    Takes a series of array and plots correlation between them...
    
    Work in progress.  To do:
        place label in the diagonals
        add fitting
        check to make sure all arrays are the same length

    Parameters
    ----------
    x : list of ndarrays or lists of numbers, optional
        This is the set of data to check correlations for. The default is None.
    labels : list of strings, optional
        If you wish to specify labels for the arrays, you can do it here. The default is None.
    template : string, optional
        string that corresponds to a named plotly template. The default is "simple_white".

    Raises
    ------
    
        DESCRIPTION.

    Returns
    -------
    gplot : Plotly figure object
        The figure object showing correlations between plots.

    '''
    # first make sure that we have lists of lists... 
    # so this first section makes sure that, if we get a single list, we put it in a list
    if type(x[0]) != np.ndarray and type(x[0]) != list: # then x is not an array or list
        xplot = [x]
    else:
        try: 
            xplot = x # if already an array of arrays, then just keep it
        except:
            raise "You need to supply a list or ndarray of floats or ints"
    
    narrays = len(x)
    gplot = make_subplots(cols = narrays, rows = narrays) # make a square plot
    
    for j, x1 in enumerate(x): # go through each y array
        for i, x2 in enumerate(x): # go through each x array
            if i == j:
                pass
            else:
                gplot.add_scatter(x = x1, y = x2, 
                                  showlegend=False, 
                                  row = i+1, col = j+1)
                try:
                    ylabel = labels[j]
                except:
                    ylabel = f"y-series {j}"
                try:
                    xlabel = labels[i]
                except:
                    xlabel = f"x-series {i}"
                gplot.update_xaxes(title = xlabel, row = i+1, col = j+1)
                gplot.update_yaxes(title = ylabel, row = i+1, col = j+1)
                
    gplot.update_layout(template = template)

    process_output(gplot, output)
    
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
    [bin_centers, bin_counts]: list of ndarray
        a list containing arrays holding the centers of bins and their corresonding counts
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


def quickHist(x, 
              xlabel = None, ylabel = None, 
              limits = None, nbins = None, width = None, 
              mode = "counts", buffer = 0.05, 
              template = "simple_white",
              output = "png"):
    """
    
    
    Parameters
    ----------
    x : list or ndarray
        The collection of numbers to be displayed as a histogram.
    xlabel : string, optional
        The title for the x-axis. The default is None.
    ylabel : string, optional
        The title for the y-axis. The default is None.
    limits : int or float, optional
        The upper and lower limits of the binning. The default is None, which means it will be determined by the limits of the data.
    nbins : int, optional
        Number of bins that you wish. If specified, then the range of data is divided by this number to find the bin widths
    width : int or float, optional
        The width of the bins desired.  If specified, then they are applied, starting at the lowest part of the range, upward. The default is None.
    mode : string, optional
        This specifies if counts or frequency is desired on the y-axis. The default is "counts".
    buffer : int or float, optional
        The fraction of the total range that is added to the left and right side of the x-axis. The default is 0.05.
    template : TYPE, optional
        Any valid name for a Plotly template. The default is "simple_white".
    output : string or Nonetype, optional
        Any valid key for showing a plot in plotly. Common options include "png", "svg", or "browser"

    Returns
    -------
    A plotly figure object.  In this object, the histogram is rendered as a bar chart.

    """
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
    
    process_output(hist, output)
    
    return hist



def quickSubs(childPlots = None, 
              layoutfig = None, nrows = None, ncols = None,
              output = "png"):
    '''
    Takes an arbitrary number of Plotly figure objects, and plots them together on a single Plotly figure. 
    Each figure object supplied is turned into a subplot in the Figure. 

    Parameters
    ----------
    childPlots : list of Plotly figure objects, optional
        These are the plots to be added to the new subplot figure. The default is None.
    layoutfig : Plotly figure object, optional
        Provides the figure object from which to take the formatting for the new figure. If None, then the last plot in the child plot list is used. The default is None.
    nrows : int, optional
        Specifies the number of rows to use in the new figure. The default is None.
    ncols : int, optional
        Specifies the number of columns to use in the new figure. The default is None.

    Returns
    -------
    newfig : Plotly figure object
        The new figure object, containing subplots of all the supplied child plots.

    '''
    if nrows == None and ncols == None: # we have specified nothing about the grid to use
        ncols = math.ceil(len(childPlots)**0.5)
        nrows = math.ceil(len(childPlots)/ncols)
    elif nrows == None: # we have only specified the number of columns to use
        nrows = math.ceil(len(childPlots)/ncols)
    elif ncols == None: # we have only specified the number of rows to use
        ncols = math.ceil(len(childPlots)/nrows)
    
    newfig = make_subplots(rows = nrows, cols = ncols)
    newfigdict = json.loads(newfig.to_json()) # add stuff to this one. <-- need to do this, because we will use the 
    # print(newfigdict)
    # print('end of first newfigdict \n')
    #print(nrows, ncols)
    
    #figdict = {"data":[], "layout":{}}
    
    for i, cp in enumerate(childPlots):
        
        if i == 0: # do not with to append the number
            label = ''
        else:
            label = i+1
        
        # specify which row and column we are working on
        row = int(i/ncols)+1
        col = int(i%ncols)+1
        
        # now parse the figure...
        oldfigdict = json.loads(cp.to_json()) 
        for entry in oldfigdict["data"]: # get the indiviual dictionaries in the data list
            entry["xaxis"] = f"x{label}"
            entry["yaxis"] = f"y{label}"
            newfigdict["data"].append(entry) # add modified version to the new figure
        # print(oldfigdict)
        # print('\n')
        # print(i, '\nbefore')
        # print(oldfigdict['layout']["xaxis"])       
        # oldfigdict["layout"][f"xaxis{label}"] = oldfigdict["layout"]["xaxis"] #rename x-axis key
        # oldfigdict["layout"][f"yaxis{label}"] = oldfigdict["layout"]["yaxis"] #rename y-axis key
        
        # oldfigdict["layout"][f"xaxis{label}"]["anchor"] = f"y{label}"
        # oldfigdict["layout"][f"yaxis{label}"]["anchor"] = f"x{label}"

        temp_x_domain = newfigdict["layout"][f"xaxis{label}"]["domain"]
        temp_y_domain = newfigdict["layout"][f"yaxis{label}"]["domain"]

        newfigdict["layout"][f"xaxis{label}"] = oldfigdict["layout"][f"xaxis"]
        newfigdict["layout"][f"yaxis{label}"] = oldfigdict["layout"][f"yaxis"]
        newfigdict["layout"][f"xaxis{label}"]['domain'] = temp_x_domain
        newfigdict["layout"][f"yaxis{label}"]['domain'] = temp_y_domain
        newfigdict["layout"][f"xaxis{label}"]["anchor"] = f"y{label}" # the anchor for x is relative to y-position
        newfigdict["layout"][f"yaxis{label}"]["anchor"] = f"x{label}" # the anchor for y is relative to x-position
        # newfigdict["layout"][f"xaxis{label}"] = oldfigdict["layout"][f"xaxis{label}"]
        # newfigdict["layout"][f"yaxis{label}"] = oldfigdict["layout"][f"yaxis{label}"]
        # print(i, '\nafter')
        # print(oldfigdict['layout'][f"xaxis{label}"])
    # set up the layout....
    if layoutfig == None:
        layoutfig = childPlots[0]
    layoutfigdict = json.loads(layoutfig.to_json())
    for key in layoutfigdict["layout"]:
        if "axis" not in key: #make sure we are not editing axes, only everything else. 
            newfigdict["layout"][key] = layoutfigdict["layout"][key]
                
    newfigjson = json.dumps(newfigdict)
    # print(newfigdict)
    newfig = pio.from_json(newfigjson)
    
    process_output(newfig, output)
    
    return newfig

# quickbar

# quick box

# quick violin

# quick sankey

# quick pie

# quick 