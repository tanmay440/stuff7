from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from models.templates.Entity import Entity


class Weapon(ABC):

    def __init__(self, image: pg.Surface | None, damage: float, cooldown: float) -> None:
        self.image = image
        self.damage = damage
        self.cooldown = cooldown
        self.timer = 0.0

    def update(self, dt: float) -> None:
        self.timer = max(0.0, self.timer - dt)

    @abstractmethod
    def attack(
        self, spawn_pos: pg.math.Vector2, dir: pg.math.Vector2, team: str
    ) -> Entity | None:
        raise NotImplementedError
