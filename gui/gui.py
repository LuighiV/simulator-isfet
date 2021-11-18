# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 12:00:28 2017

@author: Luighi
"""
from PyQt4 import QtGui
from simulatorcontentsmw import SimulatorContentsMW

class GUI(SimulatorContentsMW):
    
    def __init__(self,parent=None):
        
        super(GUI,self).__init__()
        
        
if __name__ =="__main__":
    
    import sys
    app = QtGui.QApplication([])
    mw = GUI()
    mw.show()
    
    sys.exit(app.exec_())