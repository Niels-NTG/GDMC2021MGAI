from House import House


class CornerHouse(House):

    def __init__(self, x, y, z, rotation):
        self.bottomFloorDir = 'cornerHouseBottomFloor'
        self.floorDir = 'cornerHouseFloor'
        super().__init__(x, y, z, rotation)
