import matplotlib
import matplotlib.pyplot as plt
from pylab import resize, arange,imshow
from numpy import linspace,array,zeros
from scipy import interpolate

def cmap_discretize(cmap, N):
    """Return a discrete colormap from the continuous colormap cmap.
    
        cmap: colormap instance, eg. cm.jet. 
        N: Number of colors.
    
    Example
        x = resize(arange(100), (5,100))
        djet = cmap_discretize(cm.jet, 5)
        imshow(x, cmap=djet)
    """

    cdict = cmap._segmentdata.copy()
    # N colors
    colors_i = linspace(0,1.,N)
    # N+1 indices
    indices = linspace(0,1.,N+1)
    for key in ('red','green','blue'):
        # Find the N colors
        D = array(cdict[key])
        I = interpolate.interp1d(D[:,0], D[:,1])
        colors = I(colors_i)
        # Place these colors at the correct indices.
        A = zeros((N+1,3), float)
        A[:,0] = indices
        A[1:,1] = colors
        A[:-1,2] = colors
        # Create a tuple for the dictionary.
        L = []
        for l in A:
            L.append(tuple(l))
        cdict[key] = tuple(L)
    # Return colormap object.
    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)

def totuple(A):
    L = []
    for l in A:
        L.append(tuple(l))
    return tuple(L)

def midwhite(name, cmap):
    cdict = cmap._segmentdata.copy()
    for color in ["red","green","blue"]:
        A = array(cdict[color], float)
        ind = A.shape[0]/2 - 1
        A[ind:ind+2,1:] = 1.
        cdict[color] = totuple(A)
    my_cmap = matplotlib.colors.LinearSegmentedColormap(name,cdict)
    return my_cmap

if __name__ == "__main__":
    import numpy as np
    cdict = plt.cm.RdBu._segmentdata.copy()
    for color in ["red","green","blue"]:
        A = array(cdict[color], float)
        A[5,1:2] = 1.
        cdict[color] = totuple(A)
    my_cmap = matplotlib.colors.LinearSegmentedColormap('colormap',cdict)
    x = np.arange(0, np.pi, 0.1)
    y = np.arange(0, 2*np.pi, 0.1)
    X, Y = np.meshgrid(x,y)
    Z = np.cos(X) * np.sin(Y)
    plt.imshow(Z, cmap=cmap_discretize(my_cmap, 27))
    plt.colorbar()
    plt.show()