# codechembook.numericalTools

This module contains functions that streamline common numerical tasks.

## IntegrateRange

```
integrateRange(y, x, limits, method='trapezoid')
```

Integrate a numeric function over a range less than the full extent of
the function.

### Required Params:
y (ndarray):              y-values for integration.  
x (ndarray):              x-values for integration. (need not be evenly spaced)  
limits (list of numeric): Lower and upper limits of integration.
    
### Optional Params:
method (string): which approach to use (default: 'trapezoid', options: 'rectangle', 'simpson')
    
### Returns:
(float): Value of the integral

## maxInRange

```
maxInRange(x, y, limits)
```

Find the maximum y-value that falls between two limits of x-value.

If maximum value occurs multiple times, returns the first instance (lowest index).

### Required Params:
x (ndarray or list): x-values.  
y (ndarray or list): y-values.  
limits (list):       Range of x-values to consider.
    
### Returns:
(int): Index of the first instance of the max, using indices of original array.

## minInRange

```
minInRange(x, y, limits)
```

Find the minimum y-value that falls between two limits of x-value.

If minimum value occurs multiple times, returns the first instance (lowest index).

#### Required Params:
x (ndarray or list): x-values.  
y (ndarray or list): y-values.  
limits (list):       Range of x-values to consider.
    
#### Returns:
(int): Index of the first instance of the min, using indices of original array.