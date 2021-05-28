import mapUtils
from worldLoader import WorldSlice
import interfaceUtils
import numpy as np
from CornerHouse import CornerHouse
from House import House
from Courtyard import Courtyard
import street
import WorldEdit
import threading

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


# builds a 64x64 grid filled with houses
# builds towards positive x and positive z
# corners and middle house coordinates are hard coded and correspond
# with house sizes 21x21 for corners and 22x21 (width x depth) for middlehouses
def buildHouseblock(x, y, z):
    corners = [(x + 63 - 20, z + 63 - 20), (x + 20, z + 63 - 20), (x + 20, z + 20), (x + 62 - 20, z + 20)]
    middles = [(x + 21, z + 63 - 20), (x + 20, z + 21), (x + 21 + 21, z + 20), (x + 63 - 20, z + 21 + 21)]

    rotation = 0
    for (xplace, zplace) in corners:
        newhouse = CornerHouse(x=xplace, y=y, z=zplace, rotation=rotation)
        threading.Thread(target=newhouse.place).start()
        rotation += 1
    rotation = 0
    for (xplace, zplace) in middles:
        newhouse = House(x=xplace, y=y, z=zplace, rotation=rotation)
        threading.Thread(target=newhouse.place).start()
        rotation += 1

    court = Courtyard(x=x + 21, y=y, z=z + 21)
    court.place()


# builds foundation for a 64x64 block
def foundation(x, y, z):
    farX = x + 63
    farZ = z + 63
    WorldEdit.fill(x, y - 1, z, farX, y, farZ, "minecraft:stone_bricks")


def generate_city_blocks(x, y, z):
    increase = 0
    for i in range(3):
        foundation(x + 10, y, z + 10 + increase)
        buildHouseblock(x + 10, y + 1, z + 10 + increase)
        increase += 86

    increase = 0
    for i in range(3):
        foundation(x + 10 + 86, y, z + 10 + increase)
        buildHouseblock(x + 10 + 86, y + 1, z + 10 + increase)
        increase += 86
    increase = 0
    for i in range(3):
        foundation(x + 10 + 86 + 86, y, z + 10 + increase)
        buildHouseblock(x + 10 + 86 + 86, y + 1, z + 10 + increase)
        increase += 86


def generate_city(x, y, z):
    threading.Thread(target=generate_city_blocks, args=(x, y, z)).start()
    threading.Thread(target=street.city_location, args=(x, y - 1, z)).start()


buildArea = getBuildArea()
worldSlice = WorldSlice(buildArea)

heightMap = np.array(mapUtils.calcGoodHeightmap(worldSlice))

generate_city(buildArea[0], mapUtils.getMostFrequentHeight(heightMap), buildArea[1])

if USE_BATCHING:
    interfaceUtils.sendBlocks()
