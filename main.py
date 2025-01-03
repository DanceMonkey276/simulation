"""The main script for a physical simulation"""

import sys
from typing import List
import pygame
from math_core import CoordSys
from objects import SimulationObject, Molecule, calculate_objects

# Define tweakable values
FPS: int = 30
DEBUG: bool = True
END_TIME: float = 100.0

# Create the objects in the simulation
simulation_objects: List[SimulationObject] = [
    Molecule(7000, 5000, charge=1),
    Molecule(8000, 5000, charge=-1),
]

# Calculate the position values of the objects
calculate_objects(simulation_objects, END_TIME, 1 / FPS)

# Initialize the display
pygame.display.init()
pygame.display.set_mode((1500, 1000), flags=pygame.RESIZABLE)
display: pygame.Surface = pygame.display.get_surface()
clock: pygame.time.Clock = pygame.time.Clock()
coord_sys: CoordSys = CoordSys(display)

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
    if time >= END_TIME:
        RUNNING = False

    if not PAUSE:
        # Update values
        step += 1
        time += 1 / FPS

    clock.tick(FPS)


# Quit the script
pygame.display.quit()
sys.exit(0)
