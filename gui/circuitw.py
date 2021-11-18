# -*- coding: utf-8 -*-
"""
Created on Mon May 07 19:14:42 2018

@author: Luighi
"""

import sys
sys.path.append("../")
from PyQt4 import QtGui
import parameters as param


class CircuitWidget(QtGui.QWidget):
    
    def __init__(self,parent=None):
        
        super(CircuitWidget,self).__init__()
        
        self.initGUI()
        
        
    def initGUI(self):
        
        label = QtGui.QLabel("Test circuit: ")
        self.paramw = param.ParameterBox(name="pH",edit=1,value=7) 
        
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(self.paramw)
        self.setLayout(layout)
    
    def getValue(self):
        return float(self.paramw.text())
    
if __name__ == "__main__":
    
    import sys
    
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Circuit')
    
    cw = CircuitWidget()
    
    mw.setCentralWidget(cw)
    
    mw.show()
    
    sys.exit(app.exec_())

        