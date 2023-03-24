import sys, pygame
import numpy as np

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 60

size = width, height = 600, 600
speed = np.array([10,8])

pygame.init()
pygame.display.set_caption('Test Game')

screen = pygame.display.set_mode( (width,height) )
screen_rect = screen.get_rect()

background_rect = screen_rect
background = pygame.Surface(background_rect.size)
background.fill(BLACK)
background = background.convert()

clock = pygame.time.Clock()

ballPos = np.array([60,300])
ballRadius=50

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballPos += speed
    if ballPos[0]-ballRadius < 0 or ballPos[0]+ballRadius > width:
        speed[0] = -speed[0]
    if ballPos[1]-ballRadius < 0 or ballPos[1]+ballRadius > height:
        speed[1] = -speed[1]

    screen.blit(background, background_rect)
    pygame.draw.circle(screen, WHITE, ballPos , 50)

    pygame.display.flip()
    

    clock.tick(FPS)
               
