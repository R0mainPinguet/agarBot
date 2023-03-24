
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