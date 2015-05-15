bl_info = {
    "name": "DTScripts Particle Database",
    "author": "Daniel Turton",
    "version": (0,0,2),
    "blender": (2, 6, 0),
    "api": "",
    "location": "On the Particles panel. Soon to be limited to showing only under Blender Game.",
    "description": "Creates a database and slots on objects to assign them to elements from the database. Draws a panel for database element changes.",
    "warning": "If this software borks your project or breaks into your neighbor's house, I'm not responsible. Back your stuff up.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Game Engine"} 

"""

DTScripts Particle Database
by Daniel Turton

Description:

(This will be fun. :) )

The DTScripts Particle Database is a framework that (hopefully) makes the process of creating particle effects a little easier.

Through the use of elements defined as materials, particles, projectiles and statics, the Particle Database will arrange data 
for access through the game engine within a dictionary, allowing for access to and randomization of particles generated from static / emitter objects.

Once the elements have been defined, they are "pushed" to the Blender Game Engine through a text block, accessed by a script run at the start
of the game engine. This script parses the text block and adds the elements to a dictionary accordingly.

Once done, game engine scripts can access the information tied to objects by checking their "Content" string game property and the name of the sensor tied to the property.

This file contains the logic for the creation and control of the database.

This is only the Alpha version. I hope that you enjoy what it can do now and what it will do in the future.

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
from bpy.props import *
import random
import time

ObjType = ''
DTdebug = 0
ElementDictionary = {}

def initSceneProperties(scene):
    
    #Script Management
    bpy.types.Scene.PhysPanelEdit = BoolProperty(
        name = "PanelEditMode",
        description = "Panel Edit Mode"
        )
    scene['PanelEditMode'] = 0
    
    bpy.types.Scene.element_string = StringProperty(
        name = "ElementString",
        )
    scene['ElementString'] = {}
    
    bpy.types.Scene.element_db_status = StringProperty(
        name = "element_db_status",
        )
    scene['element_db_status'] = ""
    
    bpy.types.Object.DTSContent = StringProperty(
        name = 'Content',
        )
        
    bpy.types.Scene.ElementName = StringProperty(
        name = "Element Name",
        )
    
    bpy.types.Scene.MaterialWD = StringProperty(
        )
    bpy.types.Scene.MaterialWP = StringProperty(
        )
    bpy.types.Scene.MaterialDD = StringProperty(
        )
    bpy.types.Scene.MaterialDP = StringProperty(
        )
    bpy.types.Scene.Importchoice = StringProperty(
        )
    bpy.types.Scene.Elementchoice = StringProperty(
        name = "Effect Script",
        )

    #Material stuff
    bpy.types.Scene.EditAreaUpper = FloatProperty(
        name = "Edit Area Upper",
        )
    scene['EditAreaUpper'] = 0.0

    bpy.types.Scene.EditAreaLower = FloatProperty(
        name = "Edit Area Lower",
        )
    scene['EditAreaLower'] = 0.0

    bpy.types.Scene.EditWetHitDecal = StringProperty(
        name = "Edit Wet Hit decal",
        )
    scene['EditWetHitDecal'] = ""

    bpy.types.Scene.EditWetHitParticle = StringProperty(
        name = "Edit Wet Hit particle",
        )
    scene['EditWetHitParticle'] = ""

    bpy.types.Scene.EditDryHitDecal = StringProperty(
        name = "Edit Dry Hit decal",
        )
    scene['EditDryHitDecal'] = ""
    
    bpy.types.Scene.EditDryHitParticle = StringProperty(
        name = "Edit Dry Hit particle",
        )
    scene['EditDryHitParticle'] = ""
    
    #stuff for particles
    
    bpy.types.Scene.EditModel = StringProperty(
        name = "EditTiedModel",
        description = "Edit Tied Model"
        )
    scene['EditModel'] = ""
    
    bpy.types.Scene.EditObjVelocity = StringProperty(
        name = "Edit Object Velocity",
        )
    scene['EditObjVelocity'] = ""
    
    bpy.types.Scene.EditObjAnimation = StringProperty(
        name = "Edit Object Animation",
        )
    scene['EditObjAnimation'] = ""
    
    bpy.types.Scene.EditObjMulti = IntProperty(
        name = "Edit Object Multiplier",
        )
    scene['EditObjMulti'] = ""
    
    bpy.types.Scene.EditObjFluidMulti = IntProperty(
        name = "Edit Object Fluid Multiplier",
        )
    scene['EditObjFluidMulti'] = ""
    
    bpy.types.Scene.EditEmitFreq = IntProperty(
        name = "Edit Emit Frequency",
        )
    scene['EditEmitFreq'] = ""
    
    bpy.types.Scene.EditFragCountMax = IntProperty(
        name = "Max",
        )
    scene['EditFragCountMax'] = 0
    
    bpy.types.Scene.EditFragCountMin = IntProperty(
        name = "Min",
        )
    scene['EditFragCountMin'] = 0
    
    #stuff for statics
    
    bpy.types.Scene.EditObjAnimStart = IntProperty(
        name = "Edit Object Animation Start",
        )
    scene['EditObjAnimStart'] = ""
    
    bpy.types.Scene.EditObjAnimEnd = IntProperty(
        name = "Edit Object Animation End",
        )
    scene['EditObjAnimEnd'] = ""
    return
    
#Party officially started here
initSceneProperties(bpy.context.scene)

#property groups go up here for priority registration
class ModelDB(bpy.types.PropertyGroup):
    type = StringProperty(name = "type", default="None")

bpy.utils.register_class(ModelDB)
    
class ElementDB(bpy.types.PropertyGroup):
    
    type = StringProperty(name = "type", default="None")
    mat_type = StringProperty(name = "mat_type", default="None")
    dry_hit_particle = CollectionProperty(type = ModelDB)
    dry_hit_decal = CollectionProperty(type = ModelDB)
    wet_hit_particle = CollectionProperty(type = ModelDB)
    wet_hit_decal = CollectionProperty(type = ModelDB)
    AreaLower = FloatProperty(name = "Lower Area")
    AreaUpper = FloatProperty(name = "Upper Area")
    model = CollectionProperty(type = ModelDB)
    animation = CollectionProperty(type = ModelDB)
    velocity = []
    multiplier = StringProperty(name = "Multiplier", default="None")
    fluid_multiplier = StringProperty(name = "Fluid Multiplier", default="None")
    emit_frequency = StringProperty(name = "Emit Frequency", default="None")
    frag_min = IntProperty(name = "Frag Min")
    frag_max = IntProperty(name = "Frag Max")
        
    
bpy.utils.register_class(ElementDB)
bpy.types.Scene.element_db = CollectionProperty(type = ElementDB)
bpy.types.Scene.edit_element = CollectionProperty(type = ElementDB)
bpy.types.Scene.ParticleList = CollectionProperty(type = ElementDB)  
bpy.types.Scene.MaterialList = CollectionProperty(type = ElementDB)  
bpy.types.Scene.StaticList = CollectionProperty(type = ElementDB)
bpy.types.Scene.ProjectileList = CollectionProperty(type = ElementDB)

def ElementListsReset():
    
    return
    
    
class ElementDB_Mods(bpy.types.Operator):
    bl_idname = "dtscripts.db_mods"
    bl_label = "Database Modifications"
    
    purge = bpy.props.IntProperty()
    dump = bpy.props.IntProperty()
    db_import = bpy.props.IntProperty()
    pushtobge = bpy.props.IntProperty()
    output = {}
    
    
    def listiterator(context, database1, list_entry, key):
        element_db = bpy.context.scene.element_db
        print("element_db" + "[" + list_entry + "]." + key)
        for key1 in eval("element_db" + "[\"" + list_entry + "\"]." + key).keys():
            if type(eval("element_db" + "[\"" + list_entry + "\"]." + key)[key1]) is list:
                print(eval("element_db" + "[\"" + list_entry + "\"]." + key + "." + key1).keys())
            if type(eval("element_db" + "[\"" + list_entry + "\"]." + key)[key1]) is not list:
                return str(("\t") + key1 + " = " + str(eval("element_db" + "[\"" + list_entry + "\"]." + key)[key1]) + "\n")
        
    def execute(self, context):
        scn = context.scene
        element_db = bpy.context.scene.element_db
        
        if self.db_import:
            dbase = bpy.context.scene.element_db
            entry_count = 0
            #set up script to evaluate strings!!!
            for entry in dbase.keys():
                dox.write("entry = " + dbase[entry]['name'] + "\n")
                for key in dbase[entry].keys():
                    dox.write("\t" + key + " = " + dbase[entry][key] + "\n")
                entry_count += 1
            scn["element_db_status"] = "Database imported. " + str(entry_count) + " entries processed."
            return{'FINISHED'}
            
        if self.dump:
            entry_count = 0
            dumplevel_count = 0
            dbase = bpy.context.scene.element_db
            dox = bpy.data.texts.new("DB_Dump " + time.ctime())
            dox.write("dts_info = {\"type\" : \"dump\", \"creation_time\" : \"" + time.ctime() + "\"}")
            for entry in dbase.keys():
                dox.write("{\n")
                dox.write("entry = " + dbase[entry]['name'] + "\n")
                for key in dbase[entry].keys():
                    print(entry,key)
                    
                    if type(dbase[entry][key]) is list:
                        #print(self.listiterator(dbase,entry,key))
                        for key1 in eval("element_db" + "[\"" + entry + "\"]." + key).keys():
                            #if type(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) is list:
                            if type(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) is list:
                                for item in eval("element_db" + "[\"" + entry + "\"]." + key + "." + key1).keys():
                                    print('List hit')
                                    dox.write(eval("element_db" + "[\"" + entry + "\"]." + key + "." + key1))
                            if type(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) is not list:
                                #dox.write(str(("\t") + key + " : " + key1 + " = " + str(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) + "\n"))
                                dox.write(str(("\t") + key + " = " + key1 + "\n"))
                        #for key2 in dbase[entry][key]:
                           #dox.write("\t\t" + key2 + " = " + str(eval(dbase + "[" + entry + "][" + key + "]." + key2)) + "\n")
                    if type(dbase[entry][key]) is not list:
                        dox.write("\t" + key + " = " + str(dbase[entry][key]) + "\n")
                dox.write("}\n")
                entry_count += 1
            scn["element_db_status"] = str(entry_count) + " database entries dumped to text block. Be sure to save the file externally."
            return{'FINISHED'}
        if self.purge:
            dbase = bpy.context.scene.element_db
            for item in dbase.keys():
                dbase.remove(0)
            scn["element_db_status"] = "Database purged. Please import a new database, or begin setting up elements to create a new one."
            return{'FINISHED'}
        
        if self.pushtobge:            
            entry_count = 0
            dumplevel_count = 0
            dbase = bpy.context.scene.element_db
            #run a test for the existence of the file to avoid duplicates
            try:
                bpy.data.texts["GameExport"].clear()
            except:
                bpy.data.texts.new("GameExport")
            dox = bpy.data.texts["GameExport"]
            for entry in dbase.keys():
                dox.write("{\n")
                dox.write("entry = " + dbase[entry]['name'] + "\n")
                for key in dbase[entry].keys():
                    if type(dbase[entry][key]) is list:
                        for key1 in eval("element_db" + "[\"" + entry + "\"]." + key).keys():
                            if type(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) is list:
                                for item in eval("element_db" + "[\"" + entry + "\"]." + key + "." + key1).keys():
                                    dox.write(eval("element_db" + "[\"" + entry + "\"]." + key + "." + key1))
                            if type(eval("element_db" + "[\"" + entry + "\"]." + key)[key1]) is not list:
                                dox.write(str(("\t") + key + " = " + key1 + "\n"))
                    if type(dbase[entry][key]) is not list:
                        dox.write("\t" + key + " = " + str(dbase[entry][key]) + "\n")
                dox.write("}\n")
                entry_count += 1
            scn["element_db_status"] = str(entry_count) + " database entries dumped to text block. Be sure to save the file externally."
            
            for obj in bpy.data.objects:
                if obj.DTSContent != "":
                    print(obj.name)
                    obj.game.properties['content'].value = obj.DTSContent
            
            return{'FINISHED'}
        if self.purge:
            dbase = bpy.context.scene.element_db
            for item in dbase.keys():
                dbase.remove(0)
            scn["element_db_status"] = "Database purged. Please import a new database, or begin setting up elements to create a new one."
            
            return{'FINISHED'}
            
        
        
class DB_Import_Choice(bpy.types.Operator):
    bl_idname = "dtscripts.db_import"
    bl_label = "Import Database"
    
    message = bpy.props.StringProperty()
    DoxList = []
    
    for item in bpy.data.texts.items():
        DoxList.append((item[0], item[0], item[0]))
    TextFileList = EnumProperty(
                items=DoxList,
                name="Text Documents: "
                )
    
    def execute(self, context):
        dbase = bpy.context.scene.element_db
        scn = context.scene
        if self.TextFileList:
            entry_count = 0
            listvars = ["dry_hit_particle", "dry_hit_decal", "wet_hit_particle", "wet_hit_decal", "model", "animation"]
            ignore_vars = ["{", "}"]
            for line in bpy.data.texts[scn.Importchoice].as_string().split("\n"):
                if line not in ignore_vars:         
                    if line.startswith("entry") == True:
                        new_entry = dbase.add()
                        elem_var = (line.split("=")[0]).rstrip()
                        elem_def = (line.split("=")[1]).lstrip()
                        print("element name: " + elem_def)
                        new_entry.name = elem_def
                        entry_count += 1
                    if line.startswith("entry") != True:
                        print(line)
                        element_def = line.lstrip()
                        elem_var = (element_def.split("=")[0]).rstrip()
                        elem_def = (element_def.split("=")[1]).lstrip()
                        
                        if elem_var in listvars:
                            collection_entry = eval("new_entry." + elem_var + ".add()")
                            collection_entry.name = elem_def          
                        else:
                            print(line + " not in list.")
                            new_entry[elem_var] = elem_def
                
                else:
                    print(line + " failed.")
                
            scn["element_db_status"] = "Database imported. " + str(entry_count) + " entries processed."
            return{'FINISHED'}
        return{'FINISHED'}
        

class OBJECT_OT_ErrorWindow(bpy.types.Operator):
    bl_idname = "dtscripts.errormessage"
    bl_label = "Error window"
    type = bpy.props.StringProperty()
    message = bpy.props.StringProperty()
    
    def execute(self, context):
        return{'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)
        
    def draw(self, context):
        self.layout.label("Message!")
        row = self.layout
        row.prop(self, "message")

class OBJECT_OT_EntryModifier(bpy.types.Operator):
    bl_idname = "dtscripts.entrymodifier"
    bl_label = "Entry Modifier"
    add = bpy.props.StringProperty()
    remove = bpy.props.StringProperty()
    
    def execute(self, context):
        obj = bpy.context.object
        obj_game = bpy.context.object.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.add:
            element_db[obj.DTSContent].model.append(self.add)
            return{'FINISHED'}
        if self.remove:
            element_db[obj.DTSContent].model.remove(self.remove)
            if obj.name == self.remove:
                obj.DTSContent = ""
            return{'FINISHED'}

class OBJECT_OT_WetDecal(bpy.types.Operator):
    bl_idname = "dtscripts.materialwd"
    bl_label = "Wet Decal Operations"
    
    remove = bpy.props.StringProperty()
    add = bpy.props.StringProperty()
    
    def execute(self, context):
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.remove:
            elem_count = 0
            for element in element_db[obj.DTSContent].wet_hit_decal.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].wet_hit_decal.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
            
        if self.add:
            new_model = element_db[obj.DTSContent].wet_hit_decal.add()
            new_model.name = scn.MaterialWD
            return{'FINISHED'}
    
class OBJECT_OT_WetParticle(bpy.types.Operator):
    bl_idname = "dtscripts.materialwp"
    bl_label = "Wet Particle Operations"
    
    remove = bpy.props.StringProperty()
    add = bpy.props.StringProperty()
    
    def execute(self, context):
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.remove:
            elem_count = 0
            for element in element_db[obj.DTSContent].wet_hit_particle.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].wet_hit_particle.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
        
        if self.add:
            new_model = element_db[obj.DTSContent].wet_hit_particle.add()
            new_model.name = scn.MaterialWP
            return{'FINISHED'}
            
class OBJECT_OT_DryDecal(bpy.types.Operator):
    bl_idname = "dtscripts.materialdd"
    bl_label = "Dry Decal Operations"
    
    remove = bpy.props.StringProperty()
    add = bpy.props.StringProperty()
    
    def execute(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.remove:
            elem_count = 0
            for element in element_db[obj.DTSContent].dry_hit_decal.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].dry_hit_decal.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
        
        if self.add:
            new_model = element_db[obj.DTSContent].dry_hit_decal.add()
            new_model.name = scn.MaterialDD
            return{'FINISHED'}
        

class OBJECT_OT_DryParticle(bpy.types.Operator):
    bl_idname = "dtscripts.materialdp"
    bl_label = "Dry Particle Operations"
    
    remove = bpy.props.StringProperty()
    add = bpy.props.StringProperty()
    
    def execute(self, context):
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.remove:
            elem_count = 0
            for element in element_db[obj.DTSContent].dry_hit_particle.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].dry_hit_particle.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
        
        if self.add:
            new_model = element_db[obj.DTSContent].dry_hit_particle.add()
            new_model.name = scn.MaterialDP
            return{'FINISHED'}
    
class OBJECT_OT_Particle(bpy.types.Operator):
    bl_idname = "dtscripts.particle"
    bl_label = "List Particles"
    
    remove = bpy.props.StringProperty()
    remove_anim = bpy.props.StringProperty()
    info = bpy.props.StringProperty()
    new = bpy.props.StringProperty()
    setup = bpy.props.StringProperty()
    proj_setup = bpy.props.StringProperty()
    proj_new = bpy.props.StringProperty()    
    
    def execute(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        def addProperties(object, name, type, value):
            #bpy.ops.object.select_name(name=object)
            bpy.ops.object.game_property_new()
            setting = bpy.context.object.game.properties[-1]
            setting.name = name
            setting.type = type
            setting.value = value
            return{'FINISHED'}
        
        def particle_setup(particle):
            #bpy.ops.object.select_name(name=particle)
            addProperties(particle, "content", "STRING", 0)
            bpy.ops.logic.sensor_add(type='ALWAYS', name="particle", object="")
            print("setup occured")
            
        def particle_create(particle):
            print("creation starting")
            #bpy.ops.object.select_name(name=obj.name)
            new_entry = element_db.add()
            new_entry.name = particle
            new_entry.type = "particle"
            new_model = new_entry.model.add()
            new_model.name = obj.name
            new_entry.velocity = []
            new_entry['multiplier'] = 0
            new_entry['fluid_multiplier'] = 0
            new_entry['emit_frequency'] = 0
            new_entry.frag_min = 0
            new_entry.frag_max = 0
            print("creation occured")
        
        def projectile_create(particle):
            print("creation starting")
            #bpy.ops.object.select_name(name=obj.name)
            new_entry = element_db.add()
            new_entry.name = particle
            new_entry.type = "projectile"
            new_model = new_entry.model.add()
            new_model.name = obj.name
            new_entry.velocity = []
            new_entry['multiplier'] = 0
            new_entry['fluid_multiplier'] = 0
            new_entry['emit_frequency'] = 0
            new_entry.frag_min = 0
            new_entry.frag_max = 0
            print("creation occured")
        
        def projectile_setup(projectile):
            print("running projectile setup")
            #bpy.ops.object.select_name(name=obj.name)
            obj_data = bpy.data.objects[obj.name].game
            bpy.ops.logic.sensor_add(type='COLLISION', name="bullet", object="")
            bpy.ops.logic.controller_add(type='PYTHON', name="EffectCombo", object="")
            bpy.context.object.game.controllers['EffectCombo'].text = bpy.data.texts[scn.Elementchoice]
            #bpy.ops.logic.controller_add(type='LOGIC_AND', name="And", object="")
            killobject = bpy.ops.logic.actuator_add(type='EDIT_OBJECT', name="KillBullet", object="")
            obj.game.actuators['KillBullet'].mode = "ENDOBJECT"
            addobject = bpy.ops.logic.actuator_add(type='EDIT_OBJECT', name="AddDecal", object="")
            obj.game.actuators['AddDecal'].mode = "ADDOBJECT"

            #obj_data.sensors["bullet"].link(obj_data.controllers["And"])
            obj_data.sensors["bullet"].link(obj_data.controllers["EffectCombo"])
            #obj_data.actuators["KillBullet"].link(obj_data.controllers["And"])
            obj_data.actuators["KillBullet"].link(obj_data.controllers["EffectCombo"])
            obj_data.actuators["AddDecal"].link(obj_data.controllers["EffectCombo"])
            addProperties(projectile, "content", "STRING", 0)
            addProperties(projectile, "bullet", "BOOL", 1)
        
        if self.remove:
            
            elem_count = 0
            for element in element_db[obj.DTSContent].model.keys():
                if element == self.remove:
                    if obj.name == self.remove:
                        element_db[obj.DTSContent].model.remove(elem_count)
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
        
        if self.remove_anim:
            
            elem_count = 0
            for element in element_db[obj.DTSContent].anim.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].anim.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
        
        if self.info:
            scn['EditObjAnimation'] = element_db[obj.DTSContent].animation
            scn['EditObjVelocity'] = element_db[obj.DTSContent].velocity
            scn['EditObjFluidMulti'] = element_db[obj.DTSContent]["fluid_multiplier"]
            scn['EditObjMulti'] = element_db[obj.DTSContent]['multiplier']
            scn['EditEmitFreq'] = element_db[obj.DTSContent]["emit_frequency"]
            scn['EditFragCountMax'] = element_db[obj.DTSContent].frag_max
            scn['EditFragCountMin'] = element_db[obj.DTSContent].frag_min
            return{'FINISHED'}
        
        
        if self.setup:
            print("woot" + self.setup)
            particle_setup(scn.ElementName)
            obj.DTSContent = scn.ElementName
            new_model = element_db[scn.ElementName].model.add()
            new_model.name = obj.name
            return{'FINISHED'}
        
        if self.new:
            if scn.ElementName in element_db.keys():
                print("This already exists.")
            if scn.ElementName not in element_db.keys():
                particle_create(scn.ElementName)
                particle_setup(scn.ElementName)
                obj.DTSContent = scn.ElementName
                
            return{'FINISHED'}
        
        if self.proj_new:
            if scn.ElementName in element_db.keys():
                print("This already exists.")
                return{'FINISHED'}
            if scn.ElementName not in element_db.keys():
                projectile_create(scn.ElementName)
                projectile_setup(scn.ElementName)
                obj.DTSContent = scn.ElementName
                return{'FINISHED'}
            
        if self.proj_setup:
            projectile_setup(scn.ElementName)
            new_model = element_db[scn.ElementName].model.add()
            new_model.name = obj.name
            obj.DTSContent = scn.ElementName
            return{'FINISHED'}
        
        return{'FINISHED'}
        
class OBJECT_OT_Material(bpy.types.Operator):
    bl_idname = "dtscripts.material"
    bl_label = "List Materials"
    
    remove = bpy.props.StringProperty()
    info = bpy.props.StringProperty()
    setup = bpy.props.StringProperty()
    new = bpy.props.StringProperty()
    wet_dry = bpy.props.StringProperty()
    
    def execute(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        def addProperties(object, name, prop_type, value):
            #bpy.ops.object.select_name(name=object)
            bpy.ops.object.game_property_new()
            setting = bpy.context.object.game.properties[-1]
            setting.name = name
            setting.type = prop_type
            setting.value = value
            return{'FINISHED'}
            
        def material_setup(material):
            #bpy.ops.object.select_name(name=obj.name)
            obj_data = bpy.data.objects[obj.name].game
            bpy.ops.logic.sensor_add(type='COLLISION', name="wall", object="")
            bpy.ops.logic.controller_add(type='PYTHON', name="EffectCombo", object="")
            bpy.context.object.game.controllers['EffectCombo'].text = bpy.data.texts[scn.Elementchoice]
            addProperties(material, "content", "STRING", 0)
            obj_data.sensors["wall"].link(obj_data.controllers["EffectCombo"])
            
            addProperties(material, "dmglevel", "INT", 0)
            addProperties(material, "wall", "STRING", 0)
            addProperties(material, "tank_level", "INT", 0)
            addProperties(material, "type", "STRING", 0)
            
        def material_create(material):
            #bpy.ops.object.select_name(name=material)
            new_entry = element_db.add()
            new_entry.name = material
            new_entry.type = "material"
            new_entry.mat_type = "fluid"
            new_entry.AreaLower = 0.0
            new_entry.AreaUpper = 0.0
        
        if self.remove:
            obj.DTSContent = ""
            return{'FINISHED'}
            
        if self.info:
            scn['EditAreaUpper'] = element_db[obj.DTSContent]['AreaUpper']
            scn['EditAreaLower'] = element_db[obj.DTSContent]['AreaLower']
            scn['EditWetHitDecal'] = element_db[obj.DTSContent].wet_hit_decal
            scn['EditWetHitParticle'] = element_db[obj.DTSContent].wet_hit_particle
            scn['EditDryHitDecal'] = element_db[obj.DTSContent].dry_hit_decal
            scn['EditDryHitParticle'] = element_db[obj.DTSContent].dry_hit_particle
            return{'FINISHED'}
        
        if self.setup:
            material_setup(scn.ElementName)
            return{'FINISHED'}
            
        if self.new:
            if scn.ElementName in element_db.keys():
                print("This already exists.")
                return{'FINISHED'}
            if scn.ElementName not in element_db.keys():
                material_create(scn.ElementName)
                material_setup(scn.ElementName)
                obj.DTSContent = scn.ElementName
                return{'FINISHED'}
        
        if self.wet_dry:
            element_db[obj.DTSContent]['mat_type'] = self.wet_dry
            return{'FINISHED'}
        
class OBJECT_OT_AddAnim(bpy.types.Operator):
    bl_idname = "dtscripts.addanim"
    bl_label = "List Particles"
    
    add_anim = bpy.props.StringProperty()
    info = bpy.props.StringProperty()
    AnimList = []
    
    for item in bpy.data.actions:
        AnimList.append((item.name, item.name, item.name))           
    AnimListProp = EnumProperty(
                items=AnimList,
                name="Animations: "
                )

    def execute(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.AnimListProp:
            element_db[obj.DTSContent].animation.append(self.AnimListProp, 0,0)
            return{'FINISHED'}
            
class OBJECT_OT_Static(bpy.types.Operator):
    bl_idname = "dtscripts.static"
    bl_label = "List Particles"
    
    remove = bpy.props.StringProperty()
    remove_anim = bpy.props.StringProperty()
    add_anim = bpy.props.StringProperty()
    info = bpy.props.StringProperty()
    setup = bpy.props.StringProperty()
    new = bpy.props.StringProperty()
    StaticList = []
    AnimList = []
    
                
    def execute(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        def addProperties(object, name, type, value):
            #bpy.ops.object.select_name(name=object)
            bpy.ops.object.game_property_new()
            setting = bpy.context.object.game.properties[-1]
            setting.name = name
            setting.type = type
            setting.value = value
            return{'FINISHED'}
            
        def static_setup(static):
            #bpy.ops.object.select_name(name=static)
            obj_data = bpy.data.objects[obj.name].game
            bpy.ops.logic.sensor_add(type='ALWAYS', name="decal", object="")
            obj.game.sensors['decal'].use_pulse_true_level = True
            bpy.ops.logic.controller_add(type='PYTHON', name="EffectCombo", object="")
            bpy.context.object.game.controllers['EffectCombo'].text = bpy.data.texts[scn.Elementchoice]
            killeffect = bpy.ops.logic.actuator_add(type='EDIT_OBJECT', name="KillEffect", object="")
            obj.game.actuators['KillEffect'].mode = "ENDOBJECT"
            addeffect = bpy.ops.logic.actuator_add(type='EDIT_OBJECT', name="Emitter", object="")
            obj.game.actuators['Emitter'].mode = "ADDOBJECT"
            obj.game.actuators['Emitter'].use_local_linear_velocity = True
            
            obj_data.sensors["decal"].link(obj_data.controllers["EffectCombo"])    
            obj_data.actuators["KillEffect"].link(obj_data.controllers["EffectCombo"])
            obj_data.actuators["Emitter"].link(obj_data.controllers["EffectCombo"])
            addProperties(static, "content", "STRING", 0)
            addProperties(static, "decal_timer", "TIMER", 0.000)
            addProperties(static, "data_frame", "STRING", 0)
            
        def static_create(static):
            #bpy.ops.object.select_name(name=static)
            new_entry = element_db.add()
            new_entry.name = static
            new_entry.type = "static"
            new_model = new_entry.model.add()
            new_model.name = str(obj.name)
        
        if self.remove:
            
            elem_count = 0
            for element in element_db[obj.DTSContent].area.keys():
                if element == self.remove:
                    element_db[obj.DTSContent].area.remove(elem_count)
                    if obj.name == self.remove:
                        obj.DTSContent = ""
                    return{'FINISHED'}
                elem_count += 1
            return{'FINISHED'}
            
        if self.remove_anim:
            element_db[obj.DTSContent].animation.remove(self.remove_anim)
            return{'FINISHED'}
            
        if self.info:
            anim_data = element_db[obj.DTSContent].animation
            scn['EditObjAnimation'] = element_db[obj.DTSContent].animation
            return{'FINISHED'}
        
        if self.new:
            if scn.ElementName in element_db.keys():
                print("This already exists.")
                return{'FINISHED'}
            if scn.ElementName not in element_db.keys():
                static_create(scn.ElementName)
                static_setup(scn.ElementName)
                obj.DTSContent = scn.ElementName
                return{'FINISHED'}
            
        if self.setup:
            static_setup(scn.ElementName)
            obj.DTSContent = scn.ElementName
            new_model = element_db[scn.ElementName].model.add()
            new_model.name = obj.name
            return{'FINISHED'}
    
    def invoke(self, context, event):
        scn = context.scene
        for elem in bpy.context.scene.element_db.keys():
            if elem not in scn.StaticList.keys():
                if bpy.context.scene.element_db[elem].type == "static":
                    new_elem = scn.StaticList.add()
                    new_elem['name'] = bpy.context.scene.element_db[elem].name
                    for key in bpy.context.scene.element_db[elem].keys():
                        new_elem[key] = bpy.context.scene.element_db[elem][key]
        return self.execute( context )
    
class OBJECT_OT_EditModebutton(bpy.types.Operator):
    bl_idname = "dtscripts.edittoggle"
    bl_label = "Panel Edit Mode toggle"
    
    
    
    def execute(self, context):
        print("Edit Mode Toggled!")
        scene = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        element_count = 0
        
        if obj.DTSContent != '' and obj.DTSContent not in element_db.keys():
            scene['PanelEditMode'] = False
            return{'FINISHED'}
        if scene['PanelEditMode'] == False:
            if obj.DTSContent == "":
                scene['PanelEditMode'] = False
                return{'FINISHED'}
            
            if element_db[obj.DTSContent]['type']== "fluid" or element_db[obj.DTSContent]['type'] == "dry" or element_db[obj.DTSContent]['type'] == "material":
                scene['PanelEditMode'] = True
                for entry in scene.edit_element.keys():
                    if entry == obj.DTSContent:
                        scene.edit_element.remove(element_count)
                    element_count += 1
                key = obj.DTSContent
                backup_entry = scene.edit_element.add()
                backup_entry['name'] = obj.DTSContent
                values = scene.element_db[obj.DTSContent].keys()
                for value in values:
                    backup_entry[value]  = element_db[obj.DTSContent][value]
                bpy.ops.dtscripts.material(info=obj.DTSContent)
                return{'FINISHED'}
            if element_db[obj.DTSContent]['type'] == "particle" or element_db[obj.DTSContent]['type'] == "projectile":
                scene['PanelEditMode'] = True
                for entry in scene.edit_element.keys():
                    if entry == obj.DTSContent:
                        scene.edit_element.remove(element_count)
                    element_count += 1
                key = obj.DTSContent
                backup_entry = scene.edit_element.add()
                backup_entry['name'] = obj.DTSContent
                values = scene.element_db[obj.DTSContent].keys()
                for value in values:
                    backup_entry[value]  = element_db[obj.DTSContent][value]
                bpy.ops.dtscripts.particle(info=obj.DTSContent)
                return{'FINISHED'}
            if element_db[obj.DTSContent]['type'] == "static":
                scene['PanelEditMode'] = True
                for entry in scene.edit_element.keys():
                    if entry == obj.DTSContent:
                        scene.edit_element.remove(element_count)
                    element_count += 1
                key = obj.DTSContent
                backup_entry = scene.edit_element.add()
                backup_entry['name'] = obj.DTSContent
                values = scene.element_db[obj.DTSContent].keys()
                for value in values:
                    backup_entry[value]  = element_db[obj.DTSContent][value]
                bpy.ops.dtscripts.static(info=obj.DTSContent)
                return{'FINISHED'}
        elif scene['PanelEditMode'] == True:
            scene['PanelEditMode'] = False
            return{'FINISHED'}
        
class OBJECT_OT_SaveEditbutton(bpy.types.Operator):
    bl_idname = "dtscripts.saveedit"
    bl_label = "Panel Save Edit toggle"
    
    revert = bpy.props.IntProperty()
    commit = bpy.props.IntProperty()
    deselected_revert = bpy.props.StringProperty()
    deselected_commit = bpy.props.StringProperty()
    
    def execute(self, context):
        scn = context.scene
        scene = context.scene
        obj = context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        element_count = 0
        
        if self.revert:
            key = obj.DTSContent
            values = scene.edit_element[obj.DTSContent].keys()
            for value in values:
                element_db[obj.DTSContent][value] = scene.edit_element[obj.DTSContent][value]
                #print(str(element_db[obj.DTSContent][value]) + " = " + str(scene.edit_element[obj.DTSContent][value]))
            for entry in scene.edit_element.keys():
                    if entry == obj.DTSContent:
                        scene.edit_element.remove(element_count)
                    element_count += 1
            scene['PanelEditMode'] = False
            return{'FINISHED'}
            
        if self.deselected_revert:
            key = self.deselected_revert
            values = scene.edit_element[key].keys()
            for value in values:
                element_db[key][value] = scene.edit_element[key][value]
                #print(str(element_db[key][value]) + " = " + str(scene.edit_element[key][value]))
            for entry in scene.edit_element.keys():
                    if entry == key:
                        scene.edit_element.remove(element_count)
                    element_count += 1
            scene['PanelEditMode'] = False
            return{'FINISHED'}
            
        if self.commit:
                    
            if element_db[obj.DTSContent]['type'] == "fluid" or element_db[obj.DTSContent]['type'] == "dry" or element_db[obj.DTSContent]['type'] == "material":
                update_entry = element_db[obj.DTSContent]
                update_entry.AreaLower = scn['EditAreaLower']
                update_entry.AreaUpper = scn['EditAreaUpper']
                scene['PanelEditMode'] = False
                return{'FINISHED'}
            if element_db[obj.DTSContent]['type'] == "particle" or element_db[obj.DTSContent]['type'] == "projectile":
                update_entry = element_db[obj.DTSContent]                
                update_entry['multiplier'] = scn['EditObjMulti']
                update_entry['fluid_multiplier'] = scn['EditObjFluidMulti']
                update_entry['emit_frequency'] = scn['EditEmitFreq']
                update_entry['frag_max'] = scn['EditFragCountMax']
                update_entry['frag_min'] = scn['EditFragCountMin']                
                scene['PanelEditMode'] = False
                return{'FINISHED'}
            if element_db[obj.DTSContent]['type'] == "static":
                update_entry = element_db[obj.DTSContent]
                update_entry['animation'] = (scn, 'EditObjAnimation'),(scn, 'EditObjAnimStart'),(scn, 'EditObjAnimEnd')
                scene['PanelEditMode'] = False
                return{'FINISHED'}
                
        if self.deselected_commit:
            key = self.deselected_commit        
            if element_db[key]['type'] == "fluid" or element_db[key]['type'] == "dry" or element_db[key]['type'] == "material":
                update_entry = element_db[key]
                update_entry.AreaLower = scn['EditAreaLower']
                update_entry.AreaUpper = scn['EditAreaUpper']
                scene['PanelEditMode'] = False
                return{'FINISHED'}
            if element_db[key]['type'] == "particle":
                update_entry = element_db[key]                
                update_entry['multiplier'] = scn['EditObjMulti']
                update_entry['fluid_multiplier'] = scn['EditObjFluidMulti']
                update_entry['emit_frequency'] = scn['EditEmitFreq']
                update_entry['frag_max'] = scn['EditFragCountMax']
                update_entry['frag_min'] = scn['EditFragCountMin']                
                scene['PanelEditMode'] = False
                return{'FINISHED'}
            if element_db[key]['type'] == "static":
                update_entry = element_db[key]
                update_entry['animation'] = (scn, 'EditObjAnimation'),(scn, 'EditObjAnimStart'),(scn, 'EditObjAnimEnd')
                scene['PanelEditMode'] = False
                return{'FINISHED'}

class DTS_DB_Control(bpy.types.Panel):
    bl_label = "dtscripts.db_ctl"
    bl_idname = "OBJECT_DTS_DB_CTL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle"    
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object
        obj_game = obj.game.properties
        
        row = layout.row().split(percentage=.75)
        row.prop_search(scn, "Importchoice", bpy.data, "texts")
        row.operator("dtscripts.db_import", text="Import").TextFileList
        row = layout.row()
        row.operator("dtscripts.db_mods", text="Push to BGE").pushtobge = 1
        row = layout.row()
        row.operator("dtscripts.dbrefresh", text="Refresh")
        row.operator("dtscripts.db_mods", text="Dump").dump = 1
        row = layout.row()
        row.operator("dtscripts.db_mods", text="Purge Database").purge = 1
        box = layout.box()
        box.label(text="Database Messages")
        box.label(text=scn["element_db_status"])

class refreshElements(bpy.types.Operator):
    bl_idname = "dtscripts.dbrefresh"
    bl_label = "OBJECT_DTS_DB_REFRESH"
    
    def execute(self, context):
        print("updating lists!")
        scn = context.scene
        for elem in bpy.context.scene.element_db.keys():
            if bpy.context.scene.element_db[elem].type == "particle":
                if bpy.context.scene.element_db[elem] not in scn.ParticleList.keys():
                    new_elem = scn.ParticleList.add()
                    new_elem['name'] = bpy.context.scene.element_db[elem].name
                    for key in bpy.context.scene.element_db[elem].keys():
                        new_elem[key] = bpy.context.scene.element_db[elem][key]
        
        for elem in bpy.context.scene.element_db.keys():
            if bpy.context.scene.element_db[elem].type == "static":
                if bpy.context.scene.element_db[elem] not in scn.StaticList.keys():
                    new_elem = scn.StaticList.add()
                    new_elem['name'] = bpy.context.scene.element_db[elem].name
                    for key in bpy.context.scene.element_db[elem].keys():
                        new_elem[key] = bpy.context.scene.element_db[elem][key]
        
        for elem in bpy.context.scene.element_db.keys():
            if bpy.context.scene.element_db[elem].type == "projectile":
                if bpy.context.scene.element_db[elem] not in scn.ProjectileList.keys():
                    new_elem = scn.ProjectileList.add()
                    new_elem['name'] = bpy.context.scene.element_db[elem].name
                    for key in bpy.context.scene.element_db[elem].keys():
                        new_elem[key] = bpy.context.scene.element_db[elem][key]
        
        for elem in bpy.context.scene.element_db.keys():
            if bpy.context.scene.element_db[elem].type == "material":
                if bpy.context.scene.element_db[elem] not in scn.MaterialList.keys():
                    new_elem = scn.MaterialList.add()
                    new_elem['name'] = bpy.context.scene.element_db[elem].name
                    for key in bpy.context.scene.element_db[elem].keys():
                        new_elem[key] = bpy.context.scene.element_db[elem][key]
        
        return {'FINISHED'}
        
class DTS_Element_Control(bpy.types.Operator):
    bl_label = "Element Control"
    bl_idname = "dtscripts.element_ctl" 
    
    part_new = bpy.props.StringProperty()
    part_setup = bpy.props.StringProperty()
    proj_new = bpy.props.StringProperty()
    proj_setup = bpy.props.StringProperty()
    mat_new = bpy.props.StringProperty()
    mat_setup = bpy.props.StringProperty()
    stat_new = bpy.props.StringProperty()
    stat_setup = bpy.props.StringProperty()
    
    part_choice = bpy.props.StringProperty()

    element_db = bpy.context.scene.element_db
    
    def execute(self, context):
        bpy.ops.dtscripts.dbrefresh()
        return{'FINISHED'}
        
    def invoke(self, context, event):
        bpy.ops.dtscripts.dbrefresh()
        
        bpy.context.scene.ElementName = ""
        
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)
        
        self.execute( context )
    
    def draw(self, context):
        global ObjType
        scn = context.scene
        obj = bpy.context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        if self.part_setup:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Choose the particle you would like to use.")
            #add links to effect script choice here. Don't forget to add variable to elements chunks
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop_search(scn, "ElementName", scn, "ParticleList")
            row.operator("dtscripts.particle", text="Setup").setup = self.part_setup
            
        if self.part_new:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Name the particle you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop(scn, "ElementName")
            row.operator("dtscripts.particle", text="Create").new = self.part_new
        
        if self.mat_setup:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Choose the material you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop_search(scn, "ElementName", scn, "MaterialList")
            print(obj.DTSContent)
            row.operator("dtscripts.material", text="Setup").setup = self.mat_setup
            
        if self.mat_new:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Name the material you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop(scn, "ElementName")
            row.operator("dtscripts.material", text="Create").new = self.mat_new
            
        if self.proj_setup:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Choose the projectile you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop_search(scn, "ElementName", scn, "ParticleList")
            row.operator("dtscripts.particle", text="Setup").proj_setup = self.proj_setup
            
        if self.proj_new:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Name the projectile you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop(scn, "ElementName")
            row.operator("dtscripts.particle", text="Create").proj_new = self.proj_new
            
        if self.stat_setup:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Choose the projectile you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop_search(scn, "ElementName", scn, "StaticList")
            row.operator("dtscripts.static", text="Setup").setup = self.stat_setup
            
        if self.stat_new:
            self.layout.label("Message!")
            row = self.layout.row()
            row.label(text="Name the projectile you would like to use.")
            row = self.layout.row()
            row.prop_search(scn, "Elementchoice", bpy.data, "texts")
            row = self.layout.row(align=True).split(percentage=.75)
            row.prop(scn, "ElementName")
            row.operator("dtscripts.static", text="Create").new = self.stat_new        

bpy.types.Scene.woot = bpy.props.StringProperty()
       
class DTS_PS_UserInterface(bpy.types.Panel):
    bl_label = "DTScripts.PS_UI"
    bl_idname = "OBJECT_DTS_PS_UI"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "particle" 
    

    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object
        obj_game = obj.game.properties
        element_db = bpy.context.scene.element_db
        
        row = layout.row()
        if obj.DTSContent == '':
            row = layout.row()
            row.label(text="No game properties detected. Would you like to set this object up?")
            row = layout.row()
            col = row.column()
            subrow = col.row(align=True).split(percentage=.75)
            subrow.operator("dtscripts.element_ctl", text="Projectile").proj_setup = obj.name
            subrow.operator("dtscripts.element_ctl", text="New").proj_new = obj.name
            col = row.column()
            subrow = col.row(align=True).split(percentage=.75)
            subrow.operator("dtscripts.element_ctl", text="Particle").part_setup = obj.name
            subrow.operator("dtscripts.element_ctl", text="New").part_new = obj.name
            
            row = layout.row()
            col = row.column()
            subrow = col.row(align=True).split(percentage=.75)
            subrow.operator("dtscripts.element_ctl", text="Static").stat_setup = obj.name
            subrow.operator("dtscripts.element_ctl", text="New").stat_new = obj.name
            col = row.column()
            subrow = col.row(align=True).split(percentage=.75)
            subrow.operator("dtscripts.element_ctl", text="Material").mat_setup = obj.name
            subrow.operator("dtscripts.element_ctl", text="New").mat_new = obj.name
            
                
        if obj.DTSContent != '' and obj.DTSContent in element_db.keys():
            if scn['PanelEditMode'] == 0:
                row = layout.row()
                self.layout.operator("dtscripts.edittoggle", text="Edit mode")
                
            if scn['PanelEditMode'] == 1:
                if obj.DTSContent not in scn.edit_element.keys():
                    #row.label(text="Nothing to edit here.")
                    box = layout.box()
                    boxrow = box.row()
                    boxrow.label(text="It appears you were making changes to " + scn.edit_element[0].name + ".")
                    boxrow = box.row()
                    boxrow.label(text="Would you like to save your changes?")
                    boxrow_button = box.row().split()
                    boxrow_button.operator("dtscripts.saveedit", text="Revert").deselected_revert = scn.edit_element[0].name
                    boxrow_button.operator("dtscripts.saveedit", text="Commit").deselected_commit = scn.edit_element[0].name
                    #if obj.DTSContent != '':
                        #print("update me for new DB format @ line 1052!")
                if obj.DTSContent in scn.edit_element.keys():
                    row = layout.row()
                    row.operator("dtscripts.saveedit", text="Revert").revert = 1
                    row.operator("dtscripts.saveedit", text="Commit").commit = 1
                
        
        if obj.DTSContent not in element_db.keys():
            row = layout.row()            
            for sens in bpy.context.object.game.sensors:
                global ObjType
                if sens.name == "decal":
                    row = layout.row()
                    ObjType = 'static'
                    row.label(text="Choose the " + ObjType + " you would like to use.")
                    row = layout.row()
                    row.prop_search(obj, "DTSContent", scn, "element_db")
                    
                elif sens.name == "bullet" or sens.name == "particle":
                    row = layout.row()
                    ObjType = 'particle'
                    row.label(text="Choose the " + ObjType + " you would like to use.")
                    row = layout.row()
                    row.prop_search(obj, "DTSContent", scn, "element_db")
                    
                elif sens.name == "wall":
                    row = layout.row()
                    ObjType = 'material'
                    row.label(text="Choose the " + ObjType + " you would like to use.")
                    row = layout.row()
                    row.prop_search(obj, "DTSContent", scn, "element_db")
            
            return
        if element_db[obj.DTSContent]['type'] == "fluid" or element_db[obj.DTSContent]['type'] == "dry" or element_db[obj.DTSContent]['type'] == "material":
            WDmodel_num = 0
            WPmodel_num = 0
            DDmodel_num = 0
            DPmodel_num = 0
            
            if scn['PanelEditMode'] == 0:
                
                for model in element_db[obj.DTSContent].wet_hit_decal.keys():
                    row = layout.row()
                    row.label(text="Wet Hit Decal: " + str(WDmodel_num) + ": " + model)
                    WDmodel_num += 1
                    
                for model in element_db[obj.DTSContent].wet_hit_particle.keys():
                    row = layout.row()
                    row.label(text="Wet Hit Particle: " + str(WPmodel_num) + ": " + model)
                    WPmodel_num += 1
                    
                for model in element_db[obj.DTSContent].dry_hit_decal.keys():
                    row = layout.row()
                    row.label(text="Dry Hit Decal: " + str(DDmodel_num) + ": " + model)
                    DDmodel_num += 1
                    
                for model in element_db[obj.DTSContent].dry_hit_particle.keys():
                    row = layout.row()
                    row.label(text="Dry Hit Particle: " + str(DPmodel_num) + ": " + model)
                    DPmodel_num += 1
                    
                    
                row = layout.row()
                row.label(text="Area Upper: " + str(element_db[obj.DTSContent]['AreaUpper']))
                row = layout.row()
                row.label(text="Area Lower: " + str(element_db[obj.DTSContent]['AreaLower']))
                row = layout.row()
                row.label(text=str(scn['PanelEditMode']))
            elif scn['PanelEditMode'] == 1:
                row = layout.row()
                row.prop(obj, "name")
                
                row = layout.row()
                print(element_db[obj.DTSContent]['mat_type'])
                if element_db[obj.DTSContent]['mat_type'] == "dry":
                    row.operator("dtscripts.material", text="Dry Material").wet_dry = "fluid"
                
                if element_db[obj.DTSContent]['mat_type'] == "fluid":
                    row.operator("dtscripts.material", text="Wet Material").wet_dry = "dry"
                    
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Wet Statics") 
                for model in element_db[obj.DTSContent].wet_hit_decal.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.materialwd", text="Remove " + model).remove = model
                    WDmodel_num += 1
                
                boxrow = box.row(align = True).split(percentage=.85)
                boxrow.prop_search(scn, "MaterialWD", scn, "StaticList")
                boxrow.operator("dtscripts.materialwd", text="Add").add = scn.MaterialWD
                
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Wet Particles") 
                for model in element_db[obj.DTSContent].wet_hit_particle.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.materialwp", text="Remove " + model).remove = model
                    WPmodel_num += 1
                    
                boxrow = box.row(align = True).split(percentage=.85)
                boxrow.prop_search(scn, "MaterialWP", scn, "ParticleList")
                boxrow.operator("dtscripts.materialwp", text="Add").add = scn.MaterialWP
                
                boxrow = box.row()
                
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Dry Statics") 
                for model in element_db[obj.DTSContent].dry_hit_decal.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.materialdd", text="Remove " + model).remove = model
                    DDmodel_num += 1
                
                boxrow = box.row(align = True).split(percentage=.85)
                boxrow.prop_search(scn, "MaterialDD", scn, "StaticList")
                boxrow.operator("dtscripts.materialdd", text="Add").add = scn.MaterialDD
                
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Dry Particles") 
                for model in element_db[obj.DTSContent].dry_hit_particle.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.materialdp", text="Remove " + model).remove = model
                    DPmodel_num += 1
                    
                boxrow = box.row(align = True).split(percentage=.85)
                boxrow.prop_search(scn, "MaterialDP", scn, "ParticleList")
                boxrow.operator("dtscripts.materialdp", text="Add").add = scn.MaterialDP
                
                row = layout.row()
                layout.prop(scn, 'EditAreaUpper')
                row = layout.row()
                layout.prop(scn, 'EditAreaLower')

                row = layout.row()
                row.label(text=str(scn['PanelEditMode']))
            
        elif element_db[obj.DTSContent]['type'] == "particle" or element_db[obj.DTSContent]['type'] == "projectile":
            obj = context.object
            obj_game = obj.game.properties
            model_num = 0
            anim_num = 0
            
            if scn['PanelEditMode'] == 0:
                row = layout.row()
                row.label(text="Particle name is: " + obj.DTSContent)
                
                for model in element_db[obj.DTSContent].model.keys():
                    row = layout.row()
                    row.label(text="Mesh " + str(model_num) + ": " + model)
                    model_num += 1
                                
                row = layout.row()
                if element_db[obj.DTSContent].animation != []:
                    for anim in element_db[obj.DTSContent].animation:
                        row = layout.row()
                        row.label(text="Animation " + str(anim_num) + ": " + anim[0])
                        anim_num += 1
                row = layout.row()
                row.label(text="Velocity: " + str(element_db[obj.DTSContent].velocity))
                row = layout.row()
                row.label(text="Multi: " + str(element_db[obj.DTSContent]['multiplier']))
                row = layout.row()
                row.label(text="Fluid Multi: " + str(element_db[obj.DTSContent]['fluid_multiplier']))
                row = layout.row()
                row.label(text="Emit Frequency: " + str(element_db[obj.DTSContent]['emit_frequency']))
                row = layout.row()
                row.label(text="Fragment Count")
                row.label(text="Min: " + str(element_db[obj.DTSContent]['frag_min']))
                row.label(text="Max: " + str(element_db[obj.DTSContent]['frag_max']))
            elif scn['PanelEditMode'] == 1:
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Models") 
                for model in element_db[obj.DTSContent].model.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.particle", text="Remove " + model).remove = model
                    model_num += 1
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Animations")
                if element_db[obj.DTSContent].animation != []:
                    for anim in element_db[obj.DTSContent].animation:
                        boxrow = box.row()
                        boxrow.label(text=anim[0])
                        boxrow.operator("dtscripts.particle", text="Remove " + anim[0]).remove_anim = anim[0]
                        anim_num += 1
                boxrow = box.row()
                boxrow.operator_menu_enum("dtscripts.addanim", "AnimListProp", "Add Action")
                row = layout.row()
                layout.prop(scn, 'EditObjVelocity')
                row = layout.row()
                layout.prop(scn, 'EditObjMulti')
                row = layout.row()
                layout.prop(scn, 'EditObjFluidMulti')
                row = layout.row()
                layout.prop(scn, 'EditEmitFreq')
                row = layout.row()
                row.label(text="Fragment Count")
                row.prop(scn, 'EditFragCountMin')
                row.prop(scn, 'EditFragCountMax')
        elif element_db[obj.DTSContent]['type'] == "static":
            model_num = 0
            if scn['PanelEditMode'] == 0:
                row = layout.row()
                row.label(text="Static name is: " + obj.DTSContent)
                for model in element_db[obj.DTSContent].model.keys():
                    row = layout.row()
                    row.label(text="Mesh " + str(model_num) + ": " + model)
                    model_num += 1
                row = layout.row()
                row.label(text="Animation: " + str(element_db[obj.DTSContent].animation))
                row = layout.row()
                anim_num = 0
                if element_db[obj.DTSContent].animation != []:
                    for anim in element_db[obj.DTSContent].animation:
                        boxrow = box.row()
                        boxrow.label(text="Anim Start: " + str(element_db[obj.DTSContent].animation, anim))
                        anim_num += 1
                
                row = layout.row()
                if element_db[obj.DTSContent].animation != []:
                    for anim in element_db[obj.DTSContent].animation:
                        boxrow = box.row()
                        boxrow.label(text="Anim End: " + str(element_db[obj.DTSContent].animation, anim))
                        anim_num += 1

            if scn['PanelEditMode'] == 1:
                box = layout.box()
                boxrow = box.row()
                boxrow.label(text="Models") 
                for model in element_db[obj.DTSContent].model.keys():
                    boxrow = box.row()
                    boxrow.label(text=model)
                    boxrow.operator("dtscripts.particle", text="Remove " + model).remove = model
                    model_num += 1
                row = layout.row()
                layout.prop(scn, 'EditObjAnimation')
                row = layout.row()
                layout.prop(scn, 'EditObjAnimStart')
                row = layout.row()
                layout.prop(scn, 'EditObjAnimEnd')
        
            
        else:
            row = layout.row()
            row.label(text="Is there data for this object?")


def register():
    bpy.utils.register_class(DTS_PS_UserInterface)
    bpy.utils.register_class(OBJECT_OT_EditModebutton)
    bpy.utils.register_class(OBJECT_OT_SaveEditbutton)
    bpy.utils.register_class(OBJECT_OT_WetDecal)
    bpy.utils.register_class(OBJECT_OT_WetParticle)
    bpy.utils.register_class(OBJECT_OT_DryDecal)
    bpy.utils.register_class(OBJECT_OT_DryParticle)
    bpy.utils.register_class(OBJECT_OT_ErrorWindow)
    bpy.utils.register_class(OBJECT_OT_Particle)
    bpy.utils.register_class(OBJECT_OT_Material)
    bpy.utils.register_class(OBJECT_OT_Static)
    bpy.utils.register_class(OBJECT_OT_AddAnim)
    bpy.utils.register_class(ElementDB_Mods)
    bpy.utils.register_class(DTS_DB_Control)
    bpy.utils.register_class(DTS_Element_Control)
    bpy.utils.register_class(DB_Import_Choice)
    bpy.utils.register_class(refreshElements)

def unregister():
    bpy.utils.unregister_class(DTS_PS_UserInterface)
    bpy.utils.unregister_class(OBJECT_OT_EditModebutton)
    bpy.utils.unregister_class(OBJECT_OT_SaveEditbutton)
    bpy.utils.unregister_class(OBJECT_OT_WetDecal)
    bpy.utils.unregister_class(OBJECT_OT_WetParticle)
    bpy.utils.unregister_class(OBJECT_OT_DryDecal)
    bpy.utils.unregister_class(OBJECT_OT_DryParticle)
    bpy.utils.unregister_class(OBJECT_OT_ErrorWindow)
    bpy.utils.unregister_class(OBJECT_OT_Particle)
    bpy.utils.unregister_class(OBJECT_OT_Material)
    bpy.utils.unregister_class(OBJECT_OT_Static)
    bpy.utils.unregister_class(OBJECT_OT_AddAnim)
    bpy.utils.unregister_class(ElementDB)
    bpy.utils.unregister_class(ElementDB_Mods)
    bpy.utils.unregister_class(DTS_DB_Control)
    bpy.utils.unregister_class(DTS_Element_Control)
    bpy.utils.unregister_class(DB_Import_Choice)
    bpy.utils.unregister_class(refreshElements)

if __name__ == "__main__":
    register()
