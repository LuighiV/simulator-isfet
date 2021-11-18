# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 20:12:46 2017

@author: Luighi
"""

from PyQt4 import QtGui
import graphicplot as gp
#from cycler import cycler
import pandas as pd

class ComparatorPlot(gp.GraphicPlot):
    
    def __init__(self,parent=None):
        
        super(ComparatorPlot,self).__init__()
        
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()
        self.colors=['blue', 
            'red', 
            'green', 
            'brown', 
            'orange', 
            'indigo', 
            'black']
        self.markers=[
            "o","^","s","D","v","p",        
            ]
        
        
    def plotData(self,volts,current,steps):
            
        for ind in range(len(volts)):
            l, =self.ax.plot(volts[ind],current[ind],linewidth=0.8,
                             color=self.colors[ind%len(self.colors)])
        
        self.canvas.draw()
    
    def plotPoints(self,volts,current,steps):
            
        for ind in range(len(volts)):
            l, =self.ax.plot(volts[ind],current[ind],#linewidth=0.5,
                             color=self.colors[ind%len(self.colors)],
                                linestyle="None",
                                marker=self.markers[ind%len(self.markers)],
                                fillstyle="none",
                                markersize=2,markeredgewidth=0.5)
        
        self.canvas.draw()
    
    ##Function to work with simulators    
    def plotSimulator(self, simulator,index=0):
        outdb  = simulator.outdb
        refdb = simulator.refdb
        
        self.ax.clear()
        self.ax.ticklabel_format(axis='y', style='sci', scilimits=(-3,3))
    
        if len(outdb) >0:           
            self.plotData(outdb[index]["volts"],outdb[index]["current"],outdb[index]["steps"])
            
        if len(refdb[index]) > 0:
            self.plotPoints(refdb[index]["volts"],refdb[index]["current"],range(len(refdb[index]["volts"])))
            
        self.ax.grid(linestyle=":")
        
        self.canvas.draw()
            
        
    
class ExportDialog(QtGui.QDialog):
    
    def __init__(self,parent=None):
        
        super(ExportDialog,self).__init__()
        
        self.initGUI()
        
    def initGUI(self):
        ##Setting the title
        self.setWindowTitle("Export Dialog")
        
        ##Definig main components
        textlabel = QtGui.QLabel("Enter the basename (without prefix)")
        self.basename = QtGui.QLineEdit()
        self.exportbutton = QtGui.QPushButton("Export")
        cancelbutton = QtGui.QPushButton("Cancel")
        
        buttonw=QtGui.QWidget()
        buttonl=QtGui.QHBoxLayout()
        buttonl.addStretch(1)
        buttonl.addWidget(self.exportbutton)
        buttonl.addStretch(1)
        buttonl.addWidget(cancelbutton)
        buttonl.addStretch(1)
        buttonw.setLayout(buttonl)
        
        lmain= QtGui.QVBoxLayout()
        lmain.addWidget(textlabel)
        lmain.addWidget(self.basename)
        lmain.addWidget(buttonw)
        
        self.setLayout(lmain)

        cancelbutton.clicked.connect(self.reject)
        
    def exportSimulator(self,simulator,index=0):
        outdb  = simulator.outdb
        filename=self.basename.text()
        if len(outdb) >0:           
            self.exportSimData(outdb[index]["volts"],outdb[index]["current"],outdb[index]["steps"],filename)
            
    def exportSimData(self,volts,current,steps,filename):
        
        for ind in range(len(volts)):
            df = pd.DataFrame.from_items([("volts",volts[ind]),("current",current[ind])])
            df.to_csv(''.join([filename,'-',str(ind),'.txt']),sep='\t',index=False)
        
class ComparatorWidget(QtGui.QDockWidget):
    
    def __init__(self,parent=None,title="Plot Widget"):
        
        super(ComparatorWidget,self).__init__(title)
        
        self.initGUI()
        
    def initGUI(self):
        
        main = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        self.plot = ComparatorPlot()
        self.export = QtGui.QPushButton("Export data")
        self.dialog = ExportDialog()
        self.dialog.hide()
        self.load = QtGui.QPushButton("Load")
        self.edit = QtGui.QPushButton("Edit")
        
        
        controlw= QtGui.QWidget()
        controll = QtGui.QHBoxLayout()
        controll.addWidget(self.export)
        controll.addStretch(1)
        controll.addWidget(self.load)
        controll.addSpacing(20)
        controll.addWidget(self.edit)
        controlw.setLayout(controll)
        controll.setContentsMargins(0,0,0,0)
        controlw.setContentsMargins(0,0,0,0)
        
        layout.addWidget(controlw)
        layout.addWidget(self.plot)
        main.setLayout(layout)
        
        self.setMinimumWidth(500)
        
        self.setWidget(main)
        
        #Establishing connections
        self.export.clicked.connect(self.openExportDialog)
        
    def getFileNames(self):
        filenames = QtGui.QFileDialog.getOpenFileNames(self, 'Open file', 
                './')
        
        return filenames

    def openExportDialog(self):
        self.dialog.exec_()

#        if retval == 1:
#            return self.dialog.data
#        else:
#            return None
 
if __name__ == "__main__":
    
    app = QtGui.QApplication([])
    mw = QtGui.QMainWindow()
    
    comp = ComparatorWidget()
    
    mw.setCentralWidget(comp)
    
    mw.show()
    
    import sys
    sys.exit(app.exec_())