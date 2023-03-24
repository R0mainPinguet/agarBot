import pygame
import numpy as np

class Camera:

    def __init__(self , rules):
        bx , by = rules["borders_X"] , rules["borders_Y"]
        center_vect = pygame.math.Vector2(bx/2,by/2)

        self.pos = center_vect
        self.zoom = 1.0

    def updateZoom(self,deltaZoom):
        
        self.zoom += deltaZoom/100
        
        self.zoom = max(self.zoom,0.1)                 
        self.zoom = min(self.zoom,10)
    
    def update(self,player,blobs_infos):
        
        if(player.actual_sub_blob > 1):
            avg = np.zeros(2)
            
            for i in range(player.actual_sub_blob):
                avg += blobs_infos[i,0:2]
            
            avg /= player.actual_sub_blob
            
            self.pos = pygame.math.Vector2(avg[0],avg[1])
        else:
            self.pos = pygame.math.Vector2(blobs_infos[0,0],blobs_infos[0,1])