from House import House
from Structure import Structure


class Courtyard(House):

    def _getStructureFiles(self):
        self.structures['courtyard'] = Structure.getStructuresInDir('courtyard')

    def place(self):
        Structure(
            self.rng.choice(self.structures['courtyard']),
            x=self.x, y=self.y, z=self.z,
            rotation=self.rng.integers(4),
            rotateAroundCenter=True
        ).place(includeAir=False)
