import WorldEdit
from Structure import Structure
from materials import Fences, Walls, BuildingBlocks, Doors
import numpy as np
import os


class MiddleHouse:

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
        #determine if the upperfloor is already chosen
        upperFloor = False
        for floorIndex in range(self.numberOfFloors):

            if floorIndex == 0:
                structure = self._getStructure('bottomMiddle')
                default_materials = self.findmaterials(structure)
                if 'buildingblock' in default_materials:
                    structure.replaceMaterial(default_materials['buildingblock'], self.rng.choice(BuildingBlocks))
                if 'door' in default_materials:
                    structure.replaceMaterial(default_materials['door'], self.rng.choice(Doors))
            elif not upperFloor:
                structure = self._getStructure('upperMiddle')
                default_materials = self.findmaterials(structure)
                if 'fence' in default_materials:
                    structure.replaceMaterial(default_materials['fence'], self.rng.choice(Fences))
                if 'wall' in default_materials:
                    structure.replaceMaterial(default_materials['wall'], self.rng.choice(Walls))
                if 'buildingblock' in default_materials:
                    structure.replaceMaterial(default_materials['buildingblock'], self.rng.choice(BuildingBlocks))
                if 'door' in default_materials:
                    structure.replaceMaterial(default_materials['door'], self.rng.choice(Doors))
                upperFloor = True

            self._buildStructure(structure, yOffset)

            yOffset = yOffset + structure.getSizeY()

    def findmaterials(self, structure):
        materials = structure.getMaterialList()
        material_set = set(materials)
        material_dict = {}

        #find the current balcony
        fence = material_set.intersection(Fences)
        if fence:
            fence = fence.pop()
            material_dict['fence'] = fence

        wall = material_set.intersection(Walls)
        if wall:
            wall = wall.pop()
            material_dict['wall'] = wall
        
        buildingblock = material_set.intersection(BuildingBlocks)
        if buildingblock:
            buildingblock = buildingblock.pop()
            material_dict['buildingblock'] = buildingblock
    
        door = material_set.intersection(Doors)
        if door:
            door = door.pop()
            material_dict['door'] = door

        return material_dict

    def _getStructure(self, structureType):
        return Structure(self.rng.choice(self.structures[structureType]), rotation=self.rotation)

    def _buildStructure(self, structure, yOffset):
        structure.setPosition(self.x, self.y + yOffset, self.z)
        structure.place()
