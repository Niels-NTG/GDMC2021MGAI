import numpy as np
import WorldEdit
import nbt
import interfaceUtils
import mapUtils


# With this class you can load in an NBT-encoded Minecraft Structure file
# (https://minecraft.fandom.com/wiki/Structure_Block_file_format) and place them in the world.


# TODO add optional JSON file to each structure defining the origin of the structure


class Structure:
    ROTATE_NORTH = 0
    ROTATE_EAST = 1
    ROTATE_SOUTH = 2
    ROTATE_WEST = 3
    ROTATIONS = ["north", "east", "south", "west"]
    rotation = ROTATE_NORTH

    debug = False

    def __init__(self,
                 structure: str,
                 x: int = 0, y: int = 0, z: int = 0,
                 rotation: int = ROTATE_NORTH,
                 originX: int = 0, originY: int = 0, originZ: int = 0,
                 rotateAroundCenter: bool = False
                 ):
        self.file = nbt.nbt.NBTFile('structures/' + structure + ".nbt", "rb")
        self.x = x
        self.y = y
        self.z = z
        self.origin = [originX, originY, originZ]
        # If true, set origin to the center of the block. Use structures with an odd size value on both the X and Z
        # axis for the best, most predictable result.
        if rotateAroundCenter:
            self.origin = self.getHorizontalCenter()
        self.setRotation(rotation)
        self.materialReplacements = dict()

    def setPosition(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def setOrigin(self, x=None, y=None, z=None):
        if x is not None:
            self.origin[0] = x
        if y is not None:
            self.origin[1] = y
        if z is not None:
            self.origin[2] = z

    def setRotation(self, rotation):
        if rotation is not None and 0 <= rotation <= 3:
            self.rotation = rotation

        # Change position of blocks inside structure to match rotation.
        if rotation != self.ROTATE_NORTH:
            for block in self.file["blocks"]:
                currentPosition = [
                    block["pos"][0].value,
                    block["pos"][1].value,
                    block["pos"][2].value
                ]
                newPosition = mapUtils.rotatePointAroundOrigin(self.origin, currentPosition, rotation)
                block["pos"][0].value = newPosition[0]
                block["pos"][1].value = newPosition[1]
                block["pos"][2].value = newPosition[2]

    def getSizeX(self):
        return self.file["size"][0].value

    def getSizeY(self):
        return self.file["size"][1].value

    def getSizeZ(self):
        return self.file["size"][2].value

    def getOriginInWorldSpace(self):
        return [
            self.x + self.origin[0],
            self.y + self.origin[1],
            self.z + self.origin[2]
        ]

    def getFarCornerInWorldSpace(self):
        worldSpaceOrigin = self.getOriginInWorldSpace()
        return mapUtils.rotatePointAroundOrigin(
            worldSpaceOrigin,
            [
                worldSpaceOrigin[0] + (self.getSizeX() - self.origin[0]) - 1,
                worldSpaceOrigin[1] + (self.getSizeY() - self.origin[1]) - 1,
                worldSpaceOrigin[2] + (self.getSizeZ() - self.origin[2]) - 1
            ],
            self.rotation
        )

    def getHorizontalCenter(self):
        return [
            int(np.round(self.getSizeX() / 2)),
            self.origin[1],
            int(np.round(self.getSizeZ() / 2))
        ]

    def getShortestDimension(self):
        if self.rotation % 2 == 0:
            return np.argmin([np.abs(self.getSizeX()), np.abs(self.getSizeY()), np.abs(self.getSizeZ())])
        return np.argmin([np.abs(self.getSizeZ()), np.abs(self.getSizeY()), np.abs(self.getSizeX())])

    def getLongestDimension(self):
        if self.rotation % 2 == 0:
            return np.argmax([np.abs(self.getSizeX()), np.abs(self.getSizeY()), np.abs(self.getSizeZ())])
        return np.argmax([np.abs(self.getSizeZ()), np.abs(self.getSizeY()), np.abs(self.getSizeX())])

    def getShortestHorizontalDimension(self):
        if self.rotation % 2 == 0:
            return np.argmin([np.abs(self.getSizeX()), np.abs(self.getSizeZ())]) * 2
        return np.argmin([np.abs(self.getSizeZ()), np.abs(self.getSizeX())]) * 2

    def getLongestHorizontalDimension(self):
        if self.rotation % 2 == 0:
            return np.argmax([np.abs(self.getSizeX()), np.abs(self.getSizeZ())]) * 2
        return np.argmax([np.abs(self.getSizeZ()), np.abs(self.getSizeX())]) * 2

    def getShortestSize(self):
        if self.rotation % 2 == 0:
            return [self.getSizeX(), self.getSizeY(), self.getSizeZ()][self.getShortestDimension()]
        return [self.getSizeZ(), self.getSizeY(), self.getSizeX()][self.getShortestDimension()]

    def getLongestSize(self):
        if self.rotation % 2 == 0:
            return [self.getSizeX(), self.getSizeY(), self.getSizeZ()][self.getLongestDimension()]
        return [self.getSizeZ(), self.getSizeY(), self.getSizeX()][self.getLongestDimension()]

    def getShortestHorizontalSize(self):
        if self.rotation % 2 == 0:
            return [self.getSizeX(), 0, self.getSizeZ()][self.getShortestHorizontalDimension()]
        return [self.getSizeZ(), 0, self.getSizeX()][self.getShortestHorizontalDimension()]

    def getLongestHorizontalSize(self):
        if self.rotation % 2 == 0:
            return [self.getSizeX(), 0, self.getSizeZ()][self.getLongestHorizontalDimension()]
        return [self.getSizeZ(), 0, self.getSizeX()][self.getLongestHorizontalDimension()]

    # Add dict of materials from the structure file that need replaced with something else.
    # eg. "minecraft:iron_block", "minecraft:gold_block" will put gold blocks where the structure file has iron blocks
    # when placing the structure in the world.
    def replaceMaterial(self, existingMaterial, newMaterial):
        self.materialReplacements[existingMaterial] = newMaterial

    def _getBlockMaterial(self, block):
        blockMaterial = self.file["palette"][block["state"].value]['Name'].value
        replacementMaterial = self.materialReplacements.get(blockMaterial)
        if replacementMaterial is None:
            return blockMaterial
        return replacementMaterial

    # Get block properties (also known as block states: https://minecraft.fandom.com/wiki/Block_states) of a block.
    # This may contain information on the orientation of a block or open or closed stated of a door.
    def _getBlockProperties(self, block):
        properties = dict()
        if "Properties" in self.file["palette"][block["state"].value].keys():
            for key in self.file["palette"][block["state"].value]["Properties"].keys():
                properties[key] = self.file["palette"][block["state"].value]["Properties"][key].value

                # Apply rotation to block property if needed.
                if key == "facing" and self.rotation != self.ROTATE_NORTH:
                    properties[key] = self.ROTATIONS[
                        (self.ROTATIONS.index(properties[key]) + self.rotation) % len(self.ROTATIONS)
                        ]
                if key == "axis" and (self.rotation == self.ROTATE_EAST or self.rotation == self.ROTATE_WEST):
                    if properties[key] == "x":
                        properties[key] = "z"
                    elif properties[key] == "z":
                        properties[key] = "x"

        return properties

    def getMaterialList(self):
        materials = []
        for block in self.file["blocks"]:
            blockMaterial = self._getBlockMaterial(block)
            if blockMaterial not in materials:
                materials.append(blockMaterial)
        return materials

    def place(self, includeAir=True):
        for block in self.file["blocks"]:
            blockMaterial = self._getBlockMaterial(block)

            # Skip empty parts of the structure unless includeAir is True.
            if includeAir is False and blockMaterial == "minecraft:air":
                continue

            blockPosition = [
                block["pos"][0].value + self.x,
                block["pos"][1].value + self.y,
                block["pos"][2].value + self.z
            ]
            blockProperties = self._getBlockProperties(block)
            WorldEdit.setBlock(blockPosition[0], blockPosition[1], blockPosition[2], blockMaterial, blockProperties)

        interfaceUtils.sendBlocks()

        if self.debug:
            WorldEdit.fill(
                *self.getOriginInWorldSpace(),
                *self.getOriginInWorldSpace(),
                "minecraft:orange_wool"
            )
            WorldEdit.fill(
                *self.getFarCornerInWorldSpace(),
                *self.getFarCornerInWorldSpace(),
                "minecraft:purple_wool"
            )
