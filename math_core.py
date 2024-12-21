"""Math utilities used for the physical simulation"""

from typing import Tuple
import pygame


class CoordSys:
    """Apply a custom coordinate system to a pygame screen"""

    def __init__(self, display: pygame.Surface) -> None:
        self.display = display
        self.x_tot: int = 1500
        self.y_tot: int = 1000

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
