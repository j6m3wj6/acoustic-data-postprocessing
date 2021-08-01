from lib.ui_conf import LINESTYLES, LINEWIDTHS
from PyQt5.QtWidgets import QWidget, QComboBox, \
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QAbstractItemView
from PyQt5.QtCore import Qt
from .functions import determineTypeByTestName
from .wg_selfdefined import Cbox_Color, Cbox_Linewidth
from .wg_file import Wg_File

TB_CURVES_HEADER = ['Label', 'Note', 'Data testname', 'Color', 'LineWidth']


class Wg_FilePool(QWidget):
    def __init__(self, mainwindow=None):
        super(QWidget, self).__init__()
        self.mainwindow = mainwindow
        self.setObjectName("Wg_FilePool")
        self.initUI()

    def initUI(self):
        """Initial User Interface."""
        self.vbly = QVBoxLayout()
        self.vbly.setContentsMargins(0, 0, 0, 0)
        self.vbly.setAlignment(Qt.AlignTop)
        self.setLayout(self.vbly)

    def append_file(self, fileData):
        """
        Create a Wg_File instance carrying given data and add it to this Wg_FilePool instance.

        :param FileData fileData: A FileData object generated from the imported file.
        """
        wg_file = Wg_File(self, fileData)
        self.vbly.addWidget(wg_file)

    def delete_files(self, filenames):
        """
        Removing Wg_File instances with given filenames from this Wg_FilePool instance.

        :param List[str] filenames: A list of filenames user intends to delete.
        """
        print("delete", filenames)
        wg_files = self.findChildren(QWidget, "Wg_File")
        wg_files_to_del = []
        for wg_file in wg_files:
            if wg_file.fileData.info["Name"] in filenames:
                wg_files_to_del.append(wg_file)
        print("wg_files_to_del", wg_files_to_del)
        for wg_del in wg_files_to_del:
            wg_del.toggle_all(checkState=Qt.Unchecked, link=True)
            self.vbly.removeWidget(wg_del)
            wg_del.setParent(None)

    def _get_valid_curveData(self, wg_curve, valid_testnames):
        """
        Among currently valid tests, return the first curveData of given Wg_Curve whose line is visible. 

        :param Wg_Curve wg_curve: 
                A given Wg_Curve instance, which represents a certain channel of a measurement. \n
                It can retrieve different curve data according to different testname.
        :param List[str] valid_testnames: A list of test names that is valid at the run time.
        """
        for testname in valid_testnames:
            curveData = wg_curve.get_curveData(testname)
            if curveData.line and curveData.line_props["visible"]:
                return curveData

    def _create_row(self, curveData, testname):
        """
        Create and return items of one row for the table.
        """
        label_item = QTableWidgetItem(curveData.label)
        note_item = QTableWidgetItem(curveData.note)
        testname_item = QTableWidgetItem(testname)

        cbox_color = Cbox_Color()
        cbox_color.set_color(curveData.line.get_color())
        cbox_color.setObjectName("cbox_color")
        cbox_linewidth = Cbox_Linewidth()
        lw_count = len(LINEWIDTHS)
        linewidth_index = LINEWIDTHS.index(curveData.line.get_linewidth())
        linestyle_index = LINESTYLES.index(curveData.line.get_linestyle())

        cbox_linewidth.setCurrentIndex(
            lw_count*linestyle_index + linewidth_index)
        cbox_linewidth.setObjectName("cbox_linewidth")

        testname_item.setFlags(testname_item.flags() ^ Qt.ItemIsEditable)
        return [label_item, note_item, testname_item, cbox_color, cbox_linewidth]

    def transfer_to_table(self) -> QTableWidget:
        """
        Return a table for graph properties' dialog.

        It contains curves under certain conditions, 
        such as focusing canvas, valid tests, and link status of each Wg-File instances.

        Columns includes: Label, Note, Data testname, Color, LineWidth.
        """
        # print("\ntransfer_to_table")
        wg_files = self.findChildren(QWidget, "Wg_File")
        focusing_canvas = self.mainwindow.wg_canvas.focusing_canvas
        tb_curves = QTableWidget()
        tb_curves.setColumnCount(len(TB_CURVES_HEADER))
        tb_curves.setHorizontalHeaderLabels(TB_CURVES_HEADER)

        for wg_file in wg_files:
            # visible_curveData = wg_file.get_checkedItems(mergeAll=True)
            checked_wg_curves = wg_file.get_checkedItems(mergeAll=True)
            if wg_file.link:
                row = tb_curves.rowCount()
                tb_curves.setRowCount(row + 1)
                test_item = QTableWidgetItem(f"%s [Link]" % (
                    wg_file.fileData.info["Name"]))
                test_item.setBackground(Qt.lightGray)
                test_item.setFlags(Qt.NoItemFlags)
                tb_curves.setItem(row, 0, test_item)
                tb_curves.setSpan(row, 0, 1, len(TB_CURVES_HEADER))
                for wg_curve in checked_wg_curves:
                    curveData = self._get_valid_curveData(
                        wg_curve, wg_file.fileData.valid_testnames)
                    row_items = self._create_row(
                        curveData, testname="(Link)")
                    label_item = row_items[TB_CURVES_HEADER.index('Label')]
                    label_item.setData(
                        Qt.UserRole, (wg_curve, wg_file.fileData.testnames))
                    row = tb_curves.rowCount()
                    tb_curves.setRowCount(row + 1)
                    for idx, item in enumerate(row_items):
                        if isinstance(item, QTableWidgetItem):
                            tb_curves.setItem(row, idx, item)
                        elif isinstance(item, QComboBox):
                            tb_curves.setCellWidget(row, idx, item)
            else:
                row = tb_curves.rowCount()
                tb_curves.setRowCount(row + 1)
                test_item = QTableWidgetItem(f"%s [Unlink]" % (
                    wg_file.fileData.info["Name"]))
                test_item.setBackground(Qt.lightGray)
                test_item.setFlags(Qt.NoItemFlags)
                tb_curves.setItem(row, 0, test_item)
                tb_curves.setSpan(row, 0, 1, len(TB_CURVES_HEADER))
                for testname in wg_file.fileData.valid_testnames:
                    if determineTypeByTestName(testname) not in focusing_canvas.ax_types:
                        continue

                    for wg_curve in checked_wg_curves:
                        curveData = wg_curve.get_curveData(testname)
                        if not curveData.line or not curveData.line_props["visible"]:
                            continue
                        row_items = self._create_row(curveData,  testname)
                        label_item = row_items[TB_CURVES_HEADER.index(
                            'Label')]
                        label_item.setData(
                            Qt.UserRole, (wg_curve, [testname]))
                        row = tb_curves.rowCount()
                        tb_curves.setRowCount(row + 1)
                        for idx, item in enumerate(row_items):
                            if isinstance(item, QTableWidgetItem):
                                tb_curves.setItem(row, idx, item)
                            elif isinstance(item, QComboBox):
                                tb_curves.setCellWidget(row, idx, item)

        return tb_curves

    def transfer_to_list(self) -> QListWidget:
        """
        Return a list for post processing dialog.

        It contains curves is visible on the focusing canvas.
        """
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

    def sync_curveData(self):
        wg_files = self.findChildren(QWidget, "Wg_File")
        for wg_file in wg_files:
            checked_wg_curves = wg_file.get_checkedItems(mergeAll=True)
            for wg_curve in checked_wg_curves:
                wg_curve.sync_curveData()
