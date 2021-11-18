# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 12:26:54 2017

@author: Luighi
"""

from tools.checksimulators import checkSimulators
from tools.generateprofile import generateProfile
import tools.simulation as sm
from tools.extractdata import extractData
from tools.extractmeasurements import extractFromFiles

class SimulatorProc(object):
    
    def __init__ (self):
        
        self.parameters = {
            "global":{
                "k":1.38e-23,
                "T":300,
                "eps0":8.85e-12,
                "Ka":15.8,
                "Kb":63.1e-9,
                "Kn":1e-10,
                "Nsil":3.0e18, 
                "Nnit":1.0e16,
                "q":1.6e-19,
                "NAv":6.023e23, 
                "epsw":78.5,
                "epsihp":32,
                "epsohp":32,
                "dihp":0.1e-9,
                "dohp":0.3e-9,
                "Cbulk":0.1,
                "Eabs":4.7,
                "Phim":4.7,
                "Erel":0.200,
                "Chieo":3e-3,
                "Philj":1e-3,
            },
            "mosfet":{
                "VTO":7.11E-01,
                "LAMBDA":7.59E-03,
                "RSH":8.0E+01,
                "TOX":10E-9,
                "UO":5.21E+01,
                "TPG":0,
                "UEXP":7.64E-02,
                "NSUB":3.27E+15,
                "NFS":1.21E+11,
                "NEFF":3.88,
                "VMAX":5.35E+04,
                "DELTA":1.47,
                "LD":2.91E-06,
                "UCRIT":7.97E+04,
                "XJ":6.01E-09,
                "CJ":4.44E-4,
                "IS":1E-11,
                "CJSW":5.15E-10,
                "PHI":5.55E-01,
                "GAMMA":9.95E-01,   
                "MJ":0.395,
                "MJSW":0.242,
                "PB":0.585,  
            },
            "properties":{
                "L":100e-6, 
                "W":2000e-6,
                "NRS":5,
                "NRD":5
            }        
        }
        
        self.analysis =[
            {
                "dcvar":"Vbias",
                "stepvar":"Vd",                
                "dcsweep":[0.,1.6,0.01],
                "step":[0.098,0.109,0.119,0.131,0.140],
            },        
            {
                "dcvar":"Vd",
                "stepvar":"Vbias",
                "dcsweep":[0.,2.0,0.01],
                "step":[0.75,0.8,0.85,0.9,0.95,1.0,1.05],
            },
        ]        
        
        self.pH = 7
        
        self.refdb=[{},{}]
        self.outdb=[]
        
        self.simulators=[]
        self.basename = "macromodel"
        
    def getSimulators(self):
        
        self.simulators=checkSimulators()
        
    def generateProfiles(self,simulator):
        
#        simulator = self.simulators[selected][0]
        ##Generate commands
        for ind in range(len(self.analysis)):
            generateProfile("-".join([self.basename,simulator,str(ind)])+".cir",
                                self.parameters,
                                 self.analysis[ind],
                                 simulator,
                                 pH=self.pH)
        
        
        
    def simulate(self,simulator):
#        simulator = self.simulators[selected][0]
        results = []
        for ind in range(len(self.analysis)):
            result= sm.simulate("-".join([self.basename,simulator,str(ind)])+".cir",
                        simulator)
            results +=[result]
    
        return results
    
    def getData(self,simulator):
        
        results = []
        for ind in range(len(self.analysis)):
            result= extractData("-".join([self.basename,simulator,str(ind)])+".cir",
                        simulator)
            results +=[result]
        
        self.outdb = results
        
    def setParameters(self,dic):
        self.parameters = dic
        
    def setAnalysis(self,lst):
        self.analysis = lst
    
    def setpH(self,phvalue):
        self.pH=phvalue
    
    def getReferenceData(self,filenames,index=0):
        
        dic = extractFromFiles(filenames)
        print dic
        self.refdb[index] = dic
    
if __name__ == "__main__":
    
    sim = SimulatorProc()
    sim.getSimulators()
    print sim.simulators
    
    sim.generateProfiles("PSpice")
    sim.generateProfiles("NGSpice")
    sim.generateProfiles("LTSpice")    
    
    print sim.simulate("PSpice")
    
    print sim.simulate("NGSpice")
    
    print sim.simulate("LTSpice")
    
    sim.getData("PSpice")
    lst = sim.outdb