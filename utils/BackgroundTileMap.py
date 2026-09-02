from __future__ import annotations

import pygame as pg


class BackgroundTileMap:
    """
    Tile a surface across the visible game viewport.

    Summary:
        `BackgroundTileMap` repeats one tile image across the display and
        offsets the pattern to follow the camera.

    Attributes:
        tile_image (pg.Surface): Surface repeated across the background.
        tile_w (int): Tile width in pixels.
        tile_h (int): Tile height in pixels.

    Methods:
        draw: Fill a surface with tiles aligned to the camera offset.

    Example:
        >>> tile_map = BackgroundTileMap(tile_image)
        >>> tile_map.draw(screen, camera_offset)
    """

    def __init__(self, tile_image: pg.Surface) -> None:
        """
        Initialize a tile map from one tile image.

        Args:
            tile_image: Surface repeated across the background.
        """
        self.tile_image = tile_image
        self.tile_w, self.tile_h = tile_image.get_size()

    def draw(self, surface: pg.Surface, camera_offset: pg.math.Vector2) -> None:
        """
        Draw enough tiles to cover the destination surface.

        Args:
            surface: Destination game surface.
            camera_offset: Translation used to align the background.
        """
        start_x = -((-camera_offset.x) % self.tile_w)
        start_y = -((-camera_offset.y) % self.tile_h)
        for x in range(int(start_x), surface.get_width(), self.tile_w):
            for y in range(int(start_y), surface.get_height(), self.tile_h):
                surface.blit(self.tile_image, (x, y))
