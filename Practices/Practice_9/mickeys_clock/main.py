import datetime
import pygame
import os 
pygame.init()
w ,h = 1000, 600
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()
BASE_PATH = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_PATH, "images")

background = pygame.image.load(os.path.join(IMG_DIR, "main_clock.png"))
background = pygame.transform.scale(background, (w,h))
right_hand = pygame.image.load(os.path.join(IMG_DIR, "right_hand.png")).convert_alpha()
left_hand  = pygame.image.load(os.path.join(IMG_DIR, "left_hand.png")).convert_alpha()
right_hand = pygame.transform.scale(right_hand,(300,300))
left_hand  = pygame.transform.scale(left_hand,(300,300))
centr = (w//2,h//2)
right_rect = right_hand.get_rect(center=centr)
left_rect = left_hand.get_rect(center=centr)
run = True 
while run:
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute
    second_angle = -seconds * 6
    minute_angle = -minutes * 6 
    rotated_right = pygame.transform.rotate(right_hand,minute_angle)
    rotated_left  = pygame.transform.rotate(left_hand, second_angle)
    right_rect = rotated_right.get_rect(center=centr)
    left_rect = rotated_left.get_rect(center=centr)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.blit(background, (0, 0))
    screen.blit(rotated_left, left_rect)
    screen.blit(rotated_right, right_rect)
    pygame.display.update()
    clock.tick(60)
pygame.quit()