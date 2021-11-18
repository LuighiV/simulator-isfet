# -*- coding: utf-8 -*-
"""
Created on Fri Oct 06 17:01:33 2017

@author: Luighi
"""

import numpy as np
import pandas as pd

def extractExperimentData(filename):
    
    df = pd.read_csv(filename,sep='\t')
    
    volts = list(df["Volts"].values)
    current = list(df["Current"].values)
    
    return volts, current
    
def extractFromFiles(lst):
    volts = []
    current = []
    dic = {}
    for filename in lst:
        v,c=extractExperimentData(filename)
        volts+=[v]
        current+=[c]
        
    dic["volts"]=volts
    dic["current"]=current
    
    return dic
    
if __name__ == "__main__":
    
    volts, current = extractExperimentData("idsvdsmeasurements-0.txt")