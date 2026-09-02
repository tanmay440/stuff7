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
    """
    Represent an enemy that approaches and attacks a target.

    Summary:
        `Enemy` uses a target creature to determine its movement, facing
        direction, and attack decisions.

    Attributes:
        target (Creature | None): Creature pursued and attacked by the enemy.
        attack_range (float): Distance within which the enemy attacks.

    Methods:
        ai_step: Move toward the target and attack when within range.

    Example:
        >>> enemy = Enemy(enemy_sprite, pg.math.Vector2(200, 200),
        ...               weapon=weapon, target=player)
        >>> attack = enemy.ai_step(1 / 60)
    """

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        weapon: Weapon | None = None,
        target: Creature | None = None,
        attack_range: float | None = None,
    ) -> None:
        """
        Initialize an enemy with default enemy statistics.

        Args:
            image: Optional enemy sprite.
            pos: Initial world position.
            weapon: Optional enemy weapon.
            target: Creature pursued by the enemy.
            attack_range: Optional attack range override.
        """
        super().__init__(
            image, pos, health=40.0, max_health=40.0, team="ENEMY", move_speed=120.0, weapon=weapon
        )
        self.target = target
        self.attack_range = self._resolve_attack_range(attack_range)

    def _resolve_attack_range(self, attack_range: float | None) -> float:
        """
        Determine the effective attack range.

        Args:
            attack_range: Explicit range override, if supplied.
        Returns:
            The configured or weapon-derived attack range.
        """
        if attack_range is not None:
            return attack_range
        if isinstance(self.weapon, MeleeWeapon):
            return self.weapon.reach
        if isinstance(self.weapon, RangedWeapon):
            return 300.0
        return 50.0

    def ai_step(self, dt: float) -> RangedProjectile | MeleeHitbox | None:
        """
        Move toward the target and attack when within range.

        Args:
            dt: Frame duration retained for the AI interface.
        Returns:
            A new attack entity, or `None` when no attack occurs.
        """
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
