from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir
import pandas as pd
import datetime as dt
from .obj_data import FileData, CurveData, CurveType, Measurement, Channel
from .ui_conf import COLORS
import sys
import traceback


def load_file(source):
    print("load_file")
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QDir.Files)
    filedata = None

    if dialog.exec_():
        try:
            file_name = dialog.selectedFiles()
            path = file_name[0]
            if (source == 'LEAP'):
                filedata = load_LEAP_fileData(path)
            elif (source == 'AP'):
                filedata = load_AP_fileData(path)
            elif (source == 'KLIPPEL'):
                filedata = load_KLIPPEL_fileData(path)
            elif (source == 'COMSOL'):
                filedata = load_COMSOL_fileData(path)
            # filedata.print()

        except Exception as e:
            error_class = e.__class__.__name__
            detail = e.args[0]
            cls, exc, tb = sys.exc_info()
            lastCallStack = traceback.extract_tb(tb)[-1]
            fileName = lastCallStack[0]
            lineName = lastCallStack[1]
            funcName = lastCallStack[2]
            errMsg = "File \"{}\", line {}, in {}:\n[{}] {}".format(
                fileName, lineName, funcName, error_class, detail)
            print(errMsg)

            filedata = None
    else:
        pass

    return filedata


def load_AP_fileData(path):
    print("load_AP_fileData --->")
    filename = path[path.rfind('/')+1:path.rfind('.')]
    filedata = None
    if path.endswith('.xlsx'):
        excel_data = pd.read_excel(path, engine="openpyxl", sheet_name=None)
        filedata = FileData(filename, source="AP", file_path=path,
                            import_time=dt.datetime.today())
        test_in_sequnce = []

        curve_idx = 0

        pages_in_excel = len(excel_data.keys())
        measurements_count = pages_in_excel-1

        first_page = list(excel_data.keys())[0]
        test_in_sequnce.append(list(excel_data.keys())[0])
        channel_count = int(len(excel_data[first_page].columns)/2)

        for count, page in enumerate(excel_data.keys()):
            test_name = excel_data[page].columns[0].strip()
            if test_name not in test_in_sequnce:
                measurements_count = count-1
                test_in_sequnce = []
                break

        test_in_sequnce = list(excel_data.keys())[0:-1:measurements_count+1]
        filedata.testnames = test_in_sequnce
        filedata.valid_testnames = test_in_sequnce
        # print(test_in_sequnce, measurements_count, channel_count)
        for m_idx in range(measurements_count):
            measurementData = Measurement(
                channel_count=channel_count, id=m_idx+1)
            for page in list(excel_data.keys())[m_idx:-1:measurements_count+1]:
                test_name = excel_data[page].columns[0].strip()
                _type = determineTypeByTestName(test_name)
                note = excel_data[page].columns[1].strip()
                isline = True

                for _idx in range(channel_count):
                    label = excel_data[page].iloc[0, _idx*2].strip()
                    curve_x = pd.Series(
                        excel_data[page].iloc[3:, _idx*2], name='x', dtype=float)
                    curve_y = pd.Series(
                        excel_data[page].iloc[3:, _idx*2+1], name='y', dtype=float)
                    units = [excel_data[page].iloc[2, _idx*2],
                             excel_data[page].iloc[2, _idx*2+1]]
                    if (curve_x.dtype != float or curve_y.dtype != float):
                        isline = False
                        continue

                    curveData = CurveData(channel_obj=measurementData.channel[_idx],
                                          label=label, note=note, xdata=curve_x,
                                          ydata=curve_y, _type=_type, units=units)
                    measurementData.channel[_idx].sequence[test_name] = curveData
            if (not isline and test_name in test_in_sequnce):
                print(f"{test_name} is not float type and cannot be plot.")
                test_in_sequnce.remove(test_name)
                continue

            filedata.measurements[str(m_idx)] = measurementData
    else:
        pass
    return filedata


def load_LEAP_fileData(path):
    filedata = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
            headers = file.readlines()[:11]
            # LEAP_Impedance
            filename = path[path.rfind('/')+1:path.rfind('.')].strip()
            test_name = filename
            filedata = FileData(filename, source="LEAP",
                                file_path=path, import_time=dt.datetime.today())
            measurementData = Measurement(channel_count=1, id=1)

            # Impedance_PR: T201100003660
            label = headers[4][headers[4].find('=')+1:].strip()

            units = headers[-1]
            units = units.strip().split(" ")
            units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

            data = pd.read_csv(path,  skiprows=11)
            freq = pd.Series(data.iloc[:, 0], name='x', dtype=float)
            val = pd.Series(data.iloc[:, 1], name='y', dtype=float)
            phase = pd.Series(data.iloc[:, 2], name='y', dtype=float)

            note = ""

            _type = determineTypeByTestName(test_name)

            curveData_val = CurveData(channel_obj=measurementData.channel[0],
                                      label=label, note=note, xdata=freq,
                                      ydata=val, _type=_type,
                                      units=units[0:1])

            curveData_phase = CurveData(channel_obj=measurementData.channel[0],
                                        label=label, note=note, xdata=freq,
                                        ydata=phase, _type=CurveType.PHS, units=units[0::1])

            filedata.testnames = [test_name, "Phase"]
            filedata.valid_testnames = [test_name, "Phase"]
            measurementData.channel[0].sequence[test_name] = curveData_val
            measurementData.channel[0].sequence["Phase"] = curveData_phase
            filedata.measurements['0'] = measurementData
            file.close()
    else:
        pass
    return filedata


def load_KLIPPEL_fileData(path):
    filedata = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8') as file:
            filename = path[path.rfind('/')+1:path.rfind('.')]
            filedata = FileData(filename, source="KLIPPEL",
                                file_path=path, import_time=dt.datetime.today())

            headers = file.readlines()[:3]
            if headers[0][0] == '%':
                raise Exception(
                    "file header start with %, it is a comsole file")
            test_name = headers[0].strip().strip('"')
            labels = headers[1].split('\t\t')
            labels = [c.replace('"', '').strip() for c in labels]

            unit_arr = headers[2].split('\t')
            unit_arr = [c.replace('"', '').strip() for c in unit_arr]

            data = pd.read_table(path,  skiprows=2)
            data = data.dropna()
            note = ""

            _type = determineTypeByTestName(test_name)

            for i in range(int(len(data.columns)/2)):
                measurementData = Measurement(channel_count=1, id=i+1)
                val = pd.Series(data.iloc[:, i*2+1], name='y', dtype=float)
                freq = data.iloc[:, i*2]
                freq = [float(f.replace(',', '').strip()) for f in freq]
                freq = pd.Series(freq, name='x', dtype=float)
                # 'Frequency [Hz]', 'Sound Pessure Level [dB]  / [2.83V 1m]'
                unit_x = unit_arr[i*2]
                unit_y = unit_arr[i*2+1]
                unit_x = unit_x[unit_x.find('['):unit_x.rfind(']')+1]
                unit_y = unit_y[unit_y.find('['):unit_y.rfind(']')+1]

                units = [unit_x, unit_y]  # ['[Hz]', '[dB]  / [2.83V 1m]']
                filename = unit_arr[i*2][unit_arr[i *
                                                  2].rfind('[')+1:path.rfind(']')]

                curveData_new = CurveData(channel_obj=measurementData.channel[0],
                                          label=labels[i], note=note, xdata=freq,
                                          ydata=val, _type=_type,
                                          units=units)

                measurementData.channel[0].sequence[test_name] = curveData_new
                filedata.measurements[str(i)] = measurementData
            filedata.testnames = [test_name]
            filedata.valid_testnames = [test_name]
    else:
        pass
    return filedata


def load_COMSOL_fileData(path):
    filedata = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
            headers = file.readlines()[:8]
            filename = path[path.rfind('/')+1:path.rfind('.')]
            test_name = filename
            filedata = FileData(filename, source="COMSOL",
                                file_path=path, import_time=dt.datetime.today())
            measurementData = Measurement(channel_count=1, id=1)

    #         label = headers[4][headers[4].find('=')+1:]   # Impedance_PR: T201100003660

    #         units = headers[-1]
    #         units = units.strip().split(" ")
    #         units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

            data = pd.read_table(path,  skiprows=7, delim_whitespace=True)
    #         print(data.iloc[:,0])
            freq = pd.Series(data.iloc[:, 0], name='x', dtype=float)
            val = pd.Series(data.iloc[:, 1], name='y', dtype=float)
            # print(freq, val)

            note = ""
            curveData_new = CurveData(channel_obj=measurementData.channel[0],
                                      label=test_name, note=note, xdata=freq, ydata=val, _type=CurveType.SPL)

            filedata.testnames = [test_name]
            filedata.valid_testnames = [test_name]
            measurementData.channel[0].sequence[test_name] = curveData_new
            filedata.measurements['0'] = measurementData
            file.close()
    else:
        pass
    return filedata


def determineTypeByTestName(test_name):
    if ("Phase" in test_name):
        return CurveType.PHS
    elif ("Impedance" in test_name):
        return CurveType.IMP
    elif ("SPL" in test_name or "CEA" in test_name or 'RMS' in test_name):
        return CurveType.SPL
    elif ("THD" in test_name):
        return CurveType.THD
    else:
        return CurveType.NoType


AP_path = "C:/Users/tong.wang/桌面/SAE_PlotTool/SAE_PlotTool/data/AP_yeti.xlsx"
AP_path2 = "C:/Users/tong.wang/桌面/SAE_PlotTool/SAE_PlotTool/data/AP_Acoustic Response_all_xlsx.xlsx"
LEAP_path = "C:/Users/tong.wang/桌面/SAE_PlotTool/SAE_PlotTool/data/LEAP_Impedance.txt"
KLIPPEL_path = "C:/Users/tong.wang/桌面/SAE_PlotTool/SAE_PlotTool/data/NFS_CEA2034.txt"

AP_DATA = load_AP_fileData(AP_path)
# AP_DATA2 = load_AP_fileData(AP_path)

LEAP_DATA = load_LEAP_fileData(LEAP_path)
KLIPPEL_DATA = load_KLIPPEL_fileData(KLIPPEL_path)

# AP_DATA.dumps()
# AP_DATA.print()
