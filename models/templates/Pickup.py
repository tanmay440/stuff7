from __future__ import annotations

import pygame as pg

from models.templates.Entity import Entity


class Pickup(Entity):
    """
    Represent an entity that remains active until collected.

    Summary:
        `Pickup` provides the lifecycle behavior shared by collectible items.
        Concrete subclasses define what happens when a creature collects them.

    Attributes:
        is_collected (bool): Whether the pickup has already been collected.

    Methods:
        update: Advance the pickup state.
        is_alive: Report whether the pickup is still available.

    Example:
        >>> pickup = ConcretePickup(icon, pg.math.Vector2(300, 200))
        >>> pickup.is_alive()
        True
    """

    def __init__(self, image: pg.Surface | None, pos: pg.math.Vector2) -> None:
        """
        Initialize an uncollected pickup.

        Args:
            image: Optional pickup image.
            pos: World position.
        """
        super().__init__(image, pos)
        self.is_collected = False

    def update(self, dt: float) -> None:
        """
        Update the pickup.

        Args:
            dt: Elapsed time in seconds.
        """
        pass

    def is_alive(self) -> bool:
        """
        Check whether the pickup is still available.

        Returns:
            `True` when the pickup has not been collected.
        """
        return not self.is_collected
