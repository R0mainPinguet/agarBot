import numpy as np


def loadRules(name):
    rules = dict()
    
    with open(name) as f:
        lines = f.readlines()
    
    res = []
    
    for line in lines:
        res.append(line.replace("\n",""))
        res[-1] = res[-1].split(" ")
        
    for r in res:
        if(r[0] != "#" and len(r)>1 ):
            
            if(float(r[1]).is_integer()):
                rules[r[0]] = int(r[1])
            else:
                rules[r[0]] = float(r[1])
            
    return(rules)



def arr2int(x):
    l = x.shape[0]
    s = 0
    
    for i in range(l-1,-1,-1):
        s += x[i] * 2**(l-1-i)
    
    return(s)

def int2weight(x):
    return(4*(x-32768)/32768)
    
def int2array(integer , length):
    
    arr = np.zeros(length,dtype='int')
    
    s = length
    
    while(integer > 0):
                
        if( pow(2,s-1) <= integer ):
            integer -= pow(2,s-1)
            arr[length-s] = 1
            
        s -= 1
    
    return(arr)

def deflate_func(x):
    return( max(x-2000,0)/10000 )

def speed_coeff_func(size,df_size,viscosity):
    return( np.exp((-max(size,2*df_size)+2*df_size)/viscosity) )

def compute_ranks(blobs_list,blobs_infos):
    vals = []
    
    for i in range(len(blobs_list)):
        
        vals.append(np.sum(blobs_infos[blobs_list[i].index : blobs_list[i].index+blobs_list[i].actual_sub_blob,4]) )

    return(np.flip(np.argsort(vals)))


def compute_all_distances(blobList):
    '''
    Compute the distances of all players between each other
    '''
    
    distances = np.zeros((len(blobList),len(blobList)),dtype="float")
    
    for i in range(len(blobList)-1):
        for j in range(i+1,len(blobList)):
                
                distances[i,j] = np.linalg.norm( blobList[j].center_of_gravity - blobList[i].center_of_gravity )
                distances[j,i] = distances[i,j]
        
        distances[i,i] = 1e9
    
    distances[len(blobList)-1,len(blobList)-1] = 1e9
    
    return(distances)

    
def check_collisions(rules,blobs_list,blobs_infos):
    
    pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    