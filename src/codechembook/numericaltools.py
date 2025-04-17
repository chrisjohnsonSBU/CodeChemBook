###############################################################################
#
# IntegrateRange - function to integrate a numerical series of x and y points 
# between two limits
#
###############################################################################

import numpy as np
import scipy.integrate as spi

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
    int_range = (x >= limits[0]) & (x < limits[1])
    
    # Decide which integration method the user wants
    if method == 'simpson':
        return spi.simpson(y[int_range], x[int_range])
    
    elif method == 'rectangle':
        return np.sum(y[int_range[:-1]] * (x[int_range[1:]] - x[int_range[:-1]]))
    
    else:
        # Maybe the user typed something wrong into the method keyword
        if method != 'trapezoid':
            print('Invalid method specified, defaulting to trapezoid')
            print('Please choose rectangle, trapezoid, or simpson')
        return spi.trapezoid(y[int_range], x[int_range])
    
