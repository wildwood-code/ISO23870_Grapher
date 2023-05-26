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


# ==============================================================================
# Generate Plots
# ==============================================================================

# OPEN_Plot
#
# Description:
#  Generate a plot of the specified OPEN limit with the supplied:
#    title
#    abbreviation
#    unit
#    ylimit
#    pass/fail text
#    better arrow
#    savefile
def OPEN_Plot(fun, title=None, abbr=None, unit=None, ylim=None, xypass=None, xyfail=None, xybetter=None, dbetter=None, save=None):
    y, f = fun()
    f1, f2 = np.min(f), 1000.0
    if f1<10.0:
        f1 = 1.0
    elif f1<100.0:
        f1 = 10.0
    else:
        f1 = 100.0
    plt.figure()
    ax = plt.subplot(111)
    trans = ax.transAxes
    plt.semilogx(f, y)
    plt.xlim([f1, f2])
    if ylim is not None:
        plt.ylim(ylim)
    if title is not None:
        plt.title(title, weight='bold')

    plt.xlabel('Frequency (MHz)')
    if abbr is not None and unit is not None:
        plt.ylabel(f'{abbr} ({unit})')
    elif abbr is None:
        plt.ylabel(f'LIMIT ({unit})')
    else:
        plt.ylabel(f'{abbr}')

    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.grid(visible=True, which='both')

    if xypass is not None:
        if type(xypass) is tuple:
            x, y = xypass
            ax.text(x, y, "PASS", transform=trans, weight="bold", size=16, ha='center', va='center', color='gray')
        elif type(xypass) is list:
            x, y = xypass[0], xypass[1]
            ax.text(x, y, "PASS", weight="bold", size=16, ha='center', va='center', color='gray')

    if xyfail is not None:
        if type(xyfail) is tuple:
            x, y = xyfail
            ax.text(x, y, "FAIL", transform=trans, weight="bold", size=16, ha='center', va='center', color='gray')
        elif type(xyfail) is list:
            x, y = xyfail[0], xyfail[1]
            ax.text(x, y, "FAIL", weight="bold", size=16, ha='center', va='center', color='gray')

    if xybetter is not None:
        boxstyle = 'rarrow' if dbetter is None or dbetter>0 else 'larrow'
        if type(xybetter) is tuple:
            x, y = xybetter
            ax.text(x, y, "BETTER", color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'), transform=trans)
        elif type(xybetter) is list:
            x, y = xybetter[0], xybetter[1]
            ax.text(x, y, "BETTER", color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'))

    if save is not None:
        plt.savefig(save)


# y = feval(x, fun)
#
# Description:
#   Evaluates the given function at every point in 1D array x
#
def feval(x, fun):
    if type(x) is float:
        y = fun(x)
    elif type(x) is np.ndarray:
        y = np.empty_like(x)
        it = np.nditer(x, flags=["f_index"])
        for xx in it:
            i = it.index
            y[i] = fun(float(xx))
    else:
        raise Exception("Invalid type for x. Accepts float and ndarray of float")

    return y


# ==============================================================================
# Connectors
# ------------------------------------------------------------------------------
# Defined in Section 6.1.1
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
        f = np.array([1.0, 100.0, 600.0])
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
    


if False: # Whole communication channel plots
    OPEN_Plot(ILmax_WCC_LSTA, title="Insertion Loss (IL)\nCommunication Channel (LSTA)", abbr="IL", unit="dB", ylim=[0.0, 20.0], xypass=(0.75,0.2), xyfail=(0.6, 0.4), save="C:\\Temp\\WCC_IL_LSTA.svg")
    OPEN_Plot(ILmax_WCC_LSTB, title="Insertion Loss (IL)\nCommunication Channel (LSTB)", abbr="IL", unit="dB", ylim=[0.0, 20.0], xypass=(0.75,0.35), xyfail=(0.55, 0.45), save="C:\\Temp\\WCC_IL_LSTB.svg")
    #OPEN_Plot(RLmax_WCC, title="Return Loss (RL)\nWhole Communication Channel", abbr="RL", unit="dB", ylim=[10.0, 20.0], xypass=(0.60, 0.72), xyfail=(0.60, 0.45), save="C:\\Temp\\WCC_RL.svg")
    #OPEN_Plot(LCLmax_WCC, title="Mode Conversion Loss (LCL, LCTL)\nWhole Communication Channel", abbr="LCL, LCTL", unit="dB", ylim=[20.0, 45.0], xypass=(0.75,0.55), xyfail=(0.6, 0.35), save="C:\\Temp\\WCC_LCL.svg")
    #OPEN_Plot(PSANEXT_WCC_ES, title="Near-end Crosstalk Loss (PSANEXT)\nWhole Communication Channel", abbr="PSANEXT", unit="dB", ylim=[30.0, 80.0], xypass=(0.75,0.55), xyfail=(0.6, 0.35), save="C:\\Temp\\WCC_PSAN.svg")
    #OPEN_Plot(PSAACRF_WCC_ES, title="Far-end Atten/Crosstalk Ratio (PSAACRF)\nWhole Communication Channel", abbr="PSANEXT", unit="dB", ylim=[20.0, 100.0], xypass=(0.65,0.5), xyfail=(0.45, 0.25), save="C:\\Temp\\WCC_PSAA.svg")
    #OPEN_Plot(Atten_c_class1_WCC_ES, title="Coupling Attenuation (class 1)\nWhole Communication Channel", abbr=r"$a_c$", unit="dB", ylim=[45.0, 70.0], xypass=[400.0, 61.5], xyfail=[120.0, 56.5], save="C:\\Temp\\WCC_AC.svg")
    #OPEN_Plot(Atten_s_class1_WCC_ES, title="Screening Attenuation (class 1)\nWhole Communication Channel", abbr=r"$a_s$", unit="dB", ylim=[22.0, 28.0],  xypass=[130.0, 25.3], xyfail=[130.0, 24.6], save="C:\\Temp\\WCC_AS.svg")

if False:  # Connector plots
    #OPEN_Plot(ILmax_conn, title="Insertion Loss (IL)\nConnector", abbr="IL", unit="dB", ylim=[0.0, 0.25], xypass=(0.75,0.3), xyfail=(0.6,0.5), save="C:\\Temp\\IL_conn.svg")
    #OPEN_Plot(RLmax_conn, title="Return Loss (RL)\nConnector", abbr="RL", unit="dB", ylim=[15.0,35.0], xypass=(0.60, 0.82), xyfail=(0.60, 0.68), save="C:\\Temp\\RL_conn.svg")
    #OPEN_Plot(LCLmax_conn, title="Mode Conversion Loss (LCL, LCTL)\nConnector", abbr="LCL, LCTL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), save="C:\\Temp\\LCL_conn.svg")
    #OPEN_Plot(PSANEXT_conn_ES, title="PSANEXT\nConnector", abbr="PSANEXT", unit="dB", ylim=[35.0,80.0], xypass=(0.4, 0.8), xyfail=(0.4, 0.5), save="C:\\Temp\\PSANEXT_conn.svg")
    #OPEN_Plot(PSAFEXT_conn_ES, title="PSAFEXT\nConnector", abbr="PSAFEXT", unit="dB", ylim=[20.0, 100.0], xypass=(0.4, 0.7), xyfail=(0.4, 0.4), save="C:\\Temp\\PSAFEXT_conn.svg")
    #OPEN_Plot(Atten_c_class1_conn_ES, title="Coupling Attenuation (class 1)\nConnector", abbr="$a_c$", unit="dB", ylim=[50.0, 80.0], xypass=[400.0, 63.5], xyfail=[200.0, 56.5], save="C:\\Temp\\Atten_c_conn.svg")
    OPEN_Plot(Atten_s_class1_conn_ES, title="Screening Attenuation (class 1)\nConnector", abbr="$a_s$", unit="dB", ylim=[10.0, 40.0], xypass=[150.0, 31.0], xyfail=[150.0, 26.0], save="C:\\Temp\\Atten_s_conn.svg")

if True:  # Cable plots
    #OPEN_Plot(ILmax_cable, title="Insertion Loss (IL)\nCable", abbr="IL", unit='dB/m', ylim=[0.0, 1.0], xypass=[150.0, 0.25], xyfail=[50.0, 0.4], save="C:\\Temp\\IL_cable.svg")
    OPEN_Plot(RLmax_cable, title="Return Loss (RL)\nCable", abbr="RL", unit="dB", ylim=[10.0, 25.0], xypass=[80.0, 20.0], xyfail=[80.0, 17.5], save="C:\\Temp\\RL_cable.svg")
plt.show()