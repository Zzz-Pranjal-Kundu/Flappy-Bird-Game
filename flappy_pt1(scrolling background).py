import pygame
from pygame.locals import *

pygame.init() #initialize pygame

clock=pygame.time.Clock() #timer
fps=60

screen_width=850
screen_height=620

#create game window
screen=pygame.display.set_mode((screen_width,screen_height))  #blank game window
pygame.display.set_caption("Flappy Bird")

#define game variables
ground_scroll=0
scroll_speed=4 #ground moves 4 pixels every iterartion

#load images
bg=pygame.image.load(r'C:\Users\DELL\Pictures\bg.png')
ground_img=pygame.image.load(r'C:\Users\DELL\Pictures\ground.png')

run=True #for looping through the game
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg,(0,-250)) #.blit() used for adding image to the screen

    #draw and scroll the ground
    screen.blit(ground_img,(ground_scroll,460))
    ground_scroll-=scroll_speed
    if abs(ground_scroll)>35:
        ground_scroll=0

    for event in pygame.event.get(): #gets all  events that are happening
        if event.type == pygame.QUIT: #i.e. clicking the 'X' button on the top right(TO EXIT)
            run=False

    pygame.display.update() #to update everything that has happened above it and also to display the images

pygame.quit()