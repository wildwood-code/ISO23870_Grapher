# ISO 23870-3 Physical Layer - Single data channel coupling connector
# Graph Generator for the limits in the standard
#
# Limits are from "TC9" OPEN Alliance Channel and Component Requirements for 1000BASE-T1 Link Segment Type A (LSTA) Version 2.0
# or IEEE 802.3
#    connector limits
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
from ISO_plotlib import ISO_Plots


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
        return ISO_Plots.feval(f, ILmax_conn), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, ILmax_conn)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 0.01*np.sqrt(f)


# return value is in dB
def RLmax_conn(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 189.7367, 600.0])
        return ISO_Plots.feval(f, RLmax_conn), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, RLmax_conn)
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
        return ISO_Plots.feval(f, LCLmax_conn), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, LCLmax_conn)
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
        return ISO_Plots.feval(f, PSANEXT_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, PSANEXT_conn_ES)
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
        return ISO_Plots.feval(f, PSAFEXT_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, PSAFEXT_conn_ES)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 86.67 - 20.0*np.log10(f)


# return value is in dB
def Atten_c_class1_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 100.0, 600.0])
        return ISO_Plots.feval(f, Atten_c_class1_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class1_conn_ES)
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
        return ISO_Plots.feval(f, Atten_c_class2_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class2_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 70.0


# return value is in dB
def Atten_s_class1_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class1_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class1_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 28.0


# return value is in dB
def Atten_s_class2_conn_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class2_conn_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class2_conn_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 45.0


# ==============================================================================
# Main Program Entry Point
# ==============================================================================

Plots = ISO_Plots("ISO 23870-3", "C:\\Projects\\Python\\ISO23870_Grapher\\output-3\\", ".svg")

# skip the figures occurring before the plots
Plots.ISO_Skip_Figure(4)
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-3\\FIG-005_ISO_23870-3_(E)_Ed1 Connector pinout.png")
Plots.ISO_Skip_Figure(2)

# Connector plots
Plots.ISO_Plot(ILmax_conn, abbr="IL", unit="dB", ylim=[0.0, 0.25], xypass=(0.75,0.3), xyfail=(0.6,0.5), figname="Insertion loss (IL)")
Plots.ISO_Plot(RLmax_conn, abbr="RL", unit="dB", ylim=[15.0,35.0], xypass=(0.60, 0.82), xyfail=(0.60, 0.68), figname="Return loss (RL)")
Plots.ISO_Plot(LCLmax_conn, abbr="LCL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), figname="Longitudinal conversion loss (LCL)")
Plots.ISO_Plot(LCLmax_conn, abbr="LCTL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), figname="Longitudinal conversion transfer loss (LCTL)")
Plots.ISO_Plot(Atten_c_class1_conn_ES, abbr="$a_\\mathrm{c}$", unit="dB", ylim=[50.0, 80.0], xypass=[400.0, 63.5], xyfail=[200.0, 56.5], figname="Coupling attenuation")
Plots.ISO_Plot(Atten_s_class1_conn_ES, abbr="$a_\\mathrm{s}$", unit="dB", ylim=[10.0, 40.0], xypass=[150.0, 31.0], xyfail=[150.0, 26.0], figname="Screening attenuation")

# Appendix
Plots.ISO_Start_Appendix()
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-3\\FIG-A.001_ISO_23870-10_(E)_Ed1 Qualification test sequence.png")
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-3\\FIG-A.002_ISO_23870-10_(E)_Ed1 Qualification test lot B detail.png")
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-3\\FIG-A.003_ISO_23870-10_(E)_Ed1 Qualification test 1000BASE-T1 measurement sequence.png")

Plots.ISO_Wrapup()
