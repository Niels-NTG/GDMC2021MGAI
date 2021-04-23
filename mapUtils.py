# ! /usr/bin/python3
"""### Provides tools for maps and heightmaps

This module contains functions to:
* Calculate a heightmap ideal for building
* Visualise numpy arrays
"""
__all__ = ['calcGoodHeightmap']
# __version__

import numpy as np


def calcGoodHeightmap(worldSlice):
    """**Calculates a heightmap ideal for building.**
    Trees are ignored and water is considered ground.

    Args:
        worldSlice (WorldSlice): an instance of the WorldSlice class containing the raw heightmaps and block data

    Returns:
        any: numpy array containing the calculated heightmap
    """
    hm_mbnl = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    heightmapNoTrees = hm_mbnl[:]
    area = worldSlice.rect

    for x in range(area[2]):
        for z in range(area[3]):
            while True:
                y = heightmapNoTrees[x, z]
                block = worldSlice.getBlockAt(
                    (area[0] + x, y - 1, area[1] + z))
                if block[-4:] == '_log':
                    heightmapNoTrees[x, z] -= 1
                else:
                    break

    return np.array(np.minimum(hm_mbnl, heightmapNoTrees))


def normalize(array):
    """**Normalizes the array to contain values from 0 to 1.**"""
    return (array - array.min()) / (array.max() - array.min())
