import sys

import pygame as pg

from models import (
    Enemy,
    MeleeHitbox,
    MeleeWeapon,
    Player,
    PowerupPickup,
    RangedProjectile,
    RangedWeapon,
    WeaponPickup,
)
from utils import BackgroundTileMap

FPS = 60
WINDOW_SIZE = (800, 600)


def load_assets():
    player_img = pg.image.load("mainchar2.png").convert_alpha()
    tile_img = pg.image.load("bcgtile.png").convert_alpha()
    proj_img = pg.transform.scale(pg.image.load("projectile_old.png").convert_alpha(), (20, 20))

    enemy_img = pg.Surface((40, 40))
    enemy_img.fill((200, 30, 30))

    weapon_icon = pg.Surface((24, 24))
    weapon_icon.fill((255, 215, 0))

    powerup_icon = pg.Surface((24, 24))
    powerup_icon.fill((60, 140, 255))

    effect_img = pg.Surface((32, 32), pg.SRCALPHA)
    effect_img.fill((255, 140, 0, 120))

    font = pg.font.Font(None, 72)
    hud_font = pg.font.Font(None, 28)

    return {
        "player_img": player_img,
        "tile_img": tile_img,
        "proj_img": proj_img,
        "enemy_img": enemy_img,
        "weapon_icon": weapon_icon,
        "powerup_icon": powerup_icon,
        "effect_img": effect_img,
        "font": font,
        "hud_font": hud_font,
    }


def spawn_world(assets):
    starter_weapon = RangedWeapon(
        image=None, projectile_img=assets["proj_img"], damage=10.0, cooldown=0.25, velocity=600.0
    )
    player = Player(assets["player_img"], pg.math.Vector2(400, 300), weapon=starter_weapon)

    melee_weapon = MeleeWeapon(
        image=None, effect_img=assets["effect_img"], damage=15.0, cooldown=0.6, reach=50.0, duration=0.2
    )
    ranged_weapon = RangedWeapon(
        image=None, projectile_img=assets["proj_img"], damage=8.0, cooldown=0.9, velocity=400.0
    )
    creatures = [
        Enemy(assets["enemy_img"], pg.math.Vector2(200, 200), weapon=melee_weapon, target=player),
        Enemy(assets["enemy_img"], pg.math.Vector2(600, 200), weapon=ranged_weapon, target=player),
        Enemy(assets["enemy_img"], pg.math.Vector2(400, 500), weapon=None, target=player),
    ]

    upgraded_weapon = RangedWeapon(
        image=None, projectile_img=assets["proj_img"], damage=25.0, cooldown=0.15, velocity=700.0
    )
    pickups = [
        WeaponPickup(assets["weapon_icon"], pg.math.Vector2(250, 450), stored_weapon=upgraded_weapon),
        PowerupPickup(assets["powerup_icon"], pg.math.Vector2(550, 450), stat_type="HEALTH", boost_amount=25.0),
        PowerupPickup(assets["powerup_icon"], pg.math.Vector2(400, 150), stat_type="SPEED", boost_amount=50.0),
    ]
    return player, creatures, pickups


def handle_init():
    pg.init()
    pg.display.set_caption("UML Refactor Demo")
    window = pg.display.set_mode(WINDOW_SIZE)
    clock = pg.time.Clock()
    assets = load_assets()
    tile_map = BackgroundTileMap(assets["tile_img"])
    player, creatures, pickups = spawn_world(assets)
    return window, clock, player, creatures, pickups, tile_map, assets


def handle_collisions(player, creatures, pickups, projectiles):
    if player.is_alive():
        for pickup in pickups:
            if pickup.is_alive() and player.rect.colliderect(pickup.rect):
                if isinstance(pickup, WeaponPickup):
                    pickup.collect(player)
                elif isinstance(pickup, PowerupPickup):
                    pickup.apply_effect(player)

    all_creatures = creatures + ([player] if player.is_alive() else [])
    for proj in projectiles:
        if isinstance(proj, RangedProjectile) and proj.has_collided:
            continue
        for creature in all_creatures:
            if proj.team == creature.team or not proj.rect.colliderect(creature.rect):
                continue
            if isinstance(proj, MeleeHitbox):
                if creature not in proj.hit_creatures:
                    creature.take_damage(proj.damage)
                    proj.hit_creatures.add(creature)
            else:
                creature.take_damage(proj.damage)
                proj.has_collided = True
                break


def draw_game_over(window, font):
    text = font.render("GAME OVER", True, (255, 255, 255))
    rect = text.get_rect(center=window.get_rect().center)
    window.blit(text, rect)


def render(window, tile_map, player, creatures, pickups, projectiles, camera_offset, assets):
    tile_map.draw(window, camera_offset)
    for pickup in pickups:
        pickup.draw(window, camera_offset)
    for enemy in creatures:
        enemy.draw(window, camera_offset)
    player.draw(window, camera_offset)
    for proj in projectiles:
        proj.draw(window, camera_offset)

    hud_text = assets["hud_font"].render(
        f"HP: {int(player.health)}/{int(player.max_health)}", True, (255, 255, 255)
    )
    window.blit(hud_text, (10, 10))

    if not player.is_alive():
        draw_game_over(window, assets["font"])


def main():
    window, clock, player, creatures, pickups, tile_map, assets = handle_init()
    projectiles = []

    while True:
        dt = min(clock.tick(FPS) / 1000.0, 0.1)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

        keys = pg.key.get_pressed()
        if player.is_alive():
            player_attack = player.handle_input(keys, dt)
            if player_attack:
                projectiles.append(player_attack)

        player.update(dt)
        for creature in creatures:
            creature.update(dt)
        for pickup in pickups:
            pickup.update(dt)
        for proj in projectiles:
            proj.update(dt)

        for enemy in creatures:
            enemy_attack = enemy.ai_step(dt)
            if enemy_attack:
                projectiles.append(enemy_attack)

        handle_collisions(player, creatures, pickups, projectiles)

        creatures = [c for c in creatures if c.is_alive()]
        pickups = [p for p in pickups if p.is_alive()]
        projectiles = [p for p in projectiles if p.is_alive()]

        camera_offset = pg.math.Vector2(
            window.get_width() // 2 - player.pos.x, window.get_height() // 2 - player.pos.y
        )
        render(window, tile_map, player, creatures, pickups, projectiles, camera_offset, assets)
        pg.display.flip()


if __name__ == "__main__":
    main()
