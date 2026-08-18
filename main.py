import sys
import pygame as pg
from models import Player, Weapon

def handle_init():
    pg.init()
    pg.display.set_caption("Movement and Shooting Example")
    window = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    player_img = pg.image.load("mainchar2.png").convert_alpha()
    player = Player(player_img, velocity=5)

    weapon_img = pg.Surface((50, 50))
    weapon_img.fill((255, 0, 0))
    proj_img = pg.transform.scale(pg.image.load("projectile_old.png").convert_alpha(), (20, 20))
    
    weapon = Weapon(weapon_img, timer=0.25, projectile_image=proj_img, projectile_velocity=10, team="player")
    player.weapon = weapon

    tile = pg.image.load("bcgtile.png").convert_alpha()
    
    return window, clock, player, tile

def main():
    window, clock, player, tile = handle_init()
    projectiles = []

    while True:
        dt = clock.tick(60) / 1000.0  # Normalized Delta Time

        # 1. Event Handling
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        # 2. Input & Updates
        keys = pg.key.get_pressed()
        new_bullet = player.handle_input(keys, dt)
        if new_bullet:
            projectiles.append(new_bullet)

        if player.weapon:
            player.weapon.update_canshoot(dt)

        # Update Master Projectiles & Cleanup
        for bullet in projectiles:
            bullet.update(dt)
        projectiles = [b for b in projectiles if not b.is_dead()]

        # Camera Offset Calculation
        offset_x = player.rect.centerx - window.get_width() // 2
        offset_y = player.rect.centery - window.get_height() // 2

        # 3. Rendering Phase
        # Background
        for x in range(-(offset_x % tile.get_width()), window.get_width(), tile.get_width()):
            for y in range(-(offset_y % tile.get_height()), window.get_height(), tile.get_height()):
                window.blit(tile, (x, y))

        # Projectiles (Rendered in World Space via offset)
        for bullet in projectiles:
            bullet.draw(window, offset_x, offset_y)

        # Player (Rendered at Screen Center)
        player.draw(window)

        pg.display.flip()

if __name__ == "__main__":
    main()