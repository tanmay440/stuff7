import pygame as pg
from models.FacingDir import FacingDir
from models.Vector2 import Vector2

class Player:
    def __init__(self, image, velocity=5):
        self.image = image
        self.velocity = velocity
        self.rect = self.image.get_rect(center=(400, 300))
        self.facing_dir = FacingDir(Vector2(1, 0))
        self.weapon = None

    def move(self, direction, dt):
        self.rect.x += direction.x * self.velocity * dt * 60
        self.rect.y += direction.y * self.velocity * dt * 60

    def handle_input(self, keys, dt):
        direction = Vector2(0, 0)
        if keys[pg.K_w] or keys[pg.K_UP]:    direction.y -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:  direction.y += 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:  direction.x -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]: direction.x += 1
        if direction.x != 0 or direction.y != 0:
            self.facing_dir.direction = direction.normalize()
        self.move(direction, dt)
        if (keys[pg.K_SPACE] or keys[pg.K_z] or keys[pg.K_x] or keys[pg.K_c])and self.weapon is not None:
            bullet = self.weapon.shoot(self.facing_dir.direction, self.velocity, self.rect.center)
            if bullet:
                return bullet
                
        return None

    def draw(self, surface):
        screen_center = (surface.get_width() // 2, surface.get_height() // 2)
        angle = -self.facing_dir.direction.get_rotation_angle() - 90
        rotated_img = pg.transform.rotate(self.image, angle)
        render_rect = rotated_img.get_rect(center=screen_center)
        surface.blit(rotated_img, render_rect)