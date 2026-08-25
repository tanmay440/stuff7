from __future__ import annotations

from abc import ABC, abstractmethod

import pygame as pg


class Entity(ABC):

    def __init__(self, image: pg.Surface | None, pos: pg.math.Vector2) -> None:
        self.image = image
        self.pos = pg.math.Vector2(pos)
        self.spawn_pos = pg.math.Vector2(pos)
        if image is not None:
            self.rect = image.get_rect(center=(int(pos.x), int(pos.y)))
        else:
            self.rect = pg.Rect(int(pos.x), int(pos.y), 0, 0)

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        raise NotImplementedError

    def draw(
        self,
        surface: pg.Surface,
        camera_offset: pg.math.Vector2,
        image_override: pg.Surface | None = None,
        rect_override: pg.Rect | None = None,
    ) -> None:
        img = image_override if image_override is not None else self.image
        if img is None:
            return
        base_rect = rect_override if rect_override is not None else self.rect
        screen_rect = base_rect.move(camera_offset)
        if surface.get_rect().colliderect(screen_rect):
            surface.blit(img, screen_rect)
