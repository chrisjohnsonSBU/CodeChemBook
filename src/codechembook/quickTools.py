# some tools for handlign opening and plotting....
import numpy as np
from codechembook import quickplots as qp


'''
This function is going to read from a csv quickly. 
The base behavior is to just take a number of columns and read them and return them
'''

def quickOpenCSV(file, cols = None, delimiter = ",", skip_header = 1):
    if cols == None: # no specific set of columns specified
        read_columns = np.genfromtxt(file, 
                                    delimiter = delimiter,
                                    skip_header=skip_header,
                                    unpack=True,
                                    )
    else: # probably shoudl check to make sure it is a thing that can be a list... in elif
        read_columns = np.genfromtxt(file, 
                                delimiter = delimiter,
                                skip_header=skip_header,
                                usecols=cols,
                                unpack=True,
                                )
    return read_columns



def quickPlotCSV(file, cols = None, skip_header = 1, plotType = "scatter", xcol = 0):
    '''
    xcol: int which is the column number that will be the x-data
    plotType: string the sort of plot we want "scatter" "bars" "hist", etc
    '''

    read_columns = quickOpenCSV(file, cols = cols, skip_header = skip_header)

    xdata = read_columns[xcol]
    ydata = []
    for c in range(0, xcol):
        ydata.append(read_columns[c])
    for c in range(xcol+1, len(read_columns)):
        ydata.append(read_columns[c])

    if plotType == "scatter":
        fig = qp.quickScatter(x = xdata, y = ydata)
        fig.show()

    return fig


toPlot = "/Users/benjaminlear/Documents/GitHub/Coding-for-Chemists/Data/OnePlot/0.999.csv"

quickPlotCSV(toPlot)
