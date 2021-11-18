# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 13:15:25 2017

@author: Luighi

Simulations with PSpice, LTSpice and NGSpice

"""
#import pandas as pd
from datetime import datetime


def printNetlist(filename,parameters,properties,mosfet,
                    isfetname="ISFET",
                    mosfetname="MISFET",
                    VpH=7,Vbias=1.5,Vd=0.1,
                    commands=[]):
    
    f=open(filename,mode="w")
    
    f.write(printInfo(filename))
    #Model description
    f.write("***************************************\n")
    f.write(printParameters(parameters))
    f.write("***************************************\n")
    f.write(printISFETmodel(properties,isfetname,mosfetname))
    f.write(printMOSFETmodel(mosfet,mosfetname))
    f.write("".join([".ENDS ",isfetname," \n"]))
    f.write("***************************************\n")
    #Circuit description
    f.write(printCircuit(isfetname,VpH,Vbias,Vd))
    f.write("***************************************\n")
    #Simulation comands
    f.write("\n".join(commands))
    f.write("\n")
    f.write("".join([".END"]))
    

def dictToSPICE(d):
    string = ""
    for key in sorted(d.keys()):
        string += "".join(["+ ",key," = ",str(d[key])," \n"])    
    return string

def dictToSPICEinLine(d):
    string = ""
    for key in sorted(d.keys()):
        string += "".join([key," = ",str(d[key]),"  "])    
    return string

def printCircuit(isfetname="ISFET",VpH=7,Vbias=1.5,Vd=0.1):
    string="".join(["* Reference Testbench circuit\n\
XIS 100 1 0 0 200 ",
        isfetname,"\n",
        "Vbias 1 0 DC ", str(Vbias),"\n",
        "VpH 200 0 DC ", str(VpH),"\n",
        "Vd 110 0 DC ", str(Vd),"\n",
        "Vid 110 100 DC 0\n"])
    
    return string


def printISFETmodel(d,modelname="ISFET",mosfetname="MISFET"):
    string = "".join(["* ISFET model\n\
*-------------------------\n.SUBCKT ",
                      modelname,
                      " 6 1 3 4 101 \n",
"* drain | ref.el | source | bulk | pH input\n\
Eref 1 10 value ={Eabs - Phim - Erel + Chieo + Philj}\n\
Cref 10 2 {Ceq}\n\
EP1 46 0 value ={log(KK) + 4.6*V(101)}\n\
RP1 46 0 1G\n\
EP2 23 0 value ={log(Ka) + 2.3*V(101)}\n\
RP2 23 0 1G\n\
EPH 2 10 value = {(q/Ceq)*(Nsil*((exp(-2*V(2,10)*ET)-exp(V(46)))/(exp(-2*V(2,10)*ET)+\n\
+	exp(V(23))*exp(-1*V(2,10)*ET)+exp(V(46))))+\n\
+	Nnit*((exp(-1*V(2,10)*ET))/(exp(-1*V(2,10)*ET)+(Kn/Ka)*exp(V(23)))))}\n\
RpH 101 0 1K\n\
MIS 6 2 3 4 ",
    mosfetname,
    " ",
    dictToSPICEinLine(d),
    "\n"])
    
    return string

def printMOSFETmodel(d,modelname="MISFET",modellevel="2"):
    string = string = "".join(["* MOSFET model\n\
*-------------------------\n.MODEL ",
       modelname,
       " NMOS",
       " LEVEL=",
       modellevel,
       " \n",
       dictToSPICE(d)])
       
    return string
    
def printParameters(d):
    string = "".join(["* List of parameteres\n\
*-------------------------\n.PARAM\n",
                      dictToSPICE(d),
"+ ET = {q/(k*T)}\n\
+ sq = {sqrt(8*eps0*epsw*k*T)}\n\
+ Cb = {NAv*Cbulk}\n\
+ KK = {Ka*Kb}\n\
+ Ch = {((eps0*epsihp*epsohp)/(epsohp*dihp + epsihp*dohp))}\n\
+ Cd = {(sq*ET*0.5)*sqrt(Cb)}\n\
+ Ceq = {(Cd*Ch)/(Cd + Ch)}\n"])
        
    return string

def printInfo(filename="macromodelISFET.cir"):
    i=datetime.now()
    string= "".join(["* "+filename+"\n\
* -------------------------------------------\n* ",
         i.strftime('%Y/%m/%d %H:%M:%S'),
        "\n",
"* This is a generated file by geneteratenetlist.py\n\
*     Luighi Vitón Zorrilla <luighiavz@gmail.com>\n\
*--------------------------------------------\n\
* Behavioral Macromodel for ISFET \n\
* Developed by: Sergio Martinoia and Giuseppe Massobrio \n\
*     Bioelectronics Laboratory, Dept. of Biophysical and Electronic Eng.\n\
*     Via Opera Pia 11A, 16145, Genova, ITALY \n\
* Adapted by: Luighi Vitón Zorrilla \n\
*    Instituto Nacional de Investigación y Capacitación de Telecomunicaciones\n\
*    Universidad Nacional de Ingeniería\n"])

    return string

if __name__ == "__main__":
    
    ##General parameters
    general = {"k":1.38e-23,
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
    }
    
    ##MOSFET parameters
    mosfet = {
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
    }
    
    properties ={
        "L":100e-6, 
        "W":2000e-6,
        "NRS":5,
        "NRD":5
    }
    
    commandsPSpice =[
        ".DC Vbias 0.0 1.6 0.01",
        ".STEP Vd LIST 0.098 0.109 0.119 0.131 0.140",
        ".PROBE/CSDF"
    ]
    
    commandsNGSpice=[
        ".DC Vbias 0.0 1.6 0.01",
        ".control \n\
set filetype=ascii \n\
echo Simulation NGSPICE > macromodelisfet-ngspice.txt \n\
set appendwrite \n\
foreach step 0.098 0.109 0.119 0.131 0.140 \n\
    alter Vd $step \n\
    echo Step: Vd = $step >> macromodelisfet-ngspice.txt  \n\
    run \n\
    write macromodelisfet-ngspice.txt all \n\
end \n\
quit \n\
.endc"
    ]
    
    commandsLTSpice=[
        ".DC Vbias 0.0 1.6 0.01",
        ".STEP Vd LIST 0.098 0.109 0.119 0.131 0.140",
        ".PROBE"
    ]
#    print dictToSPICE(general)
#    print dictToSPICE(mosfet)
    print printInfo()
    print printParameters(general)
    print printISFETmodel(properties)
    print printMOSFETmodel(mosfet)
    print printCircuit()
    
#    printNetlist("macromodelisfet-pspice.cir",general,properties,mosfet,commands=commandsPSpice)
#    printNetlist("macromodelisfet-ngspice.cir",general,properties,mosfet,commands=commandsNGSpice)
    printNetlist("macromodelisfet-ltspice.cir",general,properties,mosfet,commands=commandsLTSpice)
    