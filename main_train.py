import sys
import numpy as np

from Player import Player
from Camera import Camera
from Food import Food
from Projectiles import Projectiles
from Bot import Bot

from utils import loadRules,compute_ranks,compute_all_distances,check_collisions

rules = loadRules("rules.txt")
print("#== RULES ==#")
print(rules)
print("#====#")

WHITE = (255,255,255)
BLACK = (0,0,0)

bots_count = rules["bots_count"]
#===#

#== Window parameters ==#
game_length = rules["game_length"]

print("Durée de la partie : " + str(game_length // 3600) + " minutes ")

width , height = rules["width"] , rules["height"]

borders_X , borders_Y = rules["borders_X"] , rules["borders_Y"]
#==#

#== Learning parameters ==#
generations = rules["generations"]
mutation_prob = rules["mutation_prob"]
crossover_prob = rules["crossover_prob"]
elitism = rules["elitism"]
#=====#


#== External data ==#
external_data = dict()
external_data["longest_distance"] = np.sqrt(borders_X*borders_X+borders_Y*borders_Y)
#====#


#== Bots, food and projectiles initialization ==#

# Contains the bots objects
blobs_list = []

# Contains the bots position, speed, and size
blobs_infos = np.ones((rules["MAX_SUB_BLOB"] * bots_count , 5) , dtype="float")

for i in range(bots_count):
    blobs_list.append(Bot(rules,i*rules["MAX_SUB_BLOB"],blobs_infos))

print("All bots are generated !")

food = Food(rules)
projectiles = Projectiles(rules)
#====#


for generation in range(generations):
    
    frame = 0
    
    while frame < game_length:
        
        if( frame % 3600 == 0):
            print(str(frame//3600) + " minute(s)")
        
        #= Compute the ranks, distances =#
        external_data["ranks"] = compute_ranks(blobs_list,blobs_infos)
        external_data["distances"] = compute_all_distances(blobs_list)
        external_data["frame"] = frame
        #==#
        
        #= Updates =#
        projectiles.update(blobs_list,blobs_infos)
        
        for i in range(bots_count):
            blobs_list[i].update(blobs_list,blobs_infos,external_data,food,projectiles)
            
        food.update(blobs_list,blobs_infos)
        #====#
        
        check_collisions(rules,blobs_list,blobs_infos,rules["eating_percentage"])
        
        frame += 1
    
    #= Bubble sort ( too lazy for something else ) First ones are the best ones =#
    for i in range(len(blobs_list)-1):
        for j in range(i,len(blobs_list)-1):
            
            if(blobs_list[j].fitness < blobs_list[j+1].fitness):
                
                tmp = blobs_list[j]
                blobs_list[j] = blobs_list[i]
                blobs_list[i] = tmp
            
    for i in range(len(blobs_list)):
        print("Fitness de l'individu " + str(i) + " : " + str(blobs_list[i].fitness) )
    
    
    #= Roulette Selection with elitism =#
    
    
    
    #====#
    
    #= Mutation Operator =#
    
    
    
    #====#
    
    
    
    
    
    

    
