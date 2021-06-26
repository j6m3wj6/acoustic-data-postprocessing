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

    def print(self):
        print(self.info)
        print(self.get_path())
        for _f in self.files:
            _f.print()

    def append_file(self, file):
        self.files.append(file)

    def get_path(self):
        return self.info['File Location'] + '/' + self.info['Name'] + '.pkl'

    def dump(self, location=None):
        if not location:
            location = self.get_path()

        self.print()
        try:
            with open(location, 'wb') as fh:
                pickle.dump(self, fh)
                self.info["Last Saved Time"] = dt.datetime.today().strftime(
                    "%Y/%m/%d %H:%M:%S")
        except:
            print(dill.detect.badobjects(self, depth=0))
            print(dill.detect.badobjects(self, depth=1))
            print(dill.detect.badobjects(self, depth=2))

    @classmethod
    def load_project(cls, location=None):
        print("unpickle:", location)
        if location == "None":
            return Project()
        else:
            try:
                fh = open(location, 'rb')
                # with open(f"%s.pkl" % (location), 'rb') as fh:
                unpickled_data = pickle.load(fh)
                print(unpickled_data.print())
                print("----------------------------------")
                fh.close()
                return unpickled_data
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

    def print(self):
        print("\n\n-------------------------")
        print("\tName: %s \n\tSource: %s \n\tfile_path: %s" %
              (self.info["Name"], self.info["Source"], self.info["File Path"]))
        print("\tImport time: ", self.get_import_time())
        print("\tSequence:")
        print("-----------------------------\n\n")

    def setData(self, dataSequence):
        for test, curveData in dataSequence:
            self.sequence['test'] = curveData

    def get_import_time(self):
        return self.info["Import Time"].strftime("%Y/%m/%d %H:%M:%S")


class CurveData:
    def __init__(self, label=None, note=None, xdata=None, ydata=None, _type=None, units=[], color=COLORS[0]):
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
            "legend": fill(self.label, LEGEND_WRAP)
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

    def get_legend(self):
        # if (len(self.label) < LEGEND_WRAP): return self.label.ljust(LEGEND_WRAP, ' ')
        # else:
        return fill(self.label, LEGEND_WRAP)

    def get_ymax(self):
        print(self.ydata.max())

    def get_dict(self):
        dictToJSON = {
            'Data Type': self.type.value,
            'xData': self.xdata.to_numpy().tolist(),
            'yData': self.ydata.to_numpy().tolist(),
            'Label': self.label,
            'Note': self.note,
            'line_props': self.line_props
        }
        return dictToJSON

    def create_line2D(self, ax):

        self.line, = ax.plot(self.xdata, self.ydata,
                             label=self.line_props["legend"], color=self.line_props["color"], picker=True)

    def set_line(self, xdata, ydata, label, color):
        self.line = Line2D(
            xdata, ydata, label=self.get_legend(), color=color, picker=True)
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
            self.label = self.line.get_label()
            self.line_props["legend"] = self.line.get_label()
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
