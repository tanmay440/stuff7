import pygame as pg

class Projectile:
    def __init__(self, image, spawn_pos, direction, velocity, team="player", max_lifetime=3.0):
        self.image = image
        self.rect = self.image.get_rect(center=spawn_pos)
        self.direction = direction.normalize()
        self.velocity = velocity
        self.team = team
        self.lifetime = max_lifetime
        print(self.direction) 

    def update(self, dt):
        self.rect.x += self.direction.x * self.velocity * dt * 60
        self.rect.y += self.direction.y * self.velocity * dt * 60
        self.lifetime -= dt

    def is_dead(self):
        return self.lifetime <= 0

    def draw(self, surface, offset_x, offset_y):
        screen_x = self.rect.x - offset_x
        screen_y = self.rect.y - offset_y
        angle = -self.direction.get_rotation_angle() - 90
        rotated_img = pg.transform.rotate(self.image, angle)
        render_rect = rotated_img.get_rect(center=(screen_x, screen_y))
        surface.blit(rotated_img, render_rect)