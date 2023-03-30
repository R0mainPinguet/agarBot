import pygame,sys
import numpy as np

from Player import Player
from Camera import Camera
from Food import Food
from Projectiles import Projectiles
from Bot import Bot

from utils import loadRules,compute_ranks

rules = loadRules("rules.txt")
print(rules)

WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()

# If player_count=0, only the bots play, and nothing is displayed
# If player_count=1, the player will be able to interact with the bots on the screen during a game
player_count , bots_count = rules["player_count"] , rules["bots_count"]
#===#

#= Window parameters =#
FPS = rules["FPS"]
width , height = rules["width"] , rules["height"]

borders_X , borders_Y = rules["borders_X"] , rules["borders_Y"]

borders_vect = pygame.math.Vector2(borders_X,borders_Y)
center_vect = pygame.math.Vector2(borders_X/2,borders_Y/2)
#==#


# Holds the player and the bots attributes and functions
blobs_list = []

# Holds the player and the bots position, speed, and size
blobs_infos = np.ones((rules["MAX_SUB_BLOB"] * (player_count+bots_count) , 5) , dtype="float")

pygame.init()
pygame.display.set_caption('Agario')

screen = pygame.display.set_mode( (width,height) )
screen_rect = screen.get_rect()

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text
    
background_rect = screen_rect
background = pygame.Surface(background_rect.size)
background.fill(BLACK)
background = background.convert()

clock = pygame.time.Clock()

player = Player(rules,blobs_infos)
cam = Camera(rules)

blobs_list.append(player)

for i in range(bots_count):
    blobs_list.append(Bot(rules,(i+player_count)*rules["MAX_SUB_BLOB"],blobs_infos))
    
food = Food(rules)
projectiles = Projectiles(rules)

running = True

while running:
    
    # Get mouse Input as a direction
    mouse_dir = pygame.math.Vector2(pygame.mouse.get_pos())
    mouse_dir.x -= width/2
    mouse_dir.y -= height/2
    target_pos = cam.pos + mouse_dir
    
    # Get Keyboard input 
    for event in pygame.event.get():
        
        #=- Ferme la fenêtre
        if event.type == pygame.QUIT:
            running = False
        
        #=- Utilise la molette
        if event.type == pygame.MOUSEWHEEL:
            cam.updateZoom(event.y)
        
        if event.type == pygame.KEYDOWN:
            
            #=- Appuie sur W
            if event.key == pygame.K_w:
                player.shoot(target_pos,projectiles,borders_vect,blobs_infos)
            
            #=- Appuie sur Espace
            if event.key == pygame.K_SPACE:
                player.split(target_pos,blobs_infos)
    
    
    #= Background Update =#
    screen.blit(background, background_rect)
    screen.blit(update_fps(), (10,10))
    #====#
    
    #= Updates =#
    projectiles.update(blobs_list,blobs_infos)
    
    player.update(target_pos,blobs_infos)
    
    for i in range(player_count,bots_count):
        blobs_list[i].update(blobs_list,blobs_infos)
        
    food.update(blobs_list,blobs_infos)
    #====#
    
    
    #=== BOT INPUTS ==#
    
    #= Compute the rank order =#
    ranks = compute_ranks(blobs_list,blobs_infos)
    #==#
    
    #======#
    
    
    #= Displays =#
    food.show(screen,width,height,cam.pos)
    
    projectiles.show(screen,width,height,cam.pos)
    
    for i in range(player_count+bots_count):
        blobs_list[i].show(screen,width,height,cam.pos,blobs_infos)
       
    cam.update(player,blobs_infos)
    
    pygame.display.flip()
    clock.tick(FPS)
    #====#
    
sys.exit()
