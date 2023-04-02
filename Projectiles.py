import pygame
import numpy as np
import math as math


ORANGE = (255,128,0)

class Projectiles:

    def __init__(self,rules):
        self.max_projectiles = rules["max_projectiles"]
        self.actual_projectiles_count = 0
        
        #=  Column 0 1 : position =#
        #= Column 2 3 : direction =#
        #=     Column 4 : size    =#
        #=    Column 5 : speed    =#
        self.projectiles = np.ones([self.max_projectiles,6],dtype="float")
        self.projectiles[:,0:2] *= -1
        
        bx , by = rules["borders_X"] , rules["borders_Y"]
        self.borders = pygame.math.Vector2(bx,by)
        
        self.speed_loss = rules["speed_loss"]
        
    
    def update(self,blobs_list,blobs_infos):
        
        self.move()
        self.check_collisions(blobs_list,blobs_infos)
        
        
    def add(self, position ,  dir , size , borders ):
        
        if(self.actual_projectiles_count < self.max_projectiles):
            index = self.actual_projectiles_count
            
            self.projectiles[index,0:2] = [position.x,position.y]
            self.projectiles[index,2:4] = [dir.x,dir.y]
            self.projectiles[index,4] = size
            self.projectiles[index,5] = 6 # Speed of the projectile
            
            self.actual_projectiles_count += 1
        
    def move(self):
        for i in range(self.max_projectiles):
            if (self.projectiles[i,0] > 0 ):
                self.projectiles[i,0:2] += self.projectiles[i,2:4] * self.projectiles[i,5]
                self.projectiles[i,5] /= self.speed_loss
        
        self.projectiles[0:self.actual_projectiles_count,0] = np.clip(self.projectiles[0:self.actual_projectiles_count,0] , 0 , self.borders.x)
        
        self.projectiles[0:self.actual_projectiles_count,1] = np.clip(self.projectiles[0:self.actual_projectiles_count,1] , 0 , self.borders.y)
    
    
    def check_collisions(self,blobs_list,blobs_infos):
        i = 0
        
        while (i < self.actual_projectiles_count):
            
            for index in range(len(blobs_list)):
                
                blob = blobs_list[index]
                
                for k in range(blob.actual_sub_blob):
                    radius = np.sqrt(blobs_infos[blob.index+k,4] / np.pi)
                    
                    if(np.linalg.norm(blobs_infos[blob.index+k,0:2] - self.projectiles[i,0:2]) < radius):
                        
                        blobs_infos[k,4] += self.projectiles[i,4]
        
                        for j in range(i+1,self.actual_projectiles_count):
                            self.projectiles[j-1] = self.projectiles[j]
                        
                        self.actual_projectiles_count -= 1
                
            else:
                i += 1

    def show(self,screen,width,height,camPos):
        
        for i in range(self.actual_projectiles_count):
            screen_pos = pygame.math.Vector2(width/2+self.projectiles[i,0],height/2+self.projectiles[i,1]) - camPos

            if(screen_pos.x > 0 and screen_pos.y > 0 and screen_pos.x < width and screen_pos.y < height):
                
                radius = np.sqrt( self.projectiles[i,4] / np.pi )
                pygame.draw.circle(screen, ORANGE , screen_pos , radius)
