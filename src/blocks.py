#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

BLOCKSIZE=100
SCREENSIZE=600
NUMBER=7
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore

class StateSwitchEvent(QtCore.QEvent):
    StateSwitchType = QtCore.QEvent.User + 256

    def __init__(self, rand=0):
        super(StateSwitchEvent, self).__init__(StateSwitchEvent.StateSwitchType)

        self.m_rand = rand

    def rand(self):
        return self.m_rand

import time
class QGraphicsRectWidget(QtGui.QGraphicsWidget):
    def __init__(self,parent=None):
        QtGui.QGraphicsWidget.__init__(self)
        self.ran=1
        print(self.ran)
    def paint(self, painter, option, widget):
        if int(time.time())%6==0:
            rand=random.randint(1,NUMBER)
            self.ran=rand
        path=str(self.ran)+'.png'
        pixmap=QPixmap(path,"1")
        pixmap=pixmap.scaled(BLOCKSIZE, BLOCKSIZE)
        painter.drawPixmap(self.rect(), pixmap, self.rect())
        #painter.fillRect(self.rect(), QtCore.Qt.blue)




class StateSwitchTransition(QtCore.QAbstractTransition):
    def __init__(self, rand):
        super(StateSwitchTransition, self).__init__()

        self.m_rand = rand

    def eventTest(self, event):
        return (event.type() == StateSwitchEvent.StateSwitchType and
                event.rand() == self.m_rand)

    def onTransition(self, event):
        pass


class StateSwitcher(QtCore.QState):
    def __init__(self, machine):
        super(StateSwitcher, self).__init__(machine)

        self.m_stateCount = 0
        self.m_lastIndex = 0

    def onEntry(self, event):
        n = QtCore.qrand() % self.m_stateCount + 1
        while n == self.m_lastIndex:
            n = QtCore.qrand() % self.m_stateCount + 1

        self.m_lastIndex = n
        self.machine().postEvent(StateSwitchEvent(n))

    def onExit(self, event):
        pass

    def addState(self, state, animation):
        self.m_stateCount += 1
        trans = StateSwitchTransition(self.m_stateCount)
        trans.setTargetState(state)
        self.addTransition(trans)
        trans.addAnimation(animation)


def createGeometryState(w1, rect1, w2, rect2, w3, rect3, w4, rect4, parent):
    result = QtCore.QState(parent)

    result.assignProperty(w1, 'geometry', rect1)
    result.assignProperty(w2, 'geometry', rect2)
    result.assignProperty(w3, 'geometry', rect3)
    result.assignProperty(w4, 'geometry', rect4)

    return result


def startanimation(parent=None):
    import sys

    app = QtGui.QApplication(sys.argv)

    button1 = QGraphicsRectWidget()
    button2 = QGraphicsRectWidget()
    button3 = QGraphicsRectWidget()
    button4 = QGraphicsRectWidget()
    button2.setZValue(1)
    button3.setZValue(2)
    button4.setZValue(3)

    scene = QtGui.QGraphicsScene(0, 0, SCREENSIZE, SCREENSIZE,parent=parent)
    scene.setBackgroundBrush(QtCore.Qt.black)
    scene.addItem(button1)
    scene.addItem(button2)
    scene.addItem(button3)
    scene.addItem(button4)

    window = QtGui.QGraphicsView(scene,parent=parent)
    window.setFrameStyle(0)
    window.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    window.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    window.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    machine = QtCore.QStateMachine()

    group = QtCore.QState()
    timer = QtCore.QTimer()
    timer.setInterval(1250)
    timer.setSingleShot(True)
    group.entered.connect(timer.start)

    state1 = createGeometryState(button1, QtCore.QRect(BLOCKSIZE*2, 0, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(BLOCKSIZE*3, 0, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(SCREENSIZE-BLOCKSIZE*2, 0, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, 0, BLOCKSIZE, BLOCKSIZE), group)

    state2 = createGeometryState(button1, QtCore.QRect(SCREENSIZE-BLOCKSIZE,BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(SCREENSIZE-BLOCKSIZE, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), group)

    state3 = createGeometryState(button1, QtCore.QRect(BLOCKSIZE*3, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(BLOCKSIZE*2, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(0, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), group)

    state4 = createGeometryState(button1, QtCore.QRect(0, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(0, BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(0, BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(0, 0, BLOCKSIZE, BLOCKSIZE), group)

    state5 = createGeometryState(button1, QtCore.QRect( BLOCKSIZE*2,BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(BLOCKSIZE*3, BLOCKSIZE*2, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(BLOCKSIZE*2, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(BLOCKSIZE*3, BLOCKSIZE*3, BLOCKSIZE, BLOCKSIZE), group)

    state6 = createGeometryState(button1, QtCore.QRect(BLOCKSIZE, BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE,BLOCKSIZE),
            button3, QtCore.QRect(BLOCKSIZE, SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(SCREENSIZE-2*BLOCKSIZE, SCREENSIZE-2*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), group)

    state7 = createGeometryState(button1, QtCore.QRect(0, 0, BLOCKSIZE, BLOCKSIZE),
            button2, QtCore.QRect(SCREENSIZE-BLOCKSIZE, 0, BLOCKSIZE, BLOCKSIZE),
            button3, QtCore.QRect(0, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE),
            button4, QtCore.QRect(SCREENSIZE-BLOCKSIZE, SCREENSIZE-BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), group)

    group.setInitialState(state1)

    animationGroup = QtCore.QParallelAnimationGroup()
    anim = QtCore.QPropertyAnimation(button4, 'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
    animationGroup.addAnimation(anim)

    subGroup = QtCore.QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(100)
    anim = QtCore.QPropertyAnimation(button3, 'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    subGroup = QtCore.QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(150)
    anim = QtCore.QPropertyAnimation(button2, 'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    subGroup = QtCore.QSequentialAnimationGroup(animationGroup)
    subGroup.addPause(200)
    anim = QtCore.QPropertyAnimation(button1, 'geometry')
    anim.setDuration(1000)
    anim.setEasingCurve(QtCore.QEasingCurve.OutElastic)
    subGroup.addAnimation(anim)

    stateSwitcher = StateSwitcher(machine)
    group.addTransition(timer.timeout, stateSwitcher)
    stateSwitcher.addState(state1, animationGroup)
    stateSwitcher.addState(state2, animationGroup)
    stateSwitcher.addState(state3, animationGroup)
    stateSwitcher.addState(state4, animationGroup)
    stateSwitcher.addState(state5, animationGroup)
    stateSwitcher.addState(state6, animationGroup)
    stateSwitcher.addState(state7, animationGroup)

    machine.addState(group)
    machine.setInitialState(group)
    machine.start()

    window.resize(SCREENSIZE, SCREENSIZE)
    window.show()

    
    sys.exit(app.exec_())
startanimation()