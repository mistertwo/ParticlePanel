DTScripts Particle Database
by Daniel Turton

Description:

(This will be fun. :) )

The DTScripts Particle Database is a framework that (hopefully) makes the process of creating particle effects a little easier.

I'm releasing the uber-alpha version of a script that I've been working on for Blender. This was made mostly for learning python through Blender, but I hope that it will eventually help others out there who are using the game engine and would like to create particle elements and materials for them to interact with. 

My script (DTS_ParticlePanel, a Blender Addon) starts off in the Particles panel and presents you with options to create four types of elements, along with a panel for database control. You can create elements for projectiles, particles (reaction elements), statics (particle generators or decals that can appear upon impact or contact) and materials, which react when hit by projectiles and hold information on the object they're tied to. You'll need to create new elements if you're dealing with a fresh file. The "material" designation will be changing in a future release. 

If you click on the larger button for each element type, you can tie a previously created element to a new object. It's object will automatically be added to the list of objects to emit when it's called. The "material" element type will allow you to assign multiple particles and statics to be chosen at random when the element is called.

The database control panel allows you to import text files that have been previously dumped from the database. The format is human readable and can be changed within a text editor if need be. If you're wanting to start over with the database for any reason, it can be purged and started anew. This does not remove element definitions from objects that you are working with. 

The DTS_Info Loader file will (for the moment) need to be called by an object in your game with an always sensor set to tap once at the start of the game. This will pull information from the database into a dictionary in GameLogic that is accessible by various elements.

The Effects_Combo file is something that I had created before work started on this panel, as a way of simulation the action of a fishtank draining. At this moment, it reads from the database and takes in information from the material elements that it collides with. There are a few variables that are hard-coded at this moment, but eventually those will be controlled from the panel also. Right now, you can control (in the "Material" settings) whether the material you're dealing with is "wet" or "dry". "Wet" will use the fishtank effect. "Dry" will just give of a fragment reaction. 

As far as using this, place the DTS_ParticlePanel file as an addon. The other files are to be loaded in as text blocks. You'll need to have one of each type of object created. The particle, projectile and static objects need to be moved to another layer after being set up. To have everything work, you'll need to set the material element's Area Upper and lower to something other than zeros, 5 and -5 should work for trying things out. The particle will need to have it's "fragment count" settings adjusted also; 2 and 6 should work here. Be sure to commit any changes that are made.

In you main layer/scene you should have a material object, along with an emitter triggered by a key press of your choice, that fires the bullet object towards the wall. Adding controls to raise or lower the emitter "gun" is not a bad idea.

Before the game engine will be able to use the database information, once you're done setting up, you will need to "push" the information to the database. What this does is set up the objects with game engine readable variables and makes a dump of the current database to a human-readable text block. If any changes are made to the information in the database, you will need to remove the "GameExport" text block and "push" the data again.

To pull the information over into the game engine, for the moment you will need to create a random object that has an always sensor, set to tap, tied to a python controller that will run the DTS_InfoLoader script.

Once this is done, hit the play button and fire at the wall.

This is version Alpha 2. There will be error message generated and left over code for other functions that are in progress. I hope that you enjoy what it can do now and what it will do in the future.

If you have any crits or comments after trying this out, please feel free to let me know by sending an e-mail to me@danielturton.net

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
