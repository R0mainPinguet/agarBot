import numpy as np

def np2int(x):
    l = x.shape[0]
    s = 0
    
    for i in range(l-1,-1,-1):
        s += x[i] * 2**(l-1-i)
    
    return(s)

def int2weight(x):
    return(x/64)
    
class Gene:
    
    def __init__(self):        
        self.sequence = np.random.randint(0,2,16)
        
    def __str__(self):
        print("Complete sequence : ")
        print(self.sequence)
        
        print("Source type = " + str(self.sequence[0]))
        print("Source ID : " + str(np2int(self.sequence[1:4])))
        
        print("Sink type = " + str(self.sequence[4]))
        print("Sink ID : " + str(np2int(self.sequence[5:8]))) 
        
        print("Connection weight : " + str(int2weight(np2int(self.sequence[9:16]))) )
        return("")
    
    def set(self , sourceType,sourceID , sinkType,sinkID , weight):
        '''
        One gene = 16 bits
        
        Bit 0 : source type ( 0 = Input / 1 = Internal neuron )
        Bit 1 - 4 : source ID
        Bit 4 : sink type ( 0 = Internal / 1 = Ouput neuron )
        Bit 5 - 8 : sink ID
        Bit 9 - 16 : connection weight ( between -4 and 4 )
        
        Each gene represent the connection between two neurons
        '''
               
        self.sequence[0] = sourceType
        self.sequence[1:4] = sourceID
        
        self.sequence[4] = sinkType
        self.sequence[5:8] = sinkID
        
        self.sequence[9:16] = weight


class Genome:
    
    def __init__(self , count):
        '''
        The genome is composed of 'count' Genes
        '''        
        self.genes = []
        for i in range(count):
            self.genes.append( Gene() )



class Neuron:
    
    def __init__(self,type,ID):
        '''
        Declaration of each possible Neuron, with their type and ID
        # Type = 0 : Input neuron
        # Type = 1 : Internal neuron
        
        List of the Input Neurons :
        # 0 - Random
        # 1 - Sinusoidal ( 60 frames period )
        # 2 - Closest Ennemy Distance
        # 3 - Closest Ennemy Size Ratio
        # 4 - Closest Ennemy Size Difference
        # 5 - Closest Food Distance
        # 6 - Host Size
        # 7 - Host Rank
        '''
        self.ID = ID
        
        
        
class Input_Random(Neuron):
    
    def __init__(self):
        self.ID = 0
        
    def shoot(self):        
        return(np.random.rand() * 2 - 1)


class Input_Sinusoidal(Neuron):
    
    def __init__(self):
        self.ID = 1
    
    # Period = 600 frames
    def shoot(self,frame):
        return( np.sin(2 *  np.pi * frame/600) )


class Input_Closest_Ennemy_Distance(Neuron):
    
    def __init__(self):
        self.ID = 2

    def shoot(self,index,blob_list):
        

class Input_Closest_Ennemy_Size_Ratio(Neuron):
    
    def __init__(self):
        self.ID = 3
        
    def shoot(self,index,blob_list):
        pass


class Input_Closest_Ennemy_Size_Difference(Neuron):
    
    def __init__(self):
        self.ID = 4


class Input_Closest_Food_Distance(Neuron):
    
    def __init__(self):
        self.ID = 5
    

class Input_Host_Size(Neuron):
    
    def __init__(self):
        self.ID = 6


class Input_Host_Rank(Neuron):
    
    def __init__(self):
        self.ID = 7




class Ouput_Move_Closest_Ennemy(Neuron):
    
    def __init__(self):
        self.ID = 0



class Brain:
    
    def __init__(self):
        self.genome = Genome(1)


def compute_closest_ennemy(self,blobList,index):
    '''
    Compute the closest ennemy index
    '''
    closest_index = 0
    closest_distance = 1e9
    for i in range(len(blobList)):
        if(i != closest_index):
            
            dist = np.linalg.norm(blobList[i].sub_blobs[0,0:2] - blobs_infos[0,0:2])
            
            if(dist < closest_distance):
                closest_distance = dist
                closest_index = i
        
    self.closest_ennemy_index = closest_index
    
def compute_closest_food(self,food):
    '''
    Compute the closest food index
    '''        
    pass
    # self.closest_food_index = 

    
def compute_closest_projectile(self,projectiles):
    '''
    Compute the closest projectile index
    '''
    pass
    # self.closest_projectile_index = 
    
    



