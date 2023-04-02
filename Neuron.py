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
            print("-- ID = " + str(self.ID))
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


class Input_Random(Neuron):
    
    def shoot(self,data):
        
        out = np.random.rand() * 2 - 1
        
        for element in self.targets:
            
            weight,neuron = element
            
            neuron.input_signals.append( out * weight )
                
class Input_Sinusoidal(Neuron):
    
    # Period = 600 frames ( = 10 seconds at 60 fps )
    def shoot(self,data):
        
        out = np.sin(2 *  np.pi * data["frame"]/600)

        for element in self.targets:
            
            weight,neuron = element
            
            neuron.input_signals.append( out * weight )

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





#== List of the Output Neurons ==#
# 0 - Move Horizontal
# 1 - Move Vertical
# 2 - Move relative to Closest Ennemy
# 3 - Move relative to Closest Food
# 4 - Move relative to Closest Projectile

def get_output_neuron(ID):
    
    if(ID == 0):
        return( Output_Horizontal(2,0) )
    elif(ID == 1):
        return( Output_Vertical(2,1) )
    elif(ID == 2):
        return( Ouput_Move_Closest_Ennemy(2,2) )
    elif(ID == 3):
        return( Ouput_Move_Closest_Food(2,3) )
    elif(ID == 4):
        return( Ouput_Move_Closest_Projectile(2,4) )
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






