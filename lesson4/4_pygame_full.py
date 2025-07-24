#make a rock paper sissor game with scores as a pygame
# Copilot Prompt: Create a simple Rock Paper Scissors game using Pygame. Make it interactive with buttons for each choice and display the result of each round. Always import os os.environ["DISPLAY"] = ":1"

import pygame
import random
import sys
import os
os.environ["DISPLAY"] = ":1"


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
