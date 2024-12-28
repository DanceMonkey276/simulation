"""Objects that are used in the physical simulation"""

from typing import List
from math_core import Vector


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
        self.acceleration: List[Vector] = [Vector(0, 0)]

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

    @property
    def a_0(self) -> Vector:
        """Getter-function for the starting acceleration of the object

        Returns
        -------
        Vector
            The starting acceleration of the object
        """
        return self.acceleration[0]

    @a_0.setter
    def a_0(self, new_val: Vector) -> None:
        self.acceleration[0] = new_val
