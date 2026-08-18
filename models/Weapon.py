from .Projectile import Projectile
from .Vector2 import Vector2
class Weapon:
    def __init__(self, image, damage=1, timer=0.1, projectile_image=None, projectile_velocity=10, team="player"):
        self.image = image
        self.damage = damage
        self.timer = timer
        self.countdown = 0
        self.projectile_image = projectile_image
        self.team = team
        self.projectile_velocity = projectile_velocity

    def update_canshoot(self, dt):
        self.countdown -= dt

    def shoot(self, direction, player_velocity, spawn_pos):
        if self.countdown <= 0:
            self.countdown = self.timer
            return Projectile(
                image=self.projectile_image,
                spawn_pos=spawn_pos,
                direction=direction,
                velocity=self.projectile_velocity + player_velocity,
                team=self.team
            )
        return False