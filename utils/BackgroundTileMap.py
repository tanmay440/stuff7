from __future__ import annotations

import pygame as pg


class BackgroundTileMap:

    def __init__(self, tile_image: pg.Surface) -> None:
        self.tile_image = tile_image
        self.tile_w, self.tile_h = tile_image.get_size()

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        start_x = -((-camera_offset.x) % self.tile_w)
        start_y = -((-camera_offset.y) % self.tile_h)
        for x in range(int(start_x), surface.get_width(), self.tile_w):
            for y in range(int(start_y), surface.get_height(), self.tile_h):
                surface.blit(self.tile_image, (x, y))
