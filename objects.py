"""Objects that are used in the physical simulation"""

from typing import List
import pygame
from math_core import Vector, CoordSys


class SimulationObject:
    """A base class for an object in the simulation"""

    global_index: int = 0

    def __init__(
        self,
        x_0: float,
        y_0: float,
    ) -> None:
        self.position: List[Vector] = [Vector(x_0, y_0)]
        self.velocity: List[Vector] = [Vector(0, 0)]
        self.acceleration: Vector = Vector(0, 0)

        self.index = SimulationObject.global_index
        SimulationObject.global_index += 1

    def __repr__(self) -> str:
        return f"<Simulation Object #{self.index}>"

    @property
    def r_0(self) -> Vector:
        """Getter-function for the starting position of the object

        Returns
        -------
        Vector
            The starting position of the object
        """
        return self.position[0]

    @r_0.setter
    def r_0(self, new_val: Vector) -> None:
        self.position[0] = new_val

    @property
    def v_0(self) -> Vector:
        """Getter-function for the starting velocity of the object

        Returns
        -------
        Vector
            The starting velocity of the object
        """
        return self.velocity[0]

    @v_0.setter
    def v_0(self, new_val: Vector) -> None:
        self.velocity[0] = new_val

    def step(self, dt: float) -> None:
        """Calculate where the object will be in the next step

        Parameters
        ----------
        dt : float
            The time difference to the next step
        """
        self.velocity.append(self.acceleration * dt + self.velocity[-1])
        self.position.append(self.velocity[-1] * dt + self.position[-1])

        self.acceleration = Vector(0, 0)

    def draw(self, step: int, coord_sys: CoordSys) -> None:
        """Draw the object onto the screen

        Parameters
        ----------
        step : int
            The current step of the simulation
        coord_sys : CoordSys
            The coordinate System used for the simulation screen
        """
        pygame.draw.circle(
            coord_sys.display,
            (255, 255, 255),
            coord_sys.coord(*self.position[step]),
            10,
        )
        pygame.draw.circle(
            coord_sys.display,
            (0, 0, 0),
            coord_sys.coord(*self.position[step]),
            10,
            2,
        )


def calculate_objects(
    objects: List[SimulationObject], end_time: float, dt: float
) -> None:
    """Calculate the position values of all objects at every time in the simulation

    Parameters
    ----------
    objects : List[SimulationObject]
        A list containing all objects for which the values should be calculated
    dt : float
        The time difference between every step
    """
    time: float = 0
    while time <= end_time:
        for obj in objects:
            obj.step(dt)

        time += dt
