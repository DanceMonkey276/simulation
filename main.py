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
FPS: int = 60
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
    SimulationObject(8137, 9084, 140, 270),
    SimulationObject(5993, 6018, -10, 260),
    SimulationObject(1588, 8379, 230, 80),
    SimulationObject(3909, 2819, 50, 210),
    SimulationObject(8426, 3562, -280, 130),
    SimulationObject(4816, 5947, -110, 290),
    SimulationObject(5235, 7409, 90, -230),
    SimulationObject(2483, 5261, -290, -180),
    SimulationObject(1358, 7910, -160, -160),
    SimulationObject(2332, 2949, 270, -180),
    SimulationObject(4636, 9530, -50, 210),
    SimulationObject(985, 1125, -20, 200),
    SimulationObject(5372, 8847, 100, -280),
    SimulationObject(9725, 3339, 100, 220),
    SimulationObject(2838, 8600, -240, 0),
    SimulationObject(347, 9041, -50, -130),
    SimulationObject(692, 3557, -40, 190),
    SimulationObject(2073, 5674, -10, 190),
    SimulationObject(1514, 4768, -100, -70),
    SimulationObject(1340, 5008, 50, -70),
    Molecule(2538, 8494, 160, -60, charge=2, colour=(255, 136, 136)),
    Molecule(3944, 1923, -10, -220, charge=3, colour=(255, 0, 0)),
    Molecule(2825, 7686, -20, 170, charge=-2, colour=(136, 136, 255)),
    Molecule(4551, 2351, 100, -80, charge=-3, colour=(0, 0, 255)),
    Molecule(5191, 1345, 150, 20, charge=2, colour=(255, 136, 136)),
    Molecule(3387, 6318, -260, -130, charge=3, colour=(255, 0, 0)),
    Molecule(3228, 5934, -260, 80, charge=2, colour=(255, 136, 136)),
    Molecule(6456, 4856, 170, -40, charge=-2, colour=(136, 136, 255)),
    Molecule(8548, 3259, -200, -40, charge=-3, colour=(0, 0, 255)),
    Molecule(9389, 5770, -80, -180, charge=3, colour=(255, 0, 0)),
]

# Initialize the display
pygame.display.init()
pygame.display.set_mode((0.0, 0.0), flags=pygame.FULLSCREEN)
pygame.display.set_caption("Simulation")
display: pygame.Surface = pygame.display.get_surface()
clock: pygame.time.Clock = pygame.time.Clock()
coord_sys: CoordSys = CoordSys(display)

# Calculate the position values of the objects
calculate_objects(simulation_objects, END_TIME, 1 / FPS, coord_sys)

# Define starting values for the main loop
STEP: int = 0
TIME: float = 0.0
RUNNING: bool = True

PAUSE: bool = False
FULLSCREEN: bool = True
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
                    STEP += FPS
                    TIME += 1.0
                else:
                    STEP += 1
                    TIME += 1 / FPS

            elif event.key == pygame.K_F11:
                if FULLSCREEN:
                    pygame.display.set_mode(
                        flags=pygame.RESIZABLE,
                    )
                    FULLSCREEN = False
                else:
                    pygame.display.set_mode((0.0, 0.0), flags=pygame.FULLSCREEN)
                    FULLSCREEN = True

            elif event.key == pygame.K_LEFT:
                if CTRL_MOD:
                    if STEP > FPS:
                        STEP -= FPS
                        TIME -= 1.0
                    else:
                        STEP = 0
                        TIME = 0.0
                else:
                    if STEP > 0:
                        STEP -= 1
                        TIME -= 1 / FPS

        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_LCTRL, pygame.K_RCTRL}:
                CTRL_MOD = False

    # Print debug values
    if DEBUG:
        print(f"DEBUG #{STEP}:")
        print(f"  time: {round(TIME, 5)} ({END_TIME})")
        print(f"  fps: {round(clock.get_fps(), 5)} ({FPS})")
        print(f"  screen: {display.get_width()} | {display.get_height()}")
        print("")

    # Fill the display
    display.fill((121, 121, 121))

    # Draw all objects to the screen
    for obj in simulation_objects:
        obj.draw(STEP, coord_sys)

    # Update the screen
    coord_sys.draw_borders()
    pygame.display.update()

    # Check if the simulation should end
    if round(TIME, 5) >= END_TIME:
        RUNNING = False

    if not PAUSE:
        # Update values
        STEP += 1
        TIME += 1 / FPS

    clock.tick(FPS)


# Quit the script
pygame.display.quit()
sys.exit(0)
