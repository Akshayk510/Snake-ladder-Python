import random
import time
import os

class SnakeAndLadder:
    def __init__(self):
        # Game board size
        self.board_size = 100
        
        # Define snakes (head: tail)
        self.snakes = {
            16: 6,
            47: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78
        }
        
        # Define ladders (bottom: top)
        self.ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100
        }
        
        # Player positions
        self.players = {}
        self.player_count = 0
        
        # Current player turn
        self.current_player = 0
        
        # Game state
        self.game_over = False
        self.winner = None
        
    def setup_players(self, count):
        """Set up the specified number of players"""
        self.player_count = count
        for i in range(1, count + 1):
            self.players[i] = 0  # All players start at position 0 (before the board)
            
    def roll_dice(self):
        """Roll a dice and return the value"""
        return random.randint(1, 6)
        
    def move_player(self, player, steps):
        """Move a player by the specified number of steps"""
        current_pos = self.players[player]
        new_pos = current_pos + steps
        
        # Check if player won
        if new_pos > self.board_size:
            return current_pos  # Can't move beyond the board size
            
        # Check if landed on a snake
        if new_pos in self.snakes:
            print(f"Oops! Player {player} landed on a snake at {new_pos}!")
            new_pos = self.snakes[new_pos]
            print(f"Sliding down to {new_pos}")
            
        # Check if landed on a ladder
        elif new_pos in self.ladders:
            print(f"Yay! Player {player} landed on a ladder at {new_pos}!")
            new_pos = self.ladders[new_pos]
            print(f"Climbing up to {new_pos}")
            
        # Update player position
        self.players[player] = new_pos
        
        # Check if player won
        if new_pos == self.board_size:
            self.game_over = True
            self.winner = player
            
        return new_pos
        
    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player = (self.current_player % self.player_count) + 1
        
    def display_board(self):
        """Display the game board with player positions"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 50)
        print("SNAKE AND LADDER GAME")
        print("=" * 50)
        
        # Display player positions
        for player, position in self.players.items():
            print(f"Player {player}: Position {position}")
            
        print("-" * 50)
        
        # Display snakes and ladders
        print("Snakes: ", end="")
        for head, tail in self.snakes.items():
            print(f"{head}→{tail} ", end="")
        print("\n")
        
        print("Ladders: ", end="")
        for bottom, top in self.ladders.items():
            print(f"{bottom}→{top} ", end="")
        print("\n")
        
        print("-" * 50)
        
    def play_game(self):
        """Main game loop"""
        # Get number of players
        while True:
            try:
                num_players = int(input("Enter number of players (2-4): "))
                if 2 <= num_players <= 4:
                    break
                else:
                    print("Please enter a number between 2 and 4.")
            except ValueError:
                print("Please enter a valid number.")
                
        # Setup players
        self.setup_players(num_players)
        self.current_player = 1
        
        # Main game loop
        while not self.game_over:
            self.display_board()
            
            print(f"\nPlayer {self.current_player}'s turn")
            input("Press Enter to roll the dice...")
            
            # Roll dice
            dice_value = self.roll_dice()
            print(f"Player {self.current_player} rolled a {dice_value}")
            
            # Move player
            new_pos = self.move_player(self.current_player, dice_value)
            print(f"Player {self.current_player} moved to position {new_pos}")
            
            # Check if game is over
            if self.game_over:
                break
                
            # Next player's turn
            self.next_turn()
            
            # Pause for readability
            time.sleep(1)
            
        # Game over
        self.display_board()
        print(f"\nGame Over! Player {self.winner} wins!")
        
# Run the game if this script is executed directly
if __name__ == "__main__":
    game = SnakeAndLadder()
    game.play_game()