# -*- coding: utf-8 -*-
"""
Created on Sun Oct 01 01:55:24 2017

@author: Luighi
"""

import subprocess
import os

def simulate(filename,simulator):
    
    if simulator == "PSpice":
        result = simulatePSpice(filename)

    elif simulator == "NGSpice":
        result = simulateNGSpice(filename)
        
    elif simulator == "LTSpice":
        result = simulateLTSpice(filename)
    
    else:
        print "".join(["The simulator ",simulator," is not supported"])
        result = None

    return result

def simulatePSpice(filename):
    p = subprocess.Popen(["psp_cmd.exe","/r",filename],stdout=subprocess.PIPE)
    successful = False
    for line in p.stdout:
        print line
    
    if "Simulation complete." in line:
       successful = True
       
    p.wait()
    return successful

def simulateNGSpice(filename):
    text = os.path.splitext(filename)
    logname = text[0]+".log"
    successful = False
    p = subprocess.Popen(["ngspice.exe","-b","-o",logname,filename],stdout=subprocess.PIPE)
#    for line in p.stdout:
#        print line
    p.wait()
    
    ##Checking result
    f= open(logname,"r")
    
    for line in f:
        print line
    
    if "ASCII raw file" in line:
        successful = True
    
    return successful

def simulateLTSpice(filename):
    text = os.path.splitext(filename)
    logname = text[0]+".log"
    successful = False
    p = subprocess.Popen(["XVIIx64.exe","-b","-ascii",filename],stdout=subprocess.PIPE)
#    for line in p.stdout:
#        print line
    p.wait()
    
    ##Checking result
    f= open(logname,"r")
    
    for line in f:
        lastline=line
    
    if lastline.startswith("\0"):
        successful = False
    else:
        successful = True
    
    return successful

if __name__ == "__main__":
    
#    state= simulatePSpice("macromodelisfet-pspice.cir")
#    print state
#    
#    state=simulateNGSpice("macromodelisfet-ngspice.cir")
#    print state
    
    state=simulateLTSpice("macromodelisfet-ltspice.cir")
    print state