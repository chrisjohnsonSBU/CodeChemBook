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



from symbols import math, typography
def scientificNotation(number, precision = None, exponent = None):
    
    oldNumberString = f'{number:e}' # use the "e" to ensure it is always formatted with an e
    oldCoefficient, oldExponent = oldNumberString.split('e') # get the coefficient and exponent from the old number string
    oldCoefficient = float(oldCoefficient) # make sure we have a float for the coefficient
    oldExponent = int(oldExponent) # make sure we have a string for the exponent
    print(oldExponent)
    
    if exponent is not None:# this means there is a desired exponent... such as 10^6
        sciExponent = exponent # set the scientific exponent to the desired exponent
        sciCoefficient = oldCoefficient * 10**(oldExponent - exponent) # make sure we scale the coefficient by the different in the exponents.
    else:
        sciExponent = oldExponent
        sciCoefficient = oldCoefficient
    
    if precision is not None: # his means we have a level of precision we want to report to
        sciCoefficient = np.round(sciCoefficient, precision)
    
    supString = ''
    for glyph in str(sciExponent): # go through glyph by glyph and assign the correct superscript
        if glyph == '0':
            supString = supString + typography.sup_0
        elif glyph == '1':
            supString = supString + typography.sup_1
        elif glyph == '2':
            supString = supString + typography.sup_2
        elif glyph == '3':
            supString = supString + typography.sup_3
        elif glyph == '4':
            supString = supString + typography.sup_4
        elif glyph == '5':
            supString = supString + typography.sup_5
        elif glyph == '6':
            supString = supString + typography.sup_6
        elif glyph == '7':
            supString = supString + typography.sup_7
        elif glyph == '8':
            supString = supString + typography.sup_8
        elif glyph == '9':
            supString = supString + typography.sup_9
        elif glyph == '-':
            supString = supString + typography.sup_minus
        else:
            pass
        
    formattedScientificNotation = f'{sciCoefficient}{math.times}10{supString}'
    
    return formattedScientificNotation


toPlot = "/Users/benjaminlear/Documents/GitHub/Coding-for-Chemists/Data/OnePlot/0.999.csv"

quickPlotCSV(toPlot)
