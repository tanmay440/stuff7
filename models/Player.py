from .FacingDir import FacingDir
from .Vector2 import Vector2
import pygame as pg
class Player:
    def __init__(self, image, velocity=15):
        self.image = image
        self.velocity = velocity
        self.rect = self.image.get_rect(center=(400, 300))
        self.facing_dir = FacingDir(Vector2(0, 0))
        self.weapon = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, direction: Vector2):
        self.rect.x += direction.x * self.velocity
        self.rect.y += direction.y * self.velocity
    def handle_input(self, keys):
        direction = Vector2(0, 0)

        if keys[pg.K_w] or keys[pg.K_UP]:
            direction.y -= 1
            self.facing_dir.facing_for_frames=0
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            direction.y += 1
            self.facing_dir.facing_for_frames=0
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction.x -= 1
            self.facing_dir.facing_for_frames=0
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction.x += 1
            self.facing_dir.facing_for_frames=0
        if direction.x != 0 or direction.y != 0:
            self.facing_dir.direction = direction.normalize()
        else:
            self.facing_dir.facing_for_frames += 1
        self.move(direction)

    def move_forward(self):
        self.rect.y -= self.velocity

    def move_backward(self):
        self.rect.y += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_right(self):
        self.rect.x += self.velocity

    def set_weapon(self, weapon):
        self.weapon = weapon

    def get_weapon(self):
        return self.weapon
