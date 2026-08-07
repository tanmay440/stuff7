import pygame as pg
from models import Player, Weapon

def handle_player_shooting(player, keys):
    if keys[pg.K_SPACE]:
        if player.get_weapon() is not None:
            player.get_weapon().shoot()

def handle_events(player, keys):
    player.handle_input(keys)
    handle_player_shooting(player, keys)

def handle_init():
    global player, clock, overlay, window
    pg.init()
    pg.display.set_caption("My Game")
    window = pg.display.set_mode((800, 600))
    image = pg.Surface((50, 50))
    image.fill((255, 255, 255))
    player = Player(image, 5)
    weapon_image = pg.Surface((50, 50))
    weapon_image.fill((255, 0, 0))
    weapon = Weapon(weapon_image, timer=0.75)
    player.set_weapon(weapon)
    clock = pg.time.Clock()
    overlay = pg.Surface((800, 600), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 64))

def main():
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
    keys = pg.key.get_pressed()
    handle_events(player, keys)
    dt = clock.tick(60) / 1000
    if player.get_weapon() is not None:
        player.get_weapon().update_canshoot(dt)
    window.blit(overlay, (0, 0))
    player.draw(window)
    pg.display.flip()

if __name__ == "__main__":
    handle_init()
    while True:
        main()