# ISO 23870-10 Physical Layer - Cables, Connectors, Cable Assemblies, and Communication Channel
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
from ISO_plotlib import ISO_Plots, FilenamingStyle



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
        f1 = np.array([1.0])
        f2 = np.logspace(np.log10(100.0), np.log10(600.0), 101)
        f = np.concatenate((f1,f2))
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
        return ISO_Plots.feval(f, ILmax_cable), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, ILmax_cable)
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
        return ISO_Plots.feval(f, RLmax_cable), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, RLmax_cable)
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
        return ISO_Plots.feval(f, LCLmax_cable), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, LCLmax_cable)
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
        return ISO_Plots.feval(f, LCTLmax_cable), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, LCTLmax_cable)
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
        return ISO_Plots.feval(f, Atten_c_class1_cable_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class1_cable_ES)
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
        return ISO_Plots.feval(f, Atten_s_class1_cable_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class1_cable_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 35.0


# return value is in dB
def Atten_s_class2_cable_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class2_cable_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class2_cable_ES)
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
        return ISO_Plots.feval(f, ILmax_cable_assy), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, ILmax_cable_assy)
    else:
        return None


# return value is in dB
def RLmax_cable_assy(f=None):
    if f is None:
        # sample at the exact corner frequencies
        f = np.array([1.0, 130.0, 400.0, 600.0])
        return ISO_Plots.feval(f, RLmax_cable_assy), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, RLmax_cable_assy)
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
        return ISO_Plots.feval(f, LCLmax_cable_assy), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, LCLmax_cable_assy)
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
        f = np.array([30.0, 100.0, 400.0, 600.0])
        return ISO_Plots.feval(f, Atten_c_class1_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class1_cable_assy_ES)
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
        return ISO_Plots.feval(f, Atten_c_class2_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class2_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 70.0


# return value is in dB
def Atten_s_class1_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class1_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class1_cable_assy_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 28.0


# return value is in dB
def Atten_s_class2_cable_assy_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class2_cable_assy_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class2_cable_assy_ES)
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
        return ISO_Plots.feval(f, ILmax_WCC_LSTB), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, ILmax_WCC_LSTB)
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
        return ISO_Plots.feval(f, ILmax_WCC_LSTA), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, ILmax_WCC_LSTA)
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
        return ISO_Plots.feval(f, RLmax_WCC), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, RLmax_WCC)
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
        return ISO_Plots.feval(f, LCLmax_WCC), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, LCLmax_WCC)
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
        return ISO_Plots.feval(f, PSANEXT_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, PSANEXT_WCC_ES)
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
        return ISO_Plots.feval(f, PSAACRF_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, PSAACRF_WCC_ES)
    elif f<1.0 or f>600.0:
        return None
    else:
        return 43.67 - 20.0*np.log10(f/100.0)


# return value is in dB
def Atten_c_class1_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 100.0, 600.0])
        return ISO_Plots.feval(f, Atten_c_class1_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class1_WCC_ES)
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
        return ISO_Plots.feval(f, Atten_c_class2_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_c_class2_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 65.0


# return value is in dB
def Atten_s_class1_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class1_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class1_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 25.0


# return value is in dB
def Atten_s_class2_WCC_ES(f=None):
    if f is None:
        f = np.array([30.0, 600.0])
        return ISO_Plots.feval(f, Atten_s_class2_WCC_ES), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Atten_s_class2_WCC_ES)
    elif f<30.0 or f>600.0:
        return None
    else:
        return 40.0


# return value is in Ohms
def Zshield_max_ECU(f=None):
    if f is None:
        f = np.array([1.0, 60.0, 600.0])
        return ISO_Plots.feval(f, Zshield_max_ECU), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Zshield_max_ECU)
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
        return ISO_Plots.feval(f, Zshield_max_ECU_DC), f
    elif type(f) is np.ndarray:
        return ISO_Plots.feval(f, Zshield_max_ECU_DC)
    else:
        return (10.0, 1.0e3)


# ==============================================================================
# Main Program Entry Point
# ==============================================================================

Plots = ISO_Plots("ISO 23870-10", "C:\\Projects\\Python\\ISO23870_Grapher\\output-10\\", ".svg")


# Whole communication channel plots
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-10\\FIG-001_ISO_23870-10_(E)_Ed1 Comm Channel Representation.png")
Plots.ISO_Plot(ILmax_WCC_LSTB, abbr="IL", unit="dB", ylim=[0.0, 20.0], xypass=(0.75,0.35), xyfail=(0.55, 0.45), figname="HSI channel insertion loss")
Plots.ISO_Plot(RLmax_WCC, abbr="RL", unit="dB", ylim=[10.0, 20.0], xypass=(0.60, 0.72), xyfail=(0.60, 0.45), figname="HSI channel return loss")
Plots.ISO_Plot(LCLmax_WCC, abbr="LCL", unit="dB", ylim=[20.0, 45.0], xypass=(0.75,0.55), xyfail=(0.6, 0.35), figname="HSI channel longitudinal conversion loss")
Plots.ISO_Plot(LCLmax_WCC, abbr="LCTL", unit="dB", ylim=[20.0, 45.0], xypass=(0.75,0.55), xyfail=(0.6, 0.35), figname="HSI channel longitudinal conversion transfer loss")
Plots.ISO_Plot(PSANEXT_WCC_ES, abbr="PSANEXT", unit="dB", ylim=[30.0, 80.0], xypass=(0.75,0.55), xyfail=(0.6, 0.35), figname="HSI channel power sum alien near-end crosstalk")
Plots.ISO_Plot(PSAACRF_WCC_ES, abbr="PSAACRF", unit="dB", ylim=[20.0, 100.0], xypass=(0.65,0.5), xyfail=(0.45, 0.25), figname="HSI channel power sum attenuation to alien crosstalk ratio")
Plots.ISO_Plot(Atten_c_class1_WCC_ES, abbr="$a_\\mathrm{c}$", unit="dB", ylim=[45.0, 70.0], xypass=[400.0, 61.5], xyfail=[120.0, 56.5], figname="HSI channel coupling attenuation")
Plots.ISO_Plot(Atten_s_class1_WCC_ES, abbr="$a_\\mathrm{s}$", unit="dB", ylim=[22.0, 28.0],  xypass=[130.0, 25.3], xyfail=[130.0, 24.6], figname="HSI channel screening attenuation")

# Cable assembly plots
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-10\\FIG-010_ISO_23870-10_(E)_Ed1 Cable Assembly Representation.png")
Plots.ISO_Plot(RLmax_cable_assy, abbr="RL", unit="dB", ylim=[10.0, 30.0], xypass=[20.0, 23.0], xyfail=[20.0, 20.5], figname="HSI cable assembly return loss")
Plots.ISO_Plot(LCLmax_cable_assy,  abbr="LCL", unit="dB", ylim=[20.0, 45.0], xypass=[140.0, 37.7], xyfail=[140.0, 30.5], figname="HSI cable assembly longitudinal conversion loss")
Plots.ISO_Plot(LCLmax_cable_assy,  abbr="LCTL", unit="dB", ylim=[20.0, 45.0], xypass=[140.0, 37.7], xyfail=[140.0, 30.5], figname="HSI cable assembly lontigudinal conversion transfer loss")
Plots.ISO_Plot(Atten_c_class1_cable_assy_ES, abbr="$a_\\mathrm{c}$", unit="dB", ylim=[55,75], xypass=[140.0, 71.0], xyfail=[140.0, 65.0], figname="HSI cable assembly coupling attenuation")
Plots.ISO_Plot(Atten_s_class1_cable_assy_ES, abbr="$a_\\mathrm{s}$", unit="dB", ylim=[20.0, 35.0], xypass=[140.0, 30.0], xyfail=[140.0, 26.0], figname="HSI cable assembly screening attenuation")

# Cable plots
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-10\\FIG-016_ISO_23870-10_(E)_Ed1 Cable Representation.png")
Plots.ISO_Plot(ILmax_cable, abbr="IL", unit='dB/m', ylim=[0.0, 1.0], xypass=[150.0, 0.25], xyfail=[50.0, 0.4], figname="HSI cable insertion loss")
Plots.ISO_Plot(RLmax_cable, abbr="RL", unit="dB", ylim=[10.0, 25.0], xypass=[80.0, 20.0], xyfail=[80.0, 17.5], figname="HSI cable return loss")
Plots.ISO_Plot(LCLmax_cable, abbr="LCL", unit="dB", ylim=[25.0, 55.0], xypass=[140.0, 47.0], xyfail=[140.0, 36.0], figname="HSI cable longitudinal conversion loss")
Plots.ISO_Plot(LCTLmax_cable, abbr="LCTL", unit="dB", ylim=[25.0, 50.0], xypass=[140.0, 45.0], xyfail=[140.0, 34.0], figname="HSI cable longitudinal conversion transfer loss")
Plots.ISO_Plot(Atten_c_class1_cable_ES, abbr="$a_\\mathrm{c}$", unit="dB", ylim=[65.0, 75.0], xypass=[140.0, 71.0], xyfail=[140.0, 69.0], figname="HSI cable coupling attenuation")
Plots.ISO_Plot(Atten_s_class1_cable_ES, abbr="$a_\\mathrm{s}$", unit="dB", ylim=[25.0, 45.0], xypass=[140.0, 36.7], xyfail=[140.0, 33.0], figname="HSI cable screening attenuation")

# Connector plots
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-10\\FIG-023_ISO_23870-10_(E)_Ed1 Inline Representation.png")
Plots.ISO_Add_External_File("C:\\Projects\\Python\\ISO23870_Grapher\\source-10\\FIG-024_ISO_23870-10_(E)_Ed1 MDI Representation.png")
Plots.ISO_Plot(ILmax_conn, abbr="IL", unit="dB", ylim=[0.0, 0.25], xypass=(0.75,0.3), xyfail=(0.6,0.5), figname="HSI connector insertion loss")
Plots.ISO_Plot(RLmax_conn, abbr="RL", unit="dB", ylim=[15.0,35.0], xypass=(0.60, 0.82), xyfail=(0.60, 0.68), figname="HSI connector return loss")
Plots.ISO_Plot(LCLmax_conn, abbr="LCL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), figname="HSI connector longitudinal conversion loss")
Plots.ISO_Plot(LCLmax_conn, abbr="LCTL", unit="dB", ylim=[30.0, 60.0], xypass=(0.7,0.55), xyfail=(0.55, 0.35), figname="HSI connector longitudinal conversion transfer loss")
Plots.ISO_Plot(PSANEXT_conn_ES, abbr="PSANEXT", unit="dB", ylim=[35.0,80.0], xypass=(0.4, 0.8), xyfail=(0.4, 0.5), figname="HSI connector power sum alien near-end crosstalk")
Plots.ISO_Plot(PSAFEXT_conn_ES, abbr="PSAFEXT", unit="dB", ylim=[20.0, 100.0], xypass=(0.4, 0.7), xyfail=(0.4, 0.4), figname="HSI connector power sum alien far-end crosstalk")
Plots.ISO_Plot(Atten_c_class1_conn_ES, abbr="$a_\\mathrm{c}$", unit="dB", ylim=[50.0, 80.0], xypass=[400.0, 63.5], xyfail=[200.0, 56.5], figname="HSI connector coupling attenuation")
Plots.ISO_Plot(Atten_s_class1_conn_ES, abbr="$a_\\mathrm{s}$", unit="dB", ylim=[10.0, 40.0], xypass=[150.0, 31.0], xyfail=[150.0, 26.0], figname="HSI connector screening attenuation")

# Generate the key and zip files
Plots.ISO_Wrapup()
