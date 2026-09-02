from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Pickup import Pickup

if TYPE_CHECKING:
    from models.templates.Creature import Creature


class PowerupPickup(Pickup):
    """
    Apply a health, speed, or damage enhancement when collected.

    Summary:
        `PowerupPickup` applies one configured stat increase to a creature and
        then marks itself as collected.

    Attributes:
        stat_type (str): Name of the statistic to enhance.
        boost_amount (float): Amount added to the selected statistic.

    Methods:
        apply_effect: Apply the configured enhancement and consume the pickup.

    Example:
        >>> pickup = PowerupPickup(icon, pg.math.Vector2(550, 450),
        ...                        "HEALTH", 25)
        >>> pickup.apply_effect(player)
    """

    def __init__(
        self, image: pg.Surface | None, pos: pg.math.Vector2, stat_type: str, boost_amount: float
    ) -> None:
        """
        Initialize a stat powerup.

        Args:
            image: Optional pickup image.
            pos: World position of the pickup.
            stat_type: Name of the statistic to enhance.
            boost_amount: Amount added to the selected statistic.
        """
        super().__init__(image, pos)
        self.stat_type = stat_type
        self.boost_amount = boost_amount

    def apply_effect(self, creature: Creature) -> None:
        """
        Apply the configured stat increase and collect the powerup.

        Args:
            creature: Creature receiving the stat increase.
        """
        if self.stat_type == "HEALTH":
            creature.max_health += self.boost_amount
            creature.health = min(creature.health + self.boost_amount, creature.max_health)
        elif self.stat_type == "SPEED":
            creature.move_speed += self.boost_amount
        elif self.stat_type == "DAMAGE":
            if creature.weapon is not None:
                creature.weapon.damage += self.boost_amount
        self.is_collected = True
