# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 18:22:34 2017

@author: Luighi
"""

simulators = ["PSpice","NGSpice","LTSpice"]

import extractpspice as xp
import extractngspice as ng
import extractltspice as lt
import os

def extractData(filename,simulator=simulators[0]):
    
    text = os.path.splitext(filename)
    
    if simulator == simulators[0]:
        dic = extractDataPSpice(text[0]+".csd")
        
    elif simulator == simulators[1]:
        dic = extractDataNGSpice(text[0]+".txt")
        
    elif simulator == simulators[2]:
        dic = extractDataLTSpice(text[0]+".raw")
    else:
        dic = None
    
    return dic

def extractDataPSpice(filename):
    lstd = xp.getFromPSpice(filename)
    volts = xp.getSweepData(lstd)
    current = xp.getData(lstd,"I(Vid)")
    steps = xp.getStepInfo(lstd)
    
    dic = {
        "volts":volts,
        "current":current,
        "steps":steps
    }
    
    return dic
    
def extractDataNGSpice(filename):
    
    lstd = ng.getFromNGSpice(filename)
    volts = ng.getSweepData(lstd)
    current = ng.getData(lstd,"i(vid)")
    steps = ng.getStepInfo(lstd)
    
    dic = {
        "volts":volts,
        "current":current,
        "steps":steps
    }
    
    return dic

def extractDataLTSpice(filename):
    
    lstd = lt.getFromLTSpice(filename)
    volts = lt.getSweepData(lstd)
    current = lt.getData(lstd,"I(Vid)")
    steps = lt.getStepInfo(lstd)
    
    dic = {
        "volts":volts,
        "current":current,
        "steps":steps
    }
    
    return dic
    
if __name__ == "__main__":
    
    dic = extractData("macromodelisfet-ngspice.cir","NGSpice")
    ndic = extractData("macromodelisfet-pspice.cir","PSpice")
    ldic = extractData("macromodelisfet-ltspice.cir","LTSpice")