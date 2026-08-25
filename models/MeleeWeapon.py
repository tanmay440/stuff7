from __future__ import annotations

import pygame as pg

from models.MeleeHitbox import MeleeHitbox
from models.templates.Weapon import Weapon


class MeleeWeapon(Weapon):

    def __init__(
        self,
        image: pg.Surface | None,
        effect_img: pg.Surface | None,
        damage: float,
        cooldown: float,
        reach: float,
        duration: float,
    ) -> None:
        super().__init__(image, damage, cooldown)
        self.effect_img = effect_img
        self.reach = reach
        self.duration = duration

    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> MeleeHitbox | None:
        if self.timer > 0:
            return None
        self.timer = self.cooldown
        direction = dir.normalize() if dir.length_squared() > 0 else pg.math.Vector2(0, -1)
        hitbox_pos = spawn_pos + direction * self.reach
        return MeleeHitbox(
            image=self.effect_img,
            pos=hitbox_pos,
            size=self.reach,
            lifetime=self.duration,
            team=team,
            damage=self.damage,
        )
