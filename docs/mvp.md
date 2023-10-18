# Minimum Viable Product

* 2D pixel-art graphics
    - Map textures and character sprites
    - Character movement and attacks must be "animated"

* Main character
    - Keyboard to control
    - 8 directional movement
    - Sword ability for attacking
    - Shield ability for blocking attacks
    - Health bar

* Enemies
    - 3 different enemy types
    - Each enemy type will attack the player in a unique way


# Project Structure

This project will be separated out into 2 main components: Textures and logic.
The textures in this project will include the map assets, such as trees, grass, dirt, and assets for each character. 
In order achieve an animation effect, characters will need to have multiple images representing themselves standing still, walking, and attacking toward the north, south, east, and west. 
The logic for this project will be the game loop that handles user input and which textures to load in given said input and the current environment state.