# Computer-Graphics 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)
[![Language](https://img.shields.io/badge/Language-Python-blue.svg?style=flat)](https://www.python.org)
[![Requires](https://img.shields.io/badge/Requires-OpenGL-blue.svg?style=flat&)](https://www.opengl.org//)
[![Release](https://img.shields.io/badge/Release-v1.0-green.svg?style=flat)](https://github.com/salistito/Computer-Graphics)

## Table of contents

- [About](#about)
- [Requirements and Quick Start](#requirements-and-quick-start)
- [Proyect 1b - Space Wars](proyect-1b---space-wars)
- [Proyect 2c - Bird Migration Simulator](proyect-2c---bird-migration-simulator)
- [Proyect 3a - Aquarium Problem and Visualization (PDE's)](proyect-3a---aquarium-problem-and-visualization-(PDE's))
- [Credits](#credits)
- [Copyright and License](#copyright-and-license)

## About

This repository contains the three mains projects from CC3501 - Modeling and Computer Graphics for Engineers <br>
(5th semester of Computer Science Engineering at FCFM, University of Chile), 2020 fall semester edition (2020-1). 

This course has a wide range of topics, such as:
- Algorithms and Techniques for Computer Graphics 
- 2D Modeling and Visualization
- 3D Modeling and Visualization
- Illumination on Polygon Meshes
- Finite Differences for PDE's
- Scientific Visualization

These 3 works cover the most important topics and are made with Python using Open GL.

## Requirements and Quick Start:

- [Download and install python 3.7 or higher ](https://www.python.org/downloads/)
- Install the necessary modules: `pip install numpy scipy matplotlib pyopengl glfw ipython jupyter`
- Clone the repository: `https://github.com/salistito/Computer-Graphics.git`
- Enjoy :)

## Proyect 1b - Space Wars

<div>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea1b_SpaceWars/Preview/combat_1.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea1b_SpaceWars/Preview/combat_2.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea1b_SpaceWars/Preview/youWin.png" width="275" height="250"/>
</div>

A basic 2D game inspired on [Space Invaders](https://es.wikipedia.org/wiki/Space_Invaders).
You are the pilot of an attack ship that participates in a space war, your duty is to eliminate all enemies approaching your ship, which contains a long-range cannon.

This work was made with python using basic shapes, textures, keyboard commands and some basic shaders and transformations with Open GL.

To run the game it is necessary to run the space-war.py file specifying how many enemies there will be, for example:
- `python space-wars.py 10` runs the game with 10 enemies

## Proyect 2c - Bird Migration Simulator

<div>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea2c_BirdHerd/Preview/bird.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea2c_BirdHerd/Preview/birdHerd_back.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea2c_BirdHerd/Preview/birdHerd_Front.png" width="275" height="250"/>
</div>

A basic bird migration simulator, It uses an articulated model to animate the flight of the birds along a curvilinear trajectory specified.

This work was made with python using basic shapes, textures, curves in 3D, commands that depend on the cursor position and some basic shaders and transformations with Open GL.

To run the simulator it's necessary to run the bird-herd.py file specifying the migration trajectory on a csv file and how many birds there will be, for example:
- `python bird-herd.py csvFiles\sinusoidal.csv 5` runs the simulator with a sinusoidal trajectory and 5 birds 

## Proyect 3a - Aquarium Problem and Visualization (PDE's)

<div>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea3a_EDPs/Preview/solution_2.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea3a_EDPs/Preview/fish.png" width="275" height="250"/>
<img src="https://github.com/salistito/Computer-Graphics/blob/main/Tarea3a_EDPs/Preview/aquarium.png" width="275" height="250"/>
</div>

The goal of this work is to create an application that solves the heat equation for the water contained in an aquarium using Finite Differences for PDE's.
Different types of fish will prefer different sectors of the aquarium, so it is necessary to create a second application that allows to visualize how they will be distributed inside the aquarium.

To run the solver it's necessary to run the aquarium_solver.py file specifying the problem setup on a json file, for example:
- `python aquarium_solver.py ProblemJSONs\problem_setup.json` runs the solver with the problem setup specified on the json file

To run the aquarium simulator it's necessary to run the aquarium_view.py file specifying the view setup on a json file, for example:
- `python aquarium_view.py ViewJSONs\view_setup.json` runs the aquarium simulator with the view setup specified on the json file 

## Credits

Thanks to **Professor Daniel Calderón** for providing some base scripts that allowed to create these projects!

## Copyright and License

Code released under the [MIT License](https://github.com/salistito/Computer-Graphics/blob/main/LICENSE).
