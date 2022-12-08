from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def count_lakes_and_bays(prop):
    symbol = ~prop.image
    lb = label(symbol)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        flag = True
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == prop.image.shape[0] - 1 or x == prop.image.shape[1] - 1:
                flag = False
                break
        count_lakes += int(flag)
        count_bays += int(not flag)
    return count_lakes, count_bays

def has_vline(prop):
    return 1. in prop.image.mean(0)

def filling_factor(prop):
    return prop.image.sum() / prop.image.size


# *(X) , D(P)
def recognize(image):
    result = defaultdict(lambda: 0)
    labeled = label(image)
    props = regionprops(labeled)
    distances = []
    
    for prop in props:
        lakes, bays = count_lakes_and_bays(prop)
        
        if np.all(prop.image):
            result["-"] += 1
            
        elif lakes == 0: # / X * W
            if has_vline(prop):
                result["1"] += 1
            
            elif bays == 2:
                result["/"] += 1
            
            elif prop.eccentricity > 0.5:    
                if prop.eccentricity > 0.65:
                    result["X"] += 1
                else:
                    result["W"] += 1
                    
            else:
                result["*"] += 1
        
        elif lakes == 1: # A P D 0
            
            if bays == 3:
                result["A"] += 1
            
            elif bays == 2: # P D
                if prop.eccentricity > 0.7:
                    result["P"] += 1
                else:
                    result["D"] += 1
                    
            else:
                result["0"] += 1
                    
        elif lakes == 2:
            
            if has_vline(prop) and bays == 2:
                result["B"] += 1
            else:
                result["8"] += 1
                
        else:
            result["unknown"] += 1
    
    return result, distances


image = plt.imread('./files/symbols.png')
image = np.mean(image, 2)

image[image > 0] = 1
    
result, distance = recognize(image)

for key in result.keys():
    print(key, result[key])

