###############################################################################
#
# PlotFit - function to quickly plot the results of a fit using lmift 
# this assumes a 1d fit
#
###############################################################################

import numpy as np
from plotly.subplots import make_subplots
import plotly.io as pio

def plotFit(fit, 
            resample = 10, 
            residual = False, 
            components = False, 
            confidence = 0, 
            xlabel = None, 
            ylabel = None, 
            template = 'simple_white',
            output = 'png',
            colors = 'greys'):
    """
    Plot the result of a 1d fit using lmfit
    
    Required Args:
        fit (lmfit result object): the result of a fit using lmfit
        
    Optional Args:
        resample (int):    increase the density of points on the x axis by N 
                           times for a smoother model fit curve
        residual (bool):   plot the residual
        components (bool): plot the individual components of the model
        confidence (int):  plot the confidence interval of the fit (N-sigma)
                           where N = 0 (default), 1, 2, etc.
        xlabel (string):   x axis title
        ylabel (string):   y axis title
        template (string): which plotly template to use
        output (string):   output to Spyder plot window ('png') 
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
    if residual:
        fig = make_subplots(rows = 2, 
                            cols = 1, 
                            shared_xaxes = True, 
                            row_heights = [0.8, 0.2],
                            vertical_spacing = 0.05)
    else:
        fig = make_subplots()

    # If we are plotting the confidence interval, then plot +/- N * 1-sigma 
    # and fill between the two curves
    if confidence != 0 and type(confidence) == int:
        fig.add_scatter(x = smoothx, 
                        y = smoothy + confidence * fit.eval_uncertainty(**kwargs), 
                        mode = 'lines',
                        line = {'color': 'gray', 'width': 0},
                        row = 1, col = 1)
        fig.add_scatter(x = smoothx, 
                        y = smoothy - confidence * fit.eval_uncertainty(**kwargs), 
                        mode = 'lines',
                        line = {'color': 'gray', 'width': 0},
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
                    marker = {'color': 'rgb(180,180,180)', 'size': 8},
                    line = {'color': 'rgb(180,180,180)', 'width' : 8},
                    row = 1, col = 1)

    # Plot the fit curve
    fig.add_scatter(x = smoothx, 
                    y = smoothy, 
                    mode = 'lines', 
                    name = 'Best Fit', 
                    legendrank = 2, 
                    line = {'color': 'black'},
                    row = 1, col = 1)

    # If we are doing residuals, plot the residual
    if residual:
        fig.add_scatter(x = xdata, 
                        y = fit.residual, 
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
    
    # If the user supplied an x axis label, add it
    if type(xlabel) == str:
        fig.update_xaxes(title = xlabel, row = 2 if residual else 1)
    elif xlabel != None:
        print('Please enter a string for the x label.')

    # If the user supplied a y axis label, add it
    if type(ylabel) == str:
        fig.update_yaxes(title = ylabel, row = 1)
    elif ylabel != None:
        print('Please enter a string for the y label.')

    # Update the layout
    fig.update_layout(template = template, showlegend = False)

    # Plot the figure to the specified output
    if output in pio.renderers.keys():
        fig.show(output)
    elif output is None or output == 'None':
        return fig
    else:
        print("Enter 'png' to plot in Spyder or 'browser' for the browser.")
        print("Use 'None' to show nothing and return the figure object.")
    
    return fig