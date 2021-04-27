import WorldEdit
import nbt

# With this class you can load in an NBT-encoded Minecraft Structure file
# (https://minecraft.fandom.com/wiki/Structure_Block_file_format) and place them in the world.

class Structure:

    ROTATE_NORTH = 0
    ROTATE_WEST = 1
    ROTATE_SOUTH = 2
    ROTATE_EAST = 3

    def __init__(self, structure, x, y, z, rotation=ROTATE_NORTH):
        self.file = nbt.nbt.NBTFile('structures/' + structure + ".nbt", "rb")
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation
        self.materialReplacements = dict()

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

    def place(self, includeAir=False):
        for block in self.file["blocks"]:
            blockMaterial = self._getBlockMaterial(block)
            # Skip empty parts of the structure unless includeAir is True.
            if includeAir is False and blockMaterial == "minecraft:air":
                continue

            blockPosition = self._calcBlockPosition(block)
            WorldEdit.setBlock(blockPosition[0], blockPosition[1], blockPosition[2], blockMaterial)
