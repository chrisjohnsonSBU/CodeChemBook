# some tools for handlign opening and plotting....
import numpy as np
from codechembook import quickplots as qp


def quickOpenCSV(file, cols = None, delimiter = ",", skip_header = 1):
    '''
    This function is going to read from a csv quickly. 
    The base behavior is to just take a number of columns and read them and return them
    '''
    if cols == None: # no specific set of columns specified
        read_columns = np.genfromtxt(file, 
                                    delimiter = delimiter,
                                    skip_header=skip_header,
                                    unpack=True,
                                    )
    else: # probably should check to make sure it is a thing that can be a list... in elif
        read_columns = np.genfromtxt(file, 
                                delimiter = delimiter,
                                skip_header=skip_header,
                                usecols=cols,
                                unpack=True,
                                )
    return read_columns

def quickSaveCSV(file, data, format = None, delimiter = ', ', header = ''):
    # Check which type of data we have received and make a new numpy array holding it
    if isinstance(data, list) or isinstance(data, tuple):
        # If we got a list, then we need to turn rows into columns to make a 2D array
        prep_data = np.column_stack(data)

    elif isinstance(data, np.ndarray):
        # If we got a numpy array, we need to figure out what its dimension is
        if len(data.shape) > 2:
            print('This function can not handle arrays with three or more dimensions!')
            return

        elif len(data.shape) in [2, 1]:
            # Easy, we just copy it over
            prep_data = data

        # elif len(data.shape) == 1:
        #     prep_data = data
        else:
            print('Incompatible numpy array shape for this function.')
    elif isinstance(data, (int, float, complex, bool, str)):
        prep_data = np.array([data])
    else:
        print('This type is not supported by this function.')
        return

    if format is None:
        new_format = '%.14e'
    elif isinstance(format, str):
        if format[0] == '%' or format[1] == '%':
            # We have an old-school python format string, use it as is
            new_format = format

        else:
            # Assume we have an f-strings type format string
            def temp(x):
                return f'{x:{format}}'
            fast_format = np.vectorize(temp)
            prep_data = fast_format(prep_data)
            new_format = '%s'
    elif isinstance(format, list):
        if len(format) == prep_data.shape[1]:
            string_data = []
            print(f'Formatting {prep_data.shape[1]} columns with {len(format)} format statements')
            for i, f in enumerate(format):
                def temp(x):
                    return f'{x:{f}}'
                fast_format = np.vectorize(temp)
                string_data.append(fast_format(prep_data[:,i]))
            prep_data = np.column_stack(string_data)
            new_format = '%s'
        else:
            print(f'Failed: Received {prep_data.shape[1]} columns but {len(format)} format statements.\nNot writing any file.')
            return

    np.savetxt(file, prep_data, delimiter = delimiter, fmt = new_format, header = header, comments = '')

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

def quickOpenFilenames(title="Select files to open", initialdir='.', filetypes='All files, *.*', sorted = True):
    """
    Opens a file dialog to select multiple files, returning a sorted list of Path objects.
    
    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Select files to open".
    - initialdir (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                               Accepts both Path objects and strings.
    - filetypes (tuple): The types of files to display in the dialog. Defaults to showing all files.
                         Should be a tuple in the format (('Description', '*.extension')).
    
    Returns:
    - List[Path]: A sorted list of selected file paths as Path objects.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog

    app = QApplication([])  # Create a Qt application
    filepaths, _ = QFileDialog.getOpenFileNames(None, title, initialdir, filetypes)

    if sorted:
        filepaths = sorted(filepaths)

    return filepaths

def quickOpenFilename(title="Select files to open", initialdir='.', filetypes='All files, *.*'):
    """
    Opens a file dialog to select multiple files, returning a sorted list of Path objects.
    
    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Select files to open".
    - initialdir (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                               Accepts both Path objects and strings.
    - filetypes (tuple): The types of files to display in the dialog. Defaults to showing all files.
                         Should be a tuple in the format (('Description', '*.extension')).
    
    Returns:
    - Path: A Path object.
    """
    return quickOpenFilenames(title = title, initialdir = initialdir, filetypes = filetypes)[0]

def quickSaveFilename(title="Choose or create a filename to save", initialdir='.', filetypes='All files*.*'):
    """
    Opens a file dialog to choose a filename for saving, returns a Path object.
    
    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Define file to save".
    - initialdir (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                               Accepts both Path objects and strings.
    - filetypes (tuple): The types of files to display in the dialog. Defaults to showing all files.
                         Should be a tuple in the format (('Description', '*.extension')).
    
    Returns:
    - Path: the path to the filename that is to be saved.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog

    app = QApplication([])  # Create a Qt application
    filepath, _ = QFileDialog.getSaveFileName(None, title, initialdir, filetypes)

    return filepath

def scientificNotation(number, precision = None, exponent = None):
    from symbols import math, typography
    
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

