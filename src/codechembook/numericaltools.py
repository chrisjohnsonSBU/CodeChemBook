###############################################################################
#
# IntegrateRange - function to integrate a numerical series of x and y points 
# between two limits
#
###############################################################################

import scipy.integrate as spi
import numpy as np

def integrateRange(y, x, limits, method='trapezoid'):
    """
    Integrate a numeric function over a range less than the full extent of
    the function.
    
    Required Args:
        y (ndarray): the y points for integration
        x (ndarray): the x points for integration (need not be evenly spaced)
        limits (list of numeric): the lower and upper limit of integration
        
    Optional Args:
        method (string): which approach to use (trapezoid (default), rectangle, simpson)
        
    Returns:
        (float): the value of the integral
    """
    
    # Sort the limits so they are in the order [lower, upper]
    limits.sort()

    # Find the indicies of the range that we want to integrate
    integ_range = (x >= limits[0]) & (x < limits[1])
    
    # Decide which integration method the user wants
    if method == 'simpson':
        return spi.simpson(y[integ_range], x[integ_range])
    
    elif method == 'rectangle':
        return np.sum(y[integ_range[:-1]] * (x[integ_range[1:]] 
                                               - x[integ_range[:-1]]))
    
    else:
        # Maybe the user typed something wrong into the method keyword
        if method != 'trapezoid':
            print('Invalid method specified, defaulting to trapezoid')
            print('Please choose rectangle, trapezoid, or simpson')
        return spi.trapezoid(y[integ_range], x[integ_range])
    

def maxInRange(x, y, limits):
    """
    Find the maximum value in a subset of y data points of a 1D collection set 
    by maximum and minimum x values.  If maximum value occurs multiple times, 
    return the first instance (lowest index).
    
        Required Args:
    x (ndarray or list): the x-data for the signal
    y (ndarray or list): the y-data for the signal
    limits (list):       the range of x-values to consider
        
        Returns:
    (int): index of the first instance of the maximum value in the range, using 
            the indices of the original array

    """
    
    # sort the limits so they are in the order [lower, upper]
    limits.sort()
    
    if isinstance(x, list) and isinstance(y, list):
        # Get a sub-list of the values to search
        sub_y = [yi for yi, xi in zip(y, x) if xi >= limits[0] and xi <= limits[1]]
        
        # Determine the index of the first item in the sub-list in the indices of the list
        shift_index = min([i for i, xi in enumerate(x) if xi >= limits[0]])
        
        # Find the max value in the sub-list
        sub_max = max(sub_y)
        
        # Find the index of the sub-list in the indicies of the sub-list
        sub_index = sub_y.index(sub_max)
        
        # Add the index of the first item in the sub-list to the index of the item in the 
        # sub-list to get the index in the indices of the list
        return shift_index + sub_index
    
    elif isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # Find the indicies of the range that we want to search
        search_range = (x >= limits[0]) & (x <= limits[1])
        
        # Determine the index of the first item in the subarray in the indices of the array
        shift_index = np.where(search_range)
        
        # Find the max value of the subarray
        sub_max = np.max(y[search_range])
        
        # Find the index of the subarray in the indicies of the subarray
        sub_index = np.where(y[search_range] == sub_max)
        
        # Add the index of the first element in the subarray to the index of the element in 
        # the subarray to get the index in the indices of the array
        return shift_index[0][0] + sub_index[0][0]
    
    else:
        # User gave the wrong type for x and/or y
        print('Error: This function requires both x and y to be 1D ndarrays or lists.')
        
        return None
    
def minInRange(x, y, limits):
    """
    Find the minimum value in a subset of y data points of a 1D collection set 
    by maximum and minimum x values.  If minimum value occurs multiple times, 
    return the first instance (lowest index).
    
        Required Args:
    x (ndarray or list): the x-data for the signal
    y (ndarray or list): the y-data for the signal
    limits (list):       the range of x-values to consider
        
        Returns:
    (int): index of the first instance of the minimum value in the range, using 
            the indices of the original array

    """
    
    # sort the limits so they are in the order [lower, upper]
    limits.sort()
    
    if isinstance(x, list) and isinstance(y, list):
        # Get a sub-list of the values to search
        sub_y = [yi for yi, xi in zip(y, x) if xi >= limits[0] and xi <= limits[1]]
        
        # Determine the index of the first item in the sub-list in the indices of the list
        shift_index = min([i for i, xi in enumerate(x) if xi >= limits[0]])
        
        # Find the max value in the sub-list
        sub_min = min(sub_y)
        
        # Find the index of the sub-list in the indicies of the sub-list
        sub_index = sub_y.index(sub_min)
        
        # Add the index of the first item in the sub-list to the index of the item in the 
        # sub-list to get the index in the indices of the list
        return shift_index + sub_index
    
    elif isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        # Find the indicies of the range that we want to search
        search_range = (x >= limits[0]) & (x <= limits[1])
        
        # Determine the index of the first item in the subarray in the indices of the array
        shift_index = np.where(search_range)
        
        # Find the max value of the subarray
        sub_min = np.min(y[search_range])
        
        # Find the index of the subarray in the indicies of the subarray
        sub_index = np.where(y[search_range] == sub_min)
        
        # Add the index of the first element in the subarray to the index of the element in 
        # the subarray to get the index in the indices of the array
        return shift_index[0][0] + sub_index[0][0]
    
    else:
        # User gave the wrong type for x and/or y
        print('Error: This function requires both x and y to be 1D ndarrays or lists.')
        
        return None