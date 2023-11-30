# Sprint 3


## Workload Estimation

### Health bar and score   
* 10 hearts for 10 units of the player's health.
* A counter to show how many enemies remain on the level.
* Time estimation: 1 day

### Audio
* Sound effects for player/enemies taking damage or dying.
* Sound effects for player/enemy attacks.
* Background music.
* Time estimation: 2 days

### Damage tinting
* Player and enemies will briefly turn red after taking damage.
* Time estimation: 1 day

### Particle effects
* Effects for player/enemy death and meteor explosions.
* Time estimation: 1 day

### Boomerang
* Player will be able to throw a boomerang as an ability.
* The boomerang will fly a certain distance, then return to the player.
* Damage is dealt to enemies it comes in contant with.
* Time estimation: 1 day

### Game Over screen
* A Game Over screen will be displayed when the player dies.
* Time estimation: 1 day

### Boss fight
* Boss door will open when all enemies are killed in the level.
* Player will fight boss upon entering boss room.
* The boss will use a variety of attacks in stages.


## Post Sprint

For this final sprint all of the proposed features, except for the boss fight, 
have been completed.
The sound effects were taken from [Mixkil](https://mixkit.co/free-sound-effects).
The background music is [Forest Walk by Alexander Nakarada](https://www.chosic.com/download-audio/28063/). 
The boss door opens when all enemies have been eliminated.
Entering the door will end the game.

The current state of the code base makes it difficult to add new levels/rooms to the game.
This is major flaw of the code structure that needs to be addressed in a fourth sprint.
This would include creating a parent class for the Level object where all levels would
extend from, as well as fixing the sprite group management system.
Additionally, there is a lot of duplicate code between the player, enemy, and projectile sprints.
The inheritance hierarchy between these classes needs to be revisited.

For this sprint, although textures for the boss and the boss room are at least partially completed, 
there was not enough time to complete the full boss fight.