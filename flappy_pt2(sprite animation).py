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


class Bird(pygame.sprite.Sprite):   #Sprite is an object that represents visual elements in a game, such as characters, obstacles, or items
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #to inherit some functionality
        self.images=[] #for multiple pictures(animation) we need a list of pictures in pygame
        self.index=0
        self.counter=0 #controls speed of the animation(of flappy bird)
        for num in range(1,4): #to iterate through the list of images
            img=pygame.image.load(rf'C:\Users\DELL\Pictures\bird{num}.png') #formatted string for different bird positions
            self.images.append(img)
        self.image=self.images[self.index] #image that the sprite will output is taken fro list of images at self.index value
        self.rect=self.image.get_rect() #create rectangle from the boundaries of the image for you
        self.rect.center=[x,y]

    def update(self):
        #handle the animation
        self.counter+=1
        flap_cooldown=5

        if self.counter> flap_cooldown:
            self.counter=0
            self.index+=1
            if self.index>=len(self.images): #ensure that index counter does not go out of the list(self.images list) bound(otherwie error)
                self.index=0
        self.image=self.images[self.index] #since index is updated, update the image as well

bird_group = pygame.sprite.Group() #keeps track of all the sprites

flappy=Bird(100,int(screen_height/2)) #create an instance of bird class and determine the x and y coordinates

bird_group.add(flappy) #add flappy to bird_group

run=True #for looping through the game
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg,(0,-250)) #.blit() used for adding image to the screen

    bird_group.draw(screen) #draw is used to add the bird_group ot the window | draw is an inbuilt sprite function
    bird_group.update()

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