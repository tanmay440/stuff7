from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Pickup import Pickup

if TYPE_CHECKING:
    from models.templates.Creature import Creature
    from models.templates.Weapon import Weapon


class WeaponPickup(Pickup):
    """
    Replace a creature's weapon when collected.

    Summary:
        `WeaponPickup` stores a weapon in the world until a creature collects
        it, then assigns that weapon to the creature.

    Attributes:
        stored_weapon (Weapon): Weapon assigned to the collecting creature.

    Methods:
        collect: Equip the stored weapon and consume the pickup.

    Example:
        >>> pickup = WeaponPickup(icon, pg.math.Vector2(250, 450), weapon)
        >>> pickup.collect(player)
    """

    def __init__(
        self, image: pg.Surface | None, pos: pg.math.Vector2, stored_weapon: Weapon
    ) -> None:
        """
        Initialize a weapon pickup.

        Args:
            image: Optional pickup image.
            pos: World position of the pickup.
            stored_weapon: Weapon assigned to the collecting creature.
        """
        super().__init__(image, pos)
        self.stored_weapon = stored_weapon

    def collect(self, creature: Creature) -> None:
        """
        Equip the stored weapon and mark this pickup collected.

        Args:
            creature: Creature receiving the stored weapon.
        """
        creature.weapon = self.stored_weapon
        self.is_collected = True
