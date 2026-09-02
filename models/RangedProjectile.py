from __future__ import annotations

import pygame as pg

from models.templates.Entity import Entity


class RangedProjectile(Entity):
    """
    Represent a moving, temporary projectile that hits one target.

    Summary:
        `RangedProjectile` travels in a fixed direction until its lifetime
        expires or collision handling marks it as collided.

    Attributes:
        direction (pg.math.Vector2): Normalized travel direction.
        velocity (pg.math.Vector2): Projectile movement velocity.
        damage (float): Damage dealt on collision.
        team (str): Team identifier used for collision filtering.
        lifetime (float): Remaining active duration in seconds.
        has_collided (bool): Whether the projectile has hit a creature.

    Methods:
        update: Move the projectile and reduce its lifetime.
        is_alive: Report whether the projectile remains active.
        draw: Render the direction-adjusted projectile.

    Example:
        >>> projectile = RangedProjectile(image, origin, direction, 600, 10,
        ...                               "PLAYER", 3)
        >>> projectile.update(1 / 60)
    """

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        direction: pg.math.Vector2,
        speed: float,
        damage: float,
        team: str,
        lifetime: float,
    ) -> None:
        """
        Initialize a projectile.

        Args:
            image: Optional projectile sprite.
            pos: Starting world position.
            direction: Travel direction.
            speed: Travel speed in world units per second.
            damage: Damage dealt on collision.
            team: Team identifier used for collision filtering.
            lifetime: Maximum active duration in seconds.
        """
        super().__init__(image, pos)
        self.direction = direction
        self.velocity = direction * speed
        self.damage = damage
        self.team = team
        self.lifetime = lifetime
        self.has_collided = False
        self._rotated_image = self._build_rotated_image(image)

    def _build_rotated_image(self, image: pg.Surface | None) -> pg.Surface | None:
        """
        Rotate the projectile image to match its direction.

        Args:
            image: Optional source image.
        Returns:
            Rotated image, or `None` when no image is supplied.
        """
        if image is None:
            return None
        angle = self.direction.as_polar()[1]
        return pg.transform.rotate(image, -angle - 90)

    def update(self, dt: float) -> None:
        """
        Move the projectile and reduce its lifetime.

        Args:
            dt: Elapsed time in seconds.
        """
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.lifetime -= dt

    def is_alive(self) -> bool:
        """
        Check whether the projectile remains active.

        Returns:
            `True` while lifetime remains and no collision occurred.
        """
        return self.lifetime > 0 and not self.has_collided

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        """
        Draw the rotated projectile image.

        Args:
            surface: Destination surface.
            camera_offset: World-to-screen translation.
        """
        if self._rotated_image is None:
            return
        rect = self._rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        super().draw(surface, camera_offset, image_override=self._rotated_image, rect_override=rect)
