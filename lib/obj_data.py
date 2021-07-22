from enum import Enum
import pickle
import sys
from typing import Dict, Optional
import dill
import datetime as dt
from textwrap import fill
from .ui_conf import UI_CONF, COLORS, LINEWIDTH_DEFAULT
import traceback


class Extended_Enum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def index(cls, _type):
        return list(cls).index(_type)


class CurveType(Extended_Enum):
    '''Common acoustic test data types.'''
    NoType = 'None'
    SPL = 'SPL'
    IMP = 'Impedance'
    PHS = 'Phase'
    THD = 'THD'
    EXC = 'Excursion'
    ALL = 'All'


class Project():
    '''
    The top level of data structure.
    It contains general infomation and configuration of the project.

    :ivar dict info: general infomation including name, file location, create time, last saved time.
    :ivar List(FileData) files: files imported in this project.
    :ivar dict ui_cong: user interface configuration.
    '''

    def __init__(self, name: str = "Untitled") -> None:
        self.info = {
            "Name": name,
            "File Location": sys.path[0],
            'Create Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Last Saved Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
        }
        self.files = []
        self.ui_conf = UI_CONF
        print("::: initial location: ", sys.path[0])

    def get_path(self) -> None:
        """Return absolute path of this project file location in user's computer."""
        return self.info['File Location'] + '/' + self.info['Name'] + '.pkl'

    def append_file(self, file) -> None:
        """
        Append a file to this Project instance.

        :param FileData file: Given FileData instance.
        """
        self.files.append(file)

    def delete_files(self, files) -> None:
        """
        Delete specific files from this Project instance.

        :param List(FileData) files: A list of FileData instance.
        """
        for _f in files:
            self.files.remove(_f)

    def clear_files(self) -> None:
        """Clear all the files in this Project instance."""
        self.files = []

    @classmethod
    def _check_attr(self, pj):
        if pj.__dict__.keys() is not Project().__dict__.keys():
            print("Not the same", )
            print("\tpj.__dict__.keys(): ", pj.__dict__.keys())
            print("\tProject.__dict__.keys(): ", Project().__dict__.keys())
            li1 = pj.__dict__.keys()
            li2 = Project().__dict__.keys()

            print("Difference:", list(set(li1) - set(li2)) +
                  list(set(li2) - set(li1)))

    @ classmethod
    def load_project(cls, location: Optional[str] = None) -> None:
        """
        Retrieve project's data from a computer file on specific location.

        :param Optional[str] location: The absolute path of a computer file(/.pkl).
        """
        print("\nLoad Project____")

        if location == "None":
            print("location: None --> create Untitled project")
            return Project()
        else:
            print("location: ", location)
            try:
                fh = open(location, 'rb')
                # with open(f"%s.pkl" % (location), 'rb') as fh:
                unpickled_project = pickle.load(fh)
                if location is not unpickled_project.get_path():
                    print(location, unpickled_project.get_path())
                    print(
                        "WARNING: File location not the same ===> change project info.")
                    print(unpickled_project.info["File Location"])
                    print(location[0:location.rfind('/')])
                    unpickled_project.info["File Location"] = location[0:location.rfind(
                        '/')]
                unpickled_project.print()
                # Project._check_attr(unpickled_project)
                print("____________finish obj_data.Project.load_project()")
                fh.close()
                return unpickled_project
            except Exception as e:
                return Project()

    def dump(self, location: Optional[str] = None) -> None:
        """
        Save project's data to computer file on specific location.

        :param Optional[str] location: The absolute path of a folder.
        """

        if not location:
            location = self.get_path()
        try:
            with open(location, 'wb') as fh:
                self.info["Last Saved Time"] = dt.datetime.today().strftime(
                    "%Y/%m/%d %H:%M:%S")
                self.print()
                pickle.dump(self, fh)
                print("____________finish obj_data.Project.dump()")

        except Exception as e:
            error_class = e.__class__.__name__
            detail = e.args[0]
            cl, exc, tb = sys.exc_info()
            # print(cl, exc, tb)
            lastCallStack = traceback.extract_tb(tb)[-1]
            fileName = lastCallStack[0]
            lineName = lastCallStack[1]
            funcName = lastCallStack[2]
            print("#########  Error Message   #########\n")
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
                fileName, lineName, funcName, error_class, detail)
            print(errMsg)
            print("\n####################################")

    def print(self) -> None:
        """Print the infomation of this Project instance."""
        # msg = ""
        # msg += "\nProject: ================="
        # msg += ("____keys: ", self.__dict__.keys())
        # msg += ("Name: %s \nFile location: %s" %
        #         (self.info["Name"], self.get_path()))
        # msg += "============================\n"

        print("\nProject: =================")
        print("____keys: ", self.__dict__.keys())
        print("Name: %s \nFile location: %s" %
              (self.info["Name"], self.get_path()))
        # for _f in self.files:
        #     _f.print()
        print("============================\n")
        # return msg

#### Undo #####
    def update_ui_conf(self):
        self.ui_conf["MyCanvas"]["mode"] = self.wg_canvas.mode
        for mode, canvas_set in self.wg_canvas.status.items():
            self.ui_conf["MyCanvas"]["status"][mode] = [
                _c.id for _c in canvas_set]
        for _c in self.wg_canvas.canvasPool:
            self.ui_conf["MyCanvas"]["canvasPool"][str(_c.id)]["types"] = [
                _t.value for _t in _c.ax_types]
            self.ui_conf["MyCanvas"]["canvasPool"][str(
                _c.id)]["parameter"] = _c.parameter


class FileData():
    '''
    The 2nd level of data structure.
    It contains general infomation of an imported files.

    :ivar Dict info: general infomation including name, source, file path, create time, last modified time.
    :ivar List(str) testnames: a list of all testnames.
    :ivar List(str) valid_testnames:
            a list of testnames that is visible and operatable in app, which is customized by user.
    :ivar Dict measurements: user interface configuration.
    '''

    def __init__(self, name=None, source=None, file_path=None, import_time=None):
        self.info = {
            "Name": name,
            "Source": source,
            "File Path": file_path,
            'Import Time': import_time,
            'Last Modified Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
        }
#### Undo #####
        self.testnames = []
        self.valid_testnames = []
        self.measurements = {}

    def get_import_time(self) -> str:
        "Return imported time of this FileData instance."
        return self.info["Import Time"].strftime("%Y/%m/%d %H:%M:%S")

    def append_measurement(self, m_idx: int, measurement) -> None:
        """
        Append a measurement to this FileData instance.

        :param int m_idx: Index of the measurement.
        :param Measurement measurement: Given Measurement instance.
        """
        self.measurements[str(m_idx)] = measurement

#### Undo #####
    def __setstate__(self, state):
        self.__dict__.update(state)
        print(state)
        # Add baz back since it doesn't exist in the pickle
        # if "valid_testnames" not in self.__dict__.keys():
        #     self.valid_testnames = self.testnames

    def print(self):
        """Print the infomation of this FileData instance."""
        msg = "------------"
        msg += ("\n\tName: %s \n\tSource: %s \n\tfile_path: %s" %
                (self.info["Name"], self.info["Source"], self.info["File Path"]))
        msg += ("\n\tImport time: %s" % str(self.get_import_time()))
        msg += "\n\tSequence:"
        # for _k, _v in self.sequence.items():
        #     msg += ("\n\t  Key: %s" % _k)
        #     msg += ("\n\t  Curves: ")
        #     for _c in _v:
        #         msg += (f"\n\t\t%s, %s, %s" %
        #                 (_c.type.value, _c.label, _c.note))
        for _m in self.measurements.values():
            msg += _m.print()
        msg += ("\n-----------------------------")
        print(msg)
        return msg


class Measurement:
    '''
    The 3rd level of data structure.

    :ivar int id: index of this measurement.
    :ivar List(Channel) channel: a list of Channel instances in this Measurement instance.
    '''

    def __init__(self, channel_count=1, id=None):
        self.id = id
        self.channel = []
        self.init_channels(channel_count)

    def init_channels(self, count: int) -> None:
        """
        Create given numbers of Channel instances for this Measurement instance.

        :param int count: Total numbers of channels.
        """
        for i in range(count):
            self.channel.append(Channel(self, i+1))

    def print(self, console=True):
        """Print the infomation."""
        msg = ""
        msg += f"Measurement____id={self.id}\n"

        for c in self.channel:
            msg += "%s" % c.print(False)
        if (console):
            print(msg)
        return msg


class Channel:
    '''
    The 4th level of data structure.

    :ivar Measurement measurement_obj: The Measurement instance this Channel instance belongs to.
    :ivar int id: Channel's id.
    :ivar Dict sequence: A dictionary of testname and its corresponding CurveData instance.
    '''

    def __init__(self, measurement_obj=None, id=None):
        self.measurement_obj = measurement_obj
        self.id = id
        self.sequence = {}

    def print(self, console=True):
        """Print the infomation."""
        msg = f"Channel____id={self.id}\n"
        msg += "  Sequence:\n"
        for test, curve in self.sequence.items():
            msg += f"\t{test}: {curve}\n"
        if (console):
            print(msg)
        return msg


class CurveData:
    '''
    The bottom (5th) level of data structure.

    :ivar Channel channel_obj: The Channel instance this CurveData instance belongs to.
    :ivar List(float) xdata: Curve's data of x-axis.
    :ivar List(float) ydata: Curve's data of y-axis.
    :ivar str label: Curve's label.
    :ivar str note: Curve's note.
    :ivar CurveType _type: Curve's data category.
    :ivar List(str) units: Units of xdata and ydata.
    :ivar float shifted: Recorded offset value.
    :ivar matplotlib.lines.Line2D line: Matplolib Line2D object created by this CurveData instance.
    :ivar Dict line_props: style properties of ``line``.
    '''

    def __init__(self, xdata, ydata, channel_obj, label: str = "Curve", note: str = "",
                 _type=CurveType.NoType, units=[]):
        self.channel_obj = channel_obj
        self.xdata = xdata
        self.ydata = ydata
        self.label = label
        self.note = note
        self.type = _type
        self.units = units
        self.shifted = 0
        self.line = None
        self.line_props = {
            "visible": False,
            "color": "",
            "linewidth": LINEWIDTH_DEFAULT,
        }

  # Get and Set Function
    def get_legend(self, legend_wrap: int) -> str:
        """
        Return the legend wrapped with a given characters long.

        :param int legend_wrap: A given number .
        """
        return fill(self.label, legend_wrap)

    def create_line2D(self, canvas, ax_id, order, legend_wrap, color=None, linewidth=LINEWIDTH_DEFAULT):
        """
        Plot a curve on given canvas's axis with specific order, text-wrap and color.

        :param matplotlib.figure canvas: Given matplot figure.
        :param int ax_id: Id of axis.
        :param int order: Figure would plot each curve by this order.
        :param str color: Curve's color.
        :param float linewidth: Curve's linewidth.
        """
        # print("create_line2D")
        ax = canvas.fig.axes[ax_id]
        if ax_id == 0:
            linecount = len(ax.lines)-2  # two initial draggable cross lines
        else:
            linecount = len(ax.lines)
        if not color:
            if self.line_props["color"]:
                color = self.line_props["color"]
            else:
                color = COLORS[linecount % 10]
        if self.line_props["linewidth"]:
            linewidth = self.line_props["linewidth"]

        ydata = [d+self.shifted for d in self.ydata]
        self.line, = ax.plot(self.xdata, ydata,
                             label=self.get_legend(legend_wrap), color=color,
                             linewidth=linewidth, picker=True)
        self.line.set_zorder(order)
        return self.line

  # Unary Post-processing
    def shift(self, offset: float):
        """
        Shift ydata with given offset, which is always compared with the original data.
        That is, if the given offset is zero, it would be the original curve.

        :param float offset: Given offset.
        """
        xdata, ydata = self.line.get_data()
        new_ydata = [d+(offset-self.shifted) for d in ydata]
        self.line.set_data(xdata, new_ydata)
        self.shifted += (offset-self.shifted)

    def align(self, targetDB, freq):
        """
        Shift the curve to align given magnitude at given frequency.

        :param float targetDB: The target y-magnitude to align.
        :param float freq: The target x-magnitude to align.
        """
        xdata, ydata = self.line.get_data()
        (index, freq) = min(enumerate(xdata), key=lambda x: abs(x[1]-freq))
        offset = targetDB - ydata[index]
        self.shift(offset)

  # Class Function
    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle attribute line, which includes package Matplotlib.
        del state["line"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.line = None

    def print(self, console=True) -> str:
        """Print the infomation."""
        msg = (f"%s, %s, %s, line = {bool(self.line)}" % (
            self.type.value, self.label, self.note))
        if console:
            print(msg)
        return msg
