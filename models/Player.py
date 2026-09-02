from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Creature import Creature

if TYPE_CHECKING:
    from models.MeleeHitbox import MeleeHitbox
    from models.RangedProjectile import RangedProjectile
    from models.templates.Weapon import Weapon

FIRE_KEYS = (pg.K_SPACE, pg.K_z, pg.K_x, pg.K_c)


class Player(Creature):
    """
    Represent the player character and keyboard-driven controls.

    Summary:
        The player uses keyboard input for normalized movement and attacks in
        its current facing direction. It inherits health, movement, rendering,
        and weapon behavior from `Creature`.

    Attributes:
        FIRE_KEYS (tuple[int, ...]): Keyboard keys accepted for firing.

    Methods:
        handle_input: Convert keyboard state into movement and an attack.

    Example:
        >>> player = Player(sprite, pg.math.Vector2(400, 300), weapon)
        >>> attack = player.handle_input(pg.key.get_pressed(), 1 / 60)
    """

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        weapon: Weapon | None = None,
    ) -> None:
        """
        Initialize the player with default player statistics.

        Args:
            image: Optional player sprite.
            pos: Initial world position.
            weapon: Optional starting weapon.
        """
        super().__init__(
            image, pos, health=100.0, max_health=100.0, team="PLAYER", move_speed=300.0, weapon=weapon
        )

    def handle_input(self, keys, dt: float) -> RangedProjectile | MeleeHitbox | None:
        """
        Convert keyboard state into movement and an optional attack.

        Args:
            keys: Pygame keyboard state sequence.
            dt: Frame duration retained for the input interface.
        Returns:
            A new attack entity, or `None` when no attack is fired.
        """
        direction = pg.math.Vector2(0, 0)
        if keys[pg.K_w] or keys[pg.K_UP]:
            direction.y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            direction.y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction.x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction.x += 1
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.velocity = direction * self.move_speed
        self.set_facing(direction)
        if any(keys[key] for key in FIRE_KEYS):
            return self.perform_attack(self.facing_dir)
        return None
