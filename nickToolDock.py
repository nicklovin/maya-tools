from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as cmds


class RiggingDock(QtWidgets.QDialog):
    window_name = 'Rigging Dock'

    def __init__(self):
        super(RiggingDock, self).__init__()

        self.build_ui()

    def build_ui(self):
        self.setLayout(QtWidgets.QVBoxLayout())

        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(5)

        text_layout = QtWidgets.QHBoxLayout()
        text_layout.setSpacing(5)
        self.layout().addLayout(text_layout)

        example_label = QtWidgets.QLabel('Title:')
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        example_label.setFont(bold_font)

        example_line_edit = QtWidgets.QLineEdit()
        example_line_edit.setPlaceholderText('')

        text_layout.addWidget(example_label)
        text_layout.addWidget(example_line_edit)


def show_ui():
    ui = RiggingDock()
    ui.show()
    return ui
