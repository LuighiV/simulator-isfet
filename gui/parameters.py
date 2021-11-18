# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 01:28:46 2017

@author: Luighi
"""

from PyQt4 import QtGui


class ParametersWidget(QtGui.QDockWidget):
    """
    All the parameters
    """
    def __init__(self,parent=None):
        super(ParametersWidget,self).__init__("Parameters")
        
        self.initGUI()
        
    def initGUI(self):
        
        gp = GlobalParameters()
        mp = MOSFETParameters()
        
        self.parameters = gp.dic
        self.properties = mp.properties
        self.mosfet = mp.mosfet
        
        main = QtGui.QWidget()
        layout=QtGui.QVBoxLayout()
        layout.addWidget(gp)
        layout.addWidget(mp)
        
        main.setLayout(layout)
        self.setWidget(main)
        
    def getParameters(self):
        
        param={"global":self.parameters,
                    "mosfet":self.mosfet,
                    "properties":self.properties
        }
        
        return param
        
    def getParameterValues(self):
        
        param = self.getParameters()
        newdic = {}
        for key in param:
            dic = param[key]
            newdic[key]={}
            for dkey in dic:
                newdic[key][dkey] = float(dic[dkey].text())
                
        return newdic

class GlobalParameters(QtGui.QGroupBox):
    """
    General Parameters
    """
    def __init__(self,parent=None):
        
        super(GlobalParameters,self).__init__("Global Parameters")
        
        self.initGUI()
    
    def initGUI(self):
        
        
        struc = [
            ["General constans",[["k",0],["eps0",0],["T",1],["q",0],["NAv",0]]],
            ["Equilibrium constants",[["Ka",0],["Kb",0],["Kn",0]]],
            ["Binding-sites",[["Nsil",1],["Nnit",1]]],            
            ["Electrical constants",[["epsw",0],["epsihp",0],["epsohp",0]]],
            ["Geometrical properties",[["dihp",0],["dohp",0]]],
            ["Buffer Capacity",[["Cbulk",0]]],
            ["Reference electrode",[["Eabs",0],["Phim",0],["Erel",0],["Chieo",0],["Philj",0]]],
        ]
        parameters = {"k":1.38e-23,
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
        
        self.dic={}
        #General parameters        
        generalw= QtGui.QGroupBox("General constants")
        generall= QtGui.QGridLayout()
        generall.setHorizontalSpacing(40)
        genconst = struc[0][1]
        for ind in range(len(genconst)):
            obj = genconst[ind]
            param = ParameterBox(obj[0],obj[1],parameters[obj[0]])
            self.dic[obj[0]] = param
            generall.addWidget(param,ind/3,ind%3)
        generalw.setLayout(generall)
        
        #ISFET parameters
        isfetconst = struc[1:-1]
        isfetw= QtGui.QGroupBox("ISFET parameters")
        isfetl= QtGui.QGridLayout()
        
        for idx in range(len(isfetconst)):
            line = isfetconst[idx]
            subtitle= SubtitleBox(line[0]+":")
            isfetl.addWidget(subtitle,idx,0)
            
            widget2 = QtGui.QWidget()
            l2 = QtGui.QHBoxLayout() 
            widget2.setContentsMargins(0,0,0,0)
            l2.setContentsMargins(0,0,0,0)
            
            sconst = line[1]
            for ind in range(len(sconst)):
                obj = sconst[ind]
                param = ParameterBox(obj[0],obj[1],parameters[obj[0]])
                self.dic[obj[0]] = param
                l2.addWidget(param)
                l2.addSpacing(20)
            l2.addStretch(1)
            widget2.setLayout(l2)
            
            isfetl.addWidget(widget2,idx,1)
            
        isfetw.setLayout(isfetl)
        
        #Reference Electrode parameters
        refw= QtGui.QGroupBox("Reference electrode parameters")
        refl= QtGui.QGridLayout()
        refl.setHorizontalSpacing(40)
        refconst = struc[-1][1]
        for ind in range(len(refconst)):
            obj = refconst[ind]
            param = ParameterBox(obj[0],obj[1],parameters[obj[0]])
            self.dic[obj[0]] = param
            refl.addWidget(param,ind/3,ind%3)
        refw.setLayout(refl)
        
        
#        print self.dic
#        for key in self.dic:
#            print key+":"+self.dic[key].text()
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(generalw)
        layout.addWidget(isfetw)
        layout.addWidget(refw)
        self.setLayout(layout)

class MOSFETParameters(QtGui.QGroupBox):
    """
    General Parameters
    """
    def __init__(self,parent=None):
        
        super(MOSFETParameters,self).__init__("MOSFETparameters")
        
        self.initGUI()
    
    def initGUI(self):
        
        struc = [
            ["Physical properties",[["L",1],["W",1],["NRS",1],["NRD",1]]],
            ["Mosfet Parameters",[["VTO",1],["LAMBDA",1],["RSH",1],["TOX",1],
                                    ["UO",1],["TPG",0],["UEXP",1],
                                    ["NSUB",0],["NFS",0],["NEFF",0],
                                    ["VMAX",0],["DELTA",0],["LD",0],
                                    ["UCRIT",1],
                                    ["XJ",0],
                                    ["CJ",0],
                                    ["IS",0],
                                    ["CJSW",0],
                                    ["PHI",0],
                                    ["GAMMA",0],   
                                    ["MJ",0],
                                    ["MJSW",0],
                                    ["PB",0]
                                  ]],
            ]
        
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
        
        
        self.mosfet={}
        #MOSFET parameters        
        mosfetw= QtGui.QGroupBox("Model parameters")
        mosfetl= QtGui.QGridLayout()
        mosfetl.setHorizontalSpacing(20)
        mosconst = struc[1][1]
        for ind in range(len(mosconst)):
            obj = mosconst[ind]
            param = ParameterBox(obj[0],obj[1],mosfet[obj[0]])
            self.mosfet[obj[0]] = param
            mosfetl.addWidget(param,ind/4,ind%4)
        mosfetw.setLayout(mosfetl)
        
        self.properties={}
        #MOSFET parameters        
        propw= QtGui.QGroupBox("Physical properties")
        propl= QtGui.QGridLayout()
        propl.setHorizontalSpacing(20)
        propconst = struc[0][1]
        for ind in range(len(propconst)):
            obj = propconst[ind]
            param = ParameterBox(obj[0],obj[1],properties[obj[0]])
            self.properties[obj[0]] = param
            propl.addWidget(param,ind/4,ind%4)
        propw.setLayout(propl)        
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(propw)
        layout.addWidget(mosfetw)
        self.setLayout(layout)
        
class ParameterBox(QtGui.QWidget):
        
    def __init__(self,name="name",edit=0,value=0,):
        
        super(ParameterBox,self).__init__()
        
        label = QtGui.QLabel(name+"=")        
        if edit == 0:
            self.content = QtGui.QLabel(str(value))
        else:
            self.content = EditContent()         
            self.content.setText(str(value))

        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.content)
        layout.setContentsMargins(0,0,0,0)
#        self.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.setMaximumWidth(150)
        
    def setText(self,string):
        self.content.setText(string)
    
    def text(self):
        return self.content.text()

class EditContent(QtGui.QLineEdit):
    
    def __init__(self):
        
        super(EditContent,self).__init__()
        
        validator = QtGui.QDoubleValidator()
#        self.setMaximumWidth(100)
        self.setValidator(validator)

class SubtitleBox(QtGui.QLabel):
    
    def __init__(self,*args, **kwargs):
        
        super(SubtitleBox,self).__init__(*args, **kwargs)


if __name__ =="__main__":
    
    import sys
    app = QtGui.QApplication([])
    
    mw = QtGui.QMainWindow()
    mw.setWindowTitle('Control Widget')
    mw.resize(400,200)
    
    cw = ParametersWidget()
    
    print "Parameters"
    for key in cw.parameters:
        print key + " : "+cw.parameters[key].text()
    
    print "Properties"
    for key in cw.properties:
        print key + " : "+cw.properties[key].text()
    
    print "MOSFET"
    for key in cw.mosfet:
        print key + " : "+cw.mosfet[key].text()
        
    
    mw.setCentralWidget(cw)
    
    mw.show()
    
    sys.exit(app.exec_())