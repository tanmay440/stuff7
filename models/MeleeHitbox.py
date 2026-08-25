from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Entity import Entity

if TYPE_CHECKING:
    from models.templates.Creature import Creature


class MeleeHitbox(Entity):

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        size: float,
        lifetime: float,
        team: str,
        damage: float,
    ) -> None:
        super().__init__(image, pos)
        self.rect = pg.Rect(0, 0, int(size), int(size))
        self.rect.center = (int(pos.x), int(pos.y))
        self.lifetime = lifetime
        self.team = team
        self.damage = damage
        self.hit_creatures: set[Creature] = set()

    def update(self, dt: float) -> None:
        self.lifetime -= dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def is_alive(self) -> bool:
        return self.lifetime > 0

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        if self.image is None:
            return
        image_rect = self.image.get_rect(center=self.rect.center)
        super().draw(surface, camera_offset, image_override=self.image, rect_override=image_rect)
