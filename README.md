# Duskers

A simple text-based resource management and exploration game written in Python.

## Features

- Start a new game or load from up to 3 save slots
- Explore locations to gather titanium, risking robot losses
- Upgrade your abilities in the store (scan upgrades, new robots)
- Save and load your progress
- High score tracking
- Simple ASCII art interface

## How to Run

1. Install Python 3.x.
2. Open a terminal and navigate to the project directory.
3. Run the game using: python duskers.py <seed> <min animation time> <max animation time> <give names of locations you want to include in game for exploring>
   - `seed`: Optional seed for random number generation (default is 0)
   - `min animation time`: Minimum time for animations (default is 0.1 seconds)
   - `max animation time`: Maximum time for animations (default is 0.5 seconds)
   - `give names of locations`: 
## Game Flow

- **Main Menu**: New Game, Load Game, High Scores, Help, Exit
- **Game Hub**: View status, explore, upgrade, save, or return to menu
- **Explore**: Choose locations, risk encounters, collect titanium
- **Upgrade Store**: Buy upgrades with titanium
- **Save/Load**: Three save slots, each storing player name, titanium, robots, and upgrades
- **High Scores**: Top 10 scores tracked by player name

## File Structure

- `duskers.py`: Main game logic
- `save_file1.txt`, `save_file2.txt`, `save_file3.txt`: Save slots
- `high_scores.txt`: High score records

## Controls

- Type menu options as shown in brackets (e.g., `new`, `load`, `ex`, `up`, `save`, `m`, etc.)
- Follow prompts for further actions

## License

MIT License (or specify your own)