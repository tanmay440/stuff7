class Weapon:
    def __init__(self, image, damage=1, timer=0.1):
        self.image = image
        self.damage = damage
        self.timer = timer
        self.countdown = 0

    def update_canshoot(self, dt):
        self.countdown -= dt

    def shoot(self):
        if self.countdown <= 0:
            self.countdown = self.timer
            print("BANG!")
            return True

        return False
