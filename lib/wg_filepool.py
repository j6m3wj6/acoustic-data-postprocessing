from pickle import TRUE
from lib.obj_data import CurveData
from PyQt5.QtWidgets import QScrollArea, QWidget, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QAbstractItemView
from .ui_conf import ICON_DIR, LINEWIDTHS
from .wg_file import Wg_File
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon
from .dlg_load_files import determineTypeByTestName


class FilePool(QWidget):
    def __init__(self, mainwindow=None):
        super(QWidget, self).__init__()
        self.mainwindow = mainwindow
        self.setObjectName("FilePool")
        self.initUI()

    def initUI(self):
        self.vbly = QVBoxLayout()
        self.vbly.setContentsMargins(0, 0, 0, 0)
        self.vbly.setAlignment(Qt.AlignTop)
        self.setLayout(self.vbly)

    def append_file(self, fileData):
        wg_file = Wg_File(self, fileData)
        self.vbly.addWidget(wg_file)

    def delete_files(self, files):
        print("delete", files)
        wg_files = self.findChildren(QWidget, "Wg_File")
        wg_files_to_del = []
        for wg_file in wg_files:
            if wg_file.fileData.info["Name"] in files:
                wg_file.toolbtn_link.setChecked(True)
                wg_files_to_del.append(wg_file)
        print("wg_files_to_del", wg_files_to_del)
        for wg_del in wg_files_to_del:
            wg_del.toggle_all(checkState=Qt.Unchecked, link=True)
            self.vbly.removeWidget(wg_del)
            wg_del.setParent(None)

    # def set_children_checkstate(self, _type, checkstate):
    #     wg_files = self.findChildren(QWidget, "Wg_File")
    #     wg_curves = self.findChildren(QWidget, "Wg_Curve")

    #     for wg_file in wg_files:
    #         for testname in wg_file.fileData.valid_testnames:
    #             if determineTypeByTestName(testname) is not _type:
    #                 continue
    #             for wg_curve in wg_curves:
    #                 if wg_file.get_testname() == testname:
    #                     wg_curve.checkbox.handle_checked(
    #                         checkstate, False, testname)
    #                 wg_curve.get_curveData(testname).line_props["visible"] = (
    #                     checkstate == Qt.Checked)

    def _get_valid_curveData(self, wg_curve, valid_testnames):
        for testname in valid_testnames:
            curveData = wg_curve.get_curveData(testname)
            if curveData.line and curveData.line_props["visible"]:
                return curveData

    def tranfer_to_table(self):
        print("\ntranfer_to_table")
        wg_files = self.findChildren(QWidget, "Wg_File")
        focusing_canvas = self.mainwindow.wg_canvas.focusing_canvas
        tb_curves = QTableWidget()
        tb_curves.setColumnCount(4)
        tb_curves.setHorizontalHeaderLabels(
            ['Label', 'Note', 'Color', 'LineWidth'])

        for wg_file in wg_files:
            # visible_curveData = wg_file.get_checkedItems(mergeAll=True)
            checked_wg_curves = wg_file.get_checkedItems(mergeAll=True)
            if wg_file.link:
                row = tb_curves.rowCount()
                tb_curves.setRowCount(row + 1)
                test_item = QTableWidgetItem(f"%s" % (
                    wg_file.fileData.info["Name"]))
                test_item.setBackground(Qt.lightGray)
                test_item.setFlags(Qt.NoItemFlags)
                tb_curves.setItem(row, 0, test_item)
                tb_curves.setSpan(row, 0, 1, 4)
                for wg_curve in checked_wg_curves:
                    curveData = self._get_valid_curveData(
                        wg_curve, wg_file.fileData.valid_testnames)
                    label_item, note_item, color_item, linewidth_item = self._create_tbcell_color_linewidth(
                        curveData)
                    label_item.setFlags(label_item.flags() ^ Qt.ItemIsEditable)
                    label_item.setData(Qt.UserRole, wg_curve.get_curveDatas())
                    row = tb_curves.rowCount()
                    tb_curves.setRowCount(row + 1)
                    tb_curves.setItem(row, 0, label_item)
                    tb_curves.setItem(row, 1, note_item)
                    tb_curves.setItem(row, 2, color_item)
                    tb_curves.setItem(row, 3, linewidth_item)
            else:
                for testname in wg_file.fileData.valid_testnames:
                    if determineTypeByTestName(testname) not in focusing_canvas.ax_types:
                        continue
                    row = tb_curves.rowCount()
                    tb_curves.setRowCount(row + 1)
                    test_item = QTableWidgetItem(f"%s - %s" % (
                        wg_file.fileData.info["Name"], testname))
                    test_item.setBackground(Qt.lightGray)
                    test_item.setFlags(Qt.NoItemFlags)
                    tb_curves.setItem(row, 0, test_item)
                    tb_curves.setSpan(row, 0, 1, 4)
                    for wg_curve in checked_wg_curves:
                        curveData = wg_curve.get_curveData(testname)
                        if not curveData.line or not curveData.line_props["visible"]:
                            continue
                        print("curveData to carry, ", curveData.print(False))
                        label_item, note_item, color_item, linewidth_item = self._create_tbcell_color_linewidth(
                            curveData)
                        label_item.setFlags(
                            label_item.flags() ^ Qt.ItemIsEditable)
                        label_item.setData(Qt.UserRole, [curveData])
                        row = tb_curves.rowCount()
                        tb_curves.setRowCount(row + 1)
                        tb_curves.setItem(row, 0, label_item)
                        tb_curves.setItem(row, 1, note_item)
                        tb_curves.setItem(row, 2, color_item)
                        tb_curves.setItem(row, 3, linewidth_item)
        print("\ntranfer_to_table_______")
        return tb_curves

    def transfer_to_list(self):
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        focusing_canvas = self.mainwindow.wg_canvas.focusing_canvas
        wg_files = self.findChildren(QWidget, "Wg_File")
        for wg_file in wg_files:
            file_item = QListWidgetItem()
            file_item.setText(wg_file.fileData.info["Name"])
            file_item.setFlags(Qt.NoItemFlags)
            file_item.setBackground(Qt.lightGray)
            listWidget.addItem(file_item)

            # checked_wg_curves = wg_file.get_visible_curveData()

            checked_wg_curves = wg_file.get_checkedItems(mergeAll=True)
            for testname in wg_file.fileData.valid_testnames:
                if determineTypeByTestName(testname) not in focusing_canvas.ax_types:
                    continue
                for wg_curve in checked_wg_curves:
                    curveData = wg_curve.get_curveData(testname)
                    if not curveData.line:
                        continue
                    curve_item = QListWidgetItem()
                    curve_item.setData(Qt.UserRole, curveData)
                    curve_item.setText("{0:20} | {1:20} | {2:20}".format(
                        curveData.label, curveData.note, testname))
                    listWidget.addItem(curve_item)
        return listWidget

    def _create_tbcell_color_linewidth(self, curveData):
        label_item = QTableWidgetItem(curveData.label)
        note_item = QTableWidgetItem(curveData.note)
        pixmap = QPixmap(65, 20)
        pixmap.fill(QColor(curveData.line.get_color()))
        color_item = QTableWidgetItem()
        color_item.setIcon(QIcon(pixmap))

        linewidth_index = LINEWIDTHS.index(
            curveData.line.get_linewidth())
        icon_dir = ICON_DIR + f"linewidth_%s.png" % (
            linewidth_index)
        linewidth_item = QTableWidgetItem()
        linewidth_item.setIcon(QIcon(icon_dir))
        return label_item, note_item, color_item, linewidth_item

    def copy_params_from_canvas(self):
        # focusing_canvas = self.mainwindow.wg_canvas.focusing_canvas
        wg_files = self.findChildren(QWidget, "Wg_File")
        for wg_file in wg_files:
            checked_wg_curves = wg_file.get_checkedItems(mergeAll=True)
            for wg_curve in checked_wg_curves:
                wg_curve.copy_params_from_canvas()

    def save_in_project(self):
        project = self.mainwindow.project
        wg_files = self.findChildren(QWidget, "Wg_File")
        project.files = [wg.fileData for wg in wg_files]
