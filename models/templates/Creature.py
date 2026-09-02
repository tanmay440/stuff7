from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from models.templates.Entity import Entity

if TYPE_CHECKING:
    from models.MeleeHitbox import MeleeHitbox
    from models.RangedProjectile import RangedProjectile
    from models.templates.Weapon import Weapon


class Creature(Entity):
    """
    Represent a character that can move, take damage, and attack.

    Summary:
        `Creature` centralizes behavior shared by player-controlled and
        computer-controlled characters, including movement, health management,
        facing direction, sprite rotation, and weapon attacks.

    Attributes:
        health (float): Current health value.
        max_health (float): Maximum health value.
        team (str): Team identifier used for collision filtering.
        move_speed (float): Movement speed in world units per second.
        velocity (pg.math.Vector2): Current movement velocity.
        weapon (Weapon | None): Optional equipped weapon.
        facing_dir (pg.math.Vector2): Normalized facing direction.

    Methods:
        set_facing: Update the facing direction and rotated sprite.
        update: Move the creature and update its weapon cooldown.
        is_alive: Report whether health is positive.
        take_damage: Reduce health without going below zero.
        perform_attack: Request an attack from the equipped weapon.
        draw: Render the creature using its rotated sprite.

    Example:
        >>> creature = Creature(sprite, pg.math.Vector2(200, 150), 100, 100,
        ...                     "PLAYER", 300)
        >>> creature.set_facing(pg.math.Vector2(1, 0))
        >>> creature.update(1 / 60)
    """

    def __init__(
        self,
        image: pg.Surface | None,
        pos: pg.math.Vector2,
        health: float,
        max_health: float,
        team: str,
        move_speed: float,
        weapon: Weapon | None = None,
    ) -> None:
        """
        Initialize a creature.

        Args:
            image: Optional creature sprite.
            pos: Initial world position.
            health: Starting health.
            max_health: Maximum health.
            team: Team identifier used for collision filtering.
            move_speed: Movement speed in world units per second.
            weapon: Optional equipped weapon.
        """
        super().__init__(image, pos)
        self.health = health
        self.max_health = max_health
        self.team = team
        self.move_speed = move_speed
        self.velocity = pg.math.Vector2(0, 0)
        self.weapon = weapon
        self.facing_dir = pg.math.Vector2(0, 1)
        self._rotated_image = self._build_rotated_image(image, self.facing_dir) if image is not None else None

    def _build_rotated_image(self, image: pg.Surface, direction: pg.math.Vector2) -> pg.Surface:
        """
        Rotate an image to face a direction.

        Args:
            image: Source image.
            direction: Facing direction.
        Returns:
            Rotated image.
        """
        angle = direction.as_polar()[1]
        return pg.transform.rotate(image, -angle - 90)

    def set_facing(self, direction: pg.math.Vector2) -> None:
        """
        Update the creature's facing direction and sprite.

        Args:
            direction: New facing direction.
        """
        if direction.length_squared() == 0:
            return
        self.facing_dir = direction.normalize()
        if self.image is not None:
            self._rotated_image = self._build_rotated_image(self.image, self.facing_dir)

    def update(self, dt: float) -> None:
        """
        Move the creature and update its weapon.

        Args:
            dt: Elapsed time in seconds.
        """
        self.pos += self.velocity * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.weapon is not None:
            self.weapon.update(dt)

    def is_alive(self) -> bool:
        """
        Check whether the creature has positive health.

        Returns:
            `True` when the creature is alive.
        """
        return self.health > 0

    def take_damage(self, amount: float) -> None:
        """
        Reduce health without allowing it to become negative.

        Args:
            amount: Damage to apply.
        """
        self.health = max(0.0, self.health - amount)

    def perform_attack(self, dir: pg.math.Vector2) -> RangedProjectile | MeleeHitbox | None:
        """
        Request an attack from the equipped weapon.

        Args:
            dir: Attack direction.
        Returns:
            A new attack entity, or `None` if unavailable.
        """
        if self.weapon is None:
            return None
        return self.weapon.attack(self.pos, dir, self.team)

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        """
        Draw the creature using its rotated image.

        Args:
            surface: Destination surface.
            camera_offset: World-to-screen translation.
        """
        if self.image is None:
            return
        img = self._rotated_image if self._rotated_image is not None else self.image
        rect = img.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        super().draw(surface, camera_offset, image_override=img, rect_override=rect)
