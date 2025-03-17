import pygame
import sys
import random
import time
import math

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = 500
GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = BOARD_SIZE // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Player colors
PLAYER_COLORS = [RED, BLUE, GREEN, YELLOW]

class Dice:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.value = 1
        self.rolling = False
        self.roll_time = 0
        self.roll_duration = 1.0  # seconds
        self.dots = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.25, 0.75), (0.75, 0.25), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.25, 0.5), (0.25, 0.75), (0.75, 0.25), (0.75, 0.5), (0.75, 0.75)]
        }
        
    def roll(self):
        """Start rolling the dice"""
        self.rolling = True
        self.roll_time = time.time()
        
    def update(self):
        """Update dice state"""
        if self.rolling:
            # Generate random values while rolling
            self.value = random.randint(1, 6)
            
            # Check if rolling is complete
            if time.time() - self.roll_time > self.roll_duration:
                self.rolling = False
                self.value = random.randint(1, 6)
                return True  # Rolling complete
        return False
        
    def draw(self, screen):
        """Draw the dice"""
        # Draw dice body
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.size, self.size), 2)
        
        # Draw dots
        dot_radius = self.size // 10
        for dot_x, dot_y in self.dots[self.value]:
            pos_x = self.x + int(dot_x * self.size)
            pos_y = self.y + int(dot_y * self.size)
            pygame.draw.circle(screen, BLACK, (pos_x, pos_y), dot_radius)

class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.position = 0  # Start before the board
        self.target_position = 0
        self.moving = False
        self.x = 0
        self.y = 0
        self.radius = CELL_SIZE // 4
        self.move_speed = 0.1  # Movement speed
        self.move_progress = 0
        
    def move(self, steps):
        """Set target position for movement"""
        self.target_position = min(self.position + steps, 100)
        self.moving = True
        self.move_progress = 0
        
    def update(self):
        """Update player movement"""
        if self.moving:
            self.move_progress += self.move_speed
            
            if self.move_progress >= 1:
                self.position += 1
                self.move_progress = 0
                
                if self.position >= self.target_position:
                    self.moving = False
                    self.position = self.target_position
                    return True  # Movement complete
                    
        return False
        
    def update_coordinates(self, board_x, board_y):
        """Update player coordinates based on position"""
        if self.position == 0:
            # Position before the board
            self.x = board_x - 50
            self.y = board_y + BOARD_SIZE - CELL_SIZE // 2
            return
            
        # Calculate row and column
        pos = self.position - 1  # Adjust to 0-based indexing
        row = 9 - (pos // 10)  # Rows start from bottom (9) to top (0)
        
        # Columns alternate direction based on row
        if row % 2 == 1:  # Odd rows go left to right
            col = pos % 10
        else:  # Even rows go right to left
            col = 9 - (pos % 10)
            
        # Calculate pixel coordinates (center of the cell)
        # Add offset for player ID to avoid overlap
        offset_x = (self.id - 1) % 2 * 20 - 10
        offset_y = (self.id - 1) // 2 * 20 - 10
        
        self.x = board_x + col * CELL_SIZE + CELL_SIZE // 2 + offset_x
        self.y = board_y + row * CELL_SIZE + CELL_SIZE // 2 + offset_y
        
    def draw(self, screen):
        """Draw the player"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw player number
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(self.id), True, WHITE)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)

class SnakeAndLadderGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake and Ladder")
        self.clock = pygame.time.Clock()
        
        # Board position
        self.board_x = (SCREEN_WIDTH - BOARD_SIZE) // 2
        self.board_y = (SCREEN_HEIGHT - BOARD_SIZE) // 2
        
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
        
        # Game state
        self.players = []
        self.current_player = 0
        self.game_over = False
        self.winner = None
        
        # Dice
        self.dice = Dice(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2, 60)
        self.dice_rolled = False
        self.dice_value = 0
        
        # Message
        self.message = ""
        self.message_time = 0
        self.message_duration = 2.0  # seconds
        
        # Fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Game state
        self.state = "setup"  # setup, playing, game_over
        self.player_count = 2  # Default
        
    def setup_players(self, count):
        """Set up the specified number of players"""
        self.players = []
        for i in range(1, count + 1):
            self.players.append(Player(i, PLAYER_COLORS[i-1]))
            
    def roll_dice(self):
        """Roll the dice"""
        if not self.dice.rolling and not self.dice_rolled:
            self.dice.roll()
            self.dice_rolled = True
            
    def move_current_player(self):
        """Move the current player based on dice value"""
        player = self.players[self.current_player]
        player.move(self.dice_value)
        
    def next_turn(self):
        """Move to the next player's turn"""
        self.current_player = (self.current_player + 1) % len(self.players)
        self.dice_rolled = False
        
    def check_snake_or_ladder(self):
        """Check if player landed on a snake or ladder"""
        player = self.players[self.current_player]
        
        # Check for snake
        if player.position in self.snakes:
            self.show_message(f"Player {player.id} landed on a snake!")
            player.target_position = self.snakes[player.position]
            player.moving = True
            player.move_progress = 0
            return True
            
        # Check for ladder
        if player.position in self.ladders:
            self.show_message(f"Player {player.id} found a ladder!")
            player.target_position = self.ladders[player.position]
            player.moving = True
            player.move_progress = 0
            return True
            
        return False
        
    def check_winner(self):
        """Check if current player won"""
        player = self.players[self.current_player]
        if player.position == 100:
            self.game_over = True
            self.winner = player
            self.state = "game_over"
            self.show_message(f"Player {player.id} wins!")
            return True
        return False
        
    def show_message(self, text):
        """Show a message for a duration"""
        self.message = text
        self.message_time = time.time()
        
    def draw_board(self):
        """Draw the game board"""
        # Draw board background
        pygame.draw.rect(self.screen, LIGHT_BLUE, 
                        (self.board_x, self.board_y, BOARD_SIZE, BOARD_SIZE))
        pygame.draw.rect(self.screen, BLACK, 
                        (self.board_x, self.board_y, BOARD_SIZE, BOARD_SIZE), 2)
        
        # Draw grid
        for i in range(GRID_SIZE + 1):
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                            (self.board_x + i * CELL_SIZE, self.board_y),
                            (self.board_x + i * CELL_SIZE, self.board_y + BOARD_SIZE))
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK, 
                            (self.board_x, self.board_y + i * CELL_SIZE),
                            (self.board_x + BOARD_SIZE, self.board_y + i * CELL_SIZE))
        
        # Draw cell numbers
        for i in range(100):
            row = 9 - (i // 10)  # Rows start from bottom (9) to top (0)
            
            # Columns alternate direction based on row
            if row % 2 == 1:  # Odd rows go left to right
                col = i % 10
            else:  # Even rows go right to left
                col = 9 - (i % 10)
                
            num = i + 1  # Cell numbers start from 1
            
            # Highlight special cells
            if num in self.snakes:
                pygame.draw.rect(self.screen, ORANGE, 
                                (self.board_x + col * CELL_SIZE, self.board_y + row * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE))
            elif num in self.ladders:
                pygame.draw.rect(self.screen, GREEN, 
                                (self.board_x + col * CELL_SIZE, self.board_y + row * CELL_SIZE, 
                                CELL_SIZE, CELL_SIZE))
                
            # Draw number
            text = self.small_font.render(str(num), True, BLACK)
            text_rect = text.get_rect(center=(self.board_x + col * CELL_SIZE + CELL_SIZE // 2, 
                                            self.board_y + row * CELL_SIZE + CELL_SIZE // 2))
            self.screen.blit(text, text_rect)
            
    def draw_snakes_and_ladders(self):
        """Draw snakes and ladders on the board"""
        # Draw snakes
        for head, tail in self.snakes.items():
            head_pos = self.get_position_coordinates(head)
            tail_pos = self.get_position_coordinates(tail)
            
            # Draw snake body (curved line)
            points = self.get_curve_points(head_pos, tail_pos, 0.3, 5)
            if len(points) > 1:
                pygame.draw.lines(self.screen, RED, False, points, 3)
                
            # Draw snake head and tail
            pygame.draw.circle(self.screen, RED, head_pos, 5)
            pygame.draw.circle(self.screen, ORANGE, tail_pos, 5)
            
        # Draw ladders
        for bottom, top in self.ladders.items():
            bottom_pos = self.get_position_coordinates(bottom)
            top_pos = self.get_position_coordinates(top)
            
            # Draw ladder (two parallel lines with rungs)
            offset = 5
            
            # Calculate direction vector
            dx = top_pos[0] - bottom_pos[0]
            dy = top_pos[1] - bottom_pos[1]
            length = math.sqrt(dx*dx + dy*dy)
            
            # Normalize and get perpendicular
            if length > 0:
                dx, dy = dx/length, dy/length
                perp_x, perp_y = -dy, dx
                
                # Draw sides
                side1_bottom = (bottom_pos[0] + perp_x * offset, bottom_pos[1] + perp_y * offset)
                side1_top = (top_pos[0] + perp_x * offset, top_pos[1] + perp_y * offset)
                side2_bottom = (bottom_pos[0] - perp_x * offset, bottom_pos[1] - perp_y * offset)
                side2_top = (top_pos[0] - perp_x * offset, top_pos[1] - perp_y * offset)
                
                pygame.draw.line(self.screen, BROWN, side1_bottom, side1_top, 2)
                pygame.draw.line(self.screen, BROWN, side2_bottom, side2_top, 2)
                
                # Draw rungs
                steps = max(2, int(length / 30))
                for i in range(steps):
                    t = i / (steps - 1)
                    x1 = side1_bottom[0] + t * (side1_top[0] - side1_bottom[0])
                    y1 = side1_bottom[1] + t * (side1_top[1] - side1_bottom[1])
                    x2 = side2_bottom[0] + t * (side2_top[0] - side2_bottom[0])
                    y2 = side2_bottom[1] + t * (side2_top[1] - side2_bottom[1])
                    pygame.draw.line(self.screen, BROWN, (x1, y1), (x2, y2), 2)
                    
    def get_position_coordinates(self, position):
        """Get pixel coordinates for a board position"""
        if position < 1 or position > 100:
            return (0, 0)
            
        pos = position - 1  # Adjust to 0-based indexing
        row = 9 - (pos // 10)  # Rows start from bottom (9) to top (0)
        
        # Columns alternate direction based on row
        if row % 2 == 1:  # Odd rows go left to right
            col = pos % 10
        else:  # Even rows go right to left
            col = 9 - (pos % 10)
            
        # Calculate pixel coordinates (center of the cell)
        x = self.board_x + col * CELL_SIZE + CELL_SIZE // 2
        y = self.board_y + row * CELL_SIZE + CELL_SIZE // 2
        
        return (x, y)
        
    def get_curve_points(self, start, end, curvature, num_points):
        """Generate points for a curved line between start and end"""
        points = []
        
        # Calculate midpoint
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        # Calculate perpendicular direction for curve
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return [start, end]
            
        # Normalize and get perpendicular
        dx, dy = dx/length, dy/length
        perp_x, perp_y = -dy, dx
        
        # Control point for curve
        control_x = mid_x + perp_x * length * curvature
        control_y = mid_y + perp_y * length * curvature
        
        # Generate points along the quadratic curve
        for i in range(num_points):
            t = i / (num_points - 1)
            # Quadratic Bezier curve formula
            x = (1-t)**2 * start[0] + 2*(1-t)*t * control_x + t**2 * end[0]
            y = (1-t)**2 * start[1] + 2*(1-t)*t * control_y + t**2 * end[1]
            points.append((int(x), int(y)))
            
        return points
        
    def draw_ui(self):
        """Draw game UI elements"""
        # Draw player info
        for i, player in enumerate(self.players):
            y_pos = 50 + i * 30
            pygame.draw.circle(self.screen, player.color, (20, y_pos), 10)
            
            text = self.small_font.render(f"Player {player.id}: Position {player.position}", True, BLACK)
            self.screen.blit(text, (40, y_pos - 10))
            
            # Highlight current player
            if i == self.current_player and self.state == "playing":
                pygame.draw.circle(self.screen, BLACK, (20, y_pos), 12, 2)
                
        # Draw dice
        self.dice.draw(self.screen)
        
        # Draw message
        if self.message and time.time() - self.message_time < self.message_duration:
            text = self.font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            self.screen.blit(text, text_rect)
            
        # Draw instructions
        if self.state == "playing" and not self.dice_rolled:
            text = self.small_font.render("Press SPACE to roll dice", True, BLACK)
            self.screen.blit(text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
            
        elif self.state == "setup":
            text1 = self.font.render("Select number of players:", True, BLACK)
            text2 = self.font.render(f"{self.player_count}", True, BLACK)
            text3 = self.small_font.render("UP/DOWN to change, ENTER to start", True, BLACK)
            
            self.screen.blit(text1, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text2, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text3, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
            
        elif self.state == "game_over":
            text = self.font.render(f"Player {self.winner.id} wins!", True, BLACK)
            text2 = self.small_font.render("Press R to play again", True, BLACK)
            
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            
            self.screen.blit(text, text_rect)
            self.screen.blit(text2, text2_rect)
            
    def handle_setup_input(self, event):
        """Handle input during setup phase"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_count = min(self.player_count + 1, 4)
            elif event.key == pygame.K_DOWN:
                self.player_count = max(self.player_count - 1, 2)
            elif event.key == pygame.K_RETURN:
                self.setup_players(self.player_count)
                self.state = "playing"
                self.current_player = 0
                self.game_over = False
                self.winner = None
                
    def handle_playing_input(self, event):
        """Handle input during playing phase"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.dice_rolled:
                self.roll_dice()
                
    def handle_game_over_input(self, event):
        """Handle input during game over phase"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.__init__()  # Reset the game
                
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Handle input based on game state
                if self.state == "setup":
                    self.handle_setup_input(event)
                elif self.state == "playing":
                    self.handle_playing_input(event)
                elif self.state == "game_over":
                    self.handle_game_over_input(event)
                    
            # Update
            if self.state == "playing":
                # Update dice
                if self.dice.update() and self.dice_rolled:
                    self.dice_value = self.dice.value
                    self.show_message(f"Player {self.players[self.current_player].id} rolled a {self.dice_value}")
                    self.move_current_player()
                    
                # Update players
                for player in self.players:
                    player.update_coordinates(self.board_x, self.board_y)
                    
                # Check if current player finished moving
                player = self.players[self.current_player]
                if player.moving:
                    if player.update():
                        # Player finished moving
                        if not self.check_snake_or_ladder():
                            if not self.check_winner():
                                self.next_turn()
                                
            # Draw
            self.screen.fill(WHITE)
            
            if self.state != "setup":
                self.draw_board()
                self.draw_snakes_and_ladders()
                
                # Draw players
                for player in self.players:
                    player.draw(self.screen)
                    
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.run()