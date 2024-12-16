# some tools for handlign opening and plotting....
import numpy as np
from codechembook import quickPlots as qp


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
    """
    Saves a CSV file of 1D or 2D data.
    
    Parameters:
    - file (str or Path):     The path to save the file.
    - data (list or ndarray): The data to save.  Can be 1D or 2D list or ndarrays, or list of 1D ndarrays
    
    Keywords:
    - format (str or list):   A format string using either pre-Python2.6 format ('%5.3f') for f-string
                              format ('5.3f').  The colon is omitted.  Default is '.14f'.  If columns need 
                              different formatting, a list of f-string style format strings for each column 
                              can be provided.
    - delimiter (str):        The delimiter character: ', ' (comma, default), ' ' (space), '\t' (tab), or anything else
    - header (str):           Column header text.  Default is no header
    """
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

        else:
            print('Incompatible numpy array shape for this function.')

    elif isinstance(data, (int, float, complex, bool, str)):
        # For whatever reason, the user wants to write just one value
        prep_data = np.array([data])

    else:
        print('This data type is not supported by this function.')
        return

    if format is None:
        # No format statement given, let's just print 20 characters total
        new_format = '%.14e' # good for anything but the most precise measurements made by humans

    elif isinstance(format, str):
        if format[0] == '%' or format[1] == '%':
            # We have an old-school python format string, use it as is
            new_format = format

        else:
            # Assume we have an f-strings type format string
            # Quick way to format large ndarrays: define format function, vectorize, apply
            def temp(x):
                return f'{x:{format}}'
            fast_format = np.vectorize(temp)
            prep_data = fast_format(prep_data)

            # Now we have a formatted string, so we just want the format statement to keep it the same
            new_format = '%s'

    elif isinstance(format, list):
        # We want different columns to be different formats.  First make sure formats and columns match
        if len(format) == prep_data.shape[1]:
            # Empty list of columns of formatted data
            string_data = []
            print(f'Formatting {prep_data.shape[1]} columns with {len(format)} format statements')
            
            # Loop over columns and format them one by one with the appropriate format string
            for i, f in enumerate(format):
                # See previous elif for explanation
                def temp(x):
                    return f'{x:{f}}'
                fast_format = np.vectorize(temp)

                # Add the new formatted column to the data list
                string_data.append(fast_format(prep_data[:,i]))

            # Make a ndarray with the formatted columns
            prep_data = np.column_stack(string_data)

            # Now we have a formatted string, so we just want the format statement to keep it the same
            new_format = '%s'

        else:
            # Number of data columns and format strings are not the same, fail with a useful message
            print(f'Failed: Received {prep_data.shape[1]} columns but {len(format)} format statements.\nNot writing any file.')
            return

    # Write the file
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

def quickOpenFilenames(title="Select files to open", initialdir='.', filetypes='All files, *.*', sort = True):
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
    from pathlib import Path


    # Ensure initialdir is a string (if passed as a Path object)
    if isinstance(initialdir, Path):
        initialdir = str(initialdir)

    app = QApplication([])  # Create a Qt application
    filepaths, _ = QFileDialog.getOpenFileNames(None, title, initialdir, filetypes)
    
    if sort:
        filepaths = sorted(filepaths)

    return [Path(filepath) for filepath in filepaths]

def quickOpenFilename(title="Select file to open", initialdir='.', filetypes='All files, *.*'):
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
    from PyQt5.QtWidgets import QApplication, QFileDialog
    from pathlib import Path

    # Ensure initialdir is a string (if passed as a Path object)
    if isinstance(initialdir, Path):
        initialdir = str(initialdir)
        
    app = QApplication([])  # Create a Qt application
    filepath, _ = QFileDialog.getOpenFileName(None, title, initialdir, filetypes)
    
    return Path(filepath)

def quickSelectFolder(title="Select folder", initialdir="."):
    """
    Opens a folder selection dialog, returning the selected folder as a Path object.

    Parameters:
    - title (str): The title of the folder selection dialog window. Defaults to "Select folder".
    - initialdir (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                                Accepts both Path objects and strings.

    Returns:
    - Path: A Path object representing the selected folder, or None if no folder was selected.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog
    from PyQt5.QtCore import Qt
    from pathlib import Path

    if isinstance(initialdir, Path):
        initialdir = str(initialdir)

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Open the folder selection dialog with a "stay on top" flag
    dialog = QFileDialog()
    dialog.setWindowTitle(title)
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    dialog.setOptions(QFileDialog.ShowDirsOnly)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

    # Set the initial directory and open the dialog
    dialog.setDirectory(initialdir)
    if dialog.exec_():
        folderpath = dialog.selectedFiles()[0]
        return Path(folderpath)
    else:
        return None

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
    from pathlib import Path

    # Ensure initialdir is a string (if passed as a Path object)
    if isinstance(initialdir, Path):
        initialdir = str(initialdir)
        
    app = QApplication([])  # Create a Qt application
    filepath, _ = QFileDialog.getSaveFileName(None, title, initialdir, filetypes)

    return Path(filepath)

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

