from PyQt5.QtWidgets import QWidget, QComboBox, QDialog, QDialogButtonBox, \
    QHBoxLayout, QVBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from .obj_data import CurveType


class CanvasSetting_Dialog(QDialog):
    """
    :ivar MainWindow mainwindow: The mainwindow object that triggers this dialog window.
    :vartype MyCanvas wg_canvas:
            A self-defined QWidget component placed on the center of the mainwindow.

    :ivar dict form_parameter: 

    """

    def __init__(self, mainwindow=None):
        super().__init__()
        self.mainwindow = mainwindow
        self.wg_canvas = mainwindow.wg_canvas
        self.form_parameter = {}

        self.initUI()

    def initUI(self):
        """ Initial dialog's user interface. """
      # Create Component
        dlg_btnBox = QDialogButtonBox()
        dlg_btnBox.setOrientation(Qt.Horizontal)
        dlg_btnBox.setStandardButtons(QDialogButtonBox.Ok)
        dlg_btnBox.accepted.connect(self.accept)
        self.form = self._create_form()
        self.form.setObjectName("form")
      # Layout
        vbly_main = QVBoxLayout()
        vbly_main.addWidget(self.form)
        vbly_main.addWidget(dlg_btnBox)
        self.setLayout(vbly_main)
      # Style and Setting
        self.setWindowTitle("Axis Setting")
        self.resize(300, 300)

    def cb_axis_handleTextChanged(self, event, canvas_id, ax_id):
        """
        This function connect with all QComboBox components of the form in the dialog.
        It will be triggered when any comboBox's option is changed. 

        Actually, it is not allowed to have same options on different comboBoxes 
        except 'None' option. Every two options would automatically switch their positions 
        if one of those is changed.

        :param str event: Current option text which is a CurveType name
        :param int canvas_id: The index of the canvas that need to modify its axis' CurveType 
        :param int ax_id: 
                The axis index that need to modify its CurveType. 
                0 is main axis, 1 is sub axis.


        """
        canvas = self.wg_canvas.get_canvas(id=canvas_id)
        type_to_set = CurveType(event)
        tree = self.mainwindow.dwg_data.tree

        if type_to_set == canvas.ax_types[ax_id]:
            pass
        elif type_to_set == canvas.ax_types[not ax_id]:
            canvas.fig.axes[ax_id].lines = []
            canvas.fig.axes[not ax_id].lines = []
            types = canvas.ax_types
            canvas.ax_types = [types[1], types[0]]
        else:
            type_to_transfer = canvas.ax_types[ax_id]
            canvas_origin, ax_id_origin, ax_origin = self.wg_canvas.get_canvas(
                _type=type_to_set)
            canvas.ax_types[ax_id] = type_to_set
            canvas.fig.axes[ax_id].lines = []

            if canvas_origin:
                ax_origin.lines = []
                canvas_origin.ax_types[ax_id_origin] = type_to_transfer
            tree.set_children_checkstate(type_to_transfer, Qt.Unchecked)
            canvas_origin.replot()

        tree.set_children_checkstate(type_to_set, Qt.Unchecked)
        canvas.replot()

        self._load_form_parameter()

    def _load_form_parameter(self):
        for idx, _c in enumerate(self.wg_canvas.canvasPool[:-1]):
            cbox_ax0 = self.form_parameter["Canvas"][idx]["ax0"]
            cbox_ax0.setCurrentText(_c.ax_types[0].value)

            cbox_ax1 = self.form_parameter["Canvas"][idx]["ax1"]
            cbox_ax1.setCurrentText(_c.ax_types[1].value)

    def _link_func(self, canvas_id, cb_axis):
        """
        :param int canvas_id: The index of the canvas that need to modify its axis' CurveType 
        :param QComboBox cb_axis: 
                The comboBox changed by user and also trigger this ``cb_axis_handleTextChanged`` function.
        """
        ax_id = int(bool(cb_axis.objectName() == "ax1"))
        cb_axis.currentTextChanged.connect(
            lambda event: self.cb_axis_handleTextChanged(event, canvas_id, ax_id))

    def _create_form(self):
        self.form_parameter = {"Canvas": {}}
        widget = QWidget()
        layout = QFormLayout()

        for _c in self.wg_canvas.canvasPool[:-1]:
            canvas_id = _c.id
            type_list = CurveType.list()
            type_list.remove("All")
            cbox_ax0 = QComboBox()
            cbox_ax0.addItems(type_list)
            cbox_ax0.setCurrentText(_c.ax_types[0].value)
            cbox_ax0.setObjectName("ax0")
            self._link_func(canvas_id, cbox_ax0)

            cbox_ax1 = QComboBox()
            cbox_ax1.addItems(type_list)
            cbox_ax1.setCurrentText(_c.ax_types[1].value)
            cbox_ax1.setObjectName("ax1")
            self._link_func(canvas_id, cbox_ax1)

            hbly = QHBoxLayout()
            hbly.addWidget(cbox_ax0)
            hbly.addWidget(cbox_ax1)
            layout.addRow(f"Canvas {canvas_id}", hbly)

            extra = {
                canvas_id: {
                    "name": f"Canvas {canvas_id}",
                    "ax0": cbox_ax0,
                    "ax1": cbox_ax1
                }
            }
            self.form_parameter["Canvas"].update(extra)

        widget.setLayout(layout)
        return widget
