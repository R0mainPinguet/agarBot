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



def compute_ranks(blobs_list,blobs_infos):
    vals = []
    
    for i in range(len(blobs_list)):
        
        vals.append(np.sum(blobs_infos[blobs_list[i].index : blobs_list[i].index+blobs_list[i].actual_sub_blobs,4]) )
        

    return(np.flip(np.argsort(vals)))

# def compute_closest_ennemy(self,blobList,index):
#     '''
#     Compute the closest ennemy index
#     '''
#     closest_index = 0
#     closest_distance = 1e9
#     for i in range(len(blobList)):
#         if(i != closest_index):
#             
#             dist = np.linalg.norm(blobList[i].sub_blobs[0,0:2] - blobs_infos[0,0:2])
#             
#             if(dist < closest_distance):
#                 closest_distance = dist
#                 closest_index = i
#         
#     self.closest_ennemy_index = closest_index
#     
# def compute_closest_food(self,food):
#     '''
#     Compute the closest food index
#     '''        
#     pass
#     # self.closest_food_index = 
# 
#     
# def compute_closest_projectile(self,projectiles):
#     '''
#     Compute the closest projectile index
#     '''
#     pass
#     # self.closest_projectile_index = 
    
    
    