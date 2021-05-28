from Structure import Structure
from materials import Fences, Walls, BuildingBlocks, Doors
import numpy as np


class House:

    bottomFloorDir = 'bottomFloor'
    floorDir = 'floor'
    roofDir = 'roof'

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

        self.structures = dict()

        self._getStructureFiles()

    def _getStructureFiles(self):
        self.structures['bottomFloor'] = Structure.getStructuresInDir(self.bottomFloorDir)
        self.structures['floor'] = Structure.getStructuresInDir(self.floorDir)
        self.structures['roof'] = Structure.getStructuresInDir(self.roofDir)

    def findMaterials(self, structure):
        materials = structure.getMaterialList()
        materialSet = set(materials)
        materialsDict = {}

        # find the current balcony
        fence = materialSet.intersection(Fences)
        if fence:
            fence = fence.pop()
            materialsDict['fence'] = fence

        wall = materialSet.intersection(Walls)
        if wall:
            wall = wall.pop()
            materialsDict['wall'] = wall

        buildingblock = materialSet.intersection(BuildingBlocks)
        if buildingblock:
            buildingblock = buildingblock.pop()
            materialsDict['buildingblock'] = buildingblock

        door = materialSet.intersection(Doors)
        if door:
            door = door.pop()
            materialsDict['door'] = door

        return materialsDict

    def place(self):

        yOffset = 0

        # True if materials of the building are already set.
        hasChosenMaterials = False

        for floorIndex in range(self.numberOfFloors):

            if floorIndex == 0:
                structure = self._getStructure('bottomFloor')
                defaultMaterials = self.findMaterials(structure)
                if 'buildingblock' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['buildingblock'], self.rng.choice(BuildingBlocks))
                if 'door' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['door'], self.rng.choice(Doors))
            elif not hasChosenMaterials:
                structure = self._getStructure('floor')
                defaultMaterials = self.findMaterials(structure)
                if 'fence' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['fence'], self.rng.choice(Fences))
                if 'wall' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['wall'], self.rng.choice(Walls))
                if 'buildingblock' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['buildingblock'], self.rng.choice(BuildingBlocks))
                if 'door' in defaultMaterials:
                    structure.replaceMaterial(defaultMaterials['door'], self.rng.choice(Doors))
                hasChosenMaterials = True

            structure.setPosition(y=self.y + yOffset)
            structure.place()

            yOffset = yOffset + structure.getSizeY()

    def _getStructure(self, structureType):
        return Structure(
            self.rng.choice(self.structures[structureType]),
            x=self.x, y=self.y, z=self.z,
            rotation=self.rotation
        )
