class Player:
    def __init__(self, image, velocity=15):
        self.image = image
        self.velocity = velocity
        self.rect = self.image.get_rect(center=(400, 300))
        self.weapon = None

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
