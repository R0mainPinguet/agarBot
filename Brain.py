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
        
        # List of feeders neurons ( only stores the neuron address )
        self.feeders = []
        
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


class Output_Neuron(Neuron):
    
    def shoot(self):
        s = 0
        
        for input in self.input_signals:
            s += input
        
        return(math.tanh(s))
            
class Output_Move_West(Output_Neuron):
    pass

class Output_Move_North(Output_Neuron):
    pass

class Output_Move_East(Output_Neuron):
    pass

class Output_Move_South(Output_Neuron):
    pass

class Ouput_Move_Closest_Ennemy(Output_Neuron):
    pass

class Ouput_Move_Closest_Ennemy(Output_Neuron):
    pass



class Gene:
    
    def __init__(self,available_input_neurons,available_internal_neurons,available_output_neurons):
        
        self.sequence = np.random.randint(0,2,32)
        
        temp_list = []
        for x in available_internal_neurons:
            temp_list += x
        
        # Proportion of input neurons among input + internal neurons
        ratio1 = len(available_input_neurons)/(len(available_input_neurons)+len(temp_list))
        
        # Code the input type and ID #
        if(rd.random() < ratio1):
            self.sequence[0] = 0
            choice = rd.choice( available_input_neurons )
            
            # Proportion of internal neurons among internal + output neurons
            ratio2 = len(temp_list)/(len(temp_list)+len(available_output_neurons))
            
        else:
            
            self.sequence[0] = 1
            choiceLayer_Input = rd.randint(0,len(available_internal_neurons)-1)
            choice = rd.choice( available_internal_neurons[choiceLayer_Input] )
            
            temp_list2 = []
            for i in range(choiceLayer_Input+1,len(available_internal_neurons)):
                temp_list2 += available_internal_neurons[i]
                
            # Proportion of remaining internal neurons among remaining internal + output neurons
            ratio2 = len(temp_list2)/(len(temp_list2)+len(available_output_neurons))
        
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
        
        for neuron in self.input_neurons:
            neuron.shoot(data)
        
        for i in range(len(self.internal_neurons)):
            for neuron in self.internal_neurons[i]:
                neuron.shoot()
        
        outputs = []
        for neuron in self.output_neurons:
            res = neuron.shoot()
            outputs.append([neuron.ID,res])
        
        
        #= Cleaning the neuron input system =#
        for neuron in self.input_neurons:
            neuron.clear()
        
        for i in range(len(self.internal_neurons)):
            for neuron in self.internal_neurons[i]:
                neuron.clear()
        
        for neuron in self.output_neurons:
            neuron.clear()
        #====================================#
        
        return(outputs)

    
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
    
    
















