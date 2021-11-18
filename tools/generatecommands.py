# -*- coding: utf-8 -*-
"""
Created on Wed Oct 04 12:56:05 2017

@author: Luighi
"""
import os
simulators = ["PSpice","NGSpice","LTSpice"]

def generateDCcommand(var,start,stop,inc):
    
    string =" ".join([".DC",var,str(start),str(stop),str(inc)])
    return string
    
    
def generateSTEPcommand(var,step,simulator=simulators[0],filename="output"):
    
    text = os.path.splitext(filename)
    outputname = text[0]+".txt"
    
    stringlist = " ".join(map(str,step))
    if simulator == simulators[0]:
        string = " ".join([".STEP",var,"LIST",stringlist])
    elif simulator == simulators[1]:
        string = "".join([".control \n\
set filetype=ascii \n\
echo Simulation NGSPICE > ",outputname," \n\
set appendwrite \n\
foreach step ",stringlist," \n\
    alter ",var, " $step \n\
    echo Step: ", var," = $step >> ", outputname," \n\
    run \n\
    write ", outputname, " all \n\
end \n\
quit \n\
.endc"]) 
    elif simulator == simulators[2]:
        string = " ".join([".STEP",var,"LIST",stringlist])
            
    return string
    
def generateRUNcommand(simulator=simulators[0]):
    

    if simulator == simulators[0]:
        string = ".PROBE/CSDF"         
    elif simulator == simulators[1]:
        string = ""
    elif simulator == simulators[2]:
        string = ".PROBE"
    
    return string
    
if __name__ == "__main__":
    
    print generateDCcommand("Vbias",0.,1.6,0.01)
    print generateSTEPcommand("Vd",[0.098,0.109,0.119,0.131,0.140],"PSpice")
    print generateSTEPcommand("Vd",[0.098,0.109,0.119,0.131,0.140],"NGSpice")
    print generateSTEPcommand("Vd",[0.098,0.109,0.119,0.131,0.140],"LTSpice")
    
    print generateRUNcommand("PSpice")
    print generateRUNcommand("NGSpice")
    print generateRUNcommand("LTSpice")
    