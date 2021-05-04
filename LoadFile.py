import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np, pandas as pd
from Canvas import *

def load_LEAP_file():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)
    
    path = ""
    dataSequence = {}

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        path = file_name[0]
        if path.endswith('.txt'):
            with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
                headers = file.readlines()[:11]
                title = path[path.rfind('/')+1:path.rfind('.')].strip() # LEAP_Impedance
                
                if title in dataSequence: pass
                else: dataSequence[title] = []
                        
                label = headers[4][headers[4].find('=')+1:].strip()   # Impedance_PR: T201100003660

                units = headers[-1]
                units = units.strip().split(" ")
                units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

                data = pd.read_csv(path,  skiprows=11)
                freq = pd.Series(data.iloc[:,0], name='x', dtype=float)
                val = pd.Series(data.iloc[:,1], name='y', dtype=float)
                phase = pd.Series(data.iloc[:,2], name='y', dtype=float)
                
                curveDatas = []
                note = ""

                _type = determineTypeByTitle(title)

                curveDatas.append(CurveData(label=label, xdata=freq, ydata=val, _type = _type))
                curveDatas.append(CurveData(label=label, xdata=freq, ydata=phase, _type = CurveType.Phase))

                dataSequence[title].extend(curveDatas)
                file.close()
        else:
            pass
    return path, dataSequence
    
def load_AP_file():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    path = ""
    dataSequence = {}

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        path = file_name[0]
        if path.endswith('.xlsx'):
            data = pd.read_excel(path, engine="openpyxl", sheet_name=None)
            # del data['Summary']
            for key, value in data.items():
                title = data[key].columns[0].strip()
                
                _type = determineTypeByTitle(title)

                note = data[key].columns[1].strip()
                curveDatas = []
                isline = True
                for curveIndex in range(int(len(data[key].columns)/2)):
                    label = data[key].iloc[0, curveIndex*2].strip()
                    curve_x = pd.Series(data[key].iloc[3:, curveIndex*2], name='x', dtype=float)
                    curve_y = pd.Series(data[key].iloc[3:, curveIndex*2+1], name='y', dtype=float)
                    if (curve_x.dtype != float or curve_y.dtype != float): 
                        isline = False
                        continue
                    curveDatas.append(CurveData(label=label, note=note, xdata=curve_x, ydata=curve_y, _type = _type))
                
                if (not isline): continue
                if title in dataSequence: dataSequence[title].extend(curveDatas)
                else: dataSequence[title] = curveDatas
        else:
            pass
    return path, dataSequence

def load_Klippel_file():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    path = ""
    dataSequence = {}

    if dialog.exec_():
        file_name = dialog.selectedFiles()
        path = file_name[0]
        if path.endswith('.txt'):
            with open(path, 'r', encoding='UTF-8') as file:
                file_dir = path
                filename = path[file_dir.rfind('/')+1:file_dir.rfind('.')]         

                headers = file.readlines()[:3]
                title = headers[0].strip().strip('"')
                labels = headers[1].split('\t\t')
                labels = [c.replace('"', '').strip() for c in labels]
                dataSequence = {}	
                data = pd.read_table(path,  skiprows=2)
                data = data.dropna() 
                curveDatas = []
                note = ""
                
                freq = data.iloc[:, 0]
                freq = [float(f.replace(',', '').strip()) for f in freq]
                freq = pd.Series(freq, name='y', dtype=float)
                
                _type = determineTypeByTitle(title)

                for i in range(int(len(data.columns)/2)):
                    spl = pd.Series(data.iloc[:, i*2+1], name='y', dtype=float)
                    curveDatas.append(CurveData(label=labels[i], note=note, xdata=freq, ydata=spl, _type = _type))
                if title in dataSequence: pass
                else: dataSequence[title] = []
                dataSequence[title].extend(curveDatas)
        else:
            pass
    return path, dataSequence


def determineTypeByTitle(title):
    if ("Phase" in title): return CurveType.Phase 
    elif ("Impedance" in title): return CurveType.IMP
    elif ("SPL" in title or "CEA" in title or 'RMS' in title): 
        return CurveType.FreqRes
    elif ("THD" in title): return CurveType.THD
    else: return CurveType.NoType