from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from .ui_conf import LINEWIDTH_HIGHLIGHT
from .obj_data import CurveType, FileData


class MyTree(QTreeWidget):
    def __init__(self, mainwindow=None):
        super(QTreeWidget, self).__init__()
        self.wg_canvas = mainwindow.wg_canvas
        self.setColumnCount(2)
        self.setHeaderLabels(['Label', 'Note'])
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 300)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemChanged.connect(self.handleCheck)
        self.itemSelectionChanged.connect(self.handleSelect)
        # self.doubleClicked.connect(self.editText)

    def handleCheck(self, item):
        # print("MyTree handleSelect")
        try:
            if not item.parent() or isinstance(item.data(1, Qt.UserRole), CurveType):  # test root
                return
            else:  # measurement leaves
                curveData = item.data(0, Qt.UserRole)
                curveData.label = item.text(0)

                curveData.note = item.text(1)
                canvas, _, ax = self.wg_canvas.get_canvas(curveData.type)
                if curveData.line and item.checkState(0) == Qt.Unchecked:
                    curveData.line.set_label('_nolegend_')
                    curveData.line_props["visible"] = False
                    if (ax and curveData.line in ax.lines):
                        ax.lines.remove(curveData.line)
                elif item.checkState(0) == Qt.Checked:
                    if curveData.line not in ax.lines:
                        curveData.create_line2D(
                            ax, int(canvas.parameter["General"]['Legend']['text-wrap']))
                        curveData.line_props["visible"] = True

                item.setData(0, Qt.UserRole, curveData)
                canvas.fig.axes[1].set_visible(bool(canvas.fig.axes[1].lines))
        except KeyError:
            print("KeyError")
            raise KeyError
        canvas.replot()

    def handleSelect(self):
        # print("MyTree handleSelect")
        if not self.currentItem():
            return
        for c in self.wg_canvas.get_active_canvas():
            c.reset_linewidth()
        for it in self.selectedItems():
            if not it.data(0, Qt.UserRole):
                continue  # not measurement leaves
            else:
                curve = it.data(0, Qt.UserRole)
                curve.line_props["linewidth"] = LINEWIDTH_HIGHLIGHT
                # if (curve.line)
                # %%%%%
                # curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
        self.wg_canvas.replot()

    def appendChildren(self, DATA):
        fileroot = QTreeWidgetItem(self)
        fileroot.setText(0, DATA.info["Name"])
        fileroot.setText(1, DATA.info["Source"])
        fileroot.setExpanded(True)
        fileroot.setBackground(0, QColor(237, 237, 237))
        fileroot.setBackground(1, QColor(237, 237, 237))

        for test_name, curveDatas in DATA.sequence.items():
            testroot = QTreeWidgetItem()
            testroot.setText(0, test_name)
            testroot.setText(1, curveDatas[0].type.value)
            testroot.setData(1, Qt.UserRole, curveDatas[0].type)
            testroot.setFlags(testroot.flags() |
                              Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            fileroot.addChild(testroot)

            for _cd in curveDatas:
                child = QTreeWidgetItem()
                child.setText(0, _cd.label)
                child.setText(1, _cd.note)
                child.setData(0, Qt.UserRole, _cd)
                testroot.addChild(child)
                if _cd.line_props["visible"]:
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
        self.addTopLevelItem(fileroot)
        # self.expandAll()
        # fileroot.child(0).setCheckState(0, Qt.Checked)

    def removeChildren(self, filenames_to_del) -> None:
        level_to_delete = []
        for i_f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(i_f)
            print(fileroot.text(0))
            if fileroot.text(0) in filenames_to_del:
                for t in range(fileroot.childCount()):
                    testroot = fileroot.child(t)
                    testroot.setCheckState(0, Qt.Unchecked)
                level_to_delete.append(i_f)

        for _i, _l in enumerate(level_to_delete):
            self.takeTopLevelItem(_l-_i)

    def filterChildren(self, _types):
        self.unHideChildren()
        if CurveType.ALL in _types:
            return
        for i_f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(i_f)
            for i_t in range(fileroot.childCount()):
                test = fileroot.child(i_t)
                test_type = test.data(1, Qt.UserRole)
                if (test_type not in _types):
                    test.setHidden(True)

            # root.addTopLevelItem(fileroot_copy)

    def set_children_checkstate(self, _type, checkstate):
        self.unHideChildren()

        for i_f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(i_f)
            for i_t in range(fileroot.childCount()):
                test = fileroot.child(i_t)
                test_type = test.data(1, Qt.UserRole)
                if (test_type == _type):
                    test.setCheckState(0, checkstate)

            # root.addTopLevelItem(fileroot_copy)

    def unHideChildren(self):
        for i_f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(i_f)
            for i_t in range(fileroot.childCount()):
                test = fileroot.child(i_t)
                test.setHidden(False)

    def editText(self, event):
        print("double click", event, event.column(), event.row(), event.data())
        item = self.itemFromIndex(event)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.edit(event)

    def get_focusing_curves_lists(self):
        listWidget = QListWidget()
        listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        focusing_canvas = self.wg_canvas.focusing_canvas
        for f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(f)
            for t in range(fileroot.childCount()):
                testroot = fileroot.child(t)
                testType = testroot.data(1, Qt.UserRole)
                if (testroot.checkState(0) == Qt.Unchecked or testType not in focusing_canvas.ax_types):
                    continue
                test_item = QListWidgetItem()
                test_item.setText(fileroot.text(0)+' - '+testroot.text(0))
                test_item.setFlags(Qt.NoItemFlags)
                test_item.setBackground(Qt.lightGray)

                listWidget.addItem(test_item)
                for c in range(testroot.childCount()):
                    curve_item = testroot.child(c)
                    if (curve_item.checkState(0) == Qt.Checked):
                        curveData = curve_item.data(0, Qt.UserRole)
                        new_item = QListWidgetItem()
                        new_item.setData(Qt.UserRole, curveData)
                        new_item.setText(curveData.label)
                        listWidget.addItem(new_item)
        return listWidget

    def sync_with_canvas(self):
        focusing_canvas = self.wg_canvas.focusing_canvas
        for _f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(_f)
            for _t in range(fileroot.childCount()):
                testroot = fileroot.child(_t)
                testType = testroot.data(1, Qt.UserRole)
                if (testroot.checkState(0) == Qt.Unchecked or testType not in focusing_canvas.ax_types):
                    continue
                for _c in range(testroot.childCount()):
                    curve_item = testroot.child(_c)
                    if (curve_item.checkState(0) == Qt.Unchecked):
                        continue
                    curveData = curve_item.data(0, Qt.UserRole)
                    curveData.sync_with_line()
                    curve_item.setText(0, curveData.label)
                    curve_item.setData(0, Qt.UserRole, curveData)

    def save_back_to_project(self):
        project = self.wg_canvas.mainwindow.project
        for _f in range(self.topLevelItemCount()):
            fileroot = self.topLevelItem(_f)
            filename = fileroot.text(0)
            print(filename)
            for _t in range(fileroot.childCount()):
                testroot = fileroot.child(_t)
                testname = testroot.text(0)
                print(testname)
                for _c in range(testroot.childCount()):
                    curve_item = testroot.child(_c)
                    curveData = curve_item.data(0, Qt.UserRole)
                    project.files[_f].sequence[testname][_c] = curveData
        self.wg_canvas.mainwindow.project = project
