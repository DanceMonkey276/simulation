"""A python module containing math classes for a physical simulation

This module contains:
- class `CoordSys`: A dynamic coordinate system for the pygame screen
- class `Vector`: A two-dimensional vector with enhanced functionality
"""

from __future__ import annotations
from typing import Tuple, Any, Iterator
from collections.abc import Sequence
import pygame


class CoordSys:
    """Apply a dynamic coordinate system to a pygame screen

    The coordinate system features:
    - transformation of coordinates
    - transformation of lengths
    - borders to keep a constant aspect ratio
    """

    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.x_tot: int = 10000
        self.y_tot: int = 10000

    def __repr__(self) -> str:
        return f"<Coordinate System ([0, {self.x_tot}], [0, {self.y_tot}])>"

    def _update_dimensions(self) -> Tuple[float, float, float, float, float]:
        """Calculate the scale, offset and dimension for the screen

        scale factor: tells how many screen pixels a single step in the coordinate system is
        display width: the width of the pygame display
        display height: the height of the pygame display
        x_offset: compensates for different aspect ratios, 0 if aligned
        y_offset: compensates for different aspect ratios, 0 if alligned

        Returns
        -------
        `Tuple[float, float, float, float, float]`
            The scale factor, display width, display height, x offset and y offset values
        """
        # Calculate the new scale factor
        scale: float = min(
            self.display.get_width() / self.x_tot,
            self.display.get_height() / self.y_tot,
        )

        return (
            scale,  # scale factor
            self.display.get_width(),  # display width
            self.display.get_height(),  # display height
            (self.display.get_width() - self.x_tot * scale) / 2,  # x offset
            (self.display.get_height() - self.y_tot * scale) / 2,  # y offset
        )

    def distance(self, distance: float) -> float:
        """Convert a distance value from the coordinate syste to the
        value in pixels on the pygame screen

        Parametres
        ----------
        `distance` : `float`
            The original distance in the coordinate system

        Returns
        -------
        `float`
            The new distance in pixels on the screen
        """
        return distance * self._update_dimensions()[0]

    def coord(self, x: float, y: float) -> Tuple[float, float]:
        """Convert a coordinate from the coordinate system into a
        coordinate in pixels on the pygame screen

        Parametres
        ----------
        `x` : `float`
            The x-coordinate of the original coordinate
        `y` : `float`
            The y-coordinate of the original coordinate

        Returns
        -------
        `Tuple[float, float]`
            The new coordinate in pixels on the screen
        """
        scale, _, height, x_offset, y_offset = self._update_dimensions()
        return (
            x * scale + x_offset,
            height - y_offset - (y * scale),
        )

    def draw_borders(self) -> None:
        """Draw borders onto the screen to compensate for different aspect ratios
        
        Draw a black border at the edges of the display to ensure the \\
        visible part always has the same aspect ratio
        """
        _, width, height, x_offset, y_offset = self._update_dimensions()

        if x_offset:
            # Draw the borders to the right and left
            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0.0, 0.0, x_offset, height),
            )

            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (width - x_offset, 0.0, x_offset, height),
            )

        else:
            # Draw the borders to the top and bottom
            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0.0, 0.0, width, y_offset),
            )

            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0.0, height - y_offset, width, y_offset),
            )


class Vector(Sequence[float]):
    """A two-dimensional vector

    The vector features:
    - an x and y coordinate
    - addition and subtraction with another vector
    - multiplication and division with a scalar
    - magnitude property to calculate
    """

    def __init__(self, x: float, y: float) -> None:
        self.x: float = x
        self.y: float = y

    def __repr__(self) -> str:
        return f"<Vector ({self.x}, {self.y})>"

    def __len__(self) -> int:
        return 2

    # Since this vector is two-dimensional, there is no need for it to be sliceable. I added
    # the `# type: ignore` to supress an error message created by the Mypy type checker
    def __getitem__(self, index: int) -> float:  # type: ignore
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Vector index out of range")

    def __add__(self, other: Any) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise ValueError(f"Can only add two vectors, not vector and {type(other)}")

    def __sub__(self, other: Any) -> Vector:
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        raise ValueError(f"Can only subtract two vectors, not vector and {type(other)}")

    def __mul__(self, scalar: Any) -> Vector:
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        raise ValueError(
            f"Can only multiply scalar (int, float) with vector, not {type(scalar)}"
        )

    def __rmul__(self, scalar: Any) -> Vector:
        return self.__mul__(scalar)

    def __truediv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        raise ValueError(f"Can divide vector only by scalar, not {type(other)}")

    def __floordiv__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x // other, self.y // other)
        raise ValueError(f"Can divide vector only by scalar, not {type(other)}")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        raise ValueError(f"Can only compare two vectors, not vector and {type(other)}")

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y))

    @property
    def magnitude(self) -> float:
        """Calculate the magnitude of the vector

        Returns
        -------
        `float`
            The magnitude of the vector
        """
        return (self.x**2 + self.y**2) ** 0.5


def dot_product(vec1: Vector, vec2: Vector) -> float:
    """Calculate the scalar product between two vectors

    `scalar_product = v1_x * v2_x + v1_y * v2_y`


    Parametres
    ----------
    `vec1` : `Vector`
        The first vector
    `vec2` : `Vector`
        The second vector

    Returns
    -------
    `float`
        The scalar product
    """
    return vec1.x * vec2.x + vec1.y + vec2.y
