import numpy as np
import random as rd
import math as math

from utils import arr2int,int2weight,int2array

from Neuron import get_input_neuron, get_output_neuron , Internal_Neuron , get_outputs_name_list
from Gene import Gene


class Brain:
    
    def __init__(self,genome_size):
        '''
        genome_size (int) -> The number of connexions between neurons.
        
        onlyValid (bool) -> If True, the Brain will only generate valid connexions.
        Note that if it's False, the code will still clean neurons with no inputs or outputs.
        This is to optimize during runtime, as we don't have to use these neurons.
        '''
        
        onlyValid = False
        
        available_input_neurons = [0,1]
        available_internal_neurons = [[0,1,2],[3,4]] # 2 Layers with respectively 3 and 2 internal neurons
        available_output_neurons = [0,1,2,3,4]
        
        valid = False
        
        while(not valid):
            
            valid = True
            
            self.genome = []
            for i in range(genome_size):
                self.genome.append( Gene( available_input_neurons , 
                                        available_internal_neurons , 
                                        available_output_neurons ) )
        
            #== Create the input neurons, internal neurons, output neurons ==#
            self.input_neurons = []
            self.internal_neurons= []
            self.output_neurons = []
            
            for id in available_input_neurons:
                self.input_neurons.append( get_input_neuron(id) )
            
            for i in range(len(available_internal_neurons)):
                self.internal_neurons.append([])
                for id in available_internal_neurons[i]:
                    self.internal_neurons[-1].append( Internal_Neuron(1,id) )
            
            for id in available_output_neurons:
                self.output_neurons.append( get_output_neuron(id) )
            #======#
            
            
            #==- Make connexions between neurons -==#
            for gene in self.genome :
                
                inputType = gene.sequence[0]
                inputID = arr2int(gene.sequence[1:8])
                
                sinkType = gene.sequence[8]
                sinkID = arr2int(gene.sequence[9:16])
                
                weight = int2weight(arr2int(gene.sequence[16:32]))
                
                # Input is from an input neuron
                if(inputType == 0):
                    neuron = self.input_neurons[ inputID ]
                
                # Input is from an internal neuron
                else:
                    
                    found = False
                    input_layer = 0
                    while(not found):                        
                        for x in self.internal_neurons[input_layer]:
                            if(x.ID == inputID):
                                neuron = x
                                found = True
                        
                        input_layer += 1
                                        
                neuron.output_neurons_count += 1
                
                # Output is to an internal neuron
                if(sinkType == 0):
                    
                    found = False
                    input_layer = 0
                    while(not found):                        
                        for x in self.internal_neurons[input_layer]:
                            if(x.ID == sinkID):
                                
                                neuron.targets.append( ( weight , x ) )
                                
                                x.input_neurons_count += 1
                                x.feeders.append(neuron)
                                
                                found = True
                        
                        input_layer += 1
                                
                # Output is to an output neuron
                else:
                    neuron.targets.append( ( weight , self.output_neurons[sinkID] ) )
                    
                    self.output_neurons[sinkID].input_neurons_count += 1
                    self.output_neurons[sinkID].feeders.append(neuron)
            #===--===#
            
            
            #==- Remove the lonely neurons :( -==#
            found_lonely = True
            
            while( found_lonely ):
                
                found_lonely = False
                
                for i in range(len(self.input_neurons)-1,-1,-1):
                    neuron = self.input_neurons[i]
                    if(neuron.output_neurons_count == 0):
                        found_lonely = True
                        
                        # Remove the input from neurons forward
                        for target in neuron.targets:
                            weight,neuron2 = target
                            
                            neuron2.input_neurons_count -= 1
                            neuron2.feeders.remove(neuron)
                            
                        self.input_neurons.pop(i)
                
                
                for i in range(len(self.internal_neurons)):
                    neuron_layer = self.internal_neurons[i]
                    for j in range(len(self.internal_neurons[i])-1,-1,-1):
                        neuron = self.internal_neurons[i][j]
                        if(neuron.output_neurons_count == 0 or neuron.input_neurons_count == 0):
                            found_lonely = True
                            
                            # Remove the input from neurons forward
                            for target in neuron.targets:
                                weight,neuron2 = target
                                
                                neuron2.input_neurons_count -= 1
                                neuron2.feeders.remove(neuron)
                            
                            # Remove the target from neurons backward
                            for feeder in neuron.feeders:
                                feeder.output_neuron_count -= 1
                                
                                for k in range(len(feeder.targets)-1,-1,-1):
                                    if(feeder.targets[k][1] == neuron):
                                        feeder.targets.pop(k)
                                    
                            self.internal_neurons[i].pop(j)
                        
                for i in range(len(self.output_neurons)-1,-1,-1):
                    neuron = self.output_neurons[i]
                    if(neuron.input_neurons_count == 0):
                        found_lonely = True
                        
                        # Remove the target from neurons backward
                        for feeder in neuron.feeders:
                            feeder.output_neuron_count -= 1
                            
                            for j in range(len(feeder.targets)-1,-1,-1):
                                if(feeder.targets[j][1] == neuron):
                                    feeder.targets.pop(j)
                        
                        self.output_neurons.pop(i)
            #===--===#
        
            if(onlyValid and (len(self.input_neurons)==0 or len(self.output_neurons)==0)):
                valid = False
    
    def shoot(self,data):
        
        correspondance = get_outputs_name_list()
         
        for neuron in self.input_neurons:
            neuron.shoot(data)
        
        for i in range(len(self.internal_neurons)):
            for neuron in self.internal_neurons[i]:
                neuron.shoot()
        
        output_dict = dict()
        for key in correspondance:
            output_dict[key] = 0
        
        
        for neuron in self.output_neurons:
            res = neuron.shoot()
            
            key = correspondance[neuron.ID]
            output_dict[key] = res
        
        
        #= Cleaning the neuron input system =#
        for neuron in self.input_neurons:
            neuron.clear()
        
        for i in range(len(self.internal_neurons)):
            for neuron in self.internal_neurons[i]:
                neuron.clear()
        
        for neuron in self.output_neurons:
            neuron.clear()
        #====================================#
        
        return(output_dict)

    
    def __str__(self):
        
        for gene in self.genome:
            print(gene)
        
        
        print("#== List of Neurons ==#")
        
        print("#=====================#")
        print("#       Input         #")
        print("#=====================#")

        for neuron in self.input_neurons:
            print(neuron)
        
        print("#=====================#")
        print("#      Internal       #")
        print("#=====================#")
        
        for i in range(len(self.internal_neurons)):
            if(len(self.internal_neurons[i])!=0):
                print("Layer " + str(i))    
                for neuron in self.internal_neurons[i]:
                    print(neuron)

        print("#=====================#")
        print("#       Output        #")
        print("#=====================#")
        
        for neuron in self.output_neurons:
            print(neuron)
        
        print("#=====================#")

        return("")
    
    
















