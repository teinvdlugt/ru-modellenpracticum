from cc3d.core.PySteppables import *
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=10):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        for cell in self.cell_list:
            if cell.type == self.LOWER:
                cell.targetVolume = 105
                cell.lambdaVolume = 10
            if cell.type == self.UPPER:
                cell.targetVolume = 253
                cell.lambdaVolume = 10

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.LOWER:
                cell.targetVolume += 1
