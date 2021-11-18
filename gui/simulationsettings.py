# -*- coding: utf-8 -*-
"""
Created on Tue Oct 03 15:40:45 2017

@author: Luighi
"""

from PyQt4 import QtGui,QtCore


class SimulationSettings(QtGui.QWidget):
    
    def __init__(self,parent=None):
        
        super(SimulationSettings,self).__init__()
        
        self.sim1 = SimulationDCSweep("For curve IDS vs VGS")
        self.sim1.setDCvalues(0,1.6,0.01)
        self.sim1.setStepValues([0.098,0.109,0.119,0.131,0.140])
        self.sim1.setDCvar("Vbias")
        self.sim1.setStepvar("Vd")
        
        self.sim2 = SimulationDCSweep("For curve IDS vs VDS")
        self.sim2.setDCvalues(0,2.0,0.01)
        self.sim2.setStepValues([0.750,0.800,0.850,0.900,0.950,1.000,1.050])
        self.sim2.setDCvar("Vd")
        self.sim2.setStepvar("Vbias")
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.sim1)
        layout.addWidget(self.sim2)
        
        self.setLayout(layout)
        
    def getSettings(self):
        lst = [self.sim1.getSettings(),self.sim2.getSettings()]
        return lst

class SimulationDCSweep(QtGui.QGroupBox):
    
    def __init__(self,title="Simulation DC"):
        
        super(SimulationDCSweep,self).__init__(title)
        
        self.initGUI()
        
    def initGUI(self):
        
        dcbox=QtGui.QGroupBox("DC Analysis")
        
        self.sweepvariable=QtGui.QLabel("Vbias")
        self.start = ParameterBox("Start",0)
        self.stop = ParameterBox("Stop",1.6)
        self.inc = ParameterBox("Inc.",0.01)
        
        dcl = QtGui.QHBoxLayout()
        dcl.addWidget(self.start)
        dcl.addWidget(self.stop)
        dcl.addWidget(self.inc)
        dcbox.setLayout(dcl)
        
        stepbox = QtGui.QGroupBox("Step Analysis")
        self.stepvariable = QtGui.QLabel("Vd")
        listlabel = QtGui.QLabel("List")
        listlabel.setAlignment(QtCore.Qt.AlignTop)
        self.list = ListContent([0.098,0.109,0.119,0.131,0.140]) 
        stepl = QtGui.QHBoxLayout()
        stepl.addWidget(listlabel)
        stepl.addSpacing(10)
        stepl.addWidget(self.list)
        stepl.addStretch(1)
        stepbox.setLayout(stepl)
        
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(dcbox)
        layout.addWidget(stepbox)
        self.setLayout(layout)
        
#        self.setMaximumWidth(200)

    def setDCvalues(self,start,stop,inc):
        self.start.setText(str(start))
        self.stop.setText(str(stop))
        self.inc.setText(str(inc))
        
    def getDCvalues(self):
        lst = [float(self.start.text()),
               float(self.stop.text()),
                float(self.inc.text())]
        return lst
        
    def setStepValues(self,lst):
        self.list.setValues(lst)
        
    def getStepValues(self):
        content = self.list.toPlainText()
        content.trimmed()
        lcont = content.split("\n")
        values= map(float,lcont)
        return values
            
    def setDCvar(self,var):
        self.sweepvariable.setText(var)
        
    def setStepvar(self,var):
        self.stepvariable.setText(var)
    
    def getSettings(self):
        dic = {
            "dcvar": str(self.sweepvariable.text()),
            "stepvar": str(self.stepvariable.text()),
            "dcsweep": self.getDCvalues(),
            "step":self.getStepValues()
        } 
        return dic
        
class ParameterBox(QtGui.QWidget):
    
    def __init__(self,label="var",value=0):
        
        super(ParameterBox,self).__init__()
        
        qlabel = QtGui.QLabel(label)
        qlabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.qvalue = EditContent()
        self.qvalue.setText(str(value))
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(qlabel)
        layout.addWidget(self.qvalue)
        
        layout.setContentsMargins(0,0,0,0)
        self.setContentsMargins(0,0,0,0)
        
        self.setLayout(layout)

    def setText(self,string):
        self.qvalue.setText(string)
    
    def text(self):
        return self.qvalue.text()
        
class EditContent(QtGui.QLineEdit):
    
    def __init__(self):
        
        super(EditContent,self).__init__()
        
        validator = QtGui.QDoubleValidator()
#        self.setMaximumWidth(100)
        self.setValidator(validator)
        
class ListContent(QtGui.QTextEdit):
    
    def __init__(self,listvalues):
        super(ListContent,self).__init__()
        
        self.setText("\n".join(map(str,listvalues)))
        self.setMaximumHeight(100)
        self.setMaximumWidth(100)
                
    def setValues(self,listvalues):
        self.setText("\n".join(map(str,listvalues)))
        
        
if __name__ == "__main__":
    
    
    import sys
    
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Settings')
    
    cw = SimulationSettings()
    
    mw.setCentralWidget(cw)
    mw.show()

    sys.exit(app.exec_())           