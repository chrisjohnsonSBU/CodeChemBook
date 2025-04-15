'''
A quick script to check to make sure that plotly is working correctly
and that kaleido/orca works to output static images and to render
plots to a browser
'''

import plotly.graph_objects as go
import numpy as np

def plotlyTest():

    # Initialize x and y to some test data
    # Here, we will just plot a simple sine wave
    
    x = np.linspace(0,10,50)
    y = np.sin(x)
    
    # Set up the plot.  First, we will create a blank figure,
    # then we will add a scatter plot to the figure.
    
    fig = go.Figure() # Create a blank figure
    fig.add_scatter(x=x, y=y, mode='markers') # Add the data with markers
    
    # We are going to write the plot to a file and then also show it in a 
    # browser window
    
    fig.show('browser')
    fig.show('png', width=600, height=600)
    fig.write_image('test.svg', width=600, height=600)
