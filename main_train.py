import sys
import numpy as np
import random as rd

from Player import Player
from Camera import Camera
from Food import Food
from Projectiles import Projectiles
from Bot import Bot

from utils import loadRules,compute_ranks,compute_all_distances,check_collisions

from EA import Select,Crossover,Mutate


logList = []


rules = loadRules("rules.txt")

#== AVAILABLE INPUT, INTERNAL AND OUTPUT NEURONS ==#
rules["available_input_neurons"] = [0,1,2,3,6,7]
rules["available_internal_neurons"] = [[0,1,2],[3,4]]
rules["available_output_neurons"] = [0,1,2,3,4]
        
print("#== RULES ==#")
print(rules)
print("#====#")

#===#
bots_count = rules["bots_count"]
#===#

#== Window parameters ==#
game_length = rules["game_length"]

print("Durée de la partie : " + str(game_length // 3600) + " minutes et " + str( (game_length%3600)//60 ) + " secondes")

width , height = rules["width"] , rules["height"]

borders_X , borders_Y = rules["borders_X"] , rules["borders_Y"]
#==#

#== Learning parameters ==#
generations = rules["generations"]
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


#====#

for generation in range(generations):
    
    food = Food(rules)
    projectiles = Projectiles(rules)

    print("Génération " + str(generation+1) )
    
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
        for j in range(len(blobs_list)-2,i-1,-1):
            if(blobs_list[j].fitness < blobs_list[j+1].fitness):
                
                tmp = blobs_list[j]
                blobs_list[j] = blobs_list[j+1]
                blobs_list[j+1] = tmp
    
    for bot in blobs_list:
        bot.brain.plot( int(bot.fitness), rules , "logs/G" + str(generation) + "_" + str(bot.ID) + ".png")
        print("Fitness de l'individu " + str(bot.ID) + " : " + str(bot.fitness) )
    
    if( generation != generations-1):
    
        #== EVOLUTIONARY ALGORITHM ==#
        new_blobs_list = []
        
        #== Selection ==#
        print("Sélection !")
        blobs_to_crossover = Select(blobs_list,new_blobs_list,rules,logList)
        #====#
        
        #== Crossover ==#
        print("Crossover")
        Crossover( blobs_to_crossover , blobs_list , new_blobs_list , rules , logList )
        #====#
        
        #== Mutation ==#
        print("Mutation")
        Mutate(new_blobs_list , rules , logList )
        #====#
        
        blobs_list = new_blobs_list
        
        for i in range(bots_count):
            blobs_list[i].reset(rules,blobs_infos)
    
logTxt = ''.join(logList)

f = open("logs/log.txt", "w")
f.write(logTxt)
f.close()

    
