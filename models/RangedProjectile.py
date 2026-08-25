from __future__ import annotations

import pygame as pg

from models.templates.Entity import Entity


class RangedProjectile(Entity):

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
        super().__init__(image, pos)
        self.direction = direction
        self.velocity = direction * speed
        self.damage = damage
        self.team = team
        self.lifetime = lifetime
        self.has_collided = False
        self._rotated_image = self._build_rotated_image(image)

    def _build_rotated_image(self, image: pg.Surface | None) -> pg.Surface | None:
        if image is None:
            return None
        angle = self.direction.as_polar()[1]
        return pg.transform.rotate(image, -angle - 90)

    def update(self, dt: float) -> None:
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.lifetime -= dt

    def is_alive(self) -> bool:
        return self.lifetime > 0 and not self.has_collided

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        if self._rotated_image is None:
            return
        rect = self._rotated_image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        super().draw(surface, camera_offset, image_override=self._rotated_image, rect_override=rect)
