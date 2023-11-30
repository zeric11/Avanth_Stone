# Sprint 2


## Workload Estimation

For this sprint, I will need to progress the project to meet the MVP.
The majority of this sprint will be spent creating a map using the Tiled editor 
and importing the CSV files and tilemap textures into the game.
This should take approximately 4-5 days to complete.

The next part of this sprint will be complete the three enemy types.
Textures for the ghost have already been completed in sprint 1,
the step will be to create textures for the sentry and bomber enemies.
This will include creating textures for the projectiles the sentry and bomber
will launch at the player. This should take about 1-2 days to complete.

Combat logic for the player and enemies will be implemented next.
When the player attacks at a close enough distance to an enemy,
the enemy should take damage, and the enemy should also be able to deal 
damage to the player. 
If the player is using the shield ability, no damage should be blocked.
If the player/enemy will die when its health reaches 0.
The ghost enemy will attack by running into the player.
The sentry enemy will remain stationary and will attack by firing projectiles 
at the player. The Bomber enemy will fly overhead and fire projectiles down onto 
the player. Adding this logic should take about 3-4 days to complete.

The final step will be to create a health bar display.
This should be completed within a day.


## Post Sprint

As predicted, implementing the map took up the majority of the workload for this sprint.
The textures used in for the world were taken from the 
[Mystic Woods](https://game-endeavor.itch.io/mystic-woods) asset pack.
The Tiled editor was used to assemble these textures into a map and generate CSV files.

The three enemy types along with combat has been completed.

The health bar did not get implemented in time.


## Plans for Sprint 3

* Health bar and score
* Audio
* Effects:
    - Explosion effect when meteor lands
    - Smoke effect with player/enemy is killed
    - Entities briefly turn red when taking damage
* Boomerang ability
* Knockback and stun
* Game over screen after player death
* Boss room and boss fight

