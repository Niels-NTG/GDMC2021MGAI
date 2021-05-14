import WorldEdit
import nbt

# With this class you can load in an NBT-encoded Minecraft Structure file
# (https://minecraft.fandom.com/wiki/Structure_Block_file_format) and place them in the world.


class Structure:

    ROTATE_NORTH = 0
    ROTATE_WEST = 1
    ROTATE_SOUTH = 2
    ROTATE_EAST = 3
    ROTATIONS = ["north", "east", "south", "west"]

    def __init__(self, structure, x, y, z, rotation=ROTATE_NORTH):
        self.file = nbt.nbt.NBTFile('structures/' + structure + ".nbt", "rb")
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.materialReplacements = dict()

    def getSizeX(self):
        return self.file["size"][0].value

    def getSizeY(self):
        return self.file["size"][1].value

    def getSizeZ(self):
        return self.file["size"][2].value

    # Add dict of materials from the structure file that need replaced with something else.
    # eg. "minecraft:iron_block", "minecraft:gold_block" will put gold blocks where the structure file has iron blocks
    # when placing the structure in the world.
    def replaceMaterial(self, existingMaterial, newMaterial):
        self.materialReplacements[existingMaterial] = newMaterial

    def _calcBlockPosition(self, block):
        if self.rotation == 0:
            return [
                block["pos"][0].value + self.x,
                block["pos"][1].value + self.y,
                block["pos"][2].value + self.z
            ]
        elif self.rotation == 1:
            return [
                block["pos"][2].value + self.z,
                block["pos"][1].value + self.y,
                block["pos"][0].value + self.x
            ]
        elif self.rotation == 2:
            return [
                self.x - block["pos"][0].value,
                block["pos"][1].value + self.y,
                block["pos"][2].value + self.z
            ]
        elif self.rotation == 3:
            return [
                block["pos"][2].value + self.z,
                block["pos"][1].value + self.y,
                self.x - block["pos"][0].value
            ]

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

    def place(self, includeAir=False):
        for block in self.file["blocks"]:
            blockMaterial = self._getBlockMaterial(block)

            # Skip empty parts of the structure unless includeAir is True.
            if includeAir is False and blockMaterial == "minecraft:air":
                continue

            blockPosition = self._calcBlockPosition(block)
            blockProperties = self._getBlockProperties(block)
            WorldEdit.setBlock(blockPosition[0], blockPosition[1], blockPosition[2], blockMaterial, blockProperties)

        interfaceUtils.sendBlocks()
