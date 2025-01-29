"""A python module containing objects for a physical simulation

This module contains:
- class `SimulationObject`: A base class for other objects
- class `Molecule`: A molecule with a charge used for coulomb-interactions
- class `Interactions`: A class to manage and calculate \
    the interactions between the objects
- function `calculate_objects`: A function to calculate and update the \
    position values of all objects
"""

from typing import List, Tuple
import pygame
from scipy.constants import pi, epsilon_0
from math_core import Vector, CoordSys, dot_product


class SimulationObject:
    """A base class for an object in the simulation

    The object features:
    - position [`pm`], velocity [`pm/s`] and acceleration [`pm/s^2`] values
    - a way to update these values respectively
    - mass [`u`] and radius [`pm`] values
    - a way to draw itself onto a pygame screen
    - an index
    """

    global_index: int = 0

    def __init__(
        self,
        x_0: float,
        y_0: float,
        vx_0: float = 0.0,
        vy_0: float = 0.0,
        radius: float = 100.0,
        mass: float = 1.0,
        colour: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        # Motion values
        self.position: List[Vector] = [Vector(x_0, y_0)]
        self.velocity: List[Vector] = [Vector(vx_0, vy_0)]
        self.acceleration: Vector = Vector(0.0, 0.0)

        # Object properties
        self.radius: float = radius
        self.mass: float = mass
        self.colour: Tuple[int, int, int] = colour

        # Object index
        self.index: int = SimulationObject.global_index
        SimulationObject.global_index += 1

    def __repr__(self) -> str:
        return f"<Simulation Object #{self.index}>"

    @property
    def r_0(self) -> Vector:
        """Getter-function for the starting position of the object

        Returns
        -------
        `Vector`
            The starting position of the object
        """
        return self.position[0]

    @r_0.setter
    def r_0(self, new_val: Vector) -> None:
        """Setter-function for the starting position of the object

        Parametres
        ----------
        `new_val` : `Vector`
            The new starting position of the object
        """
        self.position[0] = new_val

    @property
    def v_0(self) -> Vector:
        """Getter-function for the starting velocity of the object

        Returns
        -------
        `Vector`
            The starting velocity of the object
        """
        return self.velocity[0]

    @v_0.setter
    def v_0(self, new_val: Vector) -> None:
        """Setter-function for the starting velocity of the object

        Parametres
        ----------
        `new_val` : `Vector`
            The new starting velocity of the object
        """
        self.velocity[0] = new_val

    def next(self) -> None:
        """Update the motion values of the object

        Reset the acceleration to a zero-vector \\
        Set the next velocity to the last one \\
        Set the next position to the last one
        """
        self.acceleration = Vector(0.0, 0.0)
        self.velocity.append(self.velocity[-1])
        self.position.append(self.position[-1])

    def step(self, step: int, dt: float) -> None:
        """Calculate the next position values of the object

        Apply euler chromer to the velocity and position values

        ```
        v += a * dt
        r += v * dt
        ```

        Parametres
        ----------
        `step` : `int`
            The current step of the simulation
        `dt` : `float`
            The difference in time between two steps
        """
        self.velocity[step] += self.acceleration * dt
        self.position[step] += self.velocity[step] * dt

    def draw(self, step: int, coord_sys: CoordSys) -> None:
        """Draw the object onto the screen

        Parametres
        ----------
        `step` : `int`
            The current step of the simulation
        `coord_sys` : `CoordSys`
            The coordinate system of the display
        """
        pygame.draw.circle(
            coord_sys.display,
            self.colour,
            coord_sys.coord(*self.position[step]),
            coord_sys.distance(self.radius),
        )
        pygame.draw.circle(
            coord_sys.display,
            (0, 0, 0),
            coord_sys.coord(*self.position[step]),
            coord_sys.distance(self.radius),
            2,
        )


class Molecule(SimulationObject):
    """A base class for a molecule in the simulation

    The molecule features:
    - everything from it's baseclass (`SimulationObject`)
        - position [`pm`], velocity [`pm/s`] and acceleration [`pm/s^2`] values
        - a way to update these values respectively
        - mass [`u`] and radius [`pm`] values
        - a way to draw itself onto a pygame screen
        - an index
    - a charge [`e`]
    """

    def __init__(
        self,
        x_0: float,
        y_0: float,
        vx_0: float = 0.0,
        vy_0: float = 0.0,
        radius: float = 100.0,
        mass: float = 1.0,
        colour: Tuple[int, int, int] = (255, 255, 255),
        charge: int = 0,
    ) -> None:
        super().__init__(x_0, y_0, vx_0, vy_0, radius, mass, colour)

        self.charge = charge

    def __repr__(self) -> str:
        return f"<Molecule #{self.index}>"


class Interactions:
    """Simulate interactions between objects

    This class features:
    - wall collisions:
        - calculate the collision between the object and the wall
        - use the principle of elastic collisions
    - elastic collisions
        - a collision with no friction
        - kinetic energy and momentum stays the same
    - coulomb interactions
        - calculate the force between charged objects
        - `f = 1 / (4 * pi * epsilon_0) * q_1 * q_2 / r^2`
    """

    def __init__(self, objects: List[SimulationObject]) -> None:
        self.objects = objects

    def __repr__(self) -> str:
        return "<Interactions>"

    def _wall_collision(
        self, obj: SimulationObject, step: int, coord_sys: CoordSys
    ) -> None:
        """Apply a collision between an object and the edge of the display

        Parametres
        ----------
        `obj` : `SimulationObject`
            The object that should collide with the wall
        `step` : `int`
            The current step of the simulation
        `coord_sys` : `CoordSys`
            The coordinate system of the screen
        """
        if obj.position[step].x - obj.radius <= 0:
            obj.position[step].x = obj.radius
            obj.velocity[step].x = -obj.velocity[step].x
        if obj.position[step].x + obj.radius >= coord_sys.x_tot:
            obj.position[step].x = coord_sys.x_tot - obj.radius
            obj.velocity[step].x = -obj.velocity[step].x
        if obj.position[step].y - obj.radius <= 0:
            obj.position[step].y = obj.radius
            obj.velocity[step].y = -obj.velocity[step].y
        if obj.position[step].y + obj.radius >= coord_sys.y_tot:
            obj.position[step].y = coord_sys.y_tot - obj.radius
            obj.velocity[step].y = -obj.velocity[step].y

    def _elastic_collision(
        self, obj1: SimulationObject, obj2: SimulationObject, step: int
    ) -> None:
        """Apply an elastic collision between two objects

        Resolve an elastic collision by ensuring that the total momentum \\
        of the system as well as its kinetic energy stays the same

        Parametres
        ----------
        `obj1` : `SimulationObject`
            The first interacting object
        `obj2` : `SimulationObject`
            The second interacting object
        `step` : `int`
            The current step of the simulation
        """
        distance: Vector = obj2.position[step] - obj1.position[step]

        # Check if the objects are colliding
        if distance.magnitude > obj1.radius + obj2.radius:
            return

        norm_vector: Vector = distance / distance.magnitude

        relative_velocity: float = dot_product(
            obj1.velocity[step] - obj2.velocity[step], norm_vector
        )

        # Check if the objects are moving towards each other
        if relative_velocity < 0:
            return

        impulse: Vector = (
            2 * relative_velocity / (1 / obj1.mass + 1 / obj2.mass)
        ) * norm_vector

        # Apply the impulse to the objects
        obj1.velocity[step] -= impulse / obj1.mass
        obj2.velocity[step] += impulse / obj2.mass

    def _molecule_interaction(self, obj1: Molecule, obj2: Molecule, step: int) -> None:
        """Apply the coulomb force between two molecules

        Resolve an interaction between charged objects using the formula for coulomb force: \\
        `f = 1 / (4 * pi * epsilon_0) * q_1 * q_2 / r^2`

        Parametres
        ----------
        `obj1` : `Molecule`
            The first interacting object
        `obj2` : `Molecule`
            The second interacting object
        `step` : `int`
            The current step of the simulation
        """
        # Convert the distance to metres
        distance: Vector = (obj2.position[step] - obj1.position[step]) * 1e-12

        # Avoid huge forces in case the molecules phase through each other
        if distance.magnitude <= (obj1.radius + obj2.radius) * 1e-12:
            return

        # Convert charges to coulombs
        coulomb_1: float = obj1.charge * 1.602176634e-19
        coulomb_2: float = obj2.charge * 1.602176634e-19

        # Calculate the force between the molecules using the formula for coulomb force
        force: Vector = (
            (coulomb_1 * coulomb_2)
            / (4 * pi * epsilon_0)
            * (distance / distance.magnitude**3)
        ) * 1e12

        # Apply the force
        obj1.acceleration -= force
        obj2.acceleration += force

    def calculate(self, step: int, coord_sys: CoordSys) -> None:
        """Calculate the interactions between the objects

        Parametres
        ----------
        `step` : `int`
            The current step of the simulation
        """
        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1 :]:
                if isinstance(obj1, Molecule) and isinstance(obj2, Molecule):
                    self._molecule_interaction(obj1, obj2, step)

                self._elastic_collision(obj1, obj2, step)

            self._wall_collision(obj1, step, coord_sys)


def calculate_objects(
    objects: List[SimulationObject], end_time: float, dt: float, coord_sys: CoordSys
) -> None:
    """Calculate the positions of the objects at every time

    Loop through all possible time steps, and then:
    1. Calculate the interactions between the objects
    2. Update the velocity and position values

    Parametres
    ----------
    `objects` : `List[SimulationObject]`
        The list of objects that are simulated
    `end_time` : `float`
        The time at which the simulation will end
    `dt` : `float`
        The difference in time between two steps
    """
    interactions: Interactions = Interactions(objects)

    time: float = dt
    step: int = 1

    while time <= end_time:
        # Append the next values
        for obj in objects:
            obj.next()

        # Calculate the interactions
        interactions.calculate(step, coord_sys)

        # Update the motion values
        for obj in objects:
            obj.step(step, dt)

        time += dt
        step += 1
