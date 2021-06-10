from lib.dlg_load_files import load_AP_fileData, load_KLIPPEL_fileData
import pickle
import datetime as dt
import sys
from lib.wg_canvas import CurveType
AP_path = "C:/Users/tong.wang/OneDrive - 國立台灣大學/桌面/Matlab tools/TYM-SAE_plotTool/data/AP_Acoustic Response_all_xlsx.xlsx"
AP_DATA = load_AP_fileData(AP_path)

KLIPPEL_path = "C:/Users/tong.wang/OneDrive - 國立台灣大學/桌面/Matlab tools/TYM-SAE_plotTool/data/NFS_CEA2034.txt"
KLIPPEL_DATA = load_KLIPPEL_fileData(KLIPPEL_path)


class MyApp():
    def __init__(self, parent=None):
        self.project_info = {
            "Name": "myproject",
            "File Path": sys.path[0],
            'Import Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Last Modified Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Files': []
        }
        self.files = []


# print(CurveType.list())
# _list = list(CurveType)
# print(CurveType.NoType == _list[0])
# print(CurveType.index(CurveType.NoType))

myApp = MyApp()
myApp.files.append(AP_DATA)
myApp.files.append(KLIPPEL_DATA)

pickled_DATA = pickle.dumps(myApp)
unpickled_object = pickle.loads(pickled_DATA)
print(unpickled_object.project_info)
print(unpickled_object.files[0].sequence)

pickled_DATA = pickle.dumps(unpickled_object)
# print(pickled_DATA)


a = [1, 2, 3, 4, 1, 2, 1, 1]
a[:] = [4 if x == 1 else x for x in a]
print(a)
