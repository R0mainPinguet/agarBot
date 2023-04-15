import numpy as np
import random as rd
import math as math

from utils import arr2int,int2weight,int2array

class Gene:
    
    def __init__(self,rules):
        
        self.sequence = np.random.randint(0,2,32)
        
        available_input_neurons = rules["available_input_neurons"]
        available_internal_neurons = rules["available_internal_neurons"]
        available_output_neurons = rules["available_output_neurons"]
        
        temp_list = []
        for x in available_internal_neurons:
            temp_list += x
        
        # Proportion of input neurons among input + internal neurons
        ratio1 = len(available_input_neurons)/(len(available_input_neurons)+len(temp_list))
        
        # Code the input type and ID #
        if(rd.random() < ratio1):
            self.sequence[0] = 0
            choice = rd.choice( available_input_neurons )

        else:
            
            self.sequence[0] = 1
            choiceLayer_Input = rd.randint(0,len(available_internal_neurons)-1)
            choice = rd.choice( available_internal_neurons[choiceLayer_Input] )
            
            temp_list = []
            for i in range(choiceLayer_Input+1,len(available_internal_neurons)):
                temp_list += available_internal_neurons[i]
                
        # Proportion of remaining internal neurons among remaining internal + output neurons
        ratio2 = len(temp_list)/(len(temp_list)+len(available_output_neurons))
        
        self.sequence[1:8] = int2array(choice,7)
        
        # Code the output type and ID #
        if(rd.random() < ratio2 and self.sequence[0]==1 and choiceLayer_Input<len(available_internal_neurons)-1):
            self.sequence[8] = 0
            choiceLayer_Output = rd.randint(choiceLayer_Input+1,len(available_internal_neurons)-1)
            choice = rd.choice( available_internal_neurons[choiceLayer_Output] )
        else:
            self.sequence[8] = 1
            choice = rd.choice( available_output_neurons )
            
        self.sequence[9:16] = int2array(choice,7)
    
    def __str__(self):
        print("Input sequence : ")
        print(self.sequence[0:8])
        
        print("Output sequence : ")
        print(self.sequence[8:16])
        
        print("Weight :")
        print(self.sequence[16:32])
        
        if(self.sequence[0]==0):
            print("Source : Input neuron, ID = " + str(str(arr2int(self.sequence[1:8])))) 
        else:
            print("Source : Internal neuron, ID = " + str(str(arr2int(self.sequence[1:8])))) 
        
        if(self.sequence[8]==0):
            print("Sink : Internal neuron, ID = " + str(str(arr2int(self.sequence[9:16])))) 
        else:
            print("Sink: Output neuron, ID = " + str(str(arr2int(self.sequence[9:16])))) 
        
        print("Connection weight : " + str(int2weight(arr2int(self.sequence[16:32]))))
        
        return("")
    
    def set(self , sourceType,sourceID , sinkType,sinkID , weight):
        '''
        One gene = 32 bits
        
        Bit 0 : source type ( 0 = Input / 1 = Internal neuron )
        Bit 1 - 7 : source ID
        Bit 8 : sink type ( 0 = Internal / 1 = Ouput neuron )
        Bit 9 - 15 : sink ID
        Bit 16 - 32 : connection weight ( between -4 and 4 )
        
        Each gene represent the connection between two neurons
        '''
               
        self.sequence[0] = sourceType
        self.sequence[1:8] = sourceID
        
        self.sequence[8] = sinkType
        self.sequence[9:16] = sinkID
        
        self.sequence[16:32] = weight