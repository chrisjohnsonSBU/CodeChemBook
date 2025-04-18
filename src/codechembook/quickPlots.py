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

def sampleColorScale(num_colors, color_scale = 'bluered', mid_value = None):
    '''
    Create a color scale with a given number of colors from a continuous color scale.
    Useful for plotting multiple traces with an inferred ordering or sequencing.
    See https://plotly.com/python/builtin-colorscales/ for options

    Required Args:
    num_colors (int): the number of colors needed (usually number of traces)

    Optional Args:
    color_scale (string): the name of the continuous color scale to sample.
    '''
    
    from plotly.express.colors import sample_colorscale 
    
    colors = sample_colorscale(color_scale, [i / (num_colors - 1) for i in range(num_colors)])
    
    return colors
    
def customColorScale(colors, scale=None): # continuous color scale for use in plotly
    from plotly.colors import convert_colors_to_same_type

    css_color_dict = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32"
    }

    print("starting customColorScale function")
    translated_colors = []
    for c in colors:
        if isinstance(c, str):
            if c.startswith("rgb") or c.startswith("#"): # may need to handle rgba separately
                translated_colors.append(c)
            elif c in css_color_dict.keys():
                translated_colors.append(css_color_dict[c])
            else:
                raise "You supplied a color incorrectly."
        else:
            translated_colors.append(c)
                
    if scale is None:
        scale = list(np.linspace(0,1,len(colors)))
    
    print(f"inside customColorScale: colors_to_pass = {translated_colors}, scale = {scale}")
    
    # get the formatted colors and scales
    temp_scale = convert_colors_to_same_type(
        translated_colors, 
        scale = scale,
        colortype = "rgb")
    
    # restructuring this object to be a properly formatted color scale
    color_scale = []
    for color, position in zip(temp_scale[0], temp_scale[1]):
        color_scale.append([position, color])
    
    return color_scale

def customColorList(num_colors, 
                  colors = 'bluered', # either a string or a list of colors
                  reverse = False, 
                  perceptual = False, 
                  as_string = True, # controls the output
                  ): # discrete color scale for use in plotly
    
    if isinstance(colors, str): # assume this is a named color scale
        color_list = sampleColorScale(num_colors, color_scale = colors)    
    elif isinstance(colors, list): # specifying a custom scale
        if perceptual:
            raise "perceptual is not yet implemented"
        else:
            if isinstance(colors[0], list) and len(colors[0])==2: # expect sublists of color and position
                colors_to_pass = []
                scale = []
                for item in colors:
                    colors_to_pass.append(item[0])
                    scale.append(item[1])
            else: # think of more robust treatment
                colors_to_pass = colors
                scale = None
            print(f"colors_to_pass = {colors_to_pass}, scale = {scale}")
            custom_color_scale = customColorScale(colors_to_pass, scale)
            print(custom_color_scale)
            color_list = sampleColorScale(num_colors, color_scale = custom_color_scale)    
    
    return color_list


    
    

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
    Quickly plot one xy trace in plotly.

    Optional Args:
        x (ndarray or list of ndarray):  the x coordinates to plot
        y (ndarray or list of ndarray):  the y coordinates to plot
        xlabel (string):                 x axis title
        ylabel (string):                 y axis title
        name (string or list of string): the name of the trace(s) to appear on hover or in the legend
        mode (string or list of string): plot using 'lines'(default) or 'markers'
        template (string):               which plotly template to use (default simple_white)
        output (string):                 output to Spyder plot window ('png', 'svg')
                                           or browser ('browser')
                                           or the 'normal' show behavior ('default')
                                           or 'None' for no output
                    
    Returns:
        qplot (plotly figure object): the figure object created
    """
    # if the user did not supply axis names, then we can just use the variable names
    if xlabel is None:
        xlabel = _get_name_two_calls_ago(x)
    if ylabel is None:
        ylabel = _get_name_two_calls_ago(y)


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
    
    # next, let us ensure we can iterate through x and y together
    if len(xplot) == 1:
        xplot = [xplot[0]]*len(yplot)
    elif len(xplot) != len(yplot): # both are already long lists that don't match.
        raise "your x values should be a list of length equal to y values, or a list of 1"
    
    # start the plotting
    qplot = make_subplots()
    if name is None:
        name = ['' for x in xplot]
    elif isinstance(name, str):
        name = [name]
    if mode is None:
        mode = [None for x in xplot]
    elif isinstance(mode, str):
        mode = [mode for x in xplot]
    elif isinstance(mode, list) and len(mode) == 1:
        mode = [mode[0] for x in xplot]

    # now everything is a list
    try:
        zip(yplot, name, mode)
    except:
        if len(yplot) != len(name):
            raise f"The name keyword needs a string (for one y trace) or a list that is the same length as the number of y traces.\nYou passed {len(yplot)} traces but {len(name)} names."
        if len(yplot) != len(mode):
            raise f"The mode keyword needs a string (to apply the same mode to all traces) or a list that is the same length as the number of y traces.\nYou passed {len(yplot)} traces but {len(mode)} names."    

    for xi,yi,ni,mi in zip(xplot, yplot, name, mode):
        if len(xi) != len(yi):
            raise "you do not have the same number of x and y points!"
        if mi is None:
            points = go.Scatter(x=xi, y = yi, name = ni)
        elif "lines" in mode or "markers" in mi:
            points = go.Scatter(x=xi, y = yi, mode = mi, name = ni)
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
                            line = {'dash': 'dot', 'color':'red'},
                            row = 1, col = 1) 
    
    # Plot the raw data
    fig.add_scatter(x = xdata, 
                    y = ydata, 
                    mode = 'markers', 
                    name = 'Data', 
                    legendrank = 1, 
                    marker = {'color': 'black', 'size': 8},
                    line = {'color': 'black', 'width' : 8},
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
                        line = {'color': 'red', 'width':1},
                        marker = {'color': 'red', 'size':2},
                        showlegend = False,
                        row = 2, col = 1)
        
        # Optionally plot the confidence interval of the residual
        if confidence != 0 and type(confidence) == int:
            
            fig.add_scatter(x = smoothx, 
                            y = confidence * fit.eval_uncertainty(**kwargs), 
                            mode = 'lines',
                            line = {'color': 'lightpink', 'width': 0},
                            row = 2, col = 1)
            fig.add_scatter(x = smoothx, 
                            y = -1 * confidence * fit.eval_uncertainty(**kwargs), 
                            mode = 'lines',
                            line = {'color': 'lightpink', 'width': 0},
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
