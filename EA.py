import random as rd
from copy import deepcopy

from utils import arr2int,int2weight,int2array


def Select(blobs_list,new_blobs_list,rules,logList):
    '''
    Roulette selection
    '''
    logList.append("[Selection]\n")
    
    elitism = rules["elitism"]
    bots_for_elitism = rules["bots_for_elitism"]
    
    #= Elitism =#
    for i in range(bots_for_elitism):
        new_blobs_list.append(blobs_list[i])
    
    selected_bots = bots_for_elitism
    selected_bots_index = []
    
    #= Roulette Selection + Crossover =#
    total_fitness = 0
    for i in range(len(blobs_list)):
        total_fitness += blobs_list[i].fitness
    
    while(selected_bots < len(blobs_list)):
        
        proba_parent_1 = rd.random()
        index_parent_1 = -1
        
        while( proba_parent_1 > 0 ):
            index_parent_1 += 1
            proba_parent_1 -= blobs_list[index_parent_1].fitness / total_fitness
        
        index_parent_2 = index_parent_1
        
        while(index_parent_1 == index_parent_2):
            proba_parent_2 = rd.random()
            index_parent_2 = -1
            
            while( proba_parent_2 > 0 ):
                index_parent_2 += 1
                proba_parent_2 -= blobs_list[index_parent_2].fitness / total_fitness
        
        selected_bots_index += [index_parent_1,index_parent_2]
        
        selected_bots+=2
    
        logList.append("Bot " + str(index_parent_1) + " and bot " + str(index_parent_2) + " selected.\n")
    
    logList.append("\n")
    
    return(selected_bots_index)
    
def Crossover(blobs_to_crossover,blobs_list,new_blobs_list , rules , logList):
    '''
    Exchanges connexions.
    Since the number of possibility is limited, I'll make sure that the parents and children are different
    '''
    logList.append("[Crossover]\n")
    
    crossover_prob = rules["crossover_prob"]
    
    j = 0
    
    while(len(new_blobs_list) < len(blobs_list)):
        
        child1 = deepcopy(blobs_list[blobs_to_crossover[j]])
        child2 = deepcopy(blobs_list[blobs_to_crossover[j+1]])
        
        logList.append("Bot " + str(blobs_to_crossover[j]) + " and bot " + str(blobs_to_crossover[j+1]) + " : ")
        
        j += 2
        
        for i in range( len(child1.brain.genome) ):
            
            if(rd.random() < crossover_prob):
                gene2 = child2.brain.genome[i]
                child2.brain.genome[i] = child1.brain.genome[i]
                child1.brain.genome[i] = gene2
                
                logList.append("Exchanged gene " + str(i) + ".\n")
        
        new_blobs_list.append(child1)
        if(len(new_blobs_list) < len(blobs_list)):
            new_blobs_list.append(child2)
    
    logList.append("\n")
    
def Mutate( blobs_list , rules , logList ):
    '''
    For the source / sink, randomly takes another neuron
    For the weight, randomly invert bit by bit
    '''
    logList.append("[Mutation]\n")
    
    mutation_prob = rules["mutation_prob"]
    
    available_input_neurons = rules["available_input_neurons"]
    available_internal_neurons = rules["available_internal_neurons"]
    available_output_neurons = rules["available_output_neurons"]
    
    for j in range(len(blobs_list)):
        
        ind = blobs_list[j]
        
        logList.append("Bot " + str(j) + ".\n")
        
        for g in range(len(ind.brain.genome)):
            
            logList.append("Gene " + str(g) + " : ")
            
            gene = ind.brain.genome[g]
            
            sourceTag = gene.sequence[0]
            sourceID = arr2int(gene.sequence[1:8])
            sinkTag = gene.sequence[8]
            sinkID = arr2int(gene.sequence[9:16])
            
            noMutation = True
            
            #= Source mutation =#
            if(rd.random() < mutation_prob):
                noMutation = False
                
                logList.append("\nMutation on the source.\n")
                
                #= Chooses a source before the current sink =#
                
                if(sinkTag==0):
                    
                    sinkLayer = 0
                    while( not sinkID in available_internal_neurons[sinkLayer] ):
                        sinkLayer += 1
                    
                    temp_list = []
                    for i in range(sinkLayer):
                        temp_list += available_internal_neurons[i]
                    
                else:
                    
                    temp_list = []
                    for i in range(len(available_internal_neurons)):
                        temp_list += available_internal_neurons[i]
                    
                ratio = len(available_input_neurons)/(len(available_input_neurons)+len(temp_list))
                
                if(rd.random() < ratio):
                    gene.sequence[0] = 0
                    gene.sequence[1:8] = int2array(rd.choice( available_input_neurons ),7)
                else:
                    gene.sequence[0] = 1
                    gene.sequence[1:8] = int2array(rd.choice( temp_list ),7)
            #===================#
            
            #= Sink mutation =#
            if(rd.random() < mutation_prob):
                noMutation = False
                
                logList.append("\nMutation on the sink.\n")
                
                #= Chooses a sink after the current source =#
                
                if(sourceTag==0):
                    temp_list = []
                    for i in range(len(available_internal_neurons)):
                        temp_list += available_internal_neurons[i]
                        
                else:
                    
                    sourceLayer = 0
                    while( not sourceID in available_internal_neurons[sourceLayer] ):
                        sourceLayer += 1
                    
                    temp_list = []
                    for i in range(sourceLayer,len(available_internal_neurons)):
                        temp_list += available_internal_neurons[i]
                    
                    
                ratio = len(available_output_neurons)/(len(available_output_neurons)+len(temp_list))
                
                if(rd.random() < ratio):
                    gene.sequence[8] = 1
                    gene.sequence[9:16] = int2array(rd.choice( available_output_neurons ),7)
                else:
                    gene.sequence[8] = 0
                    gene.sequence[9:16] = int2array(rd.choice( temp_list ),7)
            #=================#
            
            mutationOnWeight = False
            
            #= Weight mutation =#
            for i in range(16,32):
                if(rd.random() < mutation_prob):
                    noMutation = False
                    mutationOnWeight = True
                    gene.sequence[i] = 2*gene.sequence[i]-1
            
            if(mutationOnWeight):
                logList.append("\nMutation on the weight.\n")
                
            #=================#
            
            if(noMutation):
                logList.append(" no mutation.")
            
            logList.append("\n")
                
    logList.append("\n")
    