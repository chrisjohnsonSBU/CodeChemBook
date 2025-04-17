# some tools for handling opening and plotting....
import numpy as np
from codechembook.chemformula import ChemFormula

# make separate wrappers for latex, html, unicode, 
# copy in the library

def quickHTMLFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in HTML contexts

    Required Args:
    formula (string): an unformatted chemical formula, without charge

    Optional Args:
    charge (int):  the charge of the compound (default: 0)
    name (string): the name of the compound (default: None)
    CAS (string):  the CAS number (default: None)
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).html.replace("<span class='ChemFormula'>", "").replace("</span>", "")

def quickLatexFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in Latex contexts

    Required Args:
    formula (string): an unformatted chemical formula, without charge

    Optional Args:
    charge (int):  the charge of the compound (default: 0)
    name (string): the name of the compound (default: None)
    CAS (string):  the CAS number (default: None)
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).latex

def quickUnicodeFormula(formula, charge = 0, name = None, CAS = None):
    '''
    Outputs a properly formatted chemical formula for use in unicode

    Required Args:
    formula (string): an unformatted chemical formula, without charge

    Optional Args:
    charge (int):  the charge of the compound (default: 0)
    name (string): the name of the compound (default: None)
    CAS (string):  the CAS number (default: None)
    '''
    return ChemFormula(formula, charge = charge, name = name, cas = CAS).unicode

def quickReadCSV(file = None, cols = None, delimiter = ",", skip_header = 1):
    '''
    This function is going to read from a csv quickly. 
    The base behavior is to just take a number of columns and read them and return them
    '''
    if file is None:
        file = quickOpenFilename()
    
    if file is None:
        print('No file selected.')
        return
    
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

    from codechembook import quickPlots as qp

    read_columns = quickReadCSV(file, cols = cols, skip_header = skip_header)

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

def quickOpenFilenames(title="Select files to open", initialpath='.', filetypes='All files, *.*', sort = True):
    """
    Opens a file dialog to select multiple files, returning a sorted list of Path objects.
    
    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Select files to open".
    - initialpath (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                               Accepts both Path objects and strings.
    - filetypes (str or iterable): The types of files to display in the dialog. Defaults to showing all files.
                         Should be a string in the format 'Description, *.extension' or a list/tuple of the same.
    
    Returns:
    - List[Path]: A sorted list of selected file paths as Path objects.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
    from pathlib import Path


    # Ensure initialpath is a string (if passed as a Path object)
    if isinstance(initialpath, Path):
        initialpath = str(initialpath)
        
    # If we got a list of file types, reformat it for getOpenFileName as a string with ';;' between entries
    if isinstance(filetypes, list):
        filetypes = ';;'.join(filetypes)
    
    # Ensure QApplication instance exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        
    # Create a temporary hidden parent window to ensure the dialog appears on top
    parent = QMainWindow()
    parent.hide()  # Ensure the parent window is hidden
    
    filepaths, _ = QFileDialog.getOpenFileNames(None, title, initialpath, filetypes)
    
    # Close and clean up the parent window
    parent.close()
    parent.deleteLater()
    
    if sort:
        filepaths = sorted(filepaths)

    return [Path(filepath) for filepath in filepaths]

def quickOpenFilename(title="Select file to open", initialpath='.', filetypes='All files, *.*'):
    """
    Opens a file dialog to select multiple files, returning a sorted list of Path objects.
    
    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Select files to open".
    - initialpath (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                               Accepts both Path objects and strings.
    - filetypes (str or iterable): The types of files to display in the dialog. Defaults to showing all files.
                         Should be a string in the format 'Description, *.extension' or a list/tuple of the same.
    
    Returns:
    - Path or None: A Path object unless "Cancel" is clicked.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
    from pathlib import Path

    # Ensure initialpath is a string (if passed as a Path object)
    if isinstance(initialpath, Path):
        initialpath = str(initialpath)
        
    # If we got a list of file types, reformat it for getOpenFileName as a string with ';;' between entries
    if isinstance(filetypes, list):
        filetypes = ';;'.join(filetypes)
        
    # Ensure QApplication instance exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        
    # Create a temporary hidden parent window to ensure the dialog appears on top
    parent = QMainWindow()
    parent.hide()  # Ensure the parent window is hidden
    
    filepath, _ = QFileDialog.getOpenFileName(None, title, initialpath, filetypes)
    
    # Close and clean up the parent window
    parent.close()
    parent.deleteLater()
    
    return Path(filepath) if filepath != '' else None

def quickSelectFolder(title="Select folder", initialpath="."):
    """
    Opens a folder selection dialog, returning the selected folder as a Path object.

    Parameters:
    - title (str): The title of the folder selection dialog window. Defaults to "Select folder".
    - initialpath (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                                Accepts both Path objects and strings.

    Returns:
    - Path: A Path object representing the selected folder, or None if no folder was selected.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
    from pathlib import Path

    # Ensure initialpath is a string (if passed as a Path object)
    if isinstance(initialpath, Path):
        initialpath = str(initialpath)

    # Ensure QApplication instance exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        
    # Create a temporary hidden parent window to ensure the dialog appears on top
    parent = QMainWindow()
    parent.hide()  # Ensure the parent window is hidden

    # Open the folder selection dialog with the hidden parent
    folderpath = QFileDialog.getExistingDirectory(parent, title, initialpath)

    # Close and clean up the parent window
    parent.close()
    parent.deleteLater()

    # Return the selected folder as a Path object, or None if no folder was selected
    return Path(folderpath) if folderpath else None

def quickSaveFilename(title="Choose or create a filename to save", 
                      initialpath='.', filetypes='All files, *.*'):
    """
    Opens a file dialog to choose a filename for saving, returns a Path object.

    Parameters:
    - title (str): The title of the file selection dialog window. Defaults to "Define file to save".
    - initialpath (str or Path): The initial directory for the dialog. Defaults to the current directory '.'.
                                Accepts both Path objects and strings.
    - filetypes (str or iterable): The types of files to display in the dialog. Defaults to showing all files.
                                   Should be a string in the format 'Description, *.extension' or a list/tuple of the same.

    Returns:
    - Path: the path to the filename that is to be saved.
    """
    from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
    from pathlib import Path

    # Ensure initialpath is a string (if passed as a Path object)
    if isinstance(initialpath, Path):
        initialpath = str(initialpath)
        
    # If we got a list of file types, reformat it for getSaveFileName as a string with ';;' between entries
    if isinstance(filetypes, list):
        filetypes = ';;'.join(filetypes)
    
    # Ensure QApplication instance exists
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Create a temporary hidden parent window
    parent = QMainWindow()
    parent.hide()  # Do not display the window

    # Open the file dialog with the temporary parent
    filepath, _ = QFileDialog.getSaveFileName(parent, title, initialpath, filetypes)

    # Close the temporary parent window
    parent.close()
    parent.deleteLater()  # Ensure proper cleanup of the parent window

    return Path(filepath) if filepath else None

def quickPopupMessage(message="This is a message. Click OK to continue."):
    """
    Displays a simple popup with a message and an OK button.

    Parameters:
    - message (str): The message to display in the popup.

    Returns:
    - None
    """
    from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a QApplication if it doesn't already exist

    # Create a visible temporary parent window
    parent = QMainWindow()
    parent.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure it's always on top
    parent.setWindowTitle("Temporary Parent")
    parent.resize(1, 1)  # Make the parent very small
    parent.show()  # Show the parent window
    parent.raise_()
    parent.activateWindow()

    # Create the message box with the parent
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(message)
    msg_box.setWindowTitle("Message")
    msg_box.setStandardButtons(QMessageBox.Ok)

    # Ensure the message box is always on top
    msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
    msg_box.raise_()  # Bring it to the front
    msg_box.activateWindow()  # Make it the active window

    # Show the message box and wait for user interaction
    msg_box.exec_()

    # Clean up the parent window
    parent.hide()
    app.processEvents()
    parent.close()
    parent.deleteLater()

def quickPopupChoice(message="Choose an option:", option1="Option 1", option2="Option 2"):
    """
    Displays a popup dialog with a message and two buttons, returning the selected option as a string.

    Parameters:
    - message (str): The message to display in the popup.
    - option1 (str): The text for the first button.
    - option2 (str): The text for the second button.

    Returns:
    - str: The text of the button selected by the user.
    """
    from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a QApplication if it doesn't already exist

    # Create a visible temporary parent window to ensure the popup appears on top
    parent = QMainWindow()
    parent.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure it's always on top
    parent.setWindowTitle("Temporary Parent")
    parent.resize(1, 1)  # Make the parent very small
    parent.show()  # Show the parent window
    parent.raise_()
    parent.activateWindow()

    # Create the message box with the parent
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Question)  # Set the icon to Question
    msg_box.setText(message)
    msg_box.setWindowTitle("Make a Choice")

    # Add the two custom buttons
    button1 = msg_box.addButton(option1, QMessageBox.ActionRole)
    button2 = msg_box.addButton(option2, QMessageBox.ActionRole)

    # Ensure the message box always appears on top
    msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint)
    msg_box.raise_()
    msg_box.activateWindow()

    # Show the message box and wait for the user's choice
    msg_box.exec_()

    # Determine which button was clicked
    if msg_box.clickedButton() == button1:
        choice = option1
    elif msg_box.clickedButton() == button2:
        choice = option2
    else:
        choice = None  # Fallback in case no valid button was clicked (shouldn't happen)

    # Clean up the parent window
    parent.hide()
    app.processEvents()
    parent.close()
    parent.deleteLater()

    return choice

def quickPopupInput(message="Enter some text:"):
    """
    Displays a popup dialog with a message, a text input box, and OK/Cancel buttons.
    
    Parameters:
    - message (str): The message to display in the popup.

    Returns:
    - str: The text entered by the user if OK is clicked.
    - None: If Cancel is clicked.
    """
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMainWindow
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a QApplication if it doesn't already exist

    # Create a temporary parent window to ensure the dialog is always on top
    parent = QMainWindow()
    parent.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure it's always on top
    parent.setWindowTitle("Temporary Parent")
    parent.resize(1, 1)  # Make the parent very small
    parent.show()  # Show the parent window
    parent.raise_()
    parent.activateWindow()

    # Create the custom dialog
    dialog = QDialog(parent)
    dialog.setWindowTitle("Input Dialog")
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Always on top

    # Set up the layout
    layout = QVBoxLayout()

    # Add the message label
    label = QLabel(message)
    layout.addWidget(label)

    # Add the text input box
    text_input = QLineEdit()
    layout.addWidget(text_input)

    # Add OK and Cancel buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    # Connect button actions
    def on_ok():
        dialog.accept()  # Accept the dialog and close it

    def on_cancel():
        dialog.reject()  # Reject the dialog and close it

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    # Set the layout for the dialog
    dialog.setLayout(layout)

    # Show the dialog and wait for user interaction
    result = dialog.exec_()

    # Clean up the parent window
    parent.hide()
    app.processEvents()
    parent.close()
    parent.deleteLater()

    # Return the appropriate value based on user interaction
    if result == QDialog.Accepted:
        return text_input.text()  # Return the entered text if OK was clicked
    else:
        return None  # Return None if Cancel was clicked

def quickPopupDropdown(message="Select an option:", options=("Option 1", "Option 2", "Option 3")):
    """
    Displays a popup dialog with a message, a dropdown menu, and OK/Cancel buttons.

    Parameters:
    - message (str): The message to display in the popup.
    - options (list or tuple of str): A list or tuple of options to display in the dropdown.

    Returns:
    - int: The index of the selected option if OK is clicked.
    - None: If Cancel is clicked.
    """
    from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QMainWindow
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a QApplication if it doesn't already exist

    # Create a temporary parent window to ensure the dialog is always on top
    parent = QMainWindow()
    parent.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure it's always on top
    parent.setWindowTitle("Temporary Parent")
    parent.resize(1, 1)  # Make the parent very small
    parent.show()  # Show the parent window
    parent.raise_()
    parent.activateWindow()

    # Create the custom dialog
    dialog = QDialog(parent)
    dialog.setWindowTitle("Dropdown Dialog")
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Always on top

    # Set up the layout
    layout = QVBoxLayout()

    # Add the message label
    label = QLabel(message)
    layout.addWidget(label)

    # Add the dropdown box
    dropdown = QComboBox()
    dropdown.addItems(options)  # Populate the dropdown with options
    layout.addWidget(dropdown)

    # Add OK and Cancel buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    # Connect button actions
    def on_ok():
        dialog.accept()  # Accept the dialog and close it

    def on_cancel():
        dialog.reject()  # Reject the dialog and close it

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    # Set the layout for the dialog
    dialog.setLayout(layout)

    # Show the dialog and wait for user interaction
    result = dialog.exec_()

    # Properly clean up the parent window
    parent.hide()  # Hide the parent window immediately
    app.processEvents()  # Force event loop to process hiding
    parent.close()  # Close the parent window
    parent.deleteLater()  # Mark the parent for deletion

    # Return the appropriate value based on user interaction
    if result == QDialog.Accepted:
        return dropdown.currentIndex()  # Return the index of the selected option
    else:
        return None  # Return None if Cancel was clicked

def quickPopupCheckboxes(message="Select options:", options=("Option 1", "Option 2", "Option 3")):
    """
    Displays a popup dialog with a message, a series of checkboxes, and OK/Cancel buttons.

    Parameters:
    - message (str): The message to display in the popup.
    - options (list or tuple of str): A list or tuple of options to display as checkboxes.

    Returns:
    - tuple: A tuple of indices of the checkboxes that are checked if OK is clicked.
    - None: If Cancel is clicked.
    """
    from PyQt5.QtWidgets import (
        QApplication,
        QDialog,
        QVBoxLayout,
        QLabel,
        QCheckBox,
        QPushButton,
        QHBoxLayout,
        QMainWindow,
    )
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication([])  # Create a QApplication if it doesn't already exist

    # Create a temporary parent window to ensure the dialog is always on top
    parent = QMainWindow()
    parent.setWindowFlags(Qt.WindowStaysOnTopHint)  # Ensure it's always on top
    parent.setWindowTitle("Temporary Parent")
    parent.resize(1, 1)  # Make the parent very small
    parent.show()  # Show the parent window
    parent.raise_()
    parent.activateWindow()

    # Create the custom dialog
    dialog = QDialog(parent)
    dialog.setWindowTitle("Checkbox Dialog")
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)  # Always on top

    # Set up the layout
    layout = QVBoxLayout()

    # Add the message label
    label = QLabel(message)
    layout.addWidget(label)

    # Add checkboxes for each option
    checkboxes = []
    for option in options:
        checkbox = QCheckBox(option)
        layout.addWidget(checkbox)
        checkboxes.append(checkbox)

    # Add OK and Cancel buttons
    button_layout = QHBoxLayout()
    ok_button = QPushButton("OK")
    cancel_button = QPushButton("Cancel")
    button_layout.addWidget(ok_button)
    button_layout.addWidget(cancel_button)
    layout.addLayout(button_layout)

    # Connect button actions
    def on_ok():
        dialog.accept()  # Accept the dialog and close it

    def on_cancel():
        dialog.reject()  # Reject the dialog and close it

    ok_button.clicked.connect(on_ok)
    cancel_button.clicked.connect(on_cancel)

    # Set the layout for the dialog
    dialog.setLayout(layout)

    # Show the dialog and wait for user interaction
    result = dialog.exec_()

    # Properly clean up the parent window
    parent.hide()  # Hide the parent window immediately
    app.processEvents()  # Process any pending events
    parent.close()  # Close the parent window
    parent.deleteLater()  # Mark the parent for deletion

    # Return the appropriate value based on user interaction
    if result == QDialog.Accepted:
        # Gather indices of checkboxes that are checked
        checked_indices = tuple(i for i, checkbox in enumerate(checkboxes) if checkbox.isChecked())
        return checked_indices
    else:
        return None  # Return None if Cancel was clicked

def importFromPy(py_name, *args):
    """
    Load a function or other object from a Python file that is not in the CWD or library.

    Parameters:
    py_name (str): The name of the Python script from which you want to import.
    *args (str): Names of the objects to import from the script.
    """
    import importlib.util
    from pathlib import Path
    import sys
    import builtins
    import keyword

    # Check if the user supplied the full file name or just the stem
    if not py_name.endswith('.py'):
        filename = py_name + '.py'
    else:
        filename = py_name
        py_name = py_name.split('.')[0]

    # Locate the file
    path = Path(filename)
    if not path.exists():
        quickPopupMessage(f'{filename} not found. Please locate it using the file dialog.')
        path = quickOpenFilename(filetypes="Python Files, *.py")

        if not path:
            raise FileNotFoundError(f"The file {filename} could not be located.")

    # Load its module
    module_name = py_name
    module_spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(module_spec)

    # Import the module
    try:
        sys.modules[module_name] = module
        module_spec.loader.exec_module(module)
    except Exception as e:
        quickPopupMessage(f"Failed to load module {filename}: {e}")
        raise

    # Import objects
    imported_objects = {}
    for obj_name in args:
        try:
            imported_objects[obj_name] = getattr(module, obj_name)
        except AttributeError:
            quickPopupMessage(f"{obj_name} not found in {filename}.")
            raise ImportError(f"'{obj_name}' not found in '{filename}'.")

    # Add to the global namespace
    import __main__
    for obj_name, obj in imported_objects.items():
        # Check to make sure 
        if obj_name in dir(builtins) or keyword.iskeyword(obj_name):
            print(f"{obj_name} is a reserved keyword or built-in function name and will not be imported.")
        else:
            setattr(__main__, obj_name, obj)
            print(f"Imported {obj_name}")

    return imported_objects

