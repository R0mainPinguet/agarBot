import numpy as np
import random as rd
import math as math

from utils import arr2int,int2weight,int2array



#== List of the Input Neurons ==#
# 0 - Random
# 1 - Sinusoidal ( 60 frames period )
# 2 - Closest Ennemy Distance
# 3 - Closest Ennemy Size Ratio
# 4 - Closest Ennemy Size Difference
# 5 - Closest Food Distance
# 6 - Host Size
# 7 - Host Rank

def get_input_neuron(ID):
    
    if(ID == 0):
        return( Input_Random(0,0) )
    elif(ID == 1):
        return( Input_Sinusoidal(0,1) )
    elif(ID == 2):
        return( Input_Closest_Ennemy_Distance(0,2) )
    elif(ID == 3):
        return( Input_Closest_Ennemy_Size_Ratio(0,3) )
    elif(ID == 4):
        return( Input_Closest_Ennemy_Size_Difference(0,4) )
    elif(ID == 5):
        return( Input_Closest_Food_Distance(0,5) )
    elif(ID == 6):
        return( Input_Host_Size(0,6) )
    elif(ID == 7):
        return( Input_Host_Rank(0,7) )
    else:
        pass



#== List of the Output Neurons ==#
# 0 - Move West
# 1 - Move North
# 2 - Move East
# 3 - Move South
# 4 - Move relative to Closest Ennemy
# 5 - Move relative to Closest Food

def get_output_neuron(ID):
    
    if(ID == 0):
        return( Output_Move_West(2,0) )
    elif(ID == 1):
        return( Output_Move_North(2,1) )
    elif(ID == 2):
        return( Output_Move_East(2,2) )
    elif(ID == 3):
        return( Output_Move_South(2,3) )
    elif(ID == 4):
        return( Ouput_Move_Closest_Ennemy(2,4) )
    elif(ID == 5):
        return( Ouput_Move_Closest_Food(2,5) )
    else:
        pass



class Neuron:
    
    def __init__(self,type,ID):
        
        # type = 0 -> Input ; 1 -> Internal ; 2 -> Output
        self.type = type
        
        self.ID = ID
        
        # Number of input Neurons ( to know when the Neuron can shoot )
        self.input_neurons_count = 0
        self.output_neurons_count = 0
        
        # List of signals received from the input Neurons
        self.input_signals = []
        
        # List of target neurons ( each element is a couple ( weight , Neuron ) )
        self.targets = []
    
    def __str__(self):
        
        if(self.type==0):
            print("#= Input Neuron =#")
        elif(self.type==1):
            print("#= Internal Neuron =#")
        else:
            print("#= Output Neuron =#")
        
        print("-- ID = " + str(self.ID) )
        
        if(self.type!=2):
            
            print("Connected to " + str(self.output_neurons_count) + " neurons :")
            
            for target in self.targets:
                weight,neuron = target
                
                if(neuron.type==1):
                    print("    Internal neuron ( ID = " + str(neuron.ID) + " ) weight = " + str(weight))
                elif(neuron.type==2):
                    print("    Output neuron ( ID = " + str(neuron.ID) + " ) weight = " + str(weight))
                else:
                    print("    Wtf ?") # Not supposed to happen 
                        
        return("")
        
    def clear(self):
        self.input_signals.clear()
    



class Input_Random(Neuron):
    
    def shoot(self,data):        
        return(np.random.rand() * 2 - 1)

class Input_Sinusoidal(Neuron):
    
    # Period = 600 frames ( = 10 seconds at 60 fps )
    def shoot(self,data):
        return( np.sin(2 *  np.pi * data["frame"]/600) )

class Input_Closest_Ennemy_Distance(Neuron):

    def shoot(self,data):
        pass

class Input_Closest_Ennemy_Size_Ratio(Neuron):

    def shoot(self,index,blob_list):
        pass

class Input_Closest_Ennemy_Size_Difference(Neuron):
    pass

class Input_Closest_Food_Distance(Neuron):
    pass
    
class Input_Host_Size(Neuron):
    pass

class Input_Host_Rank(Neuron):
    pass



class Internal_Neuron(Neuron):
    
    def shoot(self):
        s = 0
        
        for input in self.input_signals:
            s += input
        
        for element in self.targets:
            
            weight,neuron = element
            
            neuron.input_signals.append( math.tanh(s) * weight )



class Output_Move_West(Neuron):
    pass

class Output_Move_North(Neuron):
    pass

class Output_Move_East(Neuron):
    pass

class Output_Move_South(Neuron):
    pass

class Ouput_Move_Closest_Ennemy(Neuron):
    pass

class Ouput_Move_Closest_Ennemy(Neuron):
    pass



class Gene:
    
    def __init__(self,available_input_neurons,available_internal_neurons,available_output_neurons):
        
        self.sequence = np.random.randint(0,2,32)
        
        # Proportion of input neurons among input + internal neurons
        ratio1 = len(available_input_neurons)/(len(available_input_neurons)+len(available_internal_neurons))
        
        # Proportion of internal neurons among internal + output neurons
        ratio2 = len(available_internal_neurons)/(len(available_internal_neurons)+len(available_output_neurons))
        
        if(rd.random() < ratio1):
            self.sequence[0] = 0
            choice = rd.choice( available_input_neurons )            
        else:
            self.sequence[0] = 1
            choice = rd.choice( available_internal_neurons )
        
        self.sequence[1:8] = int2array(choice,7)
        
        if(rd.random() < ratio2):
            self.sequence[8] = 0
            choice = rd.choice( available_internal_neurons )
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



class Brain:
    
    def __init__(self,genome_size):
        
        available_input_neurons = [0,1]
        available_internal_neurons = [0]
        available_output_neurons = [0,1,2,3,4]
        
        self.genome = []
        for i in range(genome_size):
            self.genome.append( Gene( available_input_neurons , 
                                      available_internal_neurons , 
                                      available_output_neurons ) )
        
        #== Input neurons, internal neurons, output neurons ==#
        self.input_neurons = []
        self.internal_neurons= []
        self.output_neurons = []
        
        for id in available_input_neurons:
            self.input_neurons.append( get_input_neuron(id) )
        
        for id in available_internal_neurons:
            self.internal_neurons.append( Internal_Neuron(1,id) )
        
        for id in available_output_neurons:
            self.output_neurons.append( get_output_neuron(id) )
        #======#
    
    def __str__(self):
        
        
        print("#== List of Neurons ==#")
        
        for neuron in self.input_neurons:
            print(neuron)
        
        for neuron in self.internal_neurons:
            print(neuron)
        
        for neuron in self.output_neurons:
            print(neuron)
        
        
        return("")
    
    
    def construct(self):
        
        
        #==- Make connexions -==#
        
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
                neuron = self.internal_neurons[ inputID ]
            
            neuron.output_neurons_count += 1
            
            # Output is to an internal neuron
            if(sinkType == 0):
                neuron.targets.append( ( weight , self.internal_neurons[sinkID] ) )
                self.internal_neurons[sinkID].input_neurons_count += 1
            
            # Output is to an output neuron
            else:
                neuron.targets.append( ( weight , self.output_neurons[sinkID] ) )
                self.output_neurons[sinkID].input_neurons_count += 1
        
        #===--===#
        
        
        #==- Remove the lonely neurons :( -==#
        
        for i in range(len(self.input_neurons)-1,-1,-1):
            neuron = self.input_neurons[i]
            if(neuron.output_neurons_count == 0):
                self.input_neurons.pop(i)
        
        for i in range(len(self.internal_neurons)-1,-1,-1):
            neuron = self.internal_neurons[i]
            if(neuron.output_neurons_count == 0 or neuron.input_neurons_count == 0):
                self.internal_neurons.pop(i)
                
        for i in range(len(self.output_neurons)-1,-1,-1):
            neuron = self.output_neurons[i]
            if(neuron.input_neurons_count == 0):
                self.output_neurons.pop(i)
        
        #===--===#
        
        
        
        
        
        
        
        
        
        
        
        
        
