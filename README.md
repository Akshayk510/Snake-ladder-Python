# Snake and Ladder Game

This project contains two implementations of the classic Snake and Ladder board game:

1. A text-based version that runs in the console
2. A graphical version using Pygame

## Game Rules

Snake and Ladder is a classic board game played with the following rules:

- The game is played on a 10x10 grid (100 squares)
- Players take turns rolling a dice and moving their piece forward by the number rolled
- If a player lands on the bottom of a ladder, they climb up to the top of the ladder
- If a player lands on the head of a snake, they slide down to the tail of the snake
- The first player to reach or exceed square 100 wins the game

## Text-Based Version (SnakeAndLadder.py)

### Requirements
- Python 3.x

### How to Run
```
python SnakeAndLadder.py
```

### Features
- Supports 2-4 players
- Displays the game board with player positions
- Shows snakes and ladders on the board
- Simple text-based interface

### Controls
- Follow the on-screen prompts
- Press Enter to roll the dice
- The game automatically handles player movement and turn rotation

## Graphical Version (SnakeAndLadderVisual.py)

### Requirements
- Python 3.x
- Pygame library (`pip install pygame`)

### How to Run
```
python SnakeAndLadderVisual.py
```

### Features
- Visual 10x10 game board
- Animated dice rolling
- Animated player movement
- Visual representation of snakes and ladders
- Support for 2-4 players
- Game state messages

### Controls
- **Setup Phase:**
  - UP/DOWN arrows: Change number of players
  - ENTER: Start the game
  
- **Playing Phase:**
  - SPACE: Roll the dice
  
- **Game Over Phase:**
  - R: Restart the game
  - Q: Quit the game

## Game Elements

### Snakes
The game includes the following snakes (head → tail):
- 16 → 6
- 47 → 26
- 49 → 11
- 56 → 53
- 62 → 19
- 64 → 60
- 87 → 24
- 93 → 73
- 95 → 75
- 98 → 78

### Ladders
The game includes the following ladders (bottom → top):
- 1 → 38
- 4 → 14
- 9 → 31
- 21 → 42
- 28 → 84
- 36 → 44
- 51 → 67
- 71 → 91
- 80 → 100

## Tips
- Landing on a ladder is good - it moves you up the board faster
- Avoid landing on snakes as they will send you backward
- The game is largely based on luck, but you can strategize when you have multiple players
- In the visual version, you can see all possible snake and ladder positions highlighted on the board

Enjoy playing!
