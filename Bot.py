import pygame
import numpy as np
from Projectiles import Projectiles
from Brain import Brain

from utils import deflate_func,speed_coeff_func

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
        
        #  The index inside blobs_infos
        self.index = index
        
        # The index inside blobs_list
        self.ID = index // rules["MAX_SUB_BLOB"]
        
        
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
        
        self.compute_personal_data(blobs_infos)
        
        #= Split array =#
        #= Column 0 1 : Pair of index =#
        #= Column 2  : Remaining frames =#
        self.splitArray = np.zeros((self.MAX_SUB_BLOB,3),dtype="int")
        self.pairs = 0
        #==#
        
        #= Brain part =#
        self.genomeSize = rules["genomeSize"]
        self.brain = Brain(self.genomeSize)
        
        print("#== BRAIN ==#")
        print(self.brain)
        print("#====#")
        
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
    
    
    def update(self,blobs_list,blobs_infos,external_data,food,projectiles):
                
        self.compute_personal_data(blobs_infos)
        
        self.observe(blobs_list,blobs_infos,external_data)
        
        self.think()
        
        self.act(blobs_list,blobs_infos,external_data,food,projectiles)
        
        self.deflate(blobs_infos)
        self.join(blobs_infos)
        
    
    
    def observe(self,blobs_list,blobs_infos,external_data):
        '''
        Collect informations on it's surrounding, such as :
            - Closest ennemy distance and index
            - Closest food/projectile distance and index
            - Own size, rank
        '''
        
        #= bot size =#
        self.informations["own_size"] = self.global_size
        
        #= Distance relative to the closest ennemy, food and projectile =#
        self.informations["closest_ennemy_distance"] = np.min(external_data["distances"][self.ID])
        
        # self.informations["closest_food_distance"] = self.closest_food_distance
        # self.informations["closest_projectile_distance"] = self.closest_projectile_distance
        
        #= Global informations : rank, number of frames
        self.informations["rank"] = external_data["ranks"][self.ID]
        self.informations["frame"] = external_data["frame"]
    
    
    def think(self):
        '''
        Send these informations to the bot's brain, and retrieve the output
        '''
        self.brainOutput = self.brain.shoot( self.informations )
    
    
    def act(self,blob_list,blobs_infos,external_data,food,projectiles):
        '''
        Act according to the brain output.
        List of outputs so far :
            "Horizontal" -> Horizontal Movement
            "Vertical" -> Vertical Movemement
            "Move_Closest_Ennemy" -> Movement with the direction of the closest ennemy
            "Move_Closest_Food" -> Movement with the direction of the closest food
            "Move_Closest_Projectile" -> Movement with the direction of the closest projectile
        '''
        
        closest_ennemy = np.argmin(external_data["distances"][self.ID])
        
        #== Moving ==#
        normal_mov = np.array([self.brainOutput["Horizontal"],self.brainOutput["Vertical"]])
        
        ennemy_mov = self.brainOutput["Move_Closest_Ennemy"] * blob_list[closest_ennemy].center_of_gravity
        
        # food_mov = self.brainOutput["Move_Closest_Food"] * np.array([])    
        food_mov = np.zeros(2)    
        
        # projectile_mov = self.brainOutput["Move_Closest_Projectile"] * np.array([])
        projectile_mov = np.zeros(2)
        
        global_mov = normal_mov + ennemy_mov + food_mov + projectile_mov
        if(np.linalg.norm(global_mov) != 0):
            global_mov = global_mov / np.linalg.norm(global_mov)
        
        target_pos = self.center_of_gravity + global_mov
        self.move(target_pos,blobs_infos)
        #====#
        
        #== Shooting ==#
        
        
        #====#
        
        #== Splitting ==#
        
        #====#
        
        
    def move(self,target_pos,blobs_infos):
               
        for i in range(self.index,self.index+self.actual_sub_blob):
            radius_i = np.sqrt(blobs_infos[i,4] / np.pi)
            
            direction = target_pos - blobs_infos[i,0:2]
            if(np.linalg.norm(direction) != 0):
                direction = direction / np.linalg.norm(direction)
            
            speedCoeff = speed_coeff_func(blobs_infos[i,4],self.df_size,self.viscosity) 
            
            blobs_infos[i,2:4] = ( blobs_infos[i,2:4] + direction * self.df_speed * speedCoeff) / 2
            
            new_pos = blobs_infos[i,0:2] + blobs_infos[i,2:4]
            
            
            for j in range(self.index,self.index+self.actual_sub_blob):
                
                if(j!=i):
                    radius_j = np.sqrt(blobs_infos[j,4] / np.pi)
                
                    # Collision !
                    dist = np.linalg.norm(new_pos - blobs_infos[j,0:2])
                    if( dist < radius_i+radius_j):
                        
                        dir = (blobs_infos[i,0:2] - blobs_infos[j,0:2])
                        dir = dir / np.linalg.norm(dir)
                        
                        new_pos = new_pos + dir*(radius_i+radius_j-dist)
                        
            
            blobs_infos[i,0:2] = new_pos
            
            
        blobs_infos[self.index:self.index+self.actual_sub_blob,0] = np.clip(blobs_infos[self.index:self.index+self.actual_sub_blob,0] , 0 , self.borders.x)
        blobs_infos[self.index:self.index+self.actual_sub_blob,1] = np.clip(blobs_infos[self.index:self.index+self.actual_sub_blob,1] , 0 , self.borders.y)
    
    def deflate(self,blobs_infos):
        
        for i in range(self.index,self.index+self.actual_sub_blob):
            blobs_infos[i,4] -= deflate_func(blobs_infos[i,4])
        
        
    def shoot(self,target_pos,projectiles,borders,blobs_infos):
        
        for i in range(self.index,self.index+self.actual_sub_blob):
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
        
        for i in range(self.index,self.index+self.actual_sub_blob):
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
        
        for i in range(self.index,self.index+self.actual_sub_blob):
            screen_pos = pygame.math.Vector2(width/2+blobs_infos[i,0],height/2+blobs_infos[i,1]) - camPos

            if(screen_pos.x > 0 and screen_pos.y > 0 and screen_pos.x < width and screen_pos.y < height):
                
                radius = np.sqrt( blobs_infos[i,4] / np.pi )
                
                pygame.draw.circle(screen, RED , screen_pos , radius )
            
                pygame.draw.circle(screen, RED , screen_pos , radius )
    
    
    
    
    def compute_personal_data(self,blobs_infos):
        '''
        Compute the size, center of gravity
        '''
        
        self.global_size = np.sum(blobs_infos[self.index:self.index+self.actual_sub_blob,4])
        self.center_of_gravity = np.average(blobs_infos[self.index:self.index+self.actual_sub_blob,0:2] , axis=0)
        
    
    def compute_closest_food(self,food):
        '''
        Compute the closest food index
        '''        
        pass
        # self.closest_food_index = 
    
        
    def compute_closest_projectile(self,projectiles):
        '''
        Compute the closest projectile index
        '''
        pass
        # self.closest_projectile_index = 
