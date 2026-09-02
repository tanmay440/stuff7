from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Entity import Entity

if TYPE_CHECKING:
    from models.templates.Creature import Creature


class MeleeHitbox(Entity):
    """
    Represent a stationary area attack that can hit each creature once.

    Summary:
        `MeleeHitbox` models the temporary area of effect created by a melee
        weapon and records creatures already damaged by the attack.

    Attributes:
        lifetime (float): Remaining active duration in seconds.
        team (str): Team identifier used for collision filtering.
        damage (float): Damage dealt to each creature hit.
        hit_creatures (set[Creature]): Creatures already damaged.

    Methods:
        update: Reduce the hitbox lifetime and synchronize its rectangle.
        is_alive: Report whether the hitbox remains active.
        draw: Render the melee effect.

    Example:
        >>> hitbox = MeleeHitbox(effect, origin, 50, 0.2, "ENEMY", 15)
        >>> hitbox.update(1 / 60)
    """

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        size: float,
        lifetime: float,
        team: str,
        damage: float,
    ) -> None:
        """
        Initialize a melee hitbox.

        Args:
            image: Optional attack-effect image.
            pos: Center position of the hitbox.
            size: Width and height of the square hitbox.
            lifetime: Active duration in seconds.
            team: Team identifier used for collision filtering.
            damage: Damage dealt to each creature hit.
        """
        super().__init__(image, pos)
        self.rect = pg.Rect(0, 0, int(size), int(size))
        self.rect.center = (int(pos.x), int(pos.y))
        self.lifetime = lifetime
        self.team = team
        self.damage = damage
        self.hit_creatures: set[Creature] = set()

    def update(self, dt: float) -> None:
        """
        Reduce the hitbox lifetime and keep its rectangle centered.

        Args:
            dt: Elapsed time in seconds.
        """
        self.lifetime -= dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def is_alive(self) -> bool:
        """
        Check whether the melee hitbox remains active.

        Returns:
            `True` while the hitbox lifetime is positive.
        """
        return self.lifetime > 0

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        """
        Draw the melee effect image centered on the hitbox.

        Args:
            surface: Destination surface.
            camera_offset: World-to-screen translation.
        """
        if self.image is None:
            return
        image_rect = self.image.get_rect(center=self.rect.center)
        super().draw(surface, camera_offset, image_override=self.image, rect_override=image_rect)
