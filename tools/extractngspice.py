# -*- coding: utf-8 -*-
"""
Created on Sun Oct 01 22:22:17 2017

@author: Luighi
"""

def getFromNGSpice(filename):
    """
    obtain dict from NGSpice output data
    """
    
    f = open(filename,"r")
    state = 0
    lstd = []
    
    for line in f:
        
        line = line.strip("\n")
#        print state
        if  state == 0:
            
            if line.startswith("Simulation "):
                newdic={}
                newdic["HEADER"]={}
                state=1
                
        elif state == 1:
            
            if line.startswith("Variables:"):
                newdic["NODES"]=[]
                state = 2
            else:
                values=line.split(":")
                newdic["HEADER"][values[0]]=values[1]
        
        elif state==2:
            
            if line.startswith("Values:"):
                newdic["DATA"]=[]
                state = 3
            else:
                newdic["NODES"]+=[tuple(line.split())]
                
        elif state==3:
            
            tockens = line.split()
            
            if tockens[0].isdigit():
                newlst=[tockens[1]]
                state=4
            else:
                print "Add dictionary"
                lstd+=[newdic]
                newdic={}
                newdic["HEADER"]={}
                
                values=line.split(":")
                newdic["HEADER"][values[0]]=values[1]
                state=1
                
        elif state==4:
            
            if line is "":
                newdic["DATA"]+=[newlst]
                newlst = []
                state =3
            else:
                value = line.split()
                newlst+=[value[0]]
    
    lstd+=[newdic]
    
    return lstd
    
def getData(lstd,name):
    
    lst=[]
    for dic in lstd:
        
        variablenames=[ind[1] for ind in dic["NODES"]]
        idx = variablenames.index(name)
        newlst=[]
        
        for data in dic["DATA"]:
            newlst+=[float(data[idx])]
        
        lst+=[newlst]
        
    return lst

def getStepInfo(lstd):
    lst =[]
    
    for dic in lstd:
        step=dic["HEADER"]["Step"]
        strings = step.split("=")
        values = (strings[0].strip(),float(strings[1]))
        lst+=[values]
    
    return lst

def getSweepData(lstd):
    return getData(lstd,"v-sweep")    
    
    
if __name__ == "__main__":
    
    lstd= getFromNGSpice("macromodelisfet-ngspice.txt")
    
    vsweep=getSweepData(lstd)
    current=getData(lstd,"i(vid)")
    step= getStepInfo(lstd)
    
    import pylab
    pylab.figure()
    
    for i in range(len(vsweep)):
        pylab.plot(vsweep[i],current[i],label="".join([step[i][0],"=",str(step[i][1])]))
        
    pylab.legend(loc="best")
    pylab.grid()
    