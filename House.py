import WorldEdit
from Structure import Structure
import numpy as np
import os

# TODO implement rotation


class House:

    structures = dict()
    houseWidth = 22
    houseDepth = 22

    def __init__(self, x, y, z, rotation=Structure.ROTATE_NORTH):
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
        for floorIndex in range(self.numberOfFloors):

            if floorIndex == 0:
                structure = self._getStructure('bottomFloor')
            elif floorIndex == self.numberOfFloors - 1:
                structure = self._getStructure('roof')
            else:
                structure = self._getStructure('floor')

            self._buildStructure(structure, yOffset)

            yOffset = yOffset + structure.getSizeY()

    def _getStructure(self, structureType):
        return Structure(self.rng.choice(self.structures[structureType]))

    def _buildStructure(self, structure, yOffset):
        zOffset = self.z - structure.getSizeZ()
        structure.setPosition(self.x, self.y + yOffset, zOffset)
        structure.place()
        WorldEdit.fillEmpty(
            self.x, self.y + yOffset, self.z,
            self.x + self.houseWidth - 1, self.y + yOffset, zOffset + self.houseDepth,
            self.interiorFloorMaterial
        )
