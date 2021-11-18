# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 17:36:31 2017

@author: Luighi
"""

import os

def checkSimulators():
    
    names = ["PSpice","NGSpice","LTSpice"]
    programs = ["psp_cmd.exe","ngspice.exe","XVIIx64.exe"]
    lst = []
    for ind in range(len(programs)):
        item = programs[ind]
        path = which(item)
        if path is not None:
            lst+=[[names[ind],path]]
    
    return lst
    

#Obtained from Stackoverflow
# https://stackoverflow.com/a/377028/5107192
# Thanks to: Jay and harmv
def which(program):

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

    
if __name__ == "__main__":
 
    lst=checkSimulators()
    print lst
