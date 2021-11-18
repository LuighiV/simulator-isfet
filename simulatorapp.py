# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 12:07:35 2017

@author: Luighi
"""

from PyQt4 import QtGui
from gui.gui import GUI
from simulatorproc import SimulatorProc
import sys
import time

class SimulatorApplication(QtGui.QApplication):
    
    def __init__(self,parent=None):
        
        super(SimulatorApplication,self).__init__([])
        
        self.initGUI()
        self.initSimulator()
        self.connectModules()
        
        sys.exit(self.exec_())
        
    def initGUI(self):
        
        self.gui = GUI()
        
        ##disable playsim
        playsim= self.gui.simulator.playbutton
        playsim.setDisabled(True)
        
        self.gui.show()
        
    def initSimulator(self):
        self.simulator = SimulatorProc()
        
    def connectModules(self):
        
        ##Refresh simulators
        buttonrefresh=self.gui.simulator.updatelist
        buttonrefresh.clicked.connect(self.getSimulators)
        
        ##Simulate
        playsim= self.gui.simulator.playbutton
        playsim.clicked.connect(self.performSimulation)
        
        ##LoadReference
        loadbutton1 = self.gui.cplot1.load
        loadbutton2 = self.gui.cplot2.load
        loadbutton1.clicked.connect(self.loadReference1)
        loadbutton2.clicked.connect(self.loadReference2)
        
        ##ExportData
        exportbutton1 = self.gui.cplot1.dialog.exportbutton
        exportbutton2 = self.gui.cplot2.dialog.exportbutton
        exportbutton1.clicked.connect(self.exportValues1)
        exportbutton2.clicked.connect(self.exportValues2)
        
         
    def getSimulators(self):
        
        combow = self.gui.simulator.listsim
        playsim= self.gui.simulator.playbutton
        self.simulator.getSimulators()
        
        if len(self.simulator.simulators) >0:
            simulators = [sim[0] for sim in self.simulator.simulators]  
            combow.clear()
            combow.addItems(simulators)
            playsim.setEnabled(True)
        
    def performSimulation(self):
        
        
        parw= self.gui.parameters
        sett = self.gui.settings
        cirw= self.gui.circuit
        combow = self.gui.simulator.listsim
        
        currentsim = str(combow.currentText())
        ##Get parameters
        print "Get parameters..." 
        param = parw.getParameterValues()
        print param
        
        print "Get Settings"
        analysis = sett.getSettings()
        print analysis
        
        print "Get circuit test"
        phvalue= cirw.getValue()
        
        print "Set in simulator"
        self.simulator.setParameters(param)
        self.simulator.setAnalysis(analysis)      
        self.simulator.setpH(phvalue)
        
        ##Generate Netlists
        print "Generating netlists..."
        self.simulator.generateProfiles(currentsim)
        
        ##simulate
        print "Simulating..."
        start = time.time()
        print "Start time: %f"%start 
        simout = self.simulator.simulate(currentsim)
        end = time.time() 
        print "End time: %f"%end
        print "Total time: %f"%(end-start)
        
        
        ##Getting data
        if (simout[0] and simout[1]) is True:
            print "Getting data..."
            self.simulator.getData(currentsim)
            outdb = self.simulator.outdb
            
            print outdb[0]
            
            print "Plotting data..."
            comp1 = self.gui.cplot1.plot
            comp2 = self.gui.cplot2.plot
            comp1.plotSimulator(self.simulator,0)
            comp2.plotSimulator(self.simulator,1)
            self.gui.cplot1.show()
            self.gui.cplot2.show()
#            comp1.plotData(outdb[0]["volts"],outdb[0]["current"],outdb[0]["steps"])
#            comp2.plotData(outdb[1]["volts"],outdb[1]["current"],outdb[1]["steps"])
        
        else:
            print "Simulation failed, please check log files"
        
        
    def loadReference1(self):
        filenames = self.gui.cplot1.getFileNames()
        self.simulator.getReferenceData(filenames,0)
        
        comp1 = self.gui.cplot1.plot
        comp1.plotSimulator(self.simulator,0)
        self.gui.cplot1.show()
    
    def loadReference2(self):
        filenames = self.gui.cplot2.getFileNames()
        self.simulator.getReferenceData(filenames,1)
        
        comp2 = self.gui.cplot2.plot
        comp2.plotSimulator(self.simulator,1)
        self.gui.cplot2.show()    
    
    def exportValues1(self):
        print "Exporting data plot 1..."
        dialog1 = self.gui.cplot1.dialog
        dialog1.exportSimulator(self.simulator,0)
        QtGui.QMessageBox.information(self.gui,'Message',
            "Successful export", QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
        
    def exportValues2(self):
        print "Exporting data plot 2..."
        dialog2 = self.gui.cplot2.dialog
        dialog2.exportSimulator(self.simulator,1)
        QtGui.QMessageBox.information(self.gui,'Message',
            "Successful export", QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)
        
if __name__ == "__main__":
    
    app = SimulatorApplication()