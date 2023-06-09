import pygame
import numpy as np
from Projectiles import Projectiles
from Brain import Brain

from utils import deflate_func,speed_coeff_func,check_collisions

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
        
        self.bx , self.by = rules["borders_X"] , rules["borders_Y"]
        self.borders = pygame.math.Vector2(self.bx,self.by)
        
        #= Default speed and size =#
        self.df_speed = rules["df_speed"]
        
        self.df_size = rules["df_size"]
        self.global_size = self.df_size
        self.fitness = self.df_size
        
        #=  Number of frames before merging two sub cells =#
        #= For example, 600 frames = 10 seconds at 60 fps =#
        self.merge_time = rules["merge_time"]
        self.collisions_test = np.zeros(self.MAX_SUB_BLOB,dtype="bool")
        self.collisions_time = np.zeros(self.MAX_SUB_BLOB,dtype="float")
        
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
        angle = 2*np.pi*self.ID/rules["bots_count"]
        blobs_infos[self.index,0:2] = [self.bx/2 + self.bx*np.cos(angle)/4 , self.by/2 + self.by*np.sin(angle)/4]
        blobs_infos[self.index,2:4] = [0,0]
        blobs_infos[self.index,4] = self.df_size
        #================================#
        
        self.compute_personal_data(blobs_infos)
        
        #= Brain part =#
        self.brain = Brain(rules)
        
        # print("#== BRAIN ==#")
        # print(self.brain)
        # print("#====#")
        
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
        self.informations["size"] = self.global_size
        
        self.informations["longest_distance"] = external_data["longest_distance"]
        #= Distance relative to the closest ennemy, food and projectile =#
        closest_ennemy_index = np.argmin(external_data["distances"][self.ID])
        
        self.informations["closest_ennemy_distance"] = external_data["distances"][self.ID,closest_ennemy_index]
        self.informations["closest_ennemy_index"] = closest_ennemy_index
        self.informations["closest_ennemy_size"] = blobs_list[closest_ennemy_index].global_size
        
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
        
        closest_food = self.compute_closest_food(food)
        
        closest_projectile = self.compute_closest_projectile(projectiles)
        
        #== Moving ==#
        normal_mov = np.array([self.brainOutput["Horizontal"],self.brainOutput["Vertical"]])
        
        ennemy_mov = self.brainOutput["Move_Closest_Ennemy"] * (blob_list[closest_ennemy].center_of_gravity-self.center_of_gravity)
        
        food_mov = self.brainOutput["Move_Closest_Food"] * (food.food[closest_food,0:2]-self.center_of_gravity)
        
        if(closest_projectile == -1):
            projectile_mov = np.zeros(2)
        else:
            projectile_mov = self.brainOutput["Move_Closest_Projectile"] * (projectiles.projectiles[closest_projectile,0:2]-self.center_of_gravity)
        
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
                
                if((j!=i) and (self.collisions_test[j-self.index] or self.collisions_test[i-self.index])):
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
            
            if(size > self.df_size):
                
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
            
            if(size > self.division_threshold): 

                radius = np.sqrt( size / np.pi )
                
                #= Position Updates =#
                blobs_infos[self.actual_sub_blob,0:2] = blobs_infos[i,0:2] + (radius+25)*np.array([direction.x,direction.y])
                
                #= Speed Updates =#
                blobs_infos[self.actual_sub_blob,2:4] = blobs_infos[i,2:4]*5
                
                #= Size Updates =#
                blobs_infos[i,4] /= 2
                blobs_infos[self.actual_sub_blob,4] = blobs_infos[i,4]
                
                #= Collisions Updates =#
                self.collisions_test[i-self.index] = True
                self.collisions_test[self.actual_sub_blob] = True
                
                self.collisions_time[i-self.index] = self.merge_time 
                self.collisions_time[self.actual_sub_blob] = self.merge_time 
                
                self.actual_sub_blob += 1
                
                
    def join(self,blobs_infos):
        '''
        Deals with the merge time of sub_blobs, as well as when sub_blobs are re-joining after a split
        '''
        
        if( self.actual_sub_blob > 1 ):
            
            for i in range(self.actual_sub_blob):
                
                if(self.collisions_test[i]):
                    
                    self.collisions_time[i] -= 1
                    
                    if( self.collisions_time[i] == 0 ):
                        
                        self.collisions_test[i] = False
                        
          
        for i in range(self.index,self.index+self.actual_sub_blob-1):
            radius_i = np.sqrt(blobs_infos[i,4] / np.pi)
                
            for j in range(i+1,self.index+self.actual_sub_blob):
                radius_j = np.sqrt(blobs_infos[j,4] / np.pi)
                
                dist = np.linalg.norm( blobs_infos[i,0:2] - blobs_infos[j,0:2] )
                
                if( dist < max(radius_i,radius_j) ) :
                    
                    # Merge the two cells from the sub array
                    blobs_infos[i,0:4] = (blobs_infos[i,0:4] + blobs_infos[j,0:4])/2
                    
                    blobs_infos[i,4] += blobs_infos[j,4]
                    
                    # Reorganize the array
                    for k in range(j+1,self.index+self.actual_sub_blob):
                        blobs_infos[k-1] = blobs_infos[k]
                    
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
        
        #= The fitness at the end is the max size of the blob =#
        if(self.global_size > self.fitness):
            self.fitness = self.global_size
        
        
        
        
    def compute_closest_food(self,food):
        '''
        Compute the closest food index
        '''        
        closest_food_index = 0
        closest_food_distance = 1e9
        
        for i in range(food.MAX_FOOD):
            dist = np.linalg.norm(self.center_of_gravity - food.food[i,0:2])
            if( dist < closest_food_distance):
                closest_food_index = i
                closest_food_distance = dist
        
        return(closest_food_index)
        
    def compute_closest_projectile(self,projectiles):
        '''
        Compute the closest projectile index
        '''
        closest_proj_index = -1
        closest_proj_distance = 1e9
        
        for i in range(projectiles.actual_projectiles_count):
            dist = np.linalg.norm(self.center_of_gravity - projectiles.projectiles[i,0:2])
            if( dist < closest_proj_distance):
                closest_proj_index = i
                closest_proj_distance = dist
        
        return(closest_proj_index)
        
        
    def respawn(self,blobs_list,blobs_infos,rules):
        
        self.actual_sub_blob = 1

        bx , by = rules["borders_X"] , rules["borders_Y"]
        
        self.collisions_test = np.zeros(self.MAX_SUB_BLOB,dtype="bool")
        self.collisions_time = np.zeros(self.MAX_SUB_BLOB,dtype="float")
        
        #================================#
        #= Column 0 1 : Position Vector =#
        #=  Column 2 3 : Speed Vector   =#
        #=         Column 4 : Size      =#
        collides = True
        
        while(collides):
            
            collides = False
            
            pos = np.array([np.random.randint(0,bx),np.random.randint(0,by)],dtype="float")
            
            i = 0
            while(i < len(blobs_list) and not collides):
                
                for j in range(blobs_list[i].actual_sub_blob):
                    radius = np.sqrt(blobs_infos[blobs_list[i].index+j,4] / np.pi) 
                
                    if( np.linalg.norm(pos - blobs_infos[blobs_list[i].index+j,0:2]) < radius ):
                        collides = True
                
                i += 1
        
        blobs_infos[self.index,0:2] = pos
        blobs_infos[self.index,2:4] = [0,0]
        blobs_infos[self.index,4] = self.df_size
        #================================#
        
        self.compute_personal_data(blobs_infos)

    def reset(self , rules , blobs_infos):
        
        self.actual_sub_blob = 1
                
        self.global_size = self.df_size
        self.fitness = self.df_size
        
        self.collisions_test = np.zeros(self.MAX_SUB_BLOB,dtype="bool")
        self.collisions_time = np.zeros(self.MAX_SUB_BLOB,dtype="float")
        
        #============================#
        #= Column 0 1 : Position Vector =#
        #=  Column 2 3 : Speed Vector   =#
        #=         Column 4 : Size      =#
        angle = 2*np.pi*self.ID/rules["bots_count"]
        blobs_infos[self.index,0:2] = [self.bx/2 + self.bx*np.cos(angle)/4 , self.by/2 + self.by*np.sin(angle)/4]
        blobs_infos[self.index,2:4] = [0,0]
        blobs_infos[self.index,4] = self.df_size
        #================================#
        
        self.compute_personal_data(blobs_infos)
        
        #= Dictionary of possible inputs =#
        self.informations = dict()
        
        self.brain.reset(rules)
    
        
        
        
