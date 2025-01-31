# Simulation
## About
This repository contains a physical simulation. It simulates elastic collisions and coulomb interactions between charged and uncharged Balls. The simulation is written entirely in python using the [pygame](https://pygame.org/) module.


## Usage
Running an executable or the unchanged source code will present you with a small sample, showing off all the features of the simulation.

### Linux Executable (doesn't require python)
1. Download the file named `simulation_linux` from the [latest release page](https://github.com/DanceMonkey276/simulation/releases/latest)
2. Edit the permissions if necessary, for example `chmod 744 ./simulation_linux`
3. Run the file with `./simulation_linux`

### Windows executable (doesn't require python)
1. Download the file named `simulation_windows.exe` from the [latest release page](https://github.com/DanceMonkey276/simulation/releases/latest)
2. Run it from the terminal using `./simulation_windows.exe` or double-click it in the file explorer

### Source code (all operating systems, requires python)
1. Download the source code from the [latest release page](https://github.com/DanceMonkey276/simulation/releases/latest) (as .zip file or as tarball) and extract it
2. Create a new virtual environment using `python -m venv venv` and activate it
3. Install the requirements using `pip install -r ./requirements.txt`
4. Run the program using `python main.py`

Running the simulation from the source code also allows you to modify the objects, add new ones or remove others. Feel free to play around and experiment!


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
