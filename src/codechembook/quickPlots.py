# -*- coding: utf-8 -*-
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import json
import inspect


#
# supporting utilities
#

def _get_name_two_calls_ago(x,):
    n = None
    callers_locals = inspect.currentframe().f_back.f_back.f_locals
    for name, value in callers_locals.items():
        if value is x:
            n =  f"{name}" 
    if n is None: # this is likely only to happen when the variable was a literal (and so anonymous)
        n = "untitled"
    return n

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
  
#
# 2d plots
#
    
def quickScatter(x = None, y = None, xlabel = None, ylabel = None, name = None, template = "simple_white", mode = None, output = "png"):
    """
    Quickly plot (x,y) data as a scatter plot.

    Users can supply single arrays or lists for x- and y-values, a single set of x-values and multiple sets of
    y-values, or multiple sets of x-values and y-values.  If multiple sets of y-values, name and mode can be
    lists of len(y).

    Optional Args:
        x (ndarray or list/ndarray of ndarray): x-values to plot.
        y (ndarray or list/ndarray of ndarray): y-values to plot.
        xlabel (str or list of str):            x-axis title. (default: None (use variable name))
        ylabel (str or list of str):            y-axis title. (default: None (use variable name))
        name (str or list of str):              Names of traces. (default: '')
        mode (str or list of str):              Trace appearance for Plotly Scatter object. (default: None (automatically determine))
        template (str):                         Plotly template for formatting Figure. (default: 'simple_white')
        show (str):                             Method to show the plot. (default: "png", options: valid Plotly output types, None for no output)

    Returns:
        qplot (plotly figure object): the figure object created
    """
    # if the user did not supply axis names, then we can just use the variable names
    if xlabel is None:
        xlabel = _get_name_two_calls_ago(x)
    if ylabel is None:
        ylabel = _get_name_two_calls_ago(y)

    # figure out what the user gave us for x and y
    if isinstance(x, list) or isinstance(x, np.ndarray):
        if all(isinstance(xi, list) or isinstance(xi, np.ndarray) for xi in x):
            xplot = x
        elif all(isinstance(xi, float) or isinstance(xi, int) for xi in x):
            xplot = [x]
        else:
            print("You need to supply a list or array of floats or ints for x")
            return
    
    if isinstance(y, list) or isinstance(y, np.ndarray):
        if all(isinstance(yi, list) or isinstance(yi, np.ndarray) for yi in y):
            yplot = y
        elif all(isinstance(yi, float) or isinstance(yi, int) for yi in y):
            yplot = [y]
        else:
            print("You need to supply a list or array of floats or ints for y")
            return

    # figure out what the user gave us for name
    if name is None:
        name = ['' for y in yplot]
    elif isinstance(name, str):
        if len(yplot) > 1:
            tempname = name
            name = [f'{tempname}{i}' for i, y in enumerate(yplot)]
        if len(yplot) == 1:
            name = [name]
    elif isinstance(name, list):
        if len(name) != len(yplot):
            print("your list of names is a different length than your list of y values")
            return
    else:
        print("there was a problem with your name argument")
        return

    # ensure that we have the same number of items for x and y
    if len(xplot) == 1:
        xplot = [xplot[0]] * len(yplot)
    elif len(xplot) != len(yplot):
        raise "your x values should be a list or array of length equal to y values, or a list or array of 1"

    # start the plotting
    qplot = make_subplots()
        
    # loop through the provided lists and add them to the plot
    for xi,yi,ni in zip(xplot, yplot, name):
        if len(xi) != len(yi):
            raise "you do not have the same number of x and y points!"
        if mode is None:
            points = go.Scatter(x = xi, y = yi, name = ni)
        elif "lines" in mode or "markers" in mode:
            points = go.Scatter(x = xi, y = yi, mode = mode, name = ni)
        else:
            raise "please enter either 'lines', 'markers', 'lines+markers', or None for mode"
        qplot.add_trace(points)

    # set up the axes
    qplot.update_xaxes(title = str(xlabel)) # cast as string to handle numeric values if passed
    qplot.update_yaxes(title = str(ylabel))

    # confirm that the specified template is one that we have
    if template not in pio.templates.keys():
        print('Invalid template specified, defaulting to simple_white.')
        template = 'simple_white'
    qplot.update_layout(template = template)

    process_output(qplot, output) # check to see how we should be outputting this plot

    return qplot

def quickHist(x, 
              xlabel = None, ylabel = None, 
              limits = None, nbins = None, width = None, 
              mode = "counts",
              orientation = "vertical", # can also be "horizontal"
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
    # if the user did not supply axis names, then we can just use the variable names
    if xlabel is None:
        xlabel = _get_name_two_calls_ago(x)


    # we will want the iqr for calculating the buffer space on the plot
    q75, q25 = np.percentile(x, [75,25]) # find the places for the inner quartile
    iqr = q75 - q25 # calculate the inner quartile range
    
    #default to plotting counts, I guess
    bar_centers, bar_lengths = quickBin(x, limits = limits, nbins = nbins, width = width)
    
    if "counts" in mode:
        # for the ylabel, we can use the mode, if no label was yet supplied. 
        if ylabel is None:
            ylabel = "counts"

    # adjust if we need to change the counts to frequency
    if "freq" in mode: # then we are doing frequency
        bar_lengths = bar_lengths / np.sum(x)
        
        # for the ylabel, we can use the mode, if no label was yet supplied. 
        if ylabel is None:
            ylabel = "frequency"

    # work out a buffer for the bars on either side
    # calculate the width of bars
    bar_separation = bar_centers[1] - bar_centers[0] # quickBin should always have adjacent bars
    # calculate a buffer based in iqr
    iqr_buffer = 0.05*iqr
    # take whatever is larger
    buffer = max([bar_separation, iqr_buffer])

    # now we can plot a bar chart that looks like a histogram...
    hist = make_subplots()
    
    if "v" in orientation:
        hist.add_bar(x = bar_centers, y = bar_lengths)
    elif "h" in orientation:
        hist.add_bar(x = bar_lengths, y = bar_centers)

    
    hist.update_traces(marker = dict(line = dict(width = 1, color = "black")))
    
    hist.update_xaxes(title = xlabel, range = [min(bar_centers) - buffer, max(bar_centers) + buffer])
    hist.update_yaxes(title = ylabel, range = [0, max(bar_lengths)*1.02])
    hist.update_layout(bargap = 0, template = template)
    
    process_output(hist, output)
    
    return hist

def plotFit(fit, 
            resample = 10, 
            residual = False, 
            components = False, 
            confidence = 0, 
            xlabel = None, 
            ylabel = None, 
            template = 'simple_white',
            output = 'png'):
    """
    Plot the result of a 1d fit using lmfit
    
    Required Args:
        fit (lmfit result object): the result of a fit using lmfit
        
    Optional Args:
        resample (int):    increase the density of points on the x axis by N 
                           times for a smoother model fit curve (default: 10)
        residual (bool):   plot the residual (default: False)
        components (bool): plot the individual components of the model (default: False)
        confidence (int):  plot the confidence interval of the fit (N-sigma) (default: 0)
                           where N = 0 (default), 1, 2, etc. (default: 0)
        xlabel (string):   x axis title (default: None)
        ylabel (string):   y axis title (default: None)
        template (string): which plotly template to use (default: 'simple_white')
        output (string):   output to Spyder plot window ('png', default) 
                           or browser ('browser')
                           or None for no output

    Returns:
        fig (plotly figure object): the figure object created
    """
    
    # Just making some variables for convenience
    # First figure out what the independent variable name(s) is(are)
    independent_vars = fit.model.independent_vars

    # The x data has to be the same for all the independent variables, so
    # so get it from the first one in the list for safety
    xdata = fit.userkws[independent_vars[0]]
    ydata = fit.data
    
    # Resampling the fit so that it looks smooth to the eye
    smoothx = np.linspace(xdata.min(), xdata.max(), len(xdata)*resample)

    # Need to handle the fact that there may be multiple names for the 
    # independent variable
    kwargs = {}
    for independent_var in independent_vars:
        kwargs[independent_var] = smoothx
    smoothy = fit.eval(**kwargs)
    
    # If we are plotting the residual, then we need two subplots
    if residual: # will work as long as this is not False, 0, empty list, etc
        row_heights = [0.8, 0.2] # this is the default
        if residual == 'scaled':
            row_heights = [np.max(ydata) - np.min(ydata) , np.max(fit.residual) - np.min(fit.residual)]

        fig = make_subplots(rows = 2, 
                            cols = 1, 
                            shared_xaxes = True, 
                            row_heights = row_heights,
                            vertical_spacing = 0.05)
    else:
        fig = make_subplots()

    # If we are plotting the confidence interval, then plot +/- N * 1-sigma 
    # and fill between the two curves
    if confidence != 0 and type(confidence) == int:
        fig.add_scatter(x = smoothx, 
                        y = smoothy + confidence * fit.eval_uncertainty(**kwargs), 
                        mode = 'lines',
                        line = {'color': 'lightpink', 'width': 0},
                        row = 1, col = 1)
        fig.add_scatter(x = smoothx, 
                        y = smoothy - confidence * fit.eval_uncertainty(**kwargs), 
                        mode = 'lines',
                        line = {'color': 'lightpink', 'width': 0},
                        row = 1, col = 1,
                        fill = 'tonexty')
    
    # If we are plotting the individual components, go ahead and plot them first
    if components == True:
        
        # Generate the components resampled to the smooth x array
        comps = fit.eval_components(**kwargs)
        # Loop through the components and plot each one
        for comp in comps:
            fig.add_scatter(x = smoothx, 
                            y = comps[comp], 
                            line = {'dash': 'dot', 'color':'grey'},
                            row = 1, col = 1) 
    
    # Plot the raw data
    fig.add_scatter(x = xdata, 
                    y = ydata, 
                    mode = 'markers', 
                    name = 'Data', 
                    legendrank = 1, 
                    marker = {'color': 'blue', 'size': 8},
                    line = {'color': 'blue', 'width' : 8},
                    row = 1, col = 1)

    # Plot the fit curve
    fig.add_scatter(x = smoothx, 
                    y = smoothy, 
                    mode = 'lines', 
                    name = 'Best Fit', 
                    legendrank = 2, 
                    line = {'color': 'red'},
                    row = 1, col = 1)

    # If we are doing residuals, plot the residual
    if residual:
        fig.add_scatter(x = xdata, 
                        y = -1*fit.residual, # we need to multiply this by -1, to get the 'expected' behavior of data - fit. 
                        mode = 'markers+lines', 
                        name = 'Residual', 
                        line = {'color': 'black', 'width':1},
                        marker = {'color': 'black', 'size':2},
                        showlegend = False,
                        row = 2, col = 1)
        
        # Optionally plot the confidence interval of the residual
        if confidence != 0 and type(confidence) == int:
            
            fig.add_scatter(x = smoothx, 
                            y = confidence * fit.eval_uncertainty(**kwargs), 
                            mode = 'lines',
                            line = {'color': 'gray', 'width': 0},
                            row = 2, col = 1)
            fig.add_scatter(x = smoothx, 
                            y = -1 * confidence * fit.eval_uncertainty(**kwargs), 
                            mode = 'lines',
                            line = {'color': 'gray', 'width': 0},
                            row = 2, col = 1,
                            fill = 'tonexty')
        # Limit the ticks on the Residual axis so that it is readable
        residual_lim = np.max(np.abs(fit.residual)) * 1.05
        fig.update_yaxes(title = 'Residual', 
                         range = [-residual_lim, residual_lim], 
                         nticks = 3, zeroline = True, row = 2)
        
        #fig.update_yaxes(title = 'Residual', row = 2)


    
    # Update the layout
    fig.update_layout(template = template, showlegend = False)
    
    # Flag the user if the fit did not finish successfully
    fig_full = fig.full_figure_for_development()
    if fit.ier not in (1, 2, 3, 4):
        print(fit.result.lmdif_message)

        # find min max of x and y and average instead
        fig.add_annotation(x = (np.max(xdata) - np.min(xdata))/2,
                           y = (np.max(ydata) - np.min(ydata))/2,
                           text = 'Fit not converged.\nCheck command line for info.')

    # If the user supplied an x axis label, add it
    if xlabel is None: # we can default to the name in the model
        xlabel = fit.model.independent_vars[0]
    fig.update_xaxes(title = xlabel, row = 2 if residual else 1)    

    # If the user supplied a y axis label, add it
    if ylabel is None:
        print('Please enter a string for the y label.')
    fig.update_yaxes(title = ylabel, row = 1)

    # Plot the figure to the specified output
    process_output(fig, output) # check to see how we should be outputting this plot

    return fig



# quickbar

# quick box

# quick violin

# quick sankey

# quick pie

# quick 
