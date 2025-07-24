#make a rock paper sissor game with scores as a pygame
# import pygame module

import pygame
import random
import sys
import os
os.environ["DISPLAY"] = ":1"
# or run DISPLAY=:1 python main.py 

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Game choices
CHOICES = ['rock', 'paper', 'scissors']
CHOICE_EMOJIS = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}

class RockPaperScissorsGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Rock Paper Scissors")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Game state
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.result_message = "Choose your move!"
        self.show_result = False
        
        # Button rectangles
        self.rock_button = pygame.Rect(100, 400, 150, 100)
        self.paper_button = pygame.Rect(325, 400, 150, 100)
        self.scissors_button = pygame.Rect(550, 400, 150, 100)
        self.reset_button = pygame.Rect(325, 520, 150, 50)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.rock_button.collidepoint(mouse_pos):
                        self.play_round('rock')
                    elif self.paper_button.collidepoint(mouse_pos):
                        self.play_round('paper')
                    elif self.scissors_button.collidepoint(mouse_pos):
                        self.play_round('scissors')
                    elif self.reset_button.collidepoint(mouse_pos):
                        self.reset_game()
        return True
    
    def play_round(self, player_choice):
        self.player_choice = player_choice
        self.computer_choice = random.choice(CHOICES)
        self.show_result = True
        
        # Determine winner
        if self.player_choice == self.computer_choice:
            self.result_message = "It's a tie!"
        elif (self.player_choice == 'rock' and self.computer_choice == 'scissors') or \
             (self.player_choice == 'paper' and self.computer_choice == 'rock') or \
             (self.player_choice == 'scissors' and self.computer_choice == 'paper'):
            self.result_message = "You win this round!"
            self.player_score += 1
        else:
            self.result_message = "Computer wins this round!"
            self.computer_score += 1
    
    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_choice = None
        self.computer_choice = None
        self.result_message = "Choose your move!"
        self.show_result = False
    
    def draw_button(self, rect, text, color=LIGHT_GRAY, text_color=BLACK):
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 3)
        
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, WHITE, rect, 3)
        
        text_surface = self.font_small.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_large.render("Rock Paper Scissors", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Scores
        score_text = self.font_medium.render(f"Player: {self.player_score}  Computer: {self.computer_score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(score_text, score_rect)
        
        # Game buttons
        self.draw_button(self.rock_button, "🪨 ROCK", LIGHT_GRAY)
        self.draw_button(self.paper_button, "📄 PAPER", LIGHT_GRAY)
        self.draw_button(self.scissors_button, "✂️ SCISSORS", LIGHT_GRAY)
        self.draw_button(self.reset_button, "RESET", RED, WHITE)
        
        # Show choices and result if a round was played
        if self.show_result and self.player_choice and self.computer_choice:
            # Player choice
            player_text = self.font_medium.render(f"You chose: {CHOICE_EMOJIS[self.player_choice]} {self.player_choice.title()}", True, BLUE)
            player_rect = player_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
            self.screen.blit(player_text, player_rect)
            
            # Computer choice
            computer_text = self.font_medium.render(f"Computer chose: {CHOICE_EMOJIS[self.computer_choice]} {self.computer_choice.title()}", True, RED)
            computer_rect = computer_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
            self.screen.blit(computer_text, computer_rect)
            
            # Result
            result_color = GREEN if "You win" in self.result_message else RED if "Computer wins" in self.result_message else BLACK
            result_text = self.font_medium.render(self.result_message, True, result_color)
            result_rect = result_text.get_rect(center=(WINDOW_WIDTH // 2, 320))
            self.screen.blit(result_text, result_rect)
        else:
            # Instructions
            instruction_text = self.font_medium.render(self.result_message, True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, 250))
            self.screen.blit(instruction_text, instruction_rect)
        
        # Game instructions
        instructions = [
            "Click on Rock, Paper, or Scissors to play!",
            "Rock beats Scissors, Paper beats Rock, Scissors beats Paper"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, GRAY)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 25))
            self.screen.blit(text, text_rect)
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()

