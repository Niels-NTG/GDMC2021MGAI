import WorldEdit
from Structure import Structure
import numpy as np
import os


class Courtyard:

    structures = dict()
    houseWidth = 21
    houseDepth = 21

    def __init__(self, x=0, y=0, z=0, rotation=Structure.ROTATE_NORTH):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation

        self.rng = np.random.default_rng()

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
        structure = self._getStructure('courtyard')
           
        self._buildStructure(structure, yOffset)

        yOffset = yOffset + structure.getSizeY()

    def _getStructure(self, structureType):
        return Structure(self.rng.choice(self.structures[structureType]), rotation=self.rotation)

    def _buildStructure(self, structure, yOffset):
        structure.setPosition(self.x, self.y + yOffset, self.z)
        structure.place()