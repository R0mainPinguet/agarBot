import pygame
import numpy as np
from Projectiles import Projectiles

RED = (255,0,0)

WHITE = 255,255,255
GREY = 128,128,128

def deflate_func(x):
    return( max(x-2000,0)/10000 )
    

class Bot:

    def __init__(self , rules , index , blobs_infos):
        
        self.type = "bot"
        
        self.MAX_SUB_BLOB = rules["MAX_SUB_BLOB"]
        self.actual_sub_blob = 1
        
        self.index = index
        
        bx , by = rules["borders_X"] , rules["borders_Y"]
        self.borders = pygame.math.Vector2(bx,by)
        
        #= Default speed and size =#
        self.df_speed = rules["df_speed"]
        self.df_size = rules["df_size"]
        self.global_size = self.df_size
        
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
        blobs_infos[self.index,0:2] = [10,10]
        blobs_infos[self.index,2:4] = [0,0]
        blobs_infos[self.index,4] = self.df_size
        #================================#
        
        #= Split array =#
        #= Column 0 1 : Pair of index =#
        #= Column 2  : Remaining frames =#
        self.splitArray = np.zeros((self.MAX_SUB_BLOB,3),dtype="int")
        self.pairs = 0
        #==#
        
        #= Dictionary of possible inputs =#
        self.informations = dict()

        
    # Bot AI Decomposition :
    #
    #= 1 - See
    #==  Get informations on :
    #==    - It's current state
    #==    - Other players state
    #==    - Available food / projectiles nearby
    #
    #= 2 - Think
    #==  Feed the data inside the neural network.
    #
    #= 3 - Act
    #==  Move and possibly shoot / divide itself.
    #
    #= 4 - Learn (?)
    #==  Reward or not according to the player current state.
    
    def update(self,blobs_list,blobs_infos):
        
        self.compute_size()
        
    
    
    def compute_size(self,blobs_infos):
        self.global_size = np.sum(blobs_infos[self.index:self.index+self.actual_sub_blob,4])
        
    
    def observe(self,blobs_list,blobs_infos):
        '''
        Collect informations on it's surrounding, such as :
            - Closest ennemy distance and index
            - Closest food/projectile distance and index
            - Own size, rank
        '''
        
        #= bot size =#
        self.informations["own_size"] = self.global_size
        
        
        
        
        
    def think(self):
        '''
        Send these informations to the bot's brain, and retrieve the output
        '''
    
    def act(self):
        '''
        Act according to the brain output
        '''
    
    
    def eat_food(self,index,amount):
        self.sub_blobs[index,4] += amount 
    
    
    def move(self,target_pos):
               
        for i in range(self.actual_sub_blob):
            radius_i = np.sqrt(self.sub_blobs[i,4] / np.pi)
            
            direction = target_pos - pygame.math.Vector2(self.sub_blobs[i,0],self.sub_blobs[i,1])
            direction.normalize_ip()
            
            speedCoeff = np.exp((-max(self.sub_blobs[i,4],2*self.df_size)+2*self.df_size)/self.viscosity)
            
            self.sub_blobs[i,2:4] = ( self.sub_blobs[i,2:4] + direction * self.df_speed * speedCoeff) / 2
            
            new_pos = self.sub_blobs[i,0:2] + self.sub_blobs[i,2:4]
            
            
            #= Collision part =#
            for j in range(self.actual_sub_blob):
                
                if(j!=i):
                    radius_j = np.sqrt(self.sub_blobs[j,4] / np.pi)
                
                    # Collision !
                    dist = np.linalg.norm(new_pos - self.sub_blobs[j,0:2])
                    if( dist < radius_i+radius_j):
                        
                        dir = (self.sub_blobs[i,0:2] - self.sub_blobs[j,0:2])
                        dir = dir / np.linalg.norm(dir)
                        
                        new_pos = new_pos + dir*(radius_i+radius_j-dist)
            #==#
            
            self.sub_blobs[i,0:2] = new_pos
            
            
        self.sub_blobs[0:self.actual_sub_blob,0] = np.clip(self.sub_blobs[0:self.actual_sub_blob,0] , 0 , self.borders.x)
        self.sub_blobs[0:self.actual_sub_blob,1] = np.clip(self.sub_blobs[0:self.actual_sub_blob,1] , 0 , self.borders.y)
            
    def deflate(self):
        
        for i in range(self.actual_sub_blob):
            self.sub_blobs[i,4] -= deflate_func(self.sub_blobs[i,4])
        
        
    def shoot(self,target_pos,projectiles,borders):
        
        for i in range(self.actual_sub_blob):
            direction = target_pos - pygame.math.Vector2(self.sub_blobs[i,0],self.sub_blobs[i,1])
            direction.normalize_ip()
            
            size = self.sub_blobs[i,4]
            
            if(size > self.df_size/8):
                
                pos = pygame.math.Vector2(self.sub_blobs[i,0],self.sub_blobs[i,1])
                radius = np.sqrt( size / np.pi )
                
                projectile_size = size * self.projectile_percentage
                projectile_position = pos + pygame.math.Vector2((radius+2)*direction.x,(radius+2)*direction.y)
            
                self.sub_blobs[i,4] -= projectile_size
                projectiles.add( projectile_position , direction , projectile_size , borders )
        

    def split(self,target_pos):
        
        for i in range(self.actual_sub_blob):
            direction = target_pos - pygame.math.Vector2(self.sub_blobs[i,0],self.sub_blobs[i,1])
            direction.normalize_ip()
            
            size = self.sub_blobs[i,4]
            
            if(size > self.division_threshold/8): 

                radius = np.sqrt( size / np.pi )
                
                #= Position Updates =#
                self.sub_blobs[self.actual_sub_blob,0:2] = self.sub_blobs[i,0:2] + (radius+25)*np.array([direction.x,direction.y])
                
                #= Speed Updates =#
                self.sub_blobs[self.actual_sub_blob,2:4] = self.sub_blobs[i,2:4]*5
                
                #= Size Updates =#
                self.sub_blobs[i,4] /= 2
                self.sub_blobs[self.actual_sub_blob,4] = self.sub_blobs[i,4]
                
                #= Pairs Updates =#
                self.splitArray[self.pairs] = np.array([i,self.actual_sub_blob,self.merge_time])
                
                self.actual_sub_blob += 1
                self.pairs += 1
                
                
    def join(self):
        
        if( self.actual_sub_blob > 1 ):
            
            for i in range(self.pairs):
                self.splitArray[i,2] -= 1
                
                
                if( self.splitArray[i,2] == 0 ):
                    
                    ind1 = self.splitArray[i,0]
                    ind2 = self.splitArray[i,1]
                    
                    # Merge the two cells from the sub array
                    self.sub_blobs[ind1,0:4] = (self.sub_blobs[ind1,0:4] + self.sub_blobs[ind2,0:4])/2
                    
                    self.sub_blobs[ind1,4] += self.sub_blobs[ind2,4]
                    
                    
                    # Reorganize the array
                    for j in range(ind2+1,self.actual_sub_blob):
                        self.sub_blobs[j-1] = self.sub_blobs[j]
                    
                    
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
            screen_pos = pygame.math.Vector2(width/2+blobs_infos[self.index+i,0],height/2+blobs_infos[self.index+i,1]) - camPos

            if(screen_pos.x > 0 and screen_pos.y > 0 and screen_pos.x < width and screen_pos.y < height):
                
                radius = np.sqrt( blobs_infos[self.index+i,4] / np.pi )
                
                pygame.draw.circle(screen, RED , screen_pos , radius )
            
                pygame.draw.circle(screen, RED , screen_pos , radius )
    
    
    
