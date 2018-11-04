from PySide2 import QtWidgets, QtGui, QtCore

import maya.utils as utils


class Base(object):
    # _hover = QtCore.Signal(str)
    # signal_str = 'HOVER'

    def __init__(self):
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setFamily('Calibri')
        self.setFont(font)

        self._hover = False
        self._glow_index = 0

        self._anim_timer = QtCore.QTimer()
        self._anim_timer.timeout.connect(self._animate_glow)

    def _animate_glow(self):
        if self._hover:
            if self._glow_index >= 10:
                self._glow_index = 10
                self._anim_timer.stop()
            else:
                self._glow_index += 1
        else:
            if self._glow_index <= 0:
                self._glow_index = 0
                self._anim_timer.stop()
            else:
                self._glow_index -= 1

        print self._glow_index

        utils.executeDeferred(self.update)

    def enterEvent(self, event):
        super(self.__class__, self).enterEvent(event)

        print 'running enterEvent'

        if not self.isEnabled():
            return

        self._hover = True
        self._start_anim()

    def leaveEvent(self, event):
        super(self.__class__, self).leaveEvent(event)

        if not self.isEnabled():
            return

        self._hover = False
        self._start_anim()

    def _start_anim(self):
        print 'animtimer'
        if self._anim_timer.isActive():
            return

        self._anim_timer.start(20)
