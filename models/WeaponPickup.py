from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Pickup import Pickup

if TYPE_CHECKING:
    from models.templates.Creature import Creature
    from models.templates.Weapon import Weapon


class WeaponPickup(Pickup):

    def __init__(
        self, image: pg.Surface | None, pos: pg.math.Vector2, stored_weapon: Weapon
    ) -> None:
        super().__init__(image, pos)
        self.stored_weapon = stored_weapon

    def collect(self, creature: Creature) -> None:
        creature.weapon = self.stored_weapon
        self.is_collected = True
