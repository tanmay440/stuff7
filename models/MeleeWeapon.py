from __future__ import annotations

import pygame as pg

from models.MeleeHitbox import MeleeHitbox
from models.templates.Weapon import Weapon


class MeleeWeapon(Weapon):
    """
    Create short-lived hitboxes in front of the attacker.

    Summary:
        `MeleeWeapon` creates a temporary `MeleeHitbox` positioned along the
        attacker's direction.

    Attributes:
        effect_img (pg.Surface | None): Optional hitbox-effect image.
        reach (float): Distance to the hitbox center.
        duration (float): Hitbox lifetime in seconds.

    Methods:
        attack: Create a hitbox when the cooldown has expired.

    Example:
        >>> weapon = MeleeWeapon(None, effect_image, 15, 0.6, 50, 0.2)
        >>> hitbox = weapon.attack(origin, direction, "ENEMY")
    """

    def __init__(
        self,
        image: pg.Surface | None,
        effect_img: pg.Surface | None,
        damage: float,
        cooldown: float,
        reach: float,
        duration: float,
    ) -> None:
        """
        Initialize a melee weapon.

        Args:
            image: Optional weapon image.
            effect_img: Optional attack-effect image.
            damage: Damage dealt by each hit.
            cooldown: Minimum time between attacks in seconds.
            reach: Distance from the attacker to the hitbox center.
            duration: Hitbox lifetime in seconds.
        """
        super().__init__(image, damage, cooldown)
        self.effect_img = effect_img
        self.reach = reach
        self.duration = duration

    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> MeleeHitbox | None:
        """
        Create a melee hitbox when the weapon is ready.

        Args:
            spawn_pos: Attacker's world position.
            dir: Attack direction.
            team: Team identifier assigned to the hitbox.
        Returns:
            A new melee hitbox, or `None` while cooling down.
        """
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
