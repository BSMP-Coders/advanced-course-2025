# Rock Paper Scissors Game
# Copilot Prompt: Create a simple Rock Paper Scissors game using Pygame. Make it interactive with buttons for each choice and display the result of each round. Always import os os.environ["DISPLAY"] = ":1"

import pygame
import random
import sys
import os
os.environ["DISPLAY"] = ":1"
# or run DISPLAY=:1 python main.py 

pygame.init()


WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors (Simple)")


pygame.quit()
sys.exit()
