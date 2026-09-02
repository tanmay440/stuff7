from __future__ import annotations

import pygame as pg

from models.RangedProjectile import RangedProjectile
from models.templates.Weapon import Weapon


class RangedWeapon(Weapon):
    """
    Create moving projectile attacks.

    Summary:
        `RangedWeapon` creates `RangedProjectile` instances when its shared
        cooldown timer allows another shot.

    Attributes:
        projectile_img (pg.Surface | None): Optional projectile image.
        velocity (float): Projectile speed in world units per second.
        lifetime (float): Projectile lifetime in seconds.

    Methods:
        attack: Create a projectile when the cooldown has expired.

    Example:
        >>> weapon = RangedWeapon(None, projectile_image, 10, 0.25, 600)
        >>> projectile = weapon.attack(origin, direction, "PLAYER")
    """

    def __init__(
        self,
        image: pg.Surface | None,
        projectile_img: pg.Surface | None,
        damage: float,
        cooldown: float,
        velocity: float,
        lifetime: float = 3.0,
    ) -> None:
        """
        Initialize a ranged weapon.

        Args:
            image: Optional weapon image.
            projectile_img: Optional projectile image.
            damage: Projectile damage.
            cooldown: Minimum time between shots in seconds.
            velocity: Projectile speed in world units per second.
            lifetime: Projectile lifetime in seconds.
        """
        super().__init__(image, damage, cooldown)
        self.projectile_img = projectile_img
        self.velocity = velocity
        self.lifetime = lifetime

    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> RangedProjectile | None:
        """
        Fire a projectile when the weapon is ready.

        Args:
            spawn_pos: Projectile starting world position.
            dir: Projectile travel direction.
            team: Team identifier assigned to the projectile.
        Returns:
            A new projectile, or `None` while cooling down.
        """
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
