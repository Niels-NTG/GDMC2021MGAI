import mapUtils
from worldLoader import WorldSlice
import interfaceUtils
import numpy as np

# Do we send blocks in batches to speed up the generation process?
USE_BATCHING = True
BATCH_SIZE = 100

def getGroundLevelAt(_heightMap, _area, x, z):
    return _heightMap[(x - _area[0], z - _area[1])]


def buildFloor(x, y, z, xSize, zSize, material):
    for xIndex in range(x, x + xSize):
        for zIndex in range(z, z + zSize):
            interfaceUtils.setBlock(xIndex, y, zIndex, material)


def buildWestEastWall(x, y, z, length, height, material):
    for zIndex in range(z, z + length):
        for yIndex in range(y, y + height):
            interfaceUtils.setBlock(x, yIndex, zIndex, material)


def buildNorthSouthWall(x, y, z, length, height, material):
    for xIndex in range(x, x + length):
        for yIndex in range(y, y + height):
            interfaceUtils.setBlock(xIndex, yIndex, z, material)


def buildPole(x, y, z, height, material):
    buildNorthSouthWall(x, y, z, 1, height, material)


def buildHouse(area, _heightMap):
    # TODO change type of material based on biome
    baselineHeight = np.max(_heightMap)

    interfaceUtils.clear(area[0], baselineHeight, area[1], area[2], baselineHeight + 8, area[3])

    # buildFloor(area[0], baselineHeight, area[1], area[2], area[3], "oak_planks")
    #
    # for corner in [(area[0], area[1]), (area[2], area[1]), (area[2], area[3]), (area[0], area[3])]:
    #
    #     poleBase = _heightMap[corner[0], corner[1]]
    #     buildPole(corner[0], poleBase, corner[1], baselineHeight - poleBase, "oak_log")


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

buildHouse(area=(0, 0, 8, 8), _heightMap=heightMap[0:9, 0:9])

if USE_BATCHING:
    interfaceUtils.sendBlocks()
