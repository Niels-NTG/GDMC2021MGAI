import Structure
import interfaceUtils
import WorldEdit
import nbt
import numpy as np
from random import sample

intersection = Structure.Structure('intersection', -80, 3, 135, 1)
#intersection.place()
objects = ['tree1','tree2','tree3','tree4','lantern']
crosswalks = ['crosswalk_s', 'crosswalk_plain']

def vertical_street(x, y, z):
    x_increase = 0
    y_increase = 0
    z_increase = 0
    
    #sidewalk
    for i in range(8):
        sidewalk = Structure.Structure('sidewalk_object_middle', x + x_increase, y, z, 0)
        x_increase += 8
        sidewalk.place()

    #asphalt
    x_increase = 0
    y_increase = -1   
    z_increase = 5
    for i in range(8):
        asphalt = Structure.Structure('asphalt_plain', x + x_increase, y + y_increase, z + z_increase, 0)

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
            sidewalk = Structure.Structure('sidewalk_object_middle', x + x_increase, y, z + z_increase, 0)
        
        else:
            sidewalk = Structure.Structure('sidewalk_object_middle', x + x_increase, y, z + z_increase, 0)
        
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
        intersection = Structure.Structure('intersection_plain', x, y -1, z, 0)
        
    elif epsilon == 3:
        intersection = Structure.Structure('intersection_1_stoplight', x, y-1, z, 0)
    else: 
        intersection = Structure.Structure('intersection_2_stoplight', x, y-1, z, 0)
    
    intersection.place()

    #objects integration?
    #x_increase = 0
    #y_increase = 0   
    #z_increase = 1
    #element = select_object(x, y, z, x_increase, y_increase, z_increase)
    #if element != None:
            #element.place()
    

def select_object(x, y, z, x_increase, y_increase, z_increase, intersect=False): 
    
    lantern = Structure.Structure('lantern', x + x_increase, y, z + z_increase, 0)
    tree1 = Structure.Structure('tree_1', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    tree2 = Structure.Structure('tree_2', x + x_increase, y, z + z_increase, 0)
    tree3 = Structure.Structure('tree_3', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    tree4 = Structure.Structure('tree_4', x - 1 + x_increase, y, z - 1 + z_increase, 0)
    

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
    
  
#Vertical Lines
#intersection(-330, 4, 460)
#vertical_street(-330 + 22, 4, 460)
#intersection(-330 + 86, 4, 460)
#vertical_street(-330 + 108, 4, 460)
#intersection(-330 + 172, 4, 460)


#intersection(-330, 4, 460 + 64)
#vertical_street(-330 + 22, 4, 460 + 64)
#intersection(-330 + 86, 4, 460 + 64)
#vertical_street(-330 + 108, 4, 460+ 64)
#intersection(-330 + 172, 4, 460+ 64)

#intersection(-330, 4, 460+128)
#vertical_street(-330 + 22, 4, 460+128)
#intersection(-330 + 86, 4, 460+128)
#vertical_street(-330 + 108, 4, 460+128)
#intersection(-330 + 172, 4, 460+128)

sidewalk = Structure.Structure('sidewalk_object_middle',-384, 4, 497, 3)
sidewalk.place()