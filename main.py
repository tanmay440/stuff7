import pygame as pg
pg.init()
pg.display.set_caption("My Game")
pg.display.set_mode((800, 600))
window = pg.display.get_surface()
pg.key.set_repeat(1, 5)

class Player():
    def __init__(self, image, velocity=15):
        self.image = image
        self.velocity = velocity
        if not isinstance(self.image, pg.Surface):
            raise TypeError("Image must be a pygame Surface")
        if not image is pg.Surface((50, 50)).fill((255, 255, 255)):
            self.rect = self.image.get_rect(center = (400, 300))
        self.rect = self.image.get_rect()
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

def handle_player_movement(player, keys):
    if keys[pg.K_w] or keys[pg.K_UP]:
        player.move_forward()
    if keys[pg.K_s] or keys[pg.K_DOWN]:
        player.move_backward()
    if keys[pg.K_a] or keys[pg.K_LEFT]:
        player.move_left()
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        player.move_right()
image = pg.Surface((50, 50))
image.fill((255, 255, 255))
player = Player(image, 5)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
        handle_player_movement(player, pg.key.get_pressed())
    window.fill((0, 0, 0))
    player.draw(window)
    pg.display.flip()