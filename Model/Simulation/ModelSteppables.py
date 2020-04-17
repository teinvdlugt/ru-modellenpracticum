from cc3d.core.PySteppables import *

# Model parameters
collagen_length = 10
collagen_thickness = 1


class InitialiserSteppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        for cell in self.cellList:
            if cell.type == 2: # Tumor
                cell.targetVolume = 64  # 8x8 pixels
                cell.lambdaVolume = 10  # from Scianna et al.
            if cell.type == 1: # Collagen
                cell.targetVolume = collagen_length * collagen_thickness
                cell.lambdaVolume = 11


# Maybe add growth, mitosis steppables
