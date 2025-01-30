# Simulation
## About
This repository contains a physical simulation. It simulates elastic collisions and coulomb interactions between charged and uncharged Balls. The simulation is written entirely in python using the [pygame](https://pygame.org/) module.


## Controls
Here are some important things to know about the simulation:
* You can pause the simulation by pressing the space bar
* You can step forwards or backwards manually using the arrow keys
* Holding down ctrl while stepping through the simulation will skip an entire second (FPS amount of steps)
* The simulation will start in fullscreen mode by default, which you can toggle with F11
* The screen size is dynamic and will adapt to every aspect ratio

In addition, you can customize the simulation using commandline arguments:

* `-h` or `--help` will print an overview of the arguments and exit
* `-f FRAMES` or `--fps FRAMES` will change the FPS to FRAMES. By default, this value is set to 60
* `-d` or `--debug` will activate debug mode, printing information about the simulation to the terminal, like the time that has passed or the frames per second.
* `-e TIME` or `--end-time TIME` will set the duration of the simulation to TIME seconds. By default, this value is set to 100
