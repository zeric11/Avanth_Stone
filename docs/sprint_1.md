# Sprint 1


## User Stories

The first sprint will focus on three user stories.

### 2D Graphics
"As a fan of old Zelda games, 
I want pixel-art graphics that provide an interesting and colorful representation of the map and characters. 
When I move my character around or perform some action, 
I want it to look like my character is actually moving so that the game will be more immersive/interesting."

### Controls and Abilities
"As a player, I want to be able to control the main character using my keyboard. 
Using the arrow keys, I want to be able to move vertically, horizontally, and diagonally. 
Additionally, I would like some combat abilities as a way to fight enemies."

### Enemies
"As a player, I would like a variety of enemies to fight in order to make the game challenging and fun. 
I would like each enemy to have some sort of unique fighting pattern that would require me to adapt my attack strategies."


## Workload Estimations

For the graphics portion of this sprint, I will focus on first texturing the player and the three enemies.
This task shouldn't take very long with at most a day spent on each entity.
So I will give this task a small-medium workload.

Logic for both the player controls and the enemy entities are most likely to make up the majority of this sprint's workload.
I will give each of these tasks a medium workload rating. 


## Branching Strategy

I will use feature branching for this project where each of the three user story issues will receive their own branch.
Once the feature is complete, the branch will be merged back into main.
A potential issue I see with this strategy is that, especially during the early stages of a project, 
a codebase can be difficult to modularize in such a way as to create a clean division of tasks.
For instance, getting the player to render onto the screen will depend on whether the player graphics have been finished.
Adding the enemies might require using logic implemented for the player control feature. 
Since I'm the only one working on this project, this shouldn't cause any problems, 
but these types of dependencies could stagnate workflow in a real-world development team. 


## Post Sprint

Textures for the player and the ghost enemy have been completed.
The user is able to move around in 8 directions using the arrow keys
and perform the attack and block abilities using 'z' and 'x'.
The ghost entity will follow the player around the map and perform an "attack" once it reaches the player.
The player and the ghost do not yet have a health system or a way to inflict damage.


## Challenges

This being my first time developing any sort of 2D video game, 
I ended up underestimating the amount of time needed to learn the Pygame library 
and how long it actually takes to develop a game.
Thus two of this sprint's features are half-way complete.

Another tool I tried using for the first time was GitHub Desktop for Windows.
Unfortunately, I did not correctly commit and push using the application, 
which somewhat dirtied the repository's commit history.


## Plans for Sprint 2

* FIX BUG: Ghost faces the wrong direction while chasing player.
* Finish enemy textures.
* Add health and damage.
* Add environment textures and use the Tiled editor to implement a map.