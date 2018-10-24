from PySide2 import QtWidgets, QtGui, QtCore
import pymel.core as pm
import maya.cmds as cmds
# Dockable options
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class Interpolate(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Interpolate, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Interpolator')
        self.setFixedWidth(314)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.layout().addWidget(scroll_area)

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setAlignment(QtCore.Qt.AlignTop)
        main_widget.setLayout(main_layout)
        scroll_area.setWidget(main_widget)

        self.interp_layout = QtWidgets.QVBoxLayout()
        self.interp_layout.setContentsMargins(0, 0, 0, 0)
        self.interp_layout.setSpacing(0)
        self.interp_layout.setAlignment(QtCore.Qt.AlignTop)
        main_layout.addLayout(self.interp_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setAlignment(QtCore.Qt.AlignRight)
        main_layout.addLayout(button_layout)

        add_button = QtWidgets.QPushButton('New..')
        button_layout.addWidget(add_button)

        new_widget = InterpolateWidget()
        new_widget.hide_close_button()
        self.interp_layout.addWidget(new_widget)

        self._interp_widget = []
        self._interp_widget.append(new_widget)

        self._dock_name = self._dock_widget = None

        add_button.clicked.connect(self.add)

    def add(self):
        new_widget = InterpolateWidget()
        self.interp_layout.addWidget(new_widget)
        self._interp_widget.append(new_widget)
        self.connect(new_widget, QtCore.SIGNAL('CLOSE'), self.remove)
        print 'add'

    def remove(self, interp_widget):
        print 'remove'
        self._interp_widget.remove(interp_widget)
        self.interp_layout.removeWidget(interp_widget)
        interp_widget.deleteLater()

    def connect_dock_widget(self, dock_name, dock_widget):  # Might be irrelevant
        self._dock_widget = dock_widget
        self._dock_name = dock_name

    def close_dock(self):
        if self._dock_widget:
            cmds.deleteUI(self._dock_name)
        else:
            QtWidgets.QDialog.close(self)
        self._dock_widget = self._dock_name = None


class InterpolateWidget(QtWidgets.QFrame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.setFixedHeight(150)
        # self.setFixedWidth(320)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(5)
        # self.layout().setAlignment(QtCore.Qt.AlignTop)

        title_layout = QtWidgets.QHBoxLayout()
        select_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        slider_layout = QtWidgets.QHBoxLayout()
        check_layout = QtWidgets.QHBoxLayout()
        self.layout().addLayout(title_layout)
        self.layout().addLayout(select_layout)
        self.layout().addLayout(button_layout)
        self.layout().addLayout(slider_layout)
        self.layout().addLayout(check_layout)

        title_line_edit = QtWidgets.QLineEdit('Untitled')
        title_layout.addWidget(title_line_edit)

        self.close_button = QtWidgets.QPushButton('X')
        self.close_button.setFixedHeight(20)
        self.close_button.setFixedWidth(20)
        title_layout.addWidget(self.close_button)

        store_items = QtWidgets.QPushButton('Store Items')
        clear_items = QtWidgets.QPushButton('Clear Items')

        select_layout.addSpacerItem(QtWidgets.QSpacerItem
                                    (5, 5, QtWidgets.QSizePolicy.Expanding))
        select_layout.addWidget(store_items)
        select_layout.addWidget(clear_items)
        select_layout.addSpacerItem(QtWidgets.QSpacerItem
                                    (5, 5, QtWidgets.QSizePolicy.Expanding))

        self.store_start_button = QtWidgets.QPushButton('Store Start')
        self.reset_item_button = QtWidgets.QPushButton('Reset')
        self.store_end_button = QtWidgets.QPushButton('Store End')

        button_layout.addWidget(self.store_start_button)
        button_layout.addWidget(self.reset_item_button)
        button_layout.addWidget(self.store_end_button)

        self.start_label = QtWidgets.QLabel('Start')
        self.slider = QtWidgets.QSlider()
        self.slider.setRange(0, 49)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.end_label = QtWidgets.QLabel('End')

        slider_layout.addWidget(self.start_label)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.end_label)

        self.transforms_checkbox = QtWidgets.QCheckBox('Transform')
        self.attributes_checkbox = QtWidgets.QCheckBox('UD Attributes')
        self.transforms_checkbox.setCheckState(QtCore.Qt.Checked)

        check_layout.addWidget(self.transforms_checkbox)
        check_layout.addWidget(self.attributes_checkbox)

        self.items = {}
        self.slider_down = False

        self.close_button.clicked.connect(self.close_widget)

        store_items.clicked.connect(self.store_items)
        clear_items.clicked.connect(self.clear_items)

        self.store_start_button.clicked.connect(self.store_start)
        self.store_end_button.clicked.connect(self.store_end)
        self.reset_item_button.clicked.connect(self.reset_attributes)

        self.slider.valueChanged.connect(self.set_linear_interpolation)
        self.slider.sliderReleased.connect(self._end_slider_undo)

        self.enable_buttons(False)

    def _start_slider_undo(self):
        pm.undoInfo(openChunk=True)

    def _end_slider_undo(self):
        pm.undoInfo(closeChunk=True)
        self.slider_down = False

    def store_items(self):
        selection = pm.ls(sl=True, fl=True)
        if not selection:
            return

        self.items = {}
        for node in selection:
            self.items[node.name()] = {'node': node,
                                       'start': {},
                                       'end': {},
                                       'cache': {}}

        self.enable_buttons(True)

    def clear_items(self):
        self.items = {}
        self.enable_buttons(False)

    def enable_buttons(self, value):
        self.store_start_button.setEnabled(value)
        self.reset_item_button.setEnabled(value)
        self.store_end_button.setEnabled(value)
        self.transforms_checkbox.setEnabled(value)
        self.attributes_checkbox.setEnabled(value)
        self.slider.setEnabled(value)
        self.start_label.setEnabled(value)
        self.end_label.setEnabled(value)

    def hide_close_button(self, value=True):
        self.close_button.setVisible(not(value))

    def store_start(self):
        if not self.items:
            return
        self._store('start', 0)
        self._cache()

    def store_end(self):
        if not self.items:
            return
        self._store('end', 50)
        self._cache()

    def _store(self, key, value):
        for item_dict in self.items.values():
            node = item_dict['node']
            attrs = self.get_attributes(node)
            data = item_dict[key]
            for attr in attrs:
                data[attr] = node.attr(attr).get()

            print item_dict

        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)

    def _cache(self):
        for item_dict in self.items.values():
            node = item_dict['node']
            start = item_dict['start']
            end = item_dict['end']
            if not start or not end:
                item_dict['cache'] = None
                continue

            attrs = list(set(start.keys()) and set(end.keys()))

            cache = item_dict['cache'] = {}
            for attr in attrs:
                start_attr = start[attr]
                end_attr = end[attr]

                if start_attr == end_attr:
                    cache[attr] = None
                else:
                    cache_values = cache[attr] = []
                    interval = float(end_attr - start_attr) / 49.0
                    for index in range(50):
                        cache_values.append((interval * index) + start_attr)

    def get_attributes(self, node):
        attrs = []
        if self.transforms_checkbox.isChecked():
            for transform in 'trs':
                for axis in 'xyz':
                    channel = '%s%s' % (transform, axis)
                    if node.attr(channel).isLocked():
                        continue
                    attrs.append(channel)

        if self.attributes_checkbox.isChecked():
            for attr in node.listAttr(userDefined=True):
                if attr.type() not in ('double', 'int'):
                    continue
                if attr.isLocked():
                    continue

                attrs.append(attr.name().split('.')[-1])

        return attrs

    def reset_attributes(self, *args):
        if not self.items:
            return

        for item_dict in self.items.values():
            node = item_dict['node']
            attrs = self.get_attributes(node)

            for attr in attrs:
                default_value = pm.attributeQuery(attr,
                                                  node=node,
                                                  listDefault=True)[0]
                node.attr(attr).set(default_value)

    def set_linear_interpolation(self, value):
        if not self.items:
            return

        if not self.slider_down:
            self._start_slider_undo()
            self.slider_down = True

        for item_dict in self.items.values():
            node = item_dict['node']
            start = item_dict['start']

            if not start or not item_dict['end']:
                continue

            cache = item_dict['cache']

            for attr in cache.keys():
                if cache[attr] is None:
                    continue
                pm.setAttr(node.attr(attr), cache[attr][value])

    def close_widget(self):
        print 'emit'
        self.emit(QtCore.SIGNAL('CLOSE'), self)


dialog = None


def create_ui(docked=True):
    global dialog

    if dialog is None:
        dialog = Interpolate()
    if docked:
        dialog.show(dockable=True, floating=False, area='right')
    else:
        dialog.show()


def delete_ui():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None
