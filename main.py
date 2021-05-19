import mapUtils
from worldLoader import WorldSlice
import interfaceUtils
import numpy as np
from House import House
from CornerHouse import CornerHouse
from MiddleHouse import MiddleHouse
from Courtyard import Courtyard
from Structure import Structure 


# Do we send blocks in batches to speed up the generation process?
USE_BATCHING = True
BATCH_SIZE = 100


def getBuildArea(area=(0, 0, 128, 128)):
    # x position, z position, x size, z size

    # see if a build area has been specified
    # you can set a build area in minecraft using the /setbuildarea command
    serverBuildArea = interfaceUtils.requestBuildArea()
    if serverBuildArea != -1:
        x1 = serverBuildArea["xFrom"]
        z1 = serverBuildArea["zFrom"]
        x2 = serverBuildArea["xTo"]
        z2 = serverBuildArea["zTo"]
        area = (x1, z1, x2 - x1, z2 - z1)

    print("working in area xz s%s" % (str(area)))
    return area


buildArea = getBuildArea()
worldSlice = WorldSlice(buildArea)

heightMap = np.array(mapUtils.calcGoodHeightmap(worldSlice))



#builds a 64x64 grid filled with houses 
#builds towards positive x and positive z
#corners and middle house coordinates are hard coded and correspond
#with house sizes 21x21 for corners and 22x21 (width x depth) for middlehouses
def buildHouseblock(x, y, z):
    corners = [(x+63-20,z+63-20),(x+20,z+63-20),(x+20,z+20),(x+62-20,z+20)] 
    middles = [(x+21,z+63-20),(x+20,z+21), (x+21+21,z+20), (x+63-20,z+21+21)]   

    rotation = 0 
    for (xplace,zplace) in corners:
        newhouse = CornerHouse(x=xplace, y=y, z=zplace, rotation=rotation)
        newhouse.place()
        rotation += 1
    rotation = 0 
    for (xplace,zplace) in middles:
        newhouse = MiddleHouse(x=xplace, y=y, z=zplace, rotation=rotation)
        newhouse.place()
        rotation += 1
    
    court = Courtyard(x=x+21,y=y,z=z+21)
    court.place()



buildHouseblock(27, 4, -116)

if USE_BATCHING:
    interfaceUtils.sendBlocks()