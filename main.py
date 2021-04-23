import mapUtils
from worldLoader import WorldSlice
import interfaceUtils
import numpy as np

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

if USE_BATCHING:
    interfaceUtils.sendBlocks()
