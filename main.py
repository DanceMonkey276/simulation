"""The main script for a physical simulation"""

import sys
from typing import List
import pygame
from math_core import CoordSys
from objects import SimulationObject, Molecule, calculate_objects

# Define tweakable values
FPS: float = 30.0
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

# Main loop
while RUNNING:
    # Check keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    # Fill the display
    display.fill((121, 121, 121))

    # Draw all objects to the screen
    for obj in simulation_objects:
        obj.draw(step, coord_sys)

    # Update the screen
    coord_sys.draw_borders()
    pygame.display.update()
    clock.tick(FPS)

    # Print debug values
    if DEBUG:
        print(f"DEBUG #{step}:")
        print(f"  time: {time} ({END_TIME})")
        print(f"  fps: {clock.get_fps()} ({FPS})")
        print(f"  screen: {display.get_width()} | {display.get_height()}")
        print("")

    # Check if the simulation should end
    if time >= END_TIME:
        RUNNING = False

    # Update values
    step += 1
    time += 1 / FPS

# Quit the script
pygame.display.quit()
sys.exit(0)
