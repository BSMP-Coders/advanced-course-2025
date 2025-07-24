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

font = pygame.font.Font(None, 36)
choices = ["Rock", "Paper", "Scissors"]

def draw_buttons():
    for i, choice in enumerate(choices):
        rect = pygame.Rect(50 + i*110, 200, 100, 50)
        pygame.draw.rect(screen, GRAY, rect)
        text = font.render(choice, True, BLACK)
        screen.blit(text, (rect.x + 10, rect.y + 10))
    return [pygame.Rect(50 + i*110, 200, 100, 50) for i in range(3)]


result = "Click a button!"
running = True
while running:
    screen.fill(WHITE)
    title = font.render("Rock Paper Scissors", True, BLACK)
    screen.blit(title, (70, 30))
    result_text = font.render(result, True, BLACK)
    screen.blit(result_text, (100, 100))
    buttons = draw_buttons()
    pygame.display.flip()

pygame.quit()
sys.exit()
