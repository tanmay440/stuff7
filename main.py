import pygame as pg
from models import Player, Weapon

def handle_events(player, keys):
    player.handle_input(keys)

def handle_init():
    global player, clock, tile, window, offset_x, offset_y
    offset_x = 0
    offset_y = 0
    pg.init()
    pg.display.set_caption("Movement and Shooting Example")
    window = pg.display.set_mode((800, 600))
    image=pg.image.load("mainchar2.png").convert_alpha()
    player = Player(image, 5)
    weapon_image = pg.Surface((50, 50))
    weapon_image.fill((255, 0, 0))
    projectile_image = pg.transform.scale(pg.image.load("projectile_old.png").convert_alpha(), (20, 20))
    weapon = Weapon(weapon_image, timer=0.75, projectile_image=projectile_image, projectile_velocity=10)
    player.set_weapon(weapon)
    clock = pg.time.Clock()
    tile = pg.image.load("bcgtile.png").convert_alpha()

def main():
    global player, clock, tile, window, offset_x, offset_y
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            exit()
    
    keys = pg.key.get_pressed()
    handle_events(player, keys)
    dt = clock.tick(24) / 1000
    if player.get_weapon() is not None:
        player.get_weapon().update_canshoot(dt)
    offset_x = player.rect.centerx - window.get_width() // 2
    offset_y = player.rect.centery - window.get_height() // 2
    for x in range(-(offset_x % tile.get_width()), window.get_width(), tile.get_width()):
        for y in range(-(offset_y % tile.get_height()), window.get_height(), tile.get_height()):
            window.blit(tile, (x, y))    
    player.draw(window)
    pg.display.flip()
if __name__ == "__main__":
    handle_init()
    while True:
        main()