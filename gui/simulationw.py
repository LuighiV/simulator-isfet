# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 15:46:07 2017

@author: Luighi
"""

import sys
sys.path.append("../")
from PyQt4 import QtGui

class SimulateWidget(QtGui.QWidget):
    
    def __init__(self,parent=None):
        
        super(SimulateWidget,self).__init__()
        
        self.initGUI()
        
        
    def initGUI(self):
        
        label = QtGui.QLabel("Simulator: ")
        self.listsim = QtGui.QComboBox()
        self.updatelist =QtGui.QToolButton()
        self.playbutton = QtGui.QPushButton("Simulate")
        
        self.playbutton.setIcon(self.style().standardIcon(QtGui.QStyle.SP_MediaPlay))
        self.updatelist.setIcon(self.style().standardIcon(QtGui.QStyle.SP_BrowserReload))
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.listsim)
        layout.addWidget(self.updatelist)
        layout.addSpacing(40)
        layout.addStretch(1)
        layout.addWidget(self.playbutton)
        
        self.setLayout(layout)
        
    
if __name__ == "__main__":
    
    import sys
    
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Simulation')
    
    cw = SimulateWidget()
    
    mw.setCentralWidget(cw)
    
    mw.show()
    
    sys.exit(app.exec_())

        