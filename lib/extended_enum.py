from enum import Enum
import pickle
import sys
import dill
import datetime as dt
from matplotlib.lines import Line2D
from textwrap import fill


class Extended_Enum(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def index(cls, _type):
        return list(cls).index(_type)


class CurveType(Extended_Enum):
    NoType = 'None'
    FreqRes = 'SPL'
    IMP = 'Impedance'
    Phase = 'Phase'
    THD = 'THD'
    EX = 'Excursion'


class Project():
    def __init__(self):
        self.info = {
            "Name": "myproject",
            "File Path": sys.path[0],
            'Import Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Last Modified Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
        }
        self.files = []

    def print(self):
        print(self.info)
        for _f in self.files:
            _f.print()
            # print(self.files)

    def dump(self):
        self.print()

        try:
            with open(f"%s.pkl" % (self.info['Name']), 'wb') as fh:
                pickle.dump(self, fh)
        except:
            print(dill.detect.badobjects(self, depth=0))
            print(dill.detect.badobjects(self, depth=1))
            print(dill.detect.badobjects(self, depth=2))

    @classmethod
    def _load_project(self, project_name):
        print("unpickle:", project_name)
        try:
            fh = open(f"%s.pkl" % (project_name), 'rb')
            # with open(f"%s.pkl" % (project_name), 'rb') as fh:
            unpickled_data = pickle.load(fh)
            print("unpickle:", unpickled_data)
            fh.close()
            return unpickled_data
        except Exception as e:
            print(e)
            return Project()


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

    def setData(self, dataSequence):
        for test, curveData in dataSequence:
            self.sequence['test'] = curveData

    def get_import_time(self):
        return self.info["Import Time"].strftime("%Y/%m/%d %H:%M:%S")

    def print(self):
        print("\n\n-------------------------")
        print("\tName: %s \n\tSource: %s \n\tfile_path: %s" %
              (self.info["Name"], self.info["Source"], self.info["File Path"]))
        print("\tImport time: ", self.get_import_time())
        print("\tSequence:", self.sequence)
        print("-----------------------------\n\n")


LINEWIDTH_DEFAULT = 1.5
LINEWIDTH_HIGHLIGHT = 4
COLORS = ['sienna', 'r', 'darkorange', 'gold', 'g', 'b', 'purple', 'gray']
COLORS_CMP = ['r', 'b', 'g']
LEGEND_WRAP = 25
AXIS_SCALE = {
    "all": ["linear", "log"],
    "SPL": "log",
    "Imp": "log",
}


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
            "color": color,
            "linewidth": LINEWIDTH_DEFAULT,
            "legend": fill(self.label, LEGEND_WRAP)
        }

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle baz

        del state["line"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Add baz back since it doesn't exist in the pickle
        self.line = None

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

    def set_line(self, xdata, ydata, label, color):
        self.line = Line2D(
            xdata, ydata, label=self.get_legend(), color=color, picker=True)

    def create_line2D(self, ax):
        # self.line = Line2D(self.xdata, self.ydata,
        #                    label=self.line_props["legend"], color=self.line_props["color"], picker=True)
        self.line, = ax.plot(self.xdata, self.ydata,
                             label=self.line_props["legend"], color=self.line_props["color"], picker=True)
        self.get_ymax()

    def get_legend(self):
        # if (len(self.label) < LEGEND_WRAP): return self.label.ljust(LEGEND_WRAP, ' ')
        # else:
        return fill(self.label, LEGEND_WRAP)

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

    def print(self):
        print(f"%s, %s, %s" % (self.type.value, self.label, self.note))

    def dump(self):
        self.print()
        try:
            with open(f"%s.pkl" % ("curvedata"), 'wb') as fh:
                pickle.dump(self, fh)
        except:
            print(dill.detect.baditems(self))

    def get_ymax(self):
        print(self.ydata.max())


DEFUALT_CANVAS_PARAMETER = {
    "General": {
        "Title": "SPL | THD",
        "Margin": {
            "left": 10,
            "right": 10,
            "top": 10,
            "bottom": 10
        },
        "Legend": {
            "visible": True,
            "wrap": 25
        }
    },
    "Axis": {
        "X-Axis": {
            "auto-scale": False,
            "min": 20,
            "max": 20000,
            "label": "Frequency",
            "unit": "Hz",
            "scale": "log"
        },
        "Y-Axis": {
            "auto-scale": True,
            "min": 0,
            "max": 100,
            "label": "",
            "unit": "dBSPL",
            "scale": "log"
        },
        "Sub_Y-Axis": {
            "auto-scale": True,
            "min": 0,
            "max": 100,
            "label": "",
            "unit": "dBSPL",
            "scale": "log"
        }
    }
}
