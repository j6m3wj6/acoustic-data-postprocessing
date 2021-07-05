from enum import Enum
import pickle
import sys
import dill
import datetime as dt
from matplotlib.lines import Line2D
from textwrap import fill
from .ui_conf import UI_CONF, COLORS, LINEWIDTH_DEFAULT, LEGEND_WRAP


class Extended_Enum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def index(cls, _type):
        return list(cls).index(_type)


class CurveType(Extended_Enum):
    NoType = 'None'
    SPL = 'SPL'
    IMP = 'Impedance'
    PHS = 'Phase'
    THD = 'THD'
    EXC = 'Excursion'
    ALL = 'All'


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


class Project():
    def __init__(self, name="Untitled"):
        self.info = {
            "Name": name,
            "File Location": sys.path[0],
            'Create Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Last Saved Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
        }
        self.files = []
        self.ui_conf = UI_CONF
        # # self.newattr = []
        # self.newattr2 = []

    @classmethod
    def _check_attr(self, pj):
        if pj.__dict__.keys() is not Project().__dict__.keys():
            print("Not the same", )
            print("\tpj.__dict__.keys(): ", pj.__dict__.keys())
            print("\tProject.__dict__.keys(): ", Project().__dict__.keys())
            print("Difference:", Diff(
                pj.__dict__.keys(), Project().__dict__.keys()))

    def print(self):
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
        for _f in self.files:
            _f.print()
        print("============================\n")
        # return msg

    def append_file(self, file):
        self.files.append(file)

    def delete_files(self, files):
        for _f in files:
            self.files.remove(_f)

    def clear_files(self):
        self.files = []

    def get_path(self):
        return self.info['File Location'] + '/' + self.info['Name'] + '.pkl'

    def dump(self, location=None):
        if not location:
            location = self.get_path()
        # update curveData

        self.print()
        try:
            with open(location, 'wb') as fh:
                self.info["Last Saved Time"] = dt.datetime.today().strftime(
                    "%Y/%m/%d %H:%M:%S")
                pickle.dump(self, fh)
        except:
            print(dill.detect.baditems(self))

    @classmethod
    def load_project(cls, location=None):
        print("unpickled project:")
        print("location: ", location)
        if location == "None":
            return Project()
        else:
            try:
                fh = open(location, 'rb')
                # with open(f"%s.pkl" % (location), 'rb') as fh:
                unpickled_project = pickle.load(fh)
                if location is not unpickled_project.get_path():
                    print(
                        "WARNING: File location not the same --> change project info.")
                    unpickled_project.info["File Location"] = location
                unpickled_project.print()
                # Project._check_attr(unpickled_project)
                print("____________finish obj_data.Project.load_project()")
                fh.close()
                return unpickled_project
            except Exception as e:
                return Project()

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
        # with open("ui_conf.json", "w") as fj:
        #     json.dump(self.ui_conf, fj)
        # print("update_ui_conf", self.ui_conf)

    def get_files(self, filenames):
        files_to_return = []
        for _f in self.files:
            if _f.info["Name"] in filenames and _f not in files_to_return:
                files_to_return.append(_f)
        return files_to_return


class FileData():
    def __init__(self, name=None, source=None, file_path=None, import_time=None):
        self.info = {
            "Name": name,
            "Source": source,
            "File Path": file_path,
            'Import Time': import_time,
            'Last Modified Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
        }
        self.sequence = {}
        # ----
        self.test_in_sequence = []
        self.measurements = {}

  # Funcs
    def print(self):
        msg = ""
        msg += "------------"
        msg += ("\n\tName: %s \n\tSource: %s \n\tfile_path: %s" %
                (self.info["Name"], self.info["Source"], self.info["File Path"]))
        msg += ("\n\tImport time: %s" % str(self.get_import_time()))
        msg += "\n\tSequence:"
        for _k, _v in self.sequence.items():
            msg += ("\n\t  Key: %s" % _k)
            msg += ("\n\t  Curves: ")
            for _c in _v:
                msg += (f"\n\t\t%s, %s, %s" %
                        (_c.type.value, _c.label, _c.note))
        for _m in self.measurements.values():
            msg += _m.print()
        msg += ("\n-----------------------------")
        print(msg)
        return msg

    def update_sequence(self, dataSequence):
        for test, curveData in dataSequence:
            self.sequence[test] = curveData

    def get_import_time(self):
        return self.info["Import Time"].strftime("%Y/%m/%d %H:%M:%S")

    # [(test1->(ch1 ch2 ...)) (test2->(ch1 ch2 ...))...]
    def dict_measurement(self):
        dict_measurement = {}
        for _m in self.measurements.values():
            for test in _m.channel[1].sequence.keys():
                dict_measurement[test] = []
                for _ch in _m.channel:
                    dict_measurement[test].append(_ch.sequence[test])
        return dict_measurement


class Measurement:
    def __init__(self, channel=1, id=None):
        self.id = id
        self.channel = []
        self.init_channels(channel)

    def init_channels(self, num: int) -> None:
        for i in range(num):
            self.channel.append(Channel(self, i+1))

    def print(self, console=True):
        msg = "\n============================\n"
        msg += f"Measurement____id={self.id}\n"

        for c in self.channel:
            msg += "%s" % c.print(False)
        msg += "\n============================\n"
        if (console):
            print(msg)
        return msg


class Channel:
    def __init__(self, parent=None, id=None):
        self.parent = parent
        self.id = id
        self.label = f"Ch{id}"
        self.sequence = {}

    def print(self, console=True):
        msg = f"Channel____id={self.id}\n"
        msg += "  Sequence:\n"
        for test, curve in self.sequence.items():
            msg += f"\t{test}: {curve}\n"
        if (console):
            print(msg)
        return msg

    def set_label(self, label: str) -> None:
        self.label = label

    def get_label(self):
        return self.label


class CurveData:
    def __init__(self, parent=None, label=None, note=None, xdata=None, ydata=None, _type=None, units=[], color=COLORS[0]):
        self.parent = parent
        self.label = label
        self.note = note
        self.xdata = xdata
        self.ydata = ydata
        self.type = _type
        self.shifted = 0
        self.units = units
        self.line = None
        self.line_props = {
            "visible": False,
            "color": color,
            "linewidth": LINEWIDTH_DEFAULT,
        }
  # Class Function

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle baz

        del state["line"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Add baz back since it doesn't exist in the pickle
        self.line = None

    def print(self):
        print(f"%s, %s, %s" % (self.type.value, self.label, self.note))
  # Get and Set Function

    def get_label(self, link=False):
        if self.parent and link:
            return self.parent.label
        else:
            return self.label

    def get_legend(self, legend_wrap):
        return fill(self.get_label(), legend_wrap)

    def get_ymax(self):
        print(self.ydata.max())

    def get_dict(self):
        dictToJSON = {
            'Data Type': self.type.value,
            'xData': self.xdata.to_numpy().tolist(),
            'yData': self.ydata.to_numpy().tolist(),
            'Label': self.get_label(),
            'Note': self.note,
            'line_props': self.line_props
        }
        return dictToJSON

    def create_line2D(self, ax, legend_wrap, order):
        self.label = self.label.replace('\n', '')
        linecount = len(ax.lines)
        self.line_props["color"] = COLORS[linecount % 10]
        self.line, = ax.plot(self.xdata, self.ydata,
                             label=self.get_legend(legend_wrap), color=self.line_props["color"], picker=True)
        self.line.set_zorder(order)
        return self.line
  # Curve Unary Function

    def shift(self, offset):
        xdata, ydata = self.line.get_data()
        new_ydata = [d+(offset-self.shifted) for d in ydata]
        self.line.set_data(xdata, new_ydata)
        self.shifted += (offset-self.shifted)

    def align(self, targetDB, freq):
        xdata, ydata = self.line.get_data()
        (index, freq) = min(enumerate(xdata), key=lambda x: abs(x[1]-freq))
        offset = targetDB - ydata[index]
        self.shift(offset)
  # Save and Sync

    def sync_with_line(self):
        if self.line:
            self.label = self.line.get_label().replace('\n', '')
            if self.parent:
                self.parent.label = self.label
            self.line_props["color"] = self.line.get_color()
            self.line_props["linewidth"] = self.line.get_linewidth()
        else:
            pass

    def dump(self):
        self.print()
        try:
            with open(f"%s.pkl" % ("curvedata"), 'wb') as fh:
                pickle.dump(self, fh)
        except:
            print(dill.detect.baditems(self))
