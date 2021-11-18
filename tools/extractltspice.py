# -*- coding: utf-8 -*-
"""
Created on Mon May 07 14:37:54 2018

@author: Luighi
"""
import os

def getFromLTSpice(filename):
    """
    obtain dict from LTSpice output data
    """
    
    f = open(filename,"r")
    state = 0
#    lstd = []
    
    for line in f:
        
        line = line.strip("\n")
#        print state
        if  state == 0:
            
            if line.startswith("Title"):
                newdic={}
                newdic["HEADER"]={}
                values=line.split(":")
                newdic["HEADER"][values[0]]=values[1]
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
            
            if len(tockens) >1:
                newlst=[tockens[1]]
                state=4
                
        elif state==4:
            
            tockens = line.split()
#            print tockens
            if len(tockens) >1:
                newdic["DATA"]+=[newlst]
                newlst = []
                newlst=[tockens[1]]
                
            else:
                newlst+=[tockens[0]]
    
    newdic["DATA"]+=[newlst]
    
#    lstd+=[newdic]
    
    return newdic

def groupData(inputlist):
    
    lst=[]
    state =  0
    for item in inputlist:
#        print item        
        if state==0:
            refitem = item[0]
            newlst=[item]
            state=1
        
        elif state==1:
            if item [0]> refitem:
                newlst+=[item]
            else:
                lst+=[newlst]
                newlst=[item]
    
    lst+=[newlst]
    return lst
    
def getData(dic,name):
    
    lst=[]
    gdata = groupData(dic["DATA"])
    
    variablenames=[ind[1] for ind in dic["NODES"]]
    idx = variablenames.index(name)
#    print idx
#    print gdata
    for item in gdata:
            
        newlst=[]
        
        for vector in item:
            newlst+=[float(vector[idx])]
        
        lst+=[newlst]
        
    return lst

def getStepInfo(dic):
    #this info is inside the log file resulted from the simulation
    #so the algorithm checks if the it exists in the directory
    
    nametitle = dic["HEADER"]["Title"].strip(' * ')
    fname,ext = nametitle.split('.')
#    print fname
    logfile='.'.join([fname,'log'])
    
    
    steps=[]
    if os.path.isfile(logfile):
        
        f = open (logfile,'r')
        
        for line in f:
            if line.startswith(".step"):
                value= line.split()[1].split('=')
                steps+=[tuple([value[0],float(value[1])])]
    else:
        print "The file wasn't encountered. Please provide the logfile."
    
    return steps
    
def getSweepData(dic):
    gdata = groupData(dic["DATA"])
    
    lst = []
    #every group has the same sweep data and corresponds to the 
    #first column
    for item in gdata:
        lst += [[float(i[0]) for i in item]]
        
    return lst
    
    
if __name__ == "__main__":
    
    dic= getFromLTSpice("macromodelisfet-ltspice.raw")
    
    data=groupData(dic["DATA"])
    
    vsweep=getSweepData(dic)
    current=getData(dic,"I(Vid)")
    step= getStepInfo(dic)
    
    import pylab
    pylab.figure()
    
    for i in range(len(vsweep)):
        pylab.plot(vsweep[i],current[i],label="".join([step[i][0],"=",str(step[i][1])]))
        
    pylab.legend(loc="best")
    pylab.grid()
    