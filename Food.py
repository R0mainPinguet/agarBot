import pygame
import numpy as np

GREEN = (0,255,0)

class Food:

    def __init__(self, rules):
        self.MAX_FOOD = rules["max_food"]
        self.MAX_SIZE = rules["max_size"]
        
        bx , by = rules["borders_X"] , rules["borders_Y"]
        self.borders = pygame.math.Vector2(bx,by)

        #= Column 0 1 : position of the food =#
        #=          Column 2 : size          =#
        self.food = np.random.rand(self.MAX_FOOD,3)
        self.food[:,0] *= self.borders.x
        self.food[:,1] *= self.borders.y
        
        self.food[:,2] *= (self.MAX_SIZE-50)
        self.food[:,2] += 50
        
    def update(self,blobs_list,blobs_infos):
        
        for i in range(self.MAX_FOOD):
            
            for index in range(len(blobs_list)):
                
                blob = blobs_list[index]
                
                for j in range(blob.actual_sub_blob):
                    
                    radius = np.sqrt(blobs_infos[blob.index + j,4] / np.pi)
                    
                    if(np.linalg.norm(blobs_infos[blob.index + j,0:2] - self.food[i,0:2]) < radius ):
                        
                        blobs_infos[blob.index + j,4] += self.food[i,2] 
                        
                        self.food[i] = np.random.rand(3)
                        
                        self.food[i,0] *= self.borders.x
                        self.food[i,1] *= self.borders.y
                        
                        self.food[i,2] *= (self.MAX_SIZE-1)
                        self.food[i,2] += 1

                

    def show(self,screen,width,height,camPos):
        for i in range(self.MAX_FOOD):
            if(self.food[i,0]>0):
                screen_pos = pygame.math.Vector2(width/2+self.food[i,0],height/2+self.food[i,1]) - camPos
                if(screen_pos.x > 0 and screen_pos.y > 0 and screen_pos.x < width and screen_pos.y < height):
                    radius = np.sqrt(self.food[i,2] / np.pi)
                    
                    pygame.draw.circle(screen, GREEN , screen_pos , radius )
