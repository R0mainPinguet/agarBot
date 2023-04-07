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

    
def check_collisions(rules,blobs_list,blobs_infos,eating_percentage):
    
    for i in range(len(blobs_list)):
        
        blob_i = blobs_list[i]
        
        for j in range(len(blobs_list)):
            
            if(i!=j):
                
                blob_j = blobs_list[j]
                
                for ii in range(blob_i.actual_sub_blob-1,-1,-1):
                    
                    for jj in range(blob_j.actual_sub_blob-1,-1,-1):
                        
                        size_ii = blobs_infos[blob_i.index+ii,4] 
                        size_jj = blobs_infos[blob_j.index+jj,4] 
                        
                        radius_ii = np.sqrt(size_ii / np.pi)
                        radius_jj = np.sqrt(size_jj / np.pi)
                        
                        dist = np.linalg.norm(blobs_infos[blob_i.index+ii,0:2]-blobs_infos[blob_j.index+jj,0:2])
                        
                        
                        if(dist < radius_ii and size_ii * eating_percentage > size_jj):
                            
                            blobs_infos[blob_i.index+ii,4] += size_jj
                            
                            for k in range(jj+1,blob_j.actual_sub_blob):
                                
                                blobs_infos[blob_j.index+k-1] = blobs_infos[blob_j.index+k] 
                                blob_j.collisions_test[k-1] = blob_j.collisions_test[k]
                                blob_j.collisions_time[k-1] = blob_j.collisions_time[k]
                            
                            blob_j.actual_sub_blob -= 1
                            
                            if(blob_j.actual_sub_blob==0):
                                blob_j.respawn(blobs_infos,rules)
                            
                        elif(dist < radius_jj and size_jj * eating_percentage > size_ii):
                            
                            blobs_infos[blob_j.index+jj,4] += size_ii
                            
                            for k in range(ii+1,blob_i.actual_sub_blob):
                                
                                blobs_infos[blob_i.index+k-1] = blobs_infos[blob_i.index+k] 
                                blob_i.collisions_test[k-1] = blob_i.collisions_test[k]
                                blob_i.collisions_time[k-1] = blob_i.collisions_time[k]
                                
                            
                            blob_i.actual_sub_blob -= 1
                            
                            if(blob_i.actual_sub_blob==0):
                                blob_i.respawn(blobs_infos,rules)
                            
                            
                            
                
                
            
            
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    