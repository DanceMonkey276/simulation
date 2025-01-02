"""Math utilities used for the physical simulation"""

from __future__ import annotations
from typing import Tuple, Any, Iterator
from collections.abc import Sequence
import pygame


class CoordSys:
    """Apply a custom coordinate system to a pygame screen"""

    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.x_tot: int = 15000
        self.y_tot: int = 10000

    def __repr__(self) -> str:
        return f"<Coordinate System ([0, {self.x_tot}], [0, {self.y_tot}])>"

    def _update_dimensions(self) -> Tuple[float, float, float, float, float]:
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
        """Calculate the distance in pixels on the screen relative to the coordinate system

        Parameters
        ----------
        distance : float
            The original distance that should be converted

        Returns
        -------
        float
            The new distance in pixels
        """
        return distance * self._update_dimensions()[0]

    def coord(self, x: float, y: float) -> Tuple[float, float]:
        """Calculate a coordinate as pixels on the screen relative to the coordinate systen

        Parameters
        ----------
        x : float
            The original x coordinate that should be converted
        y : float
            The original y coordinate that should be converted

        Returns
        -------
        Tuple[float, float]
            The new coordinate as pixels
        """
        scale, _, height, x_offset, y_offset = self._update_dimensions()
        return (
            x * scale + x_offset,
            height - y_offset - (y * scale),
        )

    def draw_borders(self) -> None:
        """Draw the borders onto a pygame screen to frame the coordinate system"""
        _, width, height, x_offset, y_offset = self._update_dimensions()

        if x_offset:
            # Draw the borders to the right and left
            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0, 0, x_offset, height),
            )

            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (width - x_offset, 0, x_offset, height),
            )

        else:
            # Draw the borders to the top and bottom
            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0, 0, width, y_offset),
            )

            pygame.draw.rect(
                self.display,
                (0, 0, 0),
                (0, height - y_offset, width, y_offset),
            )


class Vector(Sequence[float]):
    """A two-dimensional dynamic vector"""

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

    def __mul__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other)
        raise ValueError(
            f"Can only multiply scalar (int, float) with vector, not {type(other)}"
        )

    def __rmul__(self, scalar: Any) -> Vector:
        return self.__mul__(scalar)

    def __div__(self, other: Any) -> Vector:
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other)
        raise ValueError(f"Can divide vector only by scalar, not {type(other)}")

    def __truediv__(self, other: Any) -> Vector:
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
        float
            The magnitude of the vector
        """
        return (self.x**2 + self.y**2) ** 0.5
