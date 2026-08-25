from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Entity import Entity

if TYPE_CHECKING:
    from models.MeleeHitbox import MeleeHitbox
    from models.RangedProjectile import RangedProjectile
    from models.templates.Weapon import Weapon


class Creature(Entity):

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        health: float,
        max_health: float,
        team: str,
        move_speed: float,
        weapon: Weapon | None = None,
    ) -> None:
        super().__init__(image, pos)
        self.health = health
        self.max_health = max_health
        self.team = team
        self.move_speed = move_speed
        self.velocity = pg.math.Vector2(0, 0)
        self.weapon = weapon
        self.facing_dir = pg.math.Vector2(0, 1)
        self._rotated_image = self._build_rotated_image(image, self.facing_dir) if image is not None else None

    def _build_rotated_image(self, image: pg.Surface, direction: pg.math.Vector2) -> pg.Surface:
        angle = direction.as_polar()[1]
        return pg.transform.rotate(image, -angle - 90)

    def set_facing(self, direction: pg.math.Vector2) -> None:
        if direction.length_squared() == 0:
            return
        self.facing_dir = direction.normalize()
        if self.image is not None:
            self._rotated_image = self._build_rotated_image(self.image, self.facing_dir)

    def update(self, dt: float) -> None:
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.weapon is not None:
            self.weapon.update(dt)

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: float) -> None:
        self.health = max(0.0, self.health - amount)

    def perform_attack(self, dir: pg.math.Vector2) -> RangedProjectile | MeleeHitbox | None:
        if self.weapon is None:
            return None
        return self.weapon.attack(self.pos, dir, self.team)

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        if self.image is None:
            return
        img = self._rotated_image if self._rotated_image is not None else self.image
        rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        super().draw(surface, camera_offset, image_override=img, rect_override=rect)
