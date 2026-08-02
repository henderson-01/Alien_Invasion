# Alien Invasion Game

This is a fully functional implementation of the classic game "Alien Invasion" using Python and pygame. The game features a player-controlled ship that can move left, right, and shoot at aliens that appear from the top of the screen.

## Project Structure

- `alien_invasion.py`: Main game file. Contains the `AlienInvasion` class which manages the game loop, events, and rendering.
- `ship.py`: Contains the `Ship` class which manages the player's spaceship movement and rendering.
- `alien.py`: Contains the `Alien` class which manages individual alien movement, edge checking, and rendering.
- `bullet.py`: Contains the `Bullet` class which manages bullet movement and rendering.
- `settings.py`: Contains all settings for the game, such as screen dimensions, colors, and speeds.
- `game_stats.py`: Contains the `GameStats` class which tracks game statistics like `ships_left`.
- `scoreboard.py`: Contains the `Scoreboard` class which displays the score, level, and remaining ships.

## How to Run

1. Ensure you have Python installed on your system.
2. Ensure you have `uv` installed. In the project path, run:

   ```bash
   uv sync 
   ```

3. Run the game by executing:

   ```bash
   uv run alien_invasion.py
   ```

## Features

- **Ship Movement**: The player can move the ship left and right using the **Left** and **Right** arrow keys.
- **Shooting**: The player can shoot bullets at aliens using the **Space-bar**.
- **Alien Fleet**: Aliens spawn in a grid, move horizontally, drop down, and reverse direction when they hit the screen edges.
- **Collision Detection**:
  - Bullets destroy aliens.
  - Aliens destroy the ship upon collision.
  - Aliens destroy the ship if they reach the bottom of the screen.
- **Game Statistics**: The game tracks the number of remaining ships (`ships_left`).
- **Game Over**: When all ships are lost, the game stops.
- **Scoreboard**: Keeping track of your high scores.
- **Life's**: You can now see there is three ships representing you get three lives.

## Controls

- **Left/Right Arrow Keys**: Move the ship.
- **Space-bar**: Fire a bullet.
- **Q**: Quit the game.

## Next Steps

- Make some further improvements to the overall game. Possibly a JSON file for saving the game stats and maybe adding an option for a user's create a username to save their high scores to their username as an ID variable.

Happy Coding!
