from __future__ import annotations

from abc import ABC, abstractmethod

import pygame as pg


class Entity(ABC):
    """
    Provide the common interface for drawable, updateable game objects.

    Summary:
        `Entity` stores an object's visual representation and world-space
        position. Subclasses implement their own lifecycle state and update
        behavior, while this class supplies shared camera-aware rendering.

    Attributes:
        image (pg.Surface | None): Optional image used when drawing.
        pos (pg.math.Vector2): Current position in world coordinates.
        spawn_pos (pg.math.Vector2): Position where the entity was created.
        rect (pg.Rect): Collision and drawing rectangle.

    Methods:
        update: Advance the entity by one time step.
        is_alive: Report whether the entity remains active.
        draw: Render the entity with a camera offset.

    Example:
        >>> entity = ConcreteEntity(image, pg.math.Vector2(100, 100))
        >>> entity.update(1 / 60)
        >>> entity.draw(screen, camera_offset)
    """

    def __init__(self, image: pg.Surface | None, pos: pg.math.Vector2) -> None:
        """
        Initialize an entity at a world position.

        Args:
            image: Optional image used for the entity.
            pos: Initial world position of the entity.
        """
        self.image = image
        self.pos = pg.math.Vector2(pos)
        self.spawn_pos = pg.math.Vector2(pos)
        if image is not None:
            self.rect = image.get_rect(center=(int(pos.x), int(pos.y)))
        else:
            self.rect = pg.Rect(int(pos.x), int(pos.y), 0, 0)

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Advance the entity state by one time step.

        Args:
            dt: Elapsed time in seconds.
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Determine whether the entity should remain active.

        Returns:
            `True` when the entity is active; otherwise `False`.
        """
        raise NotImplementedError

    def draw(
        self,
        surface: pg.Surface,
        camera_offset: pg.math.Vector2,
        image_override: pg.Surface | None = None,
        rect_override: pg.Rect | None = None,
    ) -> None:
        """
        Draw the entity after applying a camera offset.

        Args:
            surface: Destination surface.
            camera_offset: Translation from world to screen coordinates.
            image_override: Optional image to draw instead of `self.image`.
            rect_override: Optional rectangle to use instead of `self.rect`.
        """
        img = image_override if image_override is not None else self.image
        if img is None:
            return
        base_rect = rect_override if rect_override is not None else self.rect
        screen_rect = base_rect.move(camera_offset)
        if surface.get_rect().colliderect(screen_rect):
            surface.blit(img, screen_rect)
