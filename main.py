"""The main script for a physical simulation"""

import sys
import pygame

# Define tweakable values
FPS: int = 30
DEBUG: bool = True
END_TIME: float = 100.0

# Initialize the display
pygame.display.init()
pygame.display.set_mode((1500, 1000))
display: pygame.Surface = pygame.display.get_surface()
clock: pygame.time.Clock = pygame.time.Clock()

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

    # Update the display
    display.fill((121, 121, 121))
    pygame.display.update()
    clock.tick(FPS)

    # Print debug values
    if DEBUG:
        print(f"DEBUG (#{step}):")
        print(f"  time: {time}")
        print(f"  fps: {clock.get_fps()}")
        print("")

    # Check if the simulation should end
    if time >= END_TIME:
        RUNNING = False

    # Update values
    step += 1
    time += 1 / FPS

pygame.display.quit()
sys.exit(0)
