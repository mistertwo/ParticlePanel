"""
DTScripts Particle Database
bullet reaction library

by Daniel Turton

version 0.01 uber alpha

This file is where the magic in the game engine occurs. Details available at www.danielturton.net.

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

cont = logic.getCurrentController()
obj = cont.owner
sens = cont.sensors
sens_name = (str(sens))[1:-1] 
scene = logic.getCurrentScene()
bpy_scene = bpy.context.scene
objList = scene.objects
prop1 = bpy.context.scene.objects[obj.name].game.properties
element_db = bge.logic.globalDict['ElementDictonary1']

#Generators(?) up here


def DrawDecal(loc,react_type):
    AddDecal = cont.actuators["AddDecal"]
    collision_mat = random.choice(element_db[react_type]['dry_hit_decal'])
    AddDecal.object = random.choice(element_db[collision_mat]['model'])
    AddDecal.instantAddObject()
    AimDecal = AddDecal.objectLastCreated
    AimDecal.alignAxisToVect(loc[2],0,1)
    return

def DrawEmitter(loc,run_time,frag_count,fluid,wall_type):
    AddDecal = cont.actuators["AddDecal"]
    MatElementChoice = random.choice(element_db[wall_type]['wet_hit_decal'])
    AddDecal.object = random.choice(element_db[MatElementChoice]['model'])
    AddDecal.instantAddObject()
    AimDecal = AddDecal.objectLastCreated
    AimDecal.alignAxisToVect(loc[2],0,1)
    AimDecal['data_frame'] = [int(run_time),fluid,frag_count,5,0,wall_type]
    return

def smokeParticle():
    
    moveit = cont.actuators["Action"]
    moveit.action = random.choice(element_db[prop1['content']]['animation'])
    moveit.frameStart = throttle_control()
    moveit.frameEnd = 30
    cont.activate(moveit)
    
    smokejitter = cont.actuators["Motion"]
    smokejitter.dLoc = element_db[prop1['content']]['velocity']
    cont.activate(smokejitter)
    return

#Logic for imported stuff goes here

def bulletHit():
    HitObj = sens['bullet'].hitObject
    print("collision object: " + str(HitObj) + " , " + str(HitObj.name))
    #print("hitobj = " + str(HitObj['content']))
    #BulletProp = bpy.context.scene.objects[obj.name].game.properties
    #TargetProp = bpy.context.scene.objects[HitObj.name].game.properties
    wall_type = element_db[HitObj['content']]['mat_type']
    #print(wall_type)
    tank_dims = (float(element_db[HitObj['content']]['AreaLower']), float(element_db[HitObj['content']]['AreaUpper']))
    #print(tank_dims)
    tank_level = HitObj['tank_level']

    if sens['bullet'].positive and element_db[HitObj['content']]['type'] != 'particle':
        print(wall_type)
        if wall_type == 'dry':
            LocVec = obj.rayCast((HitObj),obj,10,'wall',1,0,0)
            DrawDecal(LocVec,HitObj['content'])
            cont.activate(cont.actuators['KillBullet'])
        #negative tank dims	
        if wall_type == 'fluid':
            LocVec = obj.rayCast((HitObj),obj,10,'wall',1,0,0)
            #print(LocVec)
            effect_time = 0 
            frag_count = 0 
            dims_100 = 100 / (-(tank_dims[0]) + tank_dims[1])
            hit_100 = (-(tank_dims[0]) + (LocVec[1].z * 4) - HitObj.position.z) * dims_100
            #print(hit_100)

            if hit_100 >= tank_level:
                frag_obj = random.choice(element_db[HitObj['content']]['dry_hit_particle'])
                #print(frag_obj + " " + element_db[frag_obj]['frag_min'])
                frag_count = int(random.uniform(int(element_db[frag_obj]['frag_min']),int(element_db[frag_obj]['frag_max'])))
                DrawEmitter(LocVec,0,frag_count,'dry',HitObj['content'])
                cont.activate(cont.actuators['KillBullet'])
            if hit_100 < tank_level:
                tank_drop = tank_level - hit_100
                #print("tank info: " + str(tank_drop) + "," + str(tank_level))
                HitObj['tank_level'] = tank_level - tank_drop
                effect_time = tank_drop * .125
                DrawEmitter(LocVec,effect_time,0,'wet',HitObj['content'])
                cont.activate(cont.actuators['KillBullet'])
        
        else:
            cont.activate(cont.actuators['KillBullet'])

           
        
def wallHit():
    dmg_lvl = prop1['dmglevel'].value
    HitObj = sens['wall'].hitObject
    if sens['wall'].positive:
        if dmg_lvl == 20:
            obj.replaceMesh('Cube.016') 
            prop1['dmglevel'].value = dmg_lvl + 1

        if dmg_lvl == 40:
            obj.replaceMesh('Cube.019')
            prop1['dmglevel'].value = dmg_lvl + 1

        if dmg_lvl == 60:
            obj.replaceMesh('Cube.020') 
            prop1['dmglevel'].value = dmg_lvl + 1

        else:
            prop1['dmglevel'].value = dmg_lvl + 1

def decalDrop():
    decal_life = obj['data_frame'][0] 
    decal_type = obj['data_frame'][1] 
    decal_count = obj['data_frame'][2]
    emit_freq = obj['data_frame'][3] 
    frag_count = obj['data_frame'][4] 
    content = obj['data_frame'][5]

    if decal_type == 'wet':
        if obj['decal_timer'] < decal_life:
            flow_rate = 1 - (1 / (decal_life / obj['decal_timer']))
            if emit_freq == 5:
                flow_direction = (int(random.uniform(2,10)),int(random.uniform(-3,3)),int(random.uniform(-5,0)))
                flow_direction_comp = [flow_rate * x for x in flow_direction]
                bullet = cont.actuators['Emitter']
                BulletObj = random.choice(element_db[content]['wet_hit_particle'])
                bullet.object = random.choice(element_db[BulletObj]['model'])
                bullet.linearVelocity = flow_direction_comp
                cont.activate(bullet)
                obj['data_frame'][3] = 0
            if emit_freq < 10:
                obj['data_frame'][3] += 1
        if obj['decal_timer'] > decal_life:
            print('j00 dead f00 wet')
            obj.endObject()

    if decal_type == 'dry':
       if frag_count < decal_count:
            bullet = cont.actuators['Emitter']
            collision_mat = random.choice(element_db[content]['dry_hit_particle'])
            bullet.object = random.choice(element_db[collision_mat]['model'])
            bullet.linearVelocity = (int(random.uniform(2,10)),int(random.uniform(-3,3)),int(random.uniform(-5,5)))
            cont.activate(bullet)
            obj['data_frame'][4] += 1
            print(frag_count)
            print(decal_count)
       if frag_count >= decal_count:
            print('j00 dead f00 dry')
            obj.endObject()

#Logic put in to use down here

if sens_name == "emitter":
    if sens[sens_name].triggered == 1:
        print("emitter triggered!")
elif sens_name == "particle":
    if sens[sens_name].triggered == 1:
        smokeParticle()
elif sens_name == "wall":
    if sens[sens_name].triggered == 1:
        wallHit()
elif sens_name == "bullet":
    if sens[sens_name].triggered == 1:
        HitObj = sens['bullet'].hitObject
        print(str(HitObj['content']) + " , " + str(HitObj.position.z))
        if element_db[HitObj['content']]['type'] != 'particle':
            bulletHit()  
elif sens_name == "decal":
    if sens[sens_name].triggered == 1:
        decalDrop()
