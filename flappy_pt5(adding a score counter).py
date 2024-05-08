import pygame
from pygame.locals import *
import random

pygame.init() #initialize pygame

clock=pygame.time.Clock() #timer
fps=60

screen_width=850
screen_height=620

#create game window
screen=pygame.display.set_mode((screen_width,screen_height))  #blank game window
pygame.display.set_caption("Flappy Bird")

#define font 
font=pygame.font.SysFont('Bauhaus 93',60)
#define text color
white=(255,255,255)

#define game variables
ground_scroll=0
scroll_speed=4 #ground moves 4 pixels every iterartion
flying=False
game_over=False
pipe_gap=150
pipe_frequency=1600 #1600 milisecond gap (1.6 sec)
last_pipe=pygame.time.get_ticks() - pipe_frequency #to check when last pipe was created and compare it to current time | takes measure of the time whenever the game starts (-pipe_frequency so that pipes start showing as soon  as we begin)
score=0
pass_pipe=False


#load images
bg=pygame.image.load(r'C:\Users\DELL\Pictures\bg.png')
ground_img=pygame.image.load(r'C:\Users\DELL\Pictures\ground.png')


def draw_text(text,font,text_color,x,y):
    img=font.render(text,True,text_color) #converts font to image
    screen.blit(img,(x,y)) #to display the score on the screen

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
        self.vel=0  #flight velocity of the bird
        self.clicked=False #to keep track of click and release of mouse

    def update(self):
        if flying==True:
            #gravity
            self.vel+=0.5  #increase the y-axis velocity every iteration (works as gravity)
            if self.vel>8:
                self.vel=8
            if self.rect.bottom < 490: #check to ensure that the bird drops only to the ground
                self.rect.y+=int(self.vel)

        if game_over==False: #for the bird to flap and fly only when game is not over
            #jump
            if (pygame.mouse.get_pressed()[0]==1 or pygame.mouse.get_pressed()[1]==1) and self.clicked==False: #checks for mouse left(left is at idx 0) or right(right is at idx 1) clicks
                self.clicked=True
                self.vel=-5
            if (pygame.mouse.get_pressed()[0]==1 or pygame.mouse.get_pressed()[1]==1): #checks for mouse release
                self.clicked=False

            #handle the animation
            self.counter+=1
            flap_cooldown=5

            if self.counter> flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images): #ensure that index counter does not go out of the list(self.images list) bound(otherwie error)
                    self.index=0
            self.image=self.images[self.index] #since index is updated, update the image as well

            #rotate the bird image
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2) #rotation relative to velocity | default angle of rotatin: anti clock wise thus -ve
        else:
            self.image=pygame.transform.rotate(self.images[self.index],-90) #to make the bird fall vertically face down on game over



class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(r'C:\Users\DELL\Pictures\pipe.png')
        self.rect=self.image.get_rect()
        #positio 1 from the top and -1 is from the bottom
        if position == 1:
            self.image=pygame.transform.flip(self.image,False,True) #flip the image along y axis(thus false,true)
            self.rect.bottomleft=[x,y-int(pipe_gap/2)] #y coordinate adjusted to ensure proper pipe gaps
        if position == -1:
            self.rect.topleft=[x,y+int(pipe_gap/2)] #y coordinate adjusted to ensure proper pipe gaps

    def update(self): #for scrolling pipes
        self.rect.x -= scroll_speed
        if self.rect.right<0: #to erase the pipes from memory once they exit the screen view
            self.kill()


bird_group = pygame.sprite.Group() #keeps track of all the sprites of bird class
pipe_group = pygame.sprite.Group() #keeps track of all the sprites of bird class

#instance of bird class
flappy=Bird(100,int(screen_height/2)) #create an instance of bird class and determine the x and y coordinates
bird_group.add(flappy) #add flappy to bird_group


#instantiated in the main game running loop to ensure that pipes are created only until game is not yet over
# #instance of pipe class
# btm_pipe=Pipe(300,int(screen_height/2),-1) #create an instance of pipe class and determine the x and y coordinates and position -1
# top_pipe=Pipe(300,int(screen_height/2),1) #create an instance of pipe class and determine the x and y coordinates and position 1
# pipe_group.add(btm_pipe) #add btm_pipe to pipe_group
# pipe_group.add(top_pipe) #add top_pipe to pipe_group

#running logic of the game
run=True #for looping through the game
while run:

    clock.tick(fps)

    #draw background
    screen.blit(bg,(0,-250)) #.blit() used for adding image to the screen
    
    bird_group.draw(screen) #draw is used to add the bird_group ot the window | draw is an inbuilt sprite function
    bird_group.update() #update changes after every iteration
    pipe_group.draw(screen) #draw is used to add the pipe_group ot the window | draw is an inbuilt sprite function
    # pipe_group.update() #update changes after every iteration (added with draw and scrolling ground to stop generating once game is over)

    #look for collision
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top<0: #the 2 agruments set to false kills the objects on collision(for eg. on bullets hitting the enemies, which in this case is not required thus false) if 1st true->the would be killed(dltd) and 2nd true->the pipe would be killed(dltd)
        # flappy.rect.top<0 checks for collision with the top of the screen window
        game_over=True

    #check if bird has hit the ground
    if flappy.rect.bottom>=490:
        game_over=True
        flying=False

    #draw and scroll the ground
    screen.blit(ground_img,(ground_scroll,490))

    #check the score
    if len(pipe_group)>0: #to ensure that checking begins only after pipes have started generating
        if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right<pipe_group.sprites()[0].rect.right\
            and pass_pipe==False :  # \ allows next line here | checking if the bird has crossed the left boundary of the pipe and is yet to cross the right boundary
            pass_pipe=True

        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left>pipe_group.sprites()[0].rect.right: #to ensure bird has crossed the right boundary of the pipe in order to increase the score by 1 and reset the pass_pipe trigger
                score+=1
                pass_pipe=False

        draw_text(str(score),font,white,int(screen_width/2),20)


    if game_over==False and flying==True:  #for checking if game has started and is still in progress
        #generate new pipes
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipe_frequency:
            pipe_height=random.randint(-110,110) #for randowm and varying pipe heights
            #instance of pipe class
            btm_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,-1) #create an instance of pipe class and determine the x and y coordinates and position -1
            top_pipe=Pipe(screen_width,int(screen_height/2)+pipe_height,1) #create an instance of pipe class and determine the x and y coordinates and position 1
            pipe_group.add(btm_pipe) #add btm_pipe to pipe_group
            pipe_group.add(top_pipe) #add top_pipe to pipe_group
            last_pipe=time_now

        pipe_group.update() #update changes after every iteration

        #so that ground scrolls when game_over is False
        ground_scroll-=scroll_speed
        if abs(ground_scroll)>=35:
            ground_scroll=0

    #event handler
    for event in pygame.event.get(): #gets all  events that are happening
        if event.type == pygame.QUIT: #i.e. clicking the 'X' button on the top right(TO EXIT)
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False and game_over==False: #to start flyig on first mouse click
            flying=True

    pygame.display.update() #to update everything that has happened above it and also to display the images

pygame.quit()