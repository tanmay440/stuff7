from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Pickup import Pickup

if TYPE_CHECKING:
    from models.templates.Creature import Creature


class PowerupPickup(Pickup):

    def __init__(
        self, image: pg.Surface | None, pos: pg.math.Vector2, stat_type: str, boost_amount: float
    ) -> None:
        super().__init__(image, pos)
        self.stat_type = stat_type
        self.boost_amount = boost_amount

    def apply_effect(self, creature: Creature) -> None:
        if self.stat_type == "HEALTH":
            creature.max_health += self.boost_amount
            creature.health = min(creature.health + self.boost_amount, creature.max_health)
        elif self.stat_type == "SPEED":
            creature.move_speed += self.boost_amount
        elif self.stat_type == "DAMAGE":
            if creature.weapon is not None:
                creature.weapon.damage += self.boost_amount
        self.is_collected = True
