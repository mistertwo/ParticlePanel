"""
DTScripts Particle Database
Database Loader Script

by Daniel Turton

Copyright (C) 2011  Daniel Turton

This file is part of the DTScripts Particle Database.

The DTScripts Particle Database is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The DTScripts Particle Database is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the DTScripts Particle Database.  If not, see <http://www.gnu.org/licenses/>.
"""

import bpy
import bge
from bge import logic
from bge import events
import random

bge.logic.globalDict['ElementDictonary1'] = {}

def loadupdox(textfile):
    dbase = bge.logic.globalDict['ElementDictonary1']
    entry_count = 0
    listvars = ["dry_hit_particle", "dry_hit_decal", "wet_hit_particle", "wet_hit_decal", "model", "animation"]
    ignore_vars = ["{", "}"]
    for line in textfile.as_string().split("\n"):
        if line not in ignore_vars:         
            if line.startswith("entry") == True:
                elem_var = (line.split("=")[0]).rstrip()
                elem_def = (line.split("=")[1]).lstrip()
                print("element name: " + elem_def)
                dbase[elem_def] = {}
                add_var = dbase[elem_def]
                entry_count += 1
                continue
            if line.startswith("entry") != True and line != "":
                element_def = line.lstrip()
                elem_var = (element_def.split("=")[0]).rstrip()
                elem_def = (element_def.split("=")[1]).lstrip()
                
                if elem_var in listvars:
                    if elem_var not in add_var:
                        add_var[elem_var] = []
                        add_var[elem_var].append(elem_def)
                        continue
                    if elem_var in add_var:
                        add_var[elem_var].append(elem_def)
                        continue
                    
                else:
                    print(line + " not in list.")
                    add_var[elem_var] = elem_def
                    continue
        
        if line == "":
            print("failing here!!")
            return
        else:
            print(line + " failed.")
            
loadupdox(bpy.data.texts['GameExport'])
#print(bge.logic.globalDict['ElementDictonary1'])