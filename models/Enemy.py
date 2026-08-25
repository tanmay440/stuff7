from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.MeleeWeapon import MeleeWeapon
from models.RangedWeapon import RangedWeapon
from models.templates.Creature import Creature

if TYPE_CHECKING:
    from models.MeleeHitbox import MeleeHitbox
    from models.RangedProjectile import RangedProjectile
    from models.templates.Weapon import Weapon


class Enemy(Creature):

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        weapon: Weapon | None = None,
        target: Creature | None = None,
        attack_range: float | None = None,
    ) -> None:
        super().__init__(
            image, pos, health=40.0, max_health=40.0, team="ENEMY", move_speed=120.0, weapon=weapon
        )
        self.target = target
        self.attack_range = self._resolve_attack_range(attack_range)

    def _resolve_attack_range(self, attack_range: float | None) -> float:
        if attack_range is not None:
            return attack_range
        if isinstance(self.weapon, MeleeWeapon):
            return self.weapon.reach
        if isinstance(self.weapon, RangedWeapon):
            return 300.0
        return 50.0

    def ai_step(self, dt: float) -> RangedProjectile | MeleeHitbox | None:
        if self.target is None:
            self.velocity = pg.math.Vector2(0, 0)
            return None
        to_target = self.target.pos - self.pos
        distance = to_target.length()
        direction = to_target.normalize() if distance > 0 else pg.math.Vector2(0, 1)
        self.set_facing(direction)
        if distance > self.attack_range:
            self.velocity = direction * self.move_speed
            return None
        self.velocity = pg.math.Vector2(0, 0)
        return self.perform_attack(direction)
