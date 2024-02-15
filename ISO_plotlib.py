# Library for creating limit plots for ISO standards
#   - Supports linear and logarithmic frequency axis
#   - Supports pass/fail or "BETTER" annotation
#   - Supports appendix numbering

# Kerry S. Martin, martin@wild-wood.net
# 2024-02-15

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axisartist.axislines import SubplotZero
import zipfile
import re
import locale


# class decorator
def static_init(cls):
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls


@static_init
class ISO_Plots:

    # ==========================================================================
    # Static initializer - setup plot settings
    # ==========================================================================

    @classmethod
    def static_init(cls):
        # called once automatically to configure locale and font settings

        # Set to German locale to get comma decimal separater
        locale.setlocale(locale.LC_NUMERIC, "de_DE")
        plt.rcdefaults()

        # Tell matplotlib to use the locale we set above
        plt.rcParams['axes.formatter.use_locale'] = True

        # Say, "the default sans-serif font is COMIC SANS"
        plt.rcParams['font.serif'] = "Cambria"  # ISO standard figure font

        # Then, "ALWAYS use sans-serif fonts"
        plt.rcParams['font.family'] = "serif"


    # ==========================================================================
    # Initializer
    # ==========================================================================

    def __init__(self, std_name, fig_dir, fig_fmt=".svg"):
        """ISO_Plots constructor

        Args:
            std_name: name of the standard (e.g., "ISO 23760-10")
            fig_fmt: type of figure plots to generate (either ".png" or ".svg")
            fig_dir: output directory (e.g., "C:\\Temp\\output\\")
        """
        self.std_name = std_name      # name of the standard (e.g., "ISO 4091")
        self.fig_dir = fig_dir        # must end with "\\"
        self.fig_fmt = fig_fmt        # ".svg" or ".png"
        self.fig_num = 0
        self.appendix = None
        self.key_table = []
        self.zip_file_list = []


    # ==========================================================================
    # Automatic figure numbering
    # ==========================================================================

    def __next_figure(self):
        self.fig_num = self.fig_num + 1
        return self.fig_num


    def ISO_Skip_Figure(self, skip=1):
        """Skip over one or more figures in the sequence without adding a file.

        Args:
            skip: Number of figures to skip. Defaults to 1.

        Returns:
            The next figure number in the sequence.
        """
        self.fig_num = self.fig_num + skip
        return self.fig_num


    # ==========================================================================
    # Handling of external files
    # ==========================================================================

    # add external file that will be zipped up with the plots
    def ISO_Add_External_File(self, filename, skip=1):
        """Add an external file to be zipped with the other plots

        Args:
            filename: Full path to the file location. May be of any type.
            skip: Number of figures to skip. Defaults to 1. Change to 0 to prevent skipping a number.
        """
        self.__AddFileToZip(filename)
        self.ISO_Skip_Figure(skip)


    # ==========================================================================
    # Handling of appendices
    # ==========================================================================

    def ISO_Start_Appendix(self, appendix=None):
        """Starts an appendix with a fresh figure numbering system

        Args:
            appendix: Appendix letter (e.g., "A", "B") Defaults to None.

            If the appendix parameter is None, it will auto-generate the appendix
            label, starting with "A" for the first call. Subsequent calls will
            use the next capital letter (i.e., "A" -> "B" -> "C", etc.)
            Appendix will always be an uppercase single letter (first letter is
            used if more than one is passed). Currently, no letters are skipped.
        """
        if appendix is None:
            if self.appendix is None:
                self.appendix = "A"
            else:
                self.appendix = chr(ord(self.appendix[0])+1)  # next character
        else:
            self.appendix = appendix.upper()[0]  # only first letter is used

        self.fig_num = 0    # start a new figure numbering counter when starting a new appendix


    # ==========================================================================
    # Generate key table
    # ==========================================================================

    def __AddKeyToFigure(self, fig, key, value):
        if self.appendix is None:
            line = f'FIG-{fig:03}\t{key}\t{value}\n'
        else:
            line = f'FIG-{self.appendix}.{fig:03}\t{key}\t{value}\n'
        self.key_table.append(line)


    def __CreateKeyTable(self):
        keyfilename = f"{self.fig_dir}{self.std_name}_(E)_KEYS.txt"
        fh = open(keyfilename, "w")
        for line in self.key_table:
            fh.write(line)
        fh.close()
        return keyfilename


    # ==========================================================================
    # Generate zip archive
    # ==========================================================================

    def __AddFileToZip(self, filename=None):
        if filename is not None:
            self.zip_file_list.append(filename)


    def __CreateZipArchive(self):
        zip_filename = f"{self.fig_dir}FIGURES-{self.std_name}_(E).zip"
        zip = zipfile.ZipFile(zip_filename, mode="w")
        for filename in self.zip_file_list:
            m = re.search(r"[^\\]+$", filename)
            shortname = m.group(0)
            zip.write(filename, arcname=shortname)
        zip.close()


    # ==========================================================================
    # Generate plots
    # ==========================================================================

    def __FigSave(self, fig, figname=None):
        if self.appendix is None:
            if figname is not None:
                savename = f"{self.fig_dir}FIG-{fig:03}_{self.std_name}_(E)_Ed1 {figname}{self.fig_fmt}"
            else:
                savename = f"{self.fig_dir}FIG-{fig:03}_{self.std_name}_(E)_Ed1{self.fig_fmt}"
        else:
            if figname is not None:
                savename = f"{self.fig_dir}FIG-{self.appendix}.{fig:03}_{self.std_name}_(E)_Ed1 {figname}{self.fig_fmt}"
            else:
                savename = f"{self.fig_dir}FIG-{self.appendix}.{fig:03}_{self.std_name}_(E)_Ed1{self.fig_fmt}"
        plt.savefig(savename)
        self.__AddFileToZip(savename)


    def ISO_Plot(self, fun, is_dc=False, title=None, abbr=None, unit=None, logx=True, xlim=None, ylim=None, yticks=None, xypass=None, xyfail=None, xyfail2=None, xybetter=None, dbetter=None, fig=None, figname=None, show=False):
        """Generate a plot for an ISO standard

        Args:
            fun: Function to be plotted.
            is_dc: Is it a DC plot (0 Hz)? Defaults to False.
            title: Title of the display on the plot. Defaults to None.
            abbr: Abbreviated Y axis quantity, used to generate the key file. Defaults to None.
            unit: Y axis unit. Defaults to None.
            logx: Logarithmic X axis? Defaults to True.
            xlim: Fixed limits for X axis [xmin, xmax] Defaults to None.
            ylim: Fixed limits for Y axis [ymin, ymax] Defaults to None.
            yticks: Sets the yticks. (?, ?) Defaults to None.
            xypass: Location for pass label. [] or ()  Defaults to None.
            xyfail: Location for fail label. [] or () Defaults to None.
            xyfail2: Location for 2nd fail label. [] or () Defaults to None.
            xybetter: Location for better label. [] or () Defaults to None.
            dbetter: Direction of better arrow. +1 or -1 Defaults to None.
            fig: Figure number to set. Defaults to None which auto numbers.
            figname: Name of the plot used for filename generation. Defaults to None.
            show: Show the figure, or just save it? Defaults to False (do not show)

            [] or () parameters
              [x, y] = coordinates in terms of axis quantities
              (x, y) = scaled coordinates 0.0 - 1.0
        """
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
            if isinstance(title, tuple) and len(title)==0:
                # an empty tuple () simply uses the figname for the title
                plt.title(figname, weight='bold')
            else:
                plt.title(title, weight='bold')

        ax.set_xlabel('F (MHz)')

        if abbr is not None:
            Yab = abbr
        else:
            Yab = 'Y'
        if unit is not None:
            ax.set_ylabel(f'{Yab} ({unit})')
        else:
            ax.set_ylabel(Yab)

        if abbr is not None and unit is not None:
            vunit = f'{abbr} ({unit})'
        elif abbr is None:
            vunit = f'LIMIT ({unit})'
        else:
            vunit = f'{abbr}'

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
            tbetter = "BETTER"   # TODO: check/change here if pass or fail is defined
            boxstyle = 'rarrow' if dbetter is None or dbetter>0 else 'larrow'
            if type(xybetter) is tuple:
                x, y = xybetter
                ax.text(x, y, tbetter, color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'), transform=trans)
            elif type(xybetter) is list:
                x, y = xybetter[0], xybetter[1]
                ax.text(x, y, tbetter, color='gray', ha='center', va='center', rotation=90, size=16, bbox=dict(boxstyle=boxstyle, ec='gray', fc='white'))

        if is_dc:
            plt.xticks([0.0], ['0'])

        if fig is None:
            fig = self.__next_figure()
        else:
            self.fig_num = fig

        self.__AddKeyToFigure(fig, "Y", vunit)

        self.__FigSave(fig, figname)

        if show:
            plt.show()

        plt.close()


    def ISO_Wrapup(self):
        """Call this after creating all plots to finish up and write a zip file
        """
        self.__AddFileToZip(self.__CreateKeyTable())
        self.__CreateZipArchive()


    # y = feval(x, fun)
    #
    # Description:
    #   Evaluates the given function at every point in 1D array x
    #
    @staticmethod
    def feval(x, fun):
        """Helper function used to evaluate a function at one or more x values

        Args:
            x: float or np.ndarray value(s) to evaluate function at
            fun: function taking and returing a single float

        Raises:
            Exception: if X is not a valid type (float or np.ndarray)

        Returns:
            float or np.ndarray depending upon the x argument
            with evaluated fun(x)
        """
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


# End of file