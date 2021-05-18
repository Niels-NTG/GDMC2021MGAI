import WorldEdit
import mapUtils
from Structure import Structure
import numpy as np
import os


class House:

    structures = dict()
    houseWidth = 22
    houseDepth = 22

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
        for floorIndex in range(self.numberOfFloors):

            if floorIndex == 0:
                structure = self._getStructure('bottomFloor', yOffset)
            elif floorIndex == self.numberOfFloors - 1:
                structure = self._getStructure('roof', yOffset)
            else:
                structure = self._getStructure('floor', yOffset)

            self._buildStructure(structure)

            structureOrigin = structure.getOriginInWorldSpace()
            structureFarCorner = structure.getFarCornerInWorldSpace()
            structureFarCorner[1] = structure.y
            floorPerimiter = [
                *structureOrigin,
                *structureFarCorner
            ]
            print(floorPerimiter)
            # TODO draw floor by projecting point outwards? https://stackoverflow.com/questions/9605556/how-to-project-a-point-onto-a-plane-in-3d

            yOffset = yOffset + structure.getSizeY()

    def _getStructure(self, structureType, yOffset):
        return Structure(
            self.rng.choice(self.structures[structureType]),
            x=self.x, y=self.y + yOffset, z=self.z,
            rotation=self.rotation
        )

    def _buildStructure(self, structure):
        structure.place()

