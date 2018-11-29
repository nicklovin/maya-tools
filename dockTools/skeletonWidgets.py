from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
import maya.cmds as cmds
from master_rigger import Splitter
from maya_tools.widgets import iconButton as button


class CommonSkeletonToolWidget(QtWidgets.QWidget):

    current_tool_context = None

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Fixed)

        try:
            style_sheet_file = open('C:\Users\Nick\PycharmProjects\maya_tools\stylesheets\shelf button scheme.qss', 'r')
            self.setStyleSheet(style_sheet_file.read())
        except IOError:
            pass

        joint_icon = QtGui.QIcon(':/kinJoint.png')
        joint_button = button.ShelfButton(joint_icon)
        joint_button.setMinimumHeight(50)
        joint_button.setFixedWidth(50)

        self.layout().addWidget(joint_button)

        joint_button.clicked.connect(self.joint_tool_context)

    def test(self):
        print 'success'

    def joint_tool_context(self):
        if cmds.currentCtx() == self.current_tool_context:
            return

        context_string = 'jointContext1'
        context_condition = cmds.contextInfo(context_string, exists=True)
        if context_condition:
            index = 1
            while context_condition is True:
                context_string = 'jointContext%s' % index
                context_condition = cmds.contextInfo(context_string, exists=True)
                index += 1

                if index > 100:
                    print 'infinite loop'
                    break

        cmds.jointCtx(context_string)
        cmds.setToolTo(context_string)
        self.current_tool_context = context_string
        print 'Context set to %s' % context_string
