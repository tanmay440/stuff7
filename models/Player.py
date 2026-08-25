from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Creature import Creature

if TYPE_CHECKING:
    from models.MeleeHitbox import MeleeHitbox
    from models.RangedProjectile import RangedProjectile
    from models.templates.Weapon import Weapon

FIRE_KEYS = (pg.K_SPACE, pg.K_z, pg.K_x, pg.K_c)


class Player(Creature):

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        weapon: Weapon | None = None,
    ) -> None:
        super().__init__(
            image, pos, health=100.0, max_health=100.0, team="PLAYER", move_speed=300.0, weapon=weapon
        )

    def handle_input(self, keys, dt: float) -> RangedProjectile | MeleeHitbox | None:
        direction = pg.math.Vector2(0, 0)
        if keys[pg.K_w] or keys[pg.K_UP]:
            direction.y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            direction.y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction.x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction.x += 1
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * self.move_speed
        self.set_facing(direction)
        if any(keys[key] for key in FIRE_KEYS):
            return self.perform_attack(self.facing_dir)
        return None
