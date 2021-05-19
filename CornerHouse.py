import WorldEdit
from Structure import Structure
import numpy as np
import os


class CornerHouse:

    structures = dict()
    houseWidth = 21
    houseDepth = 21

    def __init__(self, x=0, y=0, z=0, rotation=Structure.ROTATE_NORTH):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation

        self.rng = np.random.default_rng()

        # Set random number of floors between 6 and 9
        self.numberOfFloors = self.rng.integers(6, 8)

        self.interiorFloorMaterial = self.rng.choice([
            "minecraft:birch_planks",
            "minecraft:acacia_planks",
            "minecraft:dark_oak_planks",
            "minecraft:jungle_planks",
            "minecraft:oak_planks",
            "minecraft:spruce_planks"
        ])

        self._getStructureFiles()

    def _getStructureFiles(self):
        structureTypes = os.listdir("./structures")
        for structureType in structureTypes:
            if structureType.endswith('.nbt'):
                continue
            structuresOfType = [
                structureType + '/' + s.replace(".nbt", "") for s in os.listdir("./structures/" + structureType)
            ]
            self.structures[structureType] = structuresOfType

    def place(self):
        yOffset = 0
        upperFloor = False
        for floorIndex in range(self.numberOfFloors):

            if floorIndex == 0:
                structure = self._getStructure('bottomCorner')
            elif not upperFloor:
                structure = self._getStructure('upperCorner')
                upperFloor = True

            self._buildStructure(structure, yOffset)

            yOffset = yOffset + structure.getSizeY()

    def _getStructure(self, structureType):
        return Structure(self.rng.choice(self.structures[structureType]), rotation=self.rotation)

    def _buildStructure(self, structure, yOffset):
        structure.setPosition(self.x, self.y + yOffset, self.z)
        structure.place()
