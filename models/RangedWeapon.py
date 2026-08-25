from __future__ import annotations

import pygame as pg

from models.RangedProjectile import RangedProjectile
from models.templates.Weapon import Weapon


class RangedWeapon(Weapon):

    def __init__(
        self,
        image: pg.Surface | None,
        projectile_img: pg.Surface | None,
        damage: float,
        cooldown: float,
        velocity: float,
        lifetime: float = 3.0,
    ) -> None:
        super().__init__(image, damage, cooldown)
        self.projectile_img = projectile_img
        self.velocity = velocity
        self.lifetime = lifetime

    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> RangedProjectile | None:
        if self.timer > 0:
            return None
        self.timer = self.cooldown
        direction = dir.normalize() if dir.length_squared() > 0 else pg.math.Vector2(0, -1)
        return RangedProjectile(
            image=self.projectile_img,
            pos=spawn_pos,
            direction=direction,
            speed=self.velocity,
            damage=self.damage,
            team=team,
            lifetime=self.lifetime,
        )
