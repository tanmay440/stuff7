from . import Vector2
import pygame as pg
class Projectile():
    def __init__(self, image, position, direction: Vector2, velocity: float):
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.direction = direction.normalize()
        self.velocity = velocity

    def update(self):
        self.rect.x += self.direction.x * self.velocity
        self.rect.y += self.direction.y * self.velocity

    def draw(self, surface):
        tempimage = self.image
        tempimage = pg.transform.rotate(tempimage, -self.direction.get_rotation_angle()-90)
        surface.blit(tempimage, self.rect)