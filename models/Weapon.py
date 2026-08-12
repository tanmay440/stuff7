from .Projectile import Projectile
from .Vector2 import Vector2
class Weapon:
    def __init__(self, image, damage=1, timer=0.1, projectile_image=None, projectile_velocity=10):
        self.image = image
        self.damage = damage
        self.timer = timer
        self.countdown = 0
        self.projectile_image = projectile_image
        self.projectile_velocity = projectile_velocity

    def update_canshoot(self, dt):
        self.countdown -= dt

    def shoot(self, dir:Vector2, player_velocity:float):
        if self.countdown <= 0:
            self.countdown = self.timer
            return Projectile(self.projectile_image, (0, 0), dir, self.projectile_velocity + player_velocity)

        return False
