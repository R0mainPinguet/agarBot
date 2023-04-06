import numpy as np
import random as rd
import math as math

from utils import arr2int,int2weight,int2array


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
        
        # List of feeders neurons ( only stores the neuron address )
        self.feeders = []
        
        # List of target neurons ( each element is a couple ( weight , Neuron ) )
        self.targets = []
    
    def __str__(self):
        
        if(self.type==0):
            print("#= Input Neuron =#")
            print("-- ID = " + str(self.ID) + " ( " + get_inputs_name_list()[self.ID] + " ) ")
        elif(self.type==1):
            print("#= Internal Neuron =#")
            print("-- ID = " + str(self.ID))
        else:
            print("#= Output Neuron =#")
            print("-- ID = " + str(self.ID) + " ( " + get_outputs_name_list()[self.ID] + " ) ")
        
        
        
        if(self.type!=0):
            print("- Expects " + str(len(self.feeders)) + " input(s) before shooting")
        
        if(self.type!=2 and self.output_neurons_count!=0 ):
            
            print("Connected to " + str(self.output_neurons_count) + " neuron(s) :")
            
            for target in self.targets:
                weight,neuron = target
                
                if(neuron.type==1):
                    print("    Internal neuron ( ID = " + str(neuron.ID) + " ) weight = " + str(weight))
                elif(neuron.type==2):
                    print("    Output neuron ( ID = " + str(neuron.ID) + " ) weight = " + str(weight))
                else:
                    print("    Wtf ?") # Not supposed to happen 
                        
        return("")
    
    def shoot_targets(self):
        
        for element in self.targets:
            
            weight,neuron = element
            
            neuron.input_signals.append( self.out * weight )
        
    def clear(self):
        self.input_signals.clear()
    


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
        return( Input_Random(0,ID) )
    elif(ID == 1):
        return( Input_Sinusoidal(0,ID) )
    elif(ID == 2):
        return( Input_Closest_Ennemy_Distance(0,ID) )
    elif(ID == 3):
        return( Input_Closest_Ennemy_Size_Ratio(0,ID) )
    elif(ID == 4):
        return( Input_Closest_Food_Distance(0,ID) )
    elif(ID == 5):
        return(Input_Closest_Projectile_Distance(0,ID) )
    elif(ID == 6):
        return( Input_Host_Size(0,ID) )
    elif(ID == 7):
        return( Input_Host_Rank(0,ID) )
    else:
        pass

def get_inputs_name_list():
    return(["Random","Sinusoidal","Closest_Ennemy_Distance","Closest_Ennemy_Size","Closest_Food_Distance","Closest_Projectile_Distance","Host_size","Host_rank"])

class Input_Random(Neuron):
    
    def compute_out(self,data):
        
        self.out = np.random.rand() * 2 - 1
        
        
                
class Input_Sinusoidal(Neuron):
    
    # Period = 600 frames ( = 10 seconds at 60 fps )
    def compute_out(self,data):
        
        self.out = np.sin(2 *  np.pi * data["frame"]/600)


class Input_Closest_Ennemy_Distance(Neuron):
    '''
    Normalized relative to the map 
    '''
    def compute_out(self,data):
       
        self.out = data["closest_ennemy_distance"] / data["longest_distance"]
               
class Input_Closest_Ennemy_Size_Ratio(Neuron):

    def compute_out(self,data):
        
        self.out = data["closest_ennemy_size"] / data["size"]
        

class Input_Closest_Food_Distance(Neuron):
    
    def compute_out(self,data):
        
        pass

class Input_Closest_Projectile_Distance(Neuron):
    
    def compute_out(self,data):
        
        pass
        
class Input_Host_Size(Neuron):
    
    def compute_out(self,data):
        
        self.out = data["size"]

class Input_Host_Rank(Neuron):
    
    def compute_out(self,data):
        
        self.out = data["rank"]





class Internal_Neuron(Neuron):
    
    def shoot(self):
        s = 0
        
        for input in self.input_signals:
            s += input
        
        for element in self.targets:
            
            weight,neuron = element
            
            neuron.input_signals.append( math.tanh(s) * weight )





#== List of the Output Neurons ==#
# 0 - Move Horizontal
# 1 - Move Vertical
# 2 - Move relative to Closest Ennemy
# 3 - Move relative to Closest Food
# 4 - Move relative to Closest Projectile

def get_output_neuron(ID):
    
    if(ID == 0):
        return( Output_Horizontal(2,ID) )
    elif(ID == 1):
        return( Output_Vertical(2,ID) )
    elif(ID == 2):
        return( Ouput_Move_Closest_Ennemy(2,ID) )
    elif(ID == 3):
        return( Ouput_Move_Closest_Food(2,ID) )
    elif(ID == 4):
        return( Ouput_Move_Closest_Projectile(2,ID) )
    else:
        pass

def get_outputs_name_list():
    return(["Horizontal","Vertical","Move_Closest_Ennemy","Move_Closest_Food","Move_Closest_Projectile"])

class Output_Neuron(Neuron):
    
    def shoot(self):
        s = 0
        
        for input in self.input_signals:
            s += input
        
        return(math.tanh(s))


class Output_Horizontal(Output_Neuron):
    pass

class Output_Vertical(Output_Neuron):
    pass

class Ouput_Move_Closest_Ennemy(Output_Neuron):
    pass

class Ouput_Move_Closest_Food(Output_Neuron):
    pass

class Ouput_Move_Closest_Projectile(Output_Neuron):
    pass






