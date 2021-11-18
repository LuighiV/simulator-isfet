# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 19:00:47 2016

@author: lviton

========================
Simulator Contents MW
========================

Describes the main window where resides the contents

Based on:
    *paramterscontestmw by the author
    *analizercontentsmw by the author
    
"""

import sys
from PyQt4 import QtGui,QtCore

import simulatormw as smw
import parameters as pw
import simulationsettings as ss
import simulationw as sw
import circuitw as tcw
import comparatorplot as cp

class SimulatorContentsMW(smw.SimulatorMW):
    
    def __init__(self):
        super(SimulatorContentsMW,self).__init__()
        
        self.initContents()
        
    def initContents(self):
        
        ##Defining the main components
        cw= QtGui.QWidget()
        self.parameters = pw.ParametersWidget()
        self.settings = ss.SimulationSettings()
        self.simulator = sw.SimulateWidget() 
        self.circuit = tcw.CircuitWidget()
        
        self.cplot1 = cp.ComparatorWidget(title="Plot IDS vs. VGS")
        self.cplot2 = cp.ComparatorWidget(title="Plot IDS vs. VDS")
        
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.parameters)
        self.viewMenu.addAction(self.parameters.toggleViewAction())
#        self.parameters.hide()
        self.parameters.visibilityChanged.connect(self.updatewindow)
        
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.cplot1)
        self.viewMenu.addAction(self.cplot1.toggleViewAction())
        self.cplot1.hide()
        self.cplot1.visibilityChanged.connect(self.updatewindow)
        
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea,self.cplot2)
        self.viewMenu.addAction(self.cplot2.toggleViewAction())
        self.cplot2.visibilityChanged.connect(self.updatewindow)
        self.cplot2.hide()
        
        controlw= QtGui.QWidget()        
        controll=QtGui.QVBoxLayout()        
        controll.addWidget(self.simulator)
        controll.addWidget(self.circuit)
        controll.addWidget(self.settings)
        controlw.setLayout(controll)
        controlw.setContentsMargins(0,0,0,0)
        controlw.setMaximumWidth(300)
        controll.setContentsMargins(0,0,0,0)
        
        
        lmain = QtGui.QHBoxLayout()
        lmain.addWidget(controlw)
        
        cw.setLayout(lmain)
        cw.setContentsMargins(0,0,0,0)
        lmain.setContentsMargins(0,0,0,0)
#        controlw.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self.setCentralWidget(cw)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        ##Adding export action
        #Actions in file menu
#        self.exportAction = QtGui.QAction('E&xport...',self)
#        self.exportAction.setShortcut('Ctrl+E')
#        self.exportAction.setStatusTip('Export data obtained from meausrements')
#        
#        self.fileMenu.addAction(self.exportAction)
#        
#        self.exportAction.triggered.connect(self.openexportdialog)
#    
#    def openAnalizerDock(self,processor):
#        self.adock.resetPlot()
#        self.adock.setProcessor(processor)
#        self.adock.show()
#        
#    def openexportdialog(self):
#        self.exportdialog = ed.ExportDialog()
#        
    def updatewindow(self,value):
#        Thanks to https://stackoverflow.com/a/2470259/5107192
#        http://doc.qt.io/qt-4.8/qwidget.html#adjustSize
#        print "Update geometry"+str(value)
        self.adjustSize()
        self.adjustSize()
        
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    
    mw= SimulatorContentsMW()
    mw.show()
    
    sys.exit(app.exec_())
    
