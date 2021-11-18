# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 22:48:22 2017

@author: Luighi
"""
import re

def getFromPSpice(filename):
    """
        Extract database from .csd file 
        result from simuation with PSpice
    """
    
    lstd=[]
    state = 0
    
    f= open(filename,'r')
    
    for line in f:
        line = line.strip("\n")
        
        if state == 0:
            if line.startswith("#H"):
                newdic = {}
                newdic['HEADER']={}
                state=1
        elif state == 1:
            if line.startswith("#N"):
                newdic['NODES']=""
                state=2   
            else:
                for item in re.findall("(\S+)='([^'\t\n\r\f\v]+)'",line):
                    newdic['HEADER'][item[0]]=item[1]
        elif state == 2:
            if line.startswith("#C"):
                newdic['DATA']=[]
                newlst=[line.split()[1],line.split()[2],""]
                state=3
            else:
                newdic['NODES']+=line
        elif state == 3:
            if line.startswith("#C"):
                newdic['DATA']+=[newlst]
                newlst=[line.split()[1],line.split()[2],""]
            elif line.startswith("#;"):
                newdic['DATA']+=[newlst]
                lstd+=[newdic]
                state=0
            else:                
                newlst[2]+=line
            
    return lstd

def getData(lstd,name):
    
    lst=[]
    for dic in lstd:
        if "SWEEPVAR" in dic["HEADER"]:
            sweep= dic["HEADER"]["SWEEPVAR"]
        else:
            sweep=""
            
        if name ==sweep:
            ilst=[float(ind[0]) for ind in dic["DATA"]]
        else:
            nodes= [node.strip("'") for node in dic["NODES"].split()]
            idx = nodes.index(name)
            
            ilst=[getValueIndex(ind[2],idx) for ind in dic["DATA"]]
            
        lst+=[ilst]
    
    return lst
    
def getValueIndex(string,idx):
    lst = string.split()
    value = lst[idx].split(":")[0]
    
    return float(value)
        
def getStepInfo(lstd):
    lst=[]
    for dic in lstd:
        subtitle = dic["HEADER"]["SUBTITLE"]
        strings = subtitle.strip("Step ").split("=")
        values = (strings[0].strip(),float(strings[1]))
        lst+=[values]
    return lst

def getSweepData(lstd):
    lst=[]
    for dic in lstd:
        ilst=[float(ind[0]) for ind in dic["DATA"]]
        lst+=[ilst]
    
    return lst
    
if __name__ == "__main__":
    lstd= getFromPSpice("macromodelisfet.csd")
    
    Vbias= getSweepData(lstd)
    xis = getData(lstd,"I(Vid)")
    step = getStepInfo(lstd)
    
    import pylab
    
    for ind in range(len(Vbias)):
        pylab.plot(Vbias[ind],xis[ind],label="".join([step[ind][0],
                         "=",str(step[ind][1])]))
    
    pylab.legend()