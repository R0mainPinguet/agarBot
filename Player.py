import pygame
import numpy as np
from Projectiles import Projectiles
from Food import Food

WHITE = 255,255,255
GREY = 128,128,128

def deflate_func(x):
    return( max(x-2000,0)/10000 )
    

class Player:

    def __init__(self , rules , blobs_infos):
        
        self.type = "player"
        
        self.MAX_SUB_BLOB = rules["MAX_SUB_BLOB"]
        self.actual_sub_blob = 1
        
        self.index = 0
        
        bx , by = rules["borders_X"] , rules["borders_Y"]
        self.borders = pygame.math.Vector2(bx,by)
        
        #= Default speed and size =#
        self.df_speed = rules["df_speed"]
        self.df_size = rules["df_size"]
        
        #=  Number of frames before merging two sub cells =#
        #= For example, 600 frames = 10 seconds at 60 fps =#
        self.merge_time = rules["merge_time"]
        
        #= The blob can shoot projectiles after having a size bigger than shoot_projectile =#
        self.shoot_threshold = rules["shoot_threshold"]
        
        #= The blob can split itself after having a size bigger than division_threshold =#
        self.division_threshold = rules["division_threshold"]
        
        # How size influences speed ( the bigger the faster ) =#
        self.viscosity = rules["viscosity"]
        
        # How much of the mass is converted into a projectile =#
        self.projectile_percentage = rules["projectile_percentage"]
        
        #================================#
        #= Column 0 1 : Position Vector =#
        #=  Column 2 3 : Speed Vector   =#
        #=         Column 4 : Size      =#
        blobs_infos[0,0:2] = [bx/2,by/2]
        blobs_infos[0,2:4] = np.array([0,0])
        blobs_infos[0,4] = self.df_size
        #================================#
        
        #= Split array =#
        #= Column 0 1 : Pair of index =#
        #= Column 2  : Remaining frames =#
        self.splitArray = np.zeros((self.MAX_SUB_BLOB,3),dtype="int")
        self.pairs = 0
        #==#

        

    def eat_food(self,index,amount,blobs_infos):
        blobs_infos[index,4] += amount 
        
    def move(self,target_pos,blobs_infos):
               
        for i in range(self.actual_sub_blob):
            radius_i = np.sqrt(blobs_infos[i,4] / np.pi)
            
            direction = target_pos - pygame.math.Vector2(blobs_infos[i,0],blobs_infos[i,1])
            direction.normalize_ip()
            
            speedCoeff = np.exp((-max(blobs_infos[i,4],2*self.df_size)+2*self.df_size)/self.viscosity)
            
            blobs_infos[i,2:4] = ( blobs_infos[i,2:4] + direction * self.df_speed * speedCoeff) / 2
            
            new_pos = blobs_infos[i,0:2] + blobs_infos[i,2:4]
            
            
            for j in range(self.actual_sub_blob):
                
                if(j!=i):
                    radius_j = np.sqrt(blobs_infos[j,4] / np.pi)
                
                    # Collision !
                    dist = np.linalg.norm(new_pos - blobs_infos[j,0:2])
                    if( dist < radius_i+radius_j):
                        
                        dir = (blobs_infos[i,0:2] - blobs_infos[j,0:2])
                        dir = dir / np.linalg.norm(dir)
                        
                        new_pos = new_pos + dir*(radius_i+radius_j-dist)
                        
            
            blobs_infos[i,0:2] = new_pos
            
            
        blobs_infos[0:self.actual_sub_blob,0] = np.clip(blobs_infos[0:self.actual_sub_blob,0] , 0 , self.borders.x)
        blobs_infos[0:self.actual_sub_blob,1] = np.clip(blobs_infos[0:self.actual_sub_blob,1] , 0 , self.borders.y)
            
    def deflate(self,blobs_infos):
        
        for i in range(self.actual_sub_blob):
            blobs_infos[i,4] -= deflate_func(blobs_infos[i,4])
        
        
    def shoot(self,target_pos,projectiles,borders,blobs_infos):
        
        for i in range(self.actual_sub_blob):
            direction = target_pos - pygame.math.Vector2(blobs_infos[i,0],blobs_infos[i,1])
            direction.normalize_ip()
            
            size = blobs_infos[i,4]
            
            if(size > self.df_size/8):
                
                pos = pygame.math.Vector2(blobs_infos[i,0],blobs_infos[i,1])
                radius = np.sqrt( size / np.pi )
                
                projectile_size = size * self.projectile_percentage
                projectile_position = pos + pygame.math.Vector2((radius+2)*direction.x,(radius+2)*direction.y)
            
                blobs_infos[i,4] -= projectile_size
                projectiles.add( projectile_position , direction , projectile_size , borders )
        

    def split(self,target_pos,blobs_infos):
        
        for i in range(self.actual_sub_blob):
            direction = target_pos - pygame.math.Vector2(blobs_infos[i,0],blobs_infos[i,1])
            direction.normalize_ip()
            
            size = blobs_infos[i,4]
            
            if(size > self.division_threshold/8): 

                radius = np.sqrt( size / np.pi )
                
                #= Position Updates =#
                blobs_infos[self.actual_sub_blob,0:2] = blobs_infos[i,0:2] + (radius+25)*np.array([direction.x,direction.y])
                
                #= Speed Updates =#
                blobs_infos[self.actual_sub_blob,2:4] = blobs_infos[i,2:4]*5
                
                #= Size Updates =#
                blobs_infos[i,4] /= 2
                blobs_infos[self.actual_sub_blob,4] = blobs_infos[i,4]
                
                #= Pairs Updates =#
                self.splitArray[self.pairs] = np.array([i,self.actual_sub_blob,self.merge_time])
                
                self.actual_sub_blob += 1
                self.pairs += 1
                
                
    def join(self,blobs_infos):
        
        if( self.actual_sub_blob > 1 ):
            
            for i in range(self.pairs):
                self.splitArray[i,2] -= 1
                
                
                if( self.splitArray[i,2] == 0 ):
                    
                    ind1 = self.splitArray[i,0]
                    ind2 = self.splitArray[i,1]
                    
                    # Merge the two cells from the sub array
                    blobs_infos[ind1,0:4] = (blobs_infos[ind1,0:4] + blobs_infos[ind2,0:4])/2
                    
                    blobs_infos[ind1,4] += blobs_infos[ind2,4]
                    
                    
                    # Reorganize the array
                    for j in range(ind2+1,self.actual_sub_blob):
                        blobs_infos[j-1] = blobs_infos[j]
                    
                    
                    # Update the indexes inside splitArray
                    for j in range(self.pairs):
                        
                        if( j>=i and j+1<self.pairs ):
                            self.splitArray[j] = self.splitArray[j+1]
                        
                        if(self.splitArray[j,0] > ind2):
                            self.splitArray[j,0] -= 1
                        
                        if(self.splitArray[j,1] > ind2):
                            self.splitArray[j,1] -= 1
                        
                    self.pairs -= 1
                    self.actual_sub_blob -= 1
    
    
    def show(self,screen,width,height,camPos,blobs_infos):
        
        for i in range(self.actual_sub_blob):
            screen_pos = pygame.math.Vector2(width/2+blobs_infos[i,0],height/2+blobs_infos[i,1]) - camPos
    
            if(screen_pos.x > 0 and screen_pos.y > 0 and screen_pos.x < width and screen_pos.y < height):
                
                radius = np.sqrt( blobs_infos[i,4] / np.pi )
                if(i==0):
                    pygame.draw.circle(screen, WHITE, screen_pos , radius )
                else:
                    pygame.draw.circle(screen, GREY , screen_pos , radius )
            
    
        
    
