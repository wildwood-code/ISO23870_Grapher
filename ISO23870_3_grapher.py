# ISO 23870 Physical Layer - Cables, Connectors, Cable Assemblies, and Communication Channel
# Graph Generator for the limits in the standard
#
# Limits are from "TC9" OPEN Alliance Channel and Component Requirements for 1000BASE-T1 Link Segment Type A (LSTA) Version 2.0
# or IEEE 802.3
#    cable limits
#    connector limits
#    cable assembly limits
#    communication channel limits
#
#  SCC = Standalone Communication Channel = 2 PCB connectors, cable, and up to 4 inline connectors
#  WCC = Whole Communication Channel = SCC + PCB end connectors
#  ES = Environmental System = power and signal cables for other applications
#
# Python code is written by Kerry S. Martin (company John Deere) for his work
# on JWG 16 to write the physical layer standards for ISO 23870
#
#
# Contact:
# Kerry S. Martin
# MartinKerryS@JohnDeere.com
# martin@wild-wood.net
#
# Several of the piecewise limits given in "TC9" have discontinuities at the corner frequencies.
# The limits generated here meet the intent of the limits in "TC9" by correcting the lines
# to meet at the endpoints.
# Most are linear when plotted as dB versus log frequency

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axisartist.axislines import SubplotZero
import zipfile
import re
import locale




# ==============================================================================
# Global variables
# ==============================================================================

# Standard definitions
STD_NAME = "ISO_23870-3"

# Key table
KEY_TABLE = []

# Zip archive
ZIP_FILE_LIST = []

# Output directory and format
FIG_DIR = "C:\\Projects\\Python\\ISO23870_Grapher\\output-3\\"     # must end with backslash
FIG_FORMAT = ".png"   # .png or .svg    # must begin with period


# ==============================================================================
# Locale and Font Settings
# ==============================================================================

# Set to German locale to get comma decimal separater
locale.setlocale(locale.LC_NUMERIC, "de_DE")
plt.rcdefaults()

# Tell matplotlib to use the locale we set above
plt.rcParams['axes.formatter.use_locale'] = True

# ISO standard figure font
ISO_FONT = "Cambria"

# Say, "the default sans-serif font is COMIC SANS"
plt.rcParams['font.serif'] = ISO_FONT

# Then, "ALWAYS use sans-serif fonts"
plt.rcParams['font.family'] = "serif"


# ==============================================================================
# Generate Key Table
# ==============================================================================

def AddKeyToFigure(fig, key, value):
    global KEY_TABLE
    line = f'FIG{fig:03}\t{key}\t{value}\n'
    KEY_TABLE.append(line)


def CreateKeyTable(filename):
    global KEY_TABLE
    fh = open(filename, "w")
    for line in KEY_TABLE:
        fh.write(line)
    fh.close()


# ==============================================================================
# Generate Zip Archive
# ==============================================================================

def AddFileToZip(filename=None):
    global ZIP_FILE_LIST
    if filename is not None:
        ZIP_FILE_LIST.append(filename)


def CreateZipArchive():
    global ZIP_FILE_LIST
    global FIG_DIR
    global STD_NAME
    zip_filename = f"{FIG_DIR}FIGURES-{STD_NAME}_(E).zip"
    zip = zipfile.ZipFile(zip_filename, mode="w")
    for filename in ZIP_FILE_LIST:
        m = re.search(r"[^\\]+$", filename)
        shortname = m.group(0)
        zip.write(filename, arcname=shortname)
    zip.close()


# ==============================================================================
# Generate Plots
# ==============================================================================

def FIGURE_FigSave(fig, figname=None):
    global FIG_DIR
    global STD_NAME
    global FIG_FORMAT
    global PLOT_LANGUAGE
    global STD_LANGUAGE
    global ISO_FONT

    if figname is not None:
        savename = f"{FIG_DIR}FIG-{fig:03}_{STD_NAME}_(E)_Ed1 {figname}{FIG_FORMAT}"
    else:
        savename = f"{FIG_DIR}FIG-{fig:03}_{STD_NAME}_(E)_Ed1{FIG_FORMAT}"
    plt.savefig(savename)
    AddFileToZip(savename)


# OPEN_Plot
#
# Description:
#  Generate a plot of the specified OPEN limit

def OPEN_Plot(fun, is_dc=False, title=None, abbr=None, unit=None, logx=True, xlim=None, ylim=None, yticks=None, xypass=None, xyfail=None, xyfail2=None, xybetter=None, dbetter=None, save=None, fig=None, figname=None):
    global FIG_DIR
    global STD_NAME
    global FIG_FORMAT

    y, f = fun()

    if type(y[0]) is tuple:
        is_multi = True
        n_traces = len(y[0])
        y = map(np.array, y)
        y = np.array(list(y))
    else:
        is_multi = False

    fh = plt.figure()
    ax = SubplotZero(fh, 111)
    fh.add_subplot(ax)
    trans = ax.transAxes
    if False:
        # TODO: may need to improve the DC (for now it is same as AC plots)
        for dir in ["yzero", "bottom"]:
            ax.axis[dir].set_axisline_style("-|>")
            ax.axis[dir].set_visible(True)
        for dir in ["left", "right", "top"]:
            ax.axis[dir].set_visible(False)
    else:
        for dir in ["left", "bottom"]:
            ax.axis[dir].set_axisline_style("-|>")
            ax.axis[dir].set_visible(True)
        for dir in ["right", "top"]:
            ax.axis[dir].set_visible(False)

    if is_dc:
        fd = np.max(f)-np.min(f)
        fc = 0.5*(np.max(f)+np.min(f))
        f1, f2 = fc-fd, fc+fd

        if is_multi:
            for idx in range(n_traces):
                yt = y[:,idx]
                plt.semilogy(f, yt, 'b-')
        else:
            plt.semilogy(f, y, 'b-')

    else:
        f1, f2 = np.min(f), 1000.0
        if f1<10.0:
            f1 = 1.0
        elif f1<100.0:
            f1 = 10.0
        else:
            f1 = 100.0

        if is_multi:
            for idx in range(n_traces):
                yt = y[:,idx]
                if logx:
                    plt.semilogx(f,yt)
                else:
                    plt.plot(f,yt)
        else:
            if logx:
                plt.semilogx(f, y)
            else:
                plt.plot(f,y)

    if xlim is not None:
        plt.xlim(xlim)
    else:
        plt.xlim([f1, f2])
    if ylim is not None:
        plt.ylim(ylim)
    if yticks is not None:
        ax.set_yticks(yticks[0], yticks[1])
    if title is not None:
        plt.title(title, weight='bold')


    ax.set_xlabel('F (MHz)')
    if unit is not None:
        ax.set_ylabel(f'Y ({unit})')
    else:
        ax.set_ylabel('Y')


    if abbr is not None and unit is not None:
        vunit = f'{abbr} ({unit})'
    elif abbr is None:
        vunit = f'LIMIT ({unit})'
    else:
        vunit = f'{abbr}'
    if fig is not None:
        AddKeyToFigure(fig, "Y", vunit)

    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.grid(visible=True, which='both')

    if xypass is not None:
        if type(xypass) is tuple:
            x, y = xypass
            ax.text(x, y, "(1)", transform=trans, weight="bold", size=16, ha='center', va='center', color='gray')
        elif type(xypass) is list:
            x, y = xypass[0], xypass[1]
            ax.text(x, y, "(1)", weight="bold", size=16, ha='center', va='center', color='gray')

    if xyfail is not None:
        if type(xyfail) is tuple:
            x, y = xyfail
            ax.text(x, y, "(2)", transform=trans, weight="bold", size=16, ha='center', va='center', color='gray')
        elif type(xyfail) is list:
            x, y = xyfail[0], xyfail[1]
            ax.text(x, y, "(2)", weight="bold", size=16, ha='center', va='center', color='gray')

    if xyfail2 is not None:
        if type(xyfail2) is tuple:
            x, y = xyfail2
            ax.text(x, y, "(2)", transform=trans, weight="bold", size=16, ha='center', va='center', color='gray')
        elif type(xyfail2) is list:
            x, y = xyfail2[0], xyfail2[1]
            ax.text(x, y, "(2)", weight="bold", size=16, ha='center', va='center', color='gray')


    if xybetter is not None:
        tbetter = "(1)"   # TODO: check/change here if pass or fail is defined
        boxstyle = 'rarrow' if dbetter is None or dbetter>0 else 'larrow'
        if type(xybetter) is tuple:
            x, y = xybetter
            ax.text(x, y, tbetter, color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'), transform=trans)
        elif type(xybetter) is list:
            x, y = xybetter[0], xybetter[1]
            ax.text(x, y, tbetter, color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'))
    if is_dc:
        plt.xticks([0.0], ['0'])

    if save is not None:
        plt.savefig(save)

    if fig is not None:
        FIGURE_FigSave(fig, figname)

    if save is None and fig is None:
        plt.show()

    plt.close()


# y = feval(x, fun)
#
# Description:
#   Evaluates the given function at every point in 1D array x
#
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


# ==============================================================================
# Connectors
# ------------------------------------------------------------------------------
# Defined in Section 6.1.1; ES defined in 6.2.1
# ==============================================================================

# return value is in dB
def ILmax_conn(f=None):
    if f is None:
        # sample at 101 points, log spaced, across the range the limit is defined
        f = np.logspace(np.log10(1.0), np.log10(600.0), 101)
        return feval(f, ILmax_conn), f
    elif type(f) is np.ndarray:
        return feval(f, ILmax_conn)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 0.01*np.sqrt(f)


# return value is in dB
def RLmax_conn(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 189.7367, 600.0])
        return feval(f, RLmax_conn), f
    elif type(f) is np.ndarray:
        return feval(f, RLmax_conn)
    elif f<1.0 or f>600.0:
        return None
    elif f<=189.7367:
        return 30.0
    else:
        return 20.0 - 20.0 * np.log10(f/600.0)


# return value is in dB
def LCLmax_conn(f=None):
    if f is None:
        f = np.array([10.0, 50.0, 600.0])
        return feval(f, LCLmax_conn), f
    elif type(f) is np.ndarray:
        return feval(f, LCLmax_conn)
    elif f<10.0 or f>600.0:
        return None
    elif f<=50.0:
        return 50.0
    else:
        return 75.1890 - 14.8261*np.log10(f)


# return value is in dB
def LCTLmax_conn(f=None):
    # LCTL limit is the same as the LCL limit for connector
    return LCLmax_conn(f)


# return value is in dB
def PSANEXT_conn_ES(f=None):
    if f is None:
        f = np.array([1.0, 100.0, 600.0])
        return feval(f, PSANEXT_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, PSANEXT_conn_ES)
    elif f<1.0 or f>600.0:
        return None
    elif f<=100.0:
        return 77.0 - 10.0*np.log10(f)
    else:
        return 87.0 - 15.0*np.log10(f) - 6.0*(f-100.0)/400.0


# return value is in dB
def PSAFEXT_conn_ES(f=None):
    if f is None:
        f = np.array([1.0, 600.0])
        return feval(f, PSAFEXT_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, PSAFEXT_conn_ES)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 86.67 - 20.0*np.log10(f)


# return value is in dB
def Atten_c_class1_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 100.0, 600.0])
        return feval(f, Atten_c_class1_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class1_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    elif f<=100.0:
        return 70.0
    else:
        return 108.5529 - 19.2765*np.log10(f)


# return value is in dB
def Atten_c_class2_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_c_class2_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class2_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 70.0


# return value is in dB
def Atten_s_class1_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class1_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class1_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 28.0


# return value is in dB
def Atten_s_class2_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class2_conn_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class2_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 45.0


# ==============================================================================
# Cables
# ------------------------------------------------------------------------------
# Defined in Section 6.1.2; ES define in Section 6.2.2
# Values are specified for maximum length = 15 m
# ==============================================================================

# return value is dB/m
def ILmax_cable(f=None):
    if f is None:
        # sample at 101 points, log spaced, across the range the limit is defined
        f = np.logspace(np.log10(1.0), np.log10(600.0), 101)
        return feval(f, ILmax_cable), f
    elif type(f) is np.ndarray:
        return feval(f, ILmax_cable)
    elif f<1.0 or f>600.0:
        return None
    else:
        sqf = np.sqrt(f)
        return (0.0023*f + (0.5907-6.0*0.01)*sqf + 0.0639/sqf) / 15.0


# return value is dB/m
def RLmax_cable(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 10.0, 40.0, 130.0, 400.0, 600.0])
        return feval(f, RLmax_cable), f
    elif type(f) is np.ndarray:
        return feval(f, RLmax_cable)
    elif f<1.0 or f>600.0:
        return None
    elif f<10.0:
        return 22.0
    elif f<40.0:
        return 26.9829 - 4.9829*np.log10(f)
    elif f<=130.0:
        return 19.0
    elif f<400.0:
        return 40.65408 - 10.24345*np.log10(f)
    else:
        return 14.0


# return value is dB/m
def LCLmax_cable(f=None):
    if f is None:
        f = np.array([10.0, 50.0, 600.0])
        return feval(f, LCLmax_cable), f
    elif type(f) is np.ndarray:
        return feval(f, LCLmax_cable)
    elif f<10.0 or f>600.0:
        return None
    elif f<=50.0:
        return 50.0
    else:
        return 81.4863 - 18.5326*np.log10(f)


# return value is dB/m
def LCTLmax_cable(f=None):
    if f is None:
        f = np.array([10.0, 50.0, 600.0])
        return feval(f, LCTLmax_cable), f
    elif type(f) is np.ndarray:
        return feval(f, LCTLmax_cable)
    elif f<10.0 or f>600.0:
        return None
    elif f<=50.0:
        return 46.0
    else:
        return 71.1890 - 14.8261*np.log10(f)


# return value is in dB
def Atten_c_class1_cable_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_c_class1_cable_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class1_cable_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 70.0


def Atten_c_class2_cable_ES(f=None):
    return Atten_c_class1_cable_ES(f)


# return value is in dB
def Atten_s_class1_cable_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class1_cable_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class1_cable_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 35.0


# return value is in dB
def Atten_s_class2_cable_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class2_cable_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class2_cable_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 45.0


# ==============================================================================
# Cable Assembly (Cable Segment with no inline connectors)
# ------------------------------------------------------------------------------
# Defined in Section 6.1.3; ES defined in Section 6.2.3
# ==============================================================================

# return value is in dB
def ILmax_cable_assy(f=None):
    # There is no limit on IL for an SCC cable segment (returns None for all freq)
    if f is None:
        # sample at 101 points, log spaced, across the range the limit is defined
        f = np.array([1.0, 600.0])
        return feval(f, ILmax_cable_assy), f
    elif type(f) is np.ndarray:
        return feval(f, ILmax_cable_assy)
    else:
        return None


# return value is in dB
def RLmax_cable_assy(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 130.0, 400.0, 600.0])
        return feval(f, RLmax_cable_assy), f
    elif type(f) is np.ndarray:
        return feval(f, RLmax_cable_assy)
    elif f<1.0 or f>600.0:
        return None
    elif f<=130.0:
        return 22.0
    elif f<400.0:
        return 56.6465 - 16.3895*np.log10(f)
    else:
        return 14.0


# return value is in dB
def LCLmax_cable_assy(f=None):
    if f is None:
        f = np.array([10.0, 50.0, 600.0])
        return feval(f, LCLmax_cable_assy), f
    elif type(f) is np.ndarray:
        return feval(f, LCLmax_cable_assy)
    elif f<10.0 or f>600.0:
        return None
    elif f<=50.0:
        return 41.0
    else:
        return 66.1890 - 14.8261*np.log10(f)


# return value is in dB
def LCTLmax_cable_assy(f=None):
    # LCTL limit is the same as the LCL limit for cable assemblies
    return LCLmax_cable_assy(f)


# return value is in dB
def Atten_c_class1_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 100.0, 600.0])
        return feval(f, Atten_c_class1_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class1_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    elif f<=100.0:
        return 70.0
    elif f<=400.0:
        return 99.8974 - 14.9487*np.log10(f)
    else:
        return 75.7768 - 5.6789*np.log10(f)


# return value is in dB
def Atten_c_class2_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_c_class2_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class2_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 70.0


# return value is in dB
def Atten_s_class1_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class1_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class1_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 28.0


# return value is in dB
def Atten_s_class2_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class2_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class2_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 45.0


# ==============================================================================
# Whole Communication Channel
# ------------------------------------------------------------------------------
# Defined in Section 6.1.4; ES defined in section 6.2.4
# ==============================================================================

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


# return value is in dB
def ILmax_WCC_LSTA(f=None):
    if f is None:
        # sample at 101 points, log spaced, across the range the limit is defined
        f = np.logspace(np.log10(1.0), np.log10(600.0), 101)
        return feval(f, ILmax_WCC_LSTA), f
    elif type(f) is np.ndarray:
        return feval(f, ILmax_WCC_LSTA)
    elif f<1.0 or f>600.0:
        return None
    else:
        sqf = np.sqrt(f)
        return 0.0023*f + 0.5907*sqf + 0.0639/sqf



# return value is in dB
def RLmax_WCC(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 10.0, 40.0, 130.0, 400.0, 600.0])
        return feval(f, RLmax_WCC), f
    elif type(f) is np.ndarray:
        return feval(f, RLmax_WCC)
    elif f<1.0 or f>600.0:
        return None
    elif f<10.0:
        return 19.0
    elif f<40.0:
        # corrected for error in OPEN standard
        return 23.9829 - 4.9829*np.log10(f)
    elif f<=130.0:
        return 16.0
    elif f<400.0:
        return 37.65408 - 10.24345*np.log10(f)
    else:
        return 11.0


# return value is in dB
def LCLmax_WCC(f=None):
    if f is None:
        f = np.array([10.0, 50.0, 600.0])
        return feval(f, LCLmax_WCC), f
    elif type(f) is np.ndarray:
        return feval(f, LCLmax_WCC)
    elif f<10.0 or f>600.0:
        return None
    elif f<=50.0:
        return 41.0
    else:
        return 66.1890 - 14.8261*np.log10(f)


# return value is in dB
def LCTLmax_WCC(f=None):
    # LCTL limit is the same as the LCL limit for cable assemblies
    return LCLmax_WCC(f)


# return value is in dB
def PSANEXT_WCC_ES(f=None):
    if f is None:
        f1 = np.array([1.0])
        f2 = np.logspace(np.log10(100.0), np.log10(600.0), 101)
        f = np.concatenate((f1,f2))
        return feval(f, PSANEXT_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, PSANEXT_WCC_ES)
    elif f<1.0 or f>600.0:
        return None
    elif f<=100.0:
        return 74.0 - 10.0*np.log10(f)
    else:
        return 84.0 - 15.0*np.log10(f) - 6.0*(f-100.0)/400.0


# return value is in dB
def PSAACRF_WCC_ES(f=None):
    if f is None:
        f = np.array([1.0, 600.0])
        return feval(f, PSAACRF_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, PSAACRF_WCC_ES)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 43.67 - 20.0*np.log10(f/100.0)


# return value is in dB
def Atten_c_class1_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 100.0, 600.0])
        return feval(f, Atten_c_class1_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class1_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    elif f<=100.0:
        return 65.0
    else:
        return 103.5529 - 19.2765*np.log10(f)


# return value is in dB
def Atten_c_class2_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_c_class2_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_c_class2_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 65.0


# return value is in dB
def Atten_s_class1_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class1_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class1_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 25.0


# return value is in dB
def Atten_s_class2_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return feval(f, Atten_s_class2_WCC_ES), f
    elif type(f) is np.ndarray:
        return feval(f, Atten_s_class2_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 40.0


# return value is in Ohms
def Zshield_max_ECU(f=None):
    if f is None:
        f = np.array([1.0, 60.0, 600.0])
        return feval(f, Zshield_max_ECU), f
    elif type(f) is np.ndarray:
        return feval(f, Zshield_max_ECU)
    elif f<1.0 or f>600.0:
        return None
    elif f<=60.0:
        return 10.0
    else:
        return 10.0 + 60.0 * np.log10(f/60.0)


# return value is in kOhms
def Zshield_max_ECU_DC(f=None):
    if f is None:
        f = np.array([-0.1, 0.1])
        return feval(f, Zshield_max_ECU_DC), f
    elif type(f) is np.ndarray:
        return feval(f, Zshield_max_ECU_DC)
    else:
        return (10.0, 1.0e3)


# ==============================================================================
# Automatic Figure Numbering
# ==============================================================================

FIGURE = 1
def next_figure():
    global FIGURE
    this_figure = FIGURE
    FIGURE = FIGURE + 1
    return this_figure

def skip_figure(skip=1):
    global FIGURE
    FIGURE = FIGURE + skip
    return None


# ==============================================================================
# Main Program Entry Point
# ==============================================================================

# skip the figures occurring before the plots
skip_figure(8)

# Connector plots
OPEN_Plot(ILmax_conn, abbr="IL", unit="dB", ylim=[0.0, 0.25], xypass=(0.75,0.3), xyfail=(0.6,0.5), fig=next_figure(), figname="Insertion Loss (IL) Connector")
OPEN_Plot(RLmax_conn, abbr="RL", unit="dB", ylim=[15.0,35.0], xypass=(0.60, 0.82), xyfail=(0.60, 0.68), fig=next_figure(), figname="Return Loss (RL) Connector")
OPEN_Plot(LCLmax_conn, abbr="LCL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), fig=next_figure(), figname="Mode Conversion Loss (LCL) Connector")
OPEN_Plot(LCLmax_conn, abbr="LCTL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), fig=next_figure(), figname="Mode Conversion Loss (LCTL) Connector")
OPEN_Plot(Atten_c_class1_conn_ES, abbr="$a_c$", unit="dB", ylim=[50.0, 80.0], xypass=[400.0, 63.5], xyfail=[200.0, 56.5], fig=next_figure(), figname="Coupling Attenuation Connector")
OPEN_Plot(Atten_s_class1_conn_ES, abbr="$a_s$", unit="dB", ylim=[10.0, 40.0], xypass=[150.0, 31.0], xyfail=[150.0, 26.0], fig=next_figure(), figname="Screening Attenuation Connector")


keyfilename = f"{FIG_DIR}{STD_NAME}_(E)_KEYS.txt"
CreateKeyTable(keyfilename)
AddFileToZip(keyfilename)
CreateZipArchive()
