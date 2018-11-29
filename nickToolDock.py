from PySide2 import QtWidgets, QtCore, QtGui
import pymel.core as pm
import maya.cmds as cmds
from functools import partial
# Dockable options
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from master_rigger import Splitter
from master_rigger import attributeManipulation as attr
from master_rigger import createNodeLibrary as node
from master_rigger import basicTools as tool
from master_rigger import curve_assignment as crv
from master_rigger import renamerLibrary as name
from dockTools import skeletonWidgets as skele
reload(attr)
reload(node)
reload(tool)
reload(crv)
reload(name)
reload(skele)


class RiggingDock(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    window_name = 'Rigging Dock'

    def __init__(self, parent=None, ss_path=''):  # set default ss if made
        super(RiggingDock, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.window_name)

        # Temp forced resizers, remove later and set default sizes
        # self.setFixedHeight(400)
        # self.setFixedWidth(600)

        # Optional Stylesheet for later work
        try:
            style_sheet_file = open(ss_path)
            self.setStyleSheet(style_sheet_file.read())
        except IOError:
            pass

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(5)

        text_layout = QtWidgets.QHBoxLayout()
        text_layout.setSpacing(5)
        self.layout().addLayout(text_layout)

        # Temporary placeholders to keep the dock active
        example_label = QtWidgets.QLabel('Title:')
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        example_label.setFont(bold_font)

        example_line_edit = QtWidgets.QLineEdit()
        example_line_edit.setPlaceholderText('')

        text_layout.addWidget(example_label)
        text_layout.addWidget(example_line_edit)

        tab_layout = QtWidgets.QHBoxLayout()
        self.layout().addLayout(tab_layout)

        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setTabPosition(tab_widget.West)
        tab_layout.addWidget(tab_widget)

        # Rigging categories
        general_tools_layout = QtWidgets.QVBoxLayout()
        skeleton_tools_layout = QtWidgets.QVBoxLayout()
        deformer_tools_layout = QtWidgets.QVBoxLayout()
        skinning_tools_layout = QtWidgets.QVBoxLayout()
        control_tools_layout = QtWidgets.QVBoxLayout()
        custom_tools_layout = QtWidgets.QVBoxLayout()

        # General tools tab ----------------------------------------------------
        general_tab = QtWidgets.QWidget()
        tab_widget.addTab(general_tab, 'General')
        general_tab.setLayout(general_tools_layout)

        # Naming functions
        name_ui = name.NamingWidget()
        general_tools_layout.addWidget(name_ui)
        general_tab.layout().addLayout(Splitter.SplitterLayout())

        # Attribute functions
        general_tab.layout().addWidget(Splitter.Splitter('Edit Attribute'))
        attr_ui = attr.AttributeWidget()
        general_tools_layout.addWidget(attr_ui)
        general_tab.layout().addLayout(Splitter.SplitterLayout())

        general_tab.layout().addWidget(Splitter.Splitter('Create Attribute'))
        add_attr_ui = attr.AddAttributesWidget()
        general_tools_layout.addWidget(add_attr_ui)
        general_tab.layout().addLayout(Splitter.SplitterLayout())

        # Node functions
        general_tab.layout().addWidget(Splitter.Splitter('Nodes'))
        node_ui = node.NodeWidget()
        general_tools_layout.addWidget(node_ui)
        general_tab.layout().addLayout(Splitter.SplitterLayout())

        # Skeleton tools tab ---------------------------------------------------
        skeleton_tab = QtWidgets.QWidget()
        tab_widget.addTab(skeleton_tab, 'Skeleton')
        skeleton_tab.setLayout(skeleton_tools_layout)

        skeleton_tab.layout().addWidget(Splitter.Splitter('Skeleton Tools'))
        skeleton_ui = skele.CommonSkeletonToolWidget()
        skeleton_tools_layout.addWidget(skeleton_ui)
        skeleton_tab.layout().addLayout(Splitter.SplitterLayout())

        # Dead Space Killer
        skeleton_tab.layout().addSpacerItem(
            QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding)
        )

        # Deformer tools tab ---------------------------------------------------
        deformer_tab = QtWidgets.QWidget()
        tab_widget.addTab(deformer_tab, 'Deformers')
        deformer_tab.setLayout(deformer_tools_layout)

        # Skinning tools tab ---------------------------------------------------
        skinning_tab = QtWidgets.QWidget()
        tab_widget.addTab(skinning_tab, 'Skinning')
        skinning_tab.setLayout(skinning_tools_layout)

        # Control tools tab ----------------------------------------------------
        controls_tab = QtWidgets.QWidget()
        tab_widget.addTab(controls_tab, 'Controls')
        controls_tab.setLayout(control_tools_layout)

        # Create Controls functions
        controls_tab.layout().addWidget(Splitter.Splitter('Create Controls'))
        curve_ui = crv.ControlCurveWidget()
        control_tools_layout.addWidget(curve_ui)
        controls_tab.layout().addLayout(Splitter.SplitterLayout())


        # Offset functions
        controls_tab.layout().addWidget(Splitter.Splitter('Offsets'))
        offset_ui = tool.OffsetNodeWidget()
        control_tools_layout.addWidget(offset_ui)
        controls_tab.layout().addLayout(Splitter.SplitterLayout())

        # Match transformations
        controls_tab.layout().addWidget(Splitter.Splitter('Transformations'))
        transforms_ui = tool.TransformWidget()
        control_tools_layout.addWidget(transforms_ui)
        controls_tab.layout().addLayout(Splitter.SplitterLayout())

        # Dead Space Killer
        controls_tab.layout().addSpacerItem(
            QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Expanding)
        )

        # Custom tools tab -----------------------------------------------------
        custom_tab = QtWidgets.QWidget()
        tab_widget.addTab(custom_tab, 'Custom')
        custom_tab.setLayout(custom_tools_layout)


dialog = None


def show_ui(docked=True):
    global dialog
    if dialog is None:
        dialog = RiggingDock()
    if docked:
        dialog.show(dockable=True, floating=False, area='right')
    else:
        dialog.show()
