# Directory notes

These notes describe the repository as it exists on 2026-09-02.

## Quick summary

- This is a small top-down Pygame combat prototype.
- The executable entry point is `main.py`.
- The code was recently refactored toward an object-oriented model.
- Gameplay includes a player, three enemies, ranged and melee attacks, weapon pickups, and stat powerups.
- The README lists `pygame` as the only external library.
- There are no dependency lockfiles, packaging files, test files, or CI configuration in the repository.

## Directory map

```text
.
|-- main.py
|-- README.md
|-- bcgtile.png
|-- mainchar.png
|-- mainchar2.png
|-- projectile_old.png
|-- models/
|   |-- Enemy.py
|   |-- MeleeHitbox.py
|   |-- MeleeWeapon.py
|   |-- Player.py
|   |-- PowerupPickup.py
|   |-- RangedProjectile.py
|   |-- RangedWeapon.py
|   |-- WeaponPickup.py
|   |-- __init__.py
|   `-- templates/
|       |-- Creature.py
|       |-- Entity.py
|       |-- Pickup.py
|       |-- Weapon.py
|       `-- __init__.py
|-- utils/
|   |-- BackgroundTileMap.py
|   `-- __init__.py
|-- .vscode/
|   `-- settings.json
`-- models/**/__pycache__/ and utils/__pycache__/
```

The `__pycache__` directories contain generated Python bytecode for both CPython
3.10 and 3.13. They are not source files.

## Running the project

From the repository root:

```bash
pip install pygame
python ./main.py
```

`main.py` loads PNGs using relative paths, so running from another working
directory may fail to find the assets. The window is 800x600 and targets 60 FPS.
Press `Escape` or close the window to exit.

## Controls

- Move with `WASD` or the arrow keys.
- Fire with `Space`, `Z`, `X`, or `C`.
- The player continuously fires while a fire key is held, subject to the
  equipped weapon cooldown.
- The player initially faces downward; movement changes the facing direction.
- The current HUD displays player health.

## Startup and game loop

1. `handle_init()` initializes Pygame, creates the window and clock, loads
   assets, creates the tile map, and spawns the world.
2. `spawn_world()` creates:
   - A player at world position `(400, 300)`.
   - A starter ranged weapon.
   - Three enemies.
   - Three pickups.
3. Each frame clamps `dt` to at most `0.1` seconds.
4. Events are processed.
5. Living-player input may create an attack entity.
6. Player, creatures, pickups, and existing projectiles update.
7. Enemy AI may create attacks.
8. Collision handling applies pickup effects and combat damage.
9. Dead creatures, collected pickups, and expired/collided projectiles are
   removed from their lists.
10. The camera is centered on the player's world position and the scene is
    rendered.

## Object model

### Base templates

- `Entity` stores an optional image, world position, original spawn position, and
  a Pygame rectangle. It supplies camera-offset drawing and requires `update()`
  and `is_alive()`.
- `Creature` extends `Entity` with health, team, movement speed, velocity,
  facing direction, and an optional weapon. It owns common movement, damage,
  facing, attack, and rotated-image behavior.
- `Pickup` extends `Entity`; it remains alive until collected and has a no-op
  update method.
- `Weapon` is an abstract cooldown-based attack factory. Its timer is reduced
  in `update()` and subclasses implement `attack()`.

### Player

`Player` is a `Creature` with 100 health, 300 movement speed, and team
`PLAYER`. `handle_input()` builds a normalized movement vector, updates
velocity/facing, and requests an attack in the facing direction when a fire key
is pressed.

### Enemy

`Enemy` is a `Creature` with 40 health, 120 movement speed, and team `ENEMY`.
Its `ai_step()` targets the player:

- Outside attack range: move directly toward the target.
- Inside attack range: stop and attempt to attack.
- No target: stop and do nothing.

Default attack ranges are melee reach for `MeleeWeapon`, 300 world units for
`RangedWeapon`, and 50 for an unarmed enemy.

### Weapons and attacks

- `RangedWeapon` creates a `RangedProjectile` after its cooldown expires.
- `RangedProjectile` moves at a fixed velocity, has damage/team/lifetime, and
  becomes dead on collision or lifetime expiry.
- `MeleeWeapon` creates a stationary `MeleeHitbox` in front of the attacker.
- `MeleeHitbox` lasts for a short duration and tracks a set of creatures already
  hit so one swing does not repeatedly damage the same creature.

### Pickups

- `WeaponPickup` replaces the collecting creature's weapon with its stored
  weapon and then disappears.
- `PowerupPickup` supports:
  - `HEALTH`: increases max health and heals by the boost amount, capped at the
    new maximum.
  - `SPEED`: increases movement speed.
  - `DAMAGE`: increases the current weapon's damage when one is equipped.
- Any powerup type is marked collected after `apply_effect()`; unknown types
  therefore disappear without changing stats.

## Initial world configuration

- Starter player weapon: ranged, damage 10, cooldown 0.25 seconds, speed 600.
- Enemy at `(200, 200)`: melee weapon, damage 15, cooldown 0.6, reach 50,
  hitbox duration 0.2.
- Enemy at `(600, 200)`: ranged weapon, damage 8, cooldown 0.9, speed 400.
- Enemy at `(400, 500)`: unarmed.
- Weapon pickup at `(250, 450)`: ranged weapon, damage 25, cooldown 0.15,
  speed 700.
- Health pickup at `(550, 450)`: +25 health/max health.
- Speed pickup at `(400, 150)`: +50 movement speed.

## Rendering and assets

- `bcgtile.png` is repeated by `BackgroundTileMap` to cover the viewport.
- `mainchar2.png` is the active player sprite.
- `mainchar.png` is present but not referenced by `main.py`.
- `projectile_old.png` is loaded and scaled to 20x20 for projectiles.
- Enemies are currently generated as solid red 40x40 surfaces.
- The weapon pickup is a solid gold 24x24 surface.
- The powerup pickup is a solid blue 24x24 surface.
- Melee effects use a translucent orange 32x32 surface.
- A large font is used for `GAME OVER`; a smaller font is used for the HUD.
- World objects are drawn with `camera_offset`; the HUD and game-over message
  are drawn in screen coordinates.

## Collision behavior

- Living players collect overlapping pickups.
- Projectiles do not damage members of their own team.
- Ranged projectiles damage the first colliding creature and are then removed.
- Melee hitboxes can damage multiple creatures, but only once per creature.
- Dead creatures are removed after collision handling, so their final damage
  state can exist for the remainder of the current frame.

## Development conventions

- Source files use type annotations and postponed annotation evaluation.
- Imports are organized around Pygame, local model classes, and `TYPE_CHECKING`
  guards for circular type references.
- Pygame vectors represent world positions, directions, and velocities.
- `models/__init__.py` exposes the concrete gameplay classes for convenient
  imports from `models`.
- `utils/__init__.py` exposes `BackgroundTileMap`.
- VS Code is configured to use the Microsoft Python extension's Conda
  environment manager and package manager.

## Notable maintenance observations

- There is no `requirements.txt`; the documented dependency is only the
  unpinned package name `pygame`.
- There are no automated tests, so behavior currently needs manual execution or
  small ad hoc checks.
- Asset loading depends on the process current working directory rather than
  the location of `main.py`.
- `main()` keeps updating enemies and projectiles after the player dies; input is
  disabled and a game-over overlay is shown, but there is no restart or quit
  prompt.
- Projectiles are removed on collision or timeout, but there is no explicit
  world-boundary cleanup; lifetime is the only general ranged-projectile limit.
- `Creature.spawn_pos` is retained by the base class but is not currently used.
- `Player.handle_input()` accepts `dt` but does not use it directly; movement is
  applied later by `Creature.update()`.
- The camera follows the player's position even after death.
- The prototype uses placeholder procedural surfaces for enemies, pickups, and
  melee effects, while only the player, tile, and projectile visuals come from
  PNG assets.
