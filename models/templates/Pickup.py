from __future__ import annotations

import pygame as pg

from models.templates.Entity import Entity


class Pickup(Entity):

    def __init__(self, image: pg.Surface | None, pos: pg.math.Vector2) -> None:
        super().__init__(image, pos)
        self.is_collected = False

    def update(self, dt: float) -> None:
        pass

    def is_alive(self) -> bool:
        return not self.is_collected
