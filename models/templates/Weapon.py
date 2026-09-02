from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from models.templates.Entity import Entity


class Weapon(ABC):
    """
    Define the interface and shared cooldown state for game weapons.

    Summary:
        `Weapon` is an abstract attack factory. Subclasses implement the
        concrete attack entity they create, while this class manages common
        damage, imagery, and time-between-attacks behavior.

    Attributes:
        image (pg.Surface | None): Optional weapon image.
        damage (float): Damage dealt by attacks.
        cooldown (float): Minimum time between attacks in seconds.
        timer (float): Remaining cooldown time in seconds.

    Methods:
        update: Reduce the remaining cooldown.
        attack: Create an attack entity when implemented by a subclass.

    Example:
        >>> weapon = ConcreteWeapon(None, damage=10, cooldown=0.25)
        >>> weapon.update(0.25)
        >>> attack = weapon.attack(origin, direction, "PLAYER")
    """

    def __init__(self, image: pg.Surface | None, damage: float, cooldown: float) -> None:
        """
        Initialize a weapon.

        Args:
            image: Optional weapon image.
            damage: Damage dealt by attacks.
            cooldown: Minimum time between attacks in seconds.
        """
        self.image = image
        self.damage = damage
        self.cooldown = cooldown
        self.timer = 0.0

    def update(self, dt: float) -> None:
        """
        Reduce the remaining attack cooldown.

        Args:
            dt: Elapsed time in seconds.
        """
        self.timer = max(0.0, self.timer - dt)

    @abstractmethod
    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> Entity | None:
        """
        Create an attack entity.

        Args:
            spawn_pos: Attack origin in world coordinates.
            dir: Attack direction.
            team: Team assigned to the attack.
        Returns:
            A new attack entity, or `None` while cooling down.
        """
        raise NotImplementedError
