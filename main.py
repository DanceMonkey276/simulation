"""The main script for a physical simulation

Simulate balls with elastic collisions or molecules with coulomb interactions

Commandline arguments of the script
 -h, --help             Display this help and exit
 -f, --fps FRAMES       Sets the frames per second of the simulation to FRAMES (integer)
 -d, --debug            Activates debug modes, prints useful information
 -e, --end-time TIME    Sets the ending time of the simulation to TIME (floating point number)
"""

import sys
from typing import List
import pygame
from math_core import CoordSys
from objects import SimulationObject, Molecule, calculate_objects

# Set defaults for the tweakable values
FPS: int = 30
DEBUG: bool = False
END_TIME: float = 100.0

# Evaluate the commandline arguments
args: List[str] = sys.argv[:]
args.pop(0)

i: int = 0

while i < len(args):
    arg: str = args[i]
    if arg in {"-h", "--help"}:
        print(
            """
Help for commandline arguments of the simulation
 -h, --help             Display this help and exit
 -f, --fps FRAMES       Sets the frames per second of the simulation to FRAMES (integer)
 -d, --debug            Activates debug modes, prints useful information
 -e, --end-time TIME    Sets the ending time of the simulation to TIME (floating point number)"""
        )
        sys.exit(0)

    elif arg in {"-f", "--fps"}:
        i += 1
        try:
            FPS = int(args[i])
        except ValueError as exc:
            raise ValueError(f"Invalid FPS value: {args[i]}") from exc
        except IndexError as exc:
            raise ValueError(f"'{arg}' needs an FPS value") from exc

    elif arg in {"-d", "--debug"}:
        DEBUG = True

    elif arg in {"-e", "--end-time"}:
        i += 1
        try:
            END_TIME = float(args[i])
        except ValueError as exc:
            raise ValueError(f"Invalid time value: {args[i]}") from exc
        except IndexError as exc:
            raise ValueError(f"'{arg}' needs a time value") from exc

    else:
        raise ValueError(f"Invalid argument: '{arg}'")

    i += 1

# Create the objects in the simulation
simulation_objects: List[SimulationObject] = [
    Molecule(7000.0, 5000.0, charge=1),
    Molecule(8000.0, 5000.0, charge=-1),
]

# Initialize the display
pygame.display.init()
pygame.display.set_mode((1500.0, 1000.0), flags=pygame.RESIZABLE)
display: pygame.Surface = pygame.display.get_surface()
clock: pygame.time.Clock = pygame.time.Clock()
coord_sys: CoordSys = CoordSys(display)

# Calculate the position values of the objects
calculate_objects(simulation_objects, END_TIME, 1 / FPS, coord_sys)

# Define starting values for the main loop
step: int = 0
time: float = 0.0
RUNNING: bool = True

PAUSE: bool = False
CTRL_MOD: bool = False

# Main loop
while RUNNING:
    # Check keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                PAUSE = not PAUSE

            elif event.key in {pygame.K_LCTRL, pygame.K_RCTRL}:
                CTRL_MOD = True

            elif event.key == pygame.K_RIGHT:
                if CTRL_MOD:
                    step += FPS
                    time += 1
                else:
                    step += 1
                    time += 1 / FPS

            elif event.key == pygame.K_LEFT:
                if CTRL_MOD:
                    if step > FPS:
                        step -= FPS
                        time -= 1
                else:
                    if step > 0:
                        step -= 1
                        time -= 1 / FPS

        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_LCTRL, pygame.K_RCTRL}:
                CTRL_MOD = False

    # Print debug values
    if DEBUG:
        print(f"DEBUG #{step}:")
        print(f"  time: {round(time, 5)} ({END_TIME})")
        print(f"  fps: {round(clock.get_fps(), 5)} ({FPS})")
        print(f"  screen: {display.get_width()} | {display.get_height()}")
        print("")

    # Fill the display
    display.fill((121, 121, 121))

    # Draw all objects to the screen
    for obj in simulation_objects:
        obj.draw(step, coord_sys)

    # Update the screen
    coord_sys.draw_borders()
    pygame.display.update()

    # Check if the simulation should end
    if round(time, 5) >= END_TIME:
        RUNNING = False

    if not PAUSE:
        # Update values
        step += 1
        time += 1 / FPS

    clock.tick(FPS)


# Quit the script
pygame.display.quit()
sys.exit(0)
