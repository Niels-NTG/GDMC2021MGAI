import Structure
import interfaceUtils
import WorldEdit
import nbt
import numpy as np
from random import sample

objects = ['street/tree1','street/tree2','street/tree3','street/tree4','street/lantern']
crosswalks = ['street/crosswalk_s', 'street/crosswalk_plain']

def vertical_street(x, y, z):
    x_increase = 0
    y_increase = 0
    z_increase = 0
    
    #sidewalk
    for i in range(8):
        sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z, 0)
        x_increase += 8
        sidewalk.place()

    #asphalt
    x_increase = 0
    y_increase = -1   
    z_increase = 5
    for i in range(8):
        asphalt = Structure.Structure('street/asphalt_plain', x + x_increase, y + y_increase, z + z_increase, 0)

        if i == 0 or i == 7:
            if np.random.randint(low=1, high=3) == 2:
                type_crosswalk = sample(crosswalks, 1)[0]
                crosswalk = Structure.Structure(type_crosswalk, x + x_increase, y + y_increase, z + z_increase, 0)
                crosswalk.place()
            else:
                asphalt.place()
        else:        
            asphalt.place()
        x_increase += 8
    x_increase = 0
    z_increase += 12   
    #sidewalk 2
    for i in range(8):
        if np.random.randint(low=1, high=3) == 2:
            sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z + z_increase, 0)
        
        else:
            sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z + z_increase, 0)
        
        x_increase += 8
        sidewalk.place()

    #objects sidewalk
    x_increase = 2
    y_increase = 0   
    z_increase = 1
    for i in range(8):
        element = select_object(x, y, z,x_increase, y_increase, z_increase) 
        if element != None:
            element.place()

        x_increase += 8 

    #objects sidewalk2
    x_increase = 2
    y_increase = 0   
    z_increase = 18

    for i in range(8):
        element = select_object(x, y, z, x_increase, y_increase, z_increase) 
        if element != None:
            element.place()

        x_increase += 8
def intersection(x,y,z):
    epsilon = np.random.randint(low=1, high=4)
    if epsilon == 2:
        intersection = Structure.Structure('street/intersection_plain', x, y -1, z, 0)
        
    elif epsilon == 3:
        intersection = Structure.Structure('street/intersection_1_stoplight', x, y-1, z, 0)
    else: 
        intersection = Structure.Structure('street/intersection_2_stoplight', x, y-1, z, 0)
    
    intersection.place()

    #objects integration?
    #x_increase = 0
    #y_increase = 0   
    #z_increase = 1
    #element = select_object(x, y, z, x_increase, y_increase, z_increase)
    #if element != None:
            #element.place()
    

def select_object(x, y, z, x_increase, y_increase, z_increase, intersect=False): 
    
    lantern = Structure.Structure('street/lantern', x + x_increase, y, z + z_increase, 0)
    tree1 = Structure.Structure('street/tree_1', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    tree2 = Structure.Structure('street/tree_2', x + x_increase, y, z + z_increase, 0)
    tree3 = Structure.Structure('street/tree_3', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    tree4 = Structure.Structure('street/tree_4', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    

    #usually trees, sometimes lanterns sometimes nothing
    epsilon = np.random.randint(low=1, high=7)
    
    element = None
    if epsilon == 2:
        element = tree1
    elif epsilon == 3:
        element = tree2
    elif epsilon == 4: 
        element = tree3
    elif epsilon == 5:
        element = tree4    
    elif epsilon == 6:
        element = lantern 
    elif intersect==True:
        element = stoplight
    return element
    
def horizontal_street(x, y, z):
    x_increase = 0
    y_increase = 0
    z_increase = 0
    
    #sidewalk
    for i in range(8):
        sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z + z_increase, 1)
        z_increase += -8
        sidewalk.place()

    #asphalt
    x_increase = -5
    y_increase = -1   
    z_increase = 0
    for i in range(8):
        asphalt = Structure.Structure('street/asphalt_plain', x + x_increase, y + y_increase, z + z_increase, 1)

        if i == 0 or i == 7:
            if np.random.randint(low=1, high=3) == 2:
                type_crosswalk = sample(crosswalks, 1)[0]
                crosswalk = Structure.Structure(type_crosswalk, x + x_increase, y + y_increase, z + z_increase, 1)
                crosswalk.place()
            else:
                asphalt.place()
        else:        
            asphalt.place()
        z_increase += -8
    
    #sidewalk 2
    x_increase += -12
    z_increase += 8   
    for i in range(8):
        if np.random.randint(low=1, high=3) == 2:
            sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z + z_increase, 1)
        
        else:
            sidewalk = Structure.Structure('street/sidewalk_object_middle', x + x_increase, y, z + z_increase, 1)
        
        z_increase += 8
        sidewalk.place()

    #objects sidewalk
    x_increase = -3
    y_increase = 0   
    z_increase = 2
    for i in range(8):
        element = select_object(x, y, z,x_increase, y_increase, z_increase) 
        if element != None:
            element.place()

        z_increase += -8 

    #objects sidewalk2
    x_increase += -17
    y_increase = 0   
    z_increase = 2

    for i in range(8):
        element = select_object(x, y, z, x_increase, y_increase, z_increase) 
        if element != None:
            element.place()

        z_increase += -8
#spawns the streets. 10 blocks from the outline of the 256x256 grid
def city_network(x, y, z):
    init_x = 31
    init_z = -13
    #horizontal_street(x + 95, y, z + init_z + 65)

    horizontal_street(x + init_x + 64, y, z + init_z + 78)
    horizontal_street(x + init_x + 150, y, z + init_z + 78)
    horizontal_street(x + init_x + 64, y, z + init_z + 78 + 86)
    horizontal_street(x + init_x + 150, y, z + init_z + 78 + 86)
    horizontal_street(x + init_x + 64, y, z + init_z + 78 + 86 + 86)
    horizontal_street(x + init_x + 150, y, z + init_z + 78 + 86 + 86)

    intersection(x + init_x + 43, y, z + init_z + 86)
    intersection(x + init_x + 43, y, z + init_z + 86 + 86)
    intersection(x + init_x + 43 + 86, y, z + init_z + 86)
    intersection(x + init_x + 43 + 86, y, z + init_z + 86 + 86)

    vertical_street(x + init_x + 65 - 86, y, z + init_z + 86)
    vertical_street(x + init_x + 65, y, z + init_z + 86)
    vertical_street(x + init_x + 65 + 86, y, z + init_z + 86)
    vertical_street(x + init_x + 65 - 86, y, z + init_z + 86 + 86)
    vertical_street(x + init_x + 65, y, z + init_z + 86 + 86)
    vertical_street(x + init_x + 65 + 86, y, z + init_z + 86 + 86)


#square city 

#left side city net
#intersection(-1031, 4, 508)
#horizontal_street(-1031 + 21, 4, 508 + 78)
#vertical_street(-1031 + 22, 4, 508)
#horizontal_street(-1031 + 107, 4, 508 + 78)
#intersection(-1031 + 86, 4, 508)
#vertical_street(-1031 + 108, 4, 508)
#horizontal_street(-1031 + 193, 4, 508 + 78)
#intersection(-1031 + 172, 4, 508)

#middle city network
#intersection(-1031, 4, 508 + 86)
#vertical_street(-1031 + 22, 4, 508 + 86)
#intersection(-1031 + 86, 4, 508 + 86)
#vertical_street(-1031 + 108, 4, 508+ 86)
#intersection(-1031 + 172, 4, 508+ 86)

#right side city network
#intersection(-1031, 4, 508+172)
#horizontal_street(-1031 + 21, 4, 508 + 78 + 86)
#vertical_street(-1031 + 22, 4, 508+ 172)
#horizontal_street(-1031 + 21 + 86, 4, 508 + 78 + 86)
#intersection(-1031 + 86, 4, 508+172)
#vertical_street(-1031 + 108, 4, 508+172)
#horizontal_street(-1031 + 21 + 86 + 86, 4, 508 + 78 + 86)
#intersection(-1031 + 172, 4, 508+172)

#horizontal_street(-385, 4, 217)
#sidewalk = Structure.Structure('street/sidewalk_object_middle',-384, 4, 497, 1)
#sidewalk.place()

#insert your x,y,z values y should be 4!
city_network(-380, 4, 14)