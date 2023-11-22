import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import mpl_toolkits.axisartist.axislines as axl
import zipfile
import re



# semilogx plot with axis arrows to fit ISO drafting requirements

def feval(x, fun):
    if type(x) is float:
        y = fun(x)
    elif type(x) is np.ndarray:
        y = None
        it = np.nditer(x, flags=["f_index"])
        for xx in it:
            i = it.index
            v = fun(float(xx))
            if y is None:
                y = np.empty(x.shape, dtype=type(v))
            y[i] = v
    else:
        raise Exception("Invalid type for x. Accepts float and ndarray of float")

    return y

# return value is in dB (IEEE 802.3bp 97.6.2.1)
def ILmax_WCC_LSTB(f=None):
    if f is None:
        # sample at 101 points, log spaced, across the range the limit is defined
        f = np.logspace(np.log10(1.0), np.log10(600.0), 101)
        return feval(f, ILmax_WCC_LSTB), f
    elif type(f) is np.ndarray:
        return feval(f, ILmax_WCC_LSTB)
    elif f<1.0 or f>600.0:
        return None
    else:
        sqf = np.sqrt(f)
        return 0.0040*f + (0.7131+0.08+0.018)*sqf + 0.1100/sqf


# calculate the data
y, f = ILmax_WCC_LSTB()
f1, f2 = 1.0, 1000.0             # frequency range

fh = plt.figure()                 # create an empty figure
ax = axl.SubplotZero(fh, 111)     # create a single axis subplot
fh.add_subplot(ax)
for dir in ["left", "bottom"]:
    ax.axis[dir].set_axisline_style("-|>")
    ax.axis[dir].set_visible(True)
for dir in ["right", "top"]:
    ax.axis[dir].set_visible(False)

plt.semilogx(f, y)
fh.show()
_ = input('Enter to continue')
