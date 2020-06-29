from cc3d.core.PySteppables import *
import math


_8oversqrtpi = 8 / sqrt(math.pi)
def volume_to_surface(volume):
    """ Calculates perimeter(="surface") of a pixelated disk having the specified area(="volume").
        This stems from: vol = pi r^2, surface = 8 * r = 8 * sqrt(vol/pi). """
    return _8oversqrtpi * sqrt(volume)


class GrowthSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        for cell in self.cell_list_by_type(self.LOWER, self.UPPER):
            cell.targetVolume = cell.volume
            cell.lambdaVolume = 10.0
            cell.targetSurface = volume_to_surface(cell.targetVolume)
            cell.lambdaSurface = 2.0

    def step(self, mcs):
        for cell in self.cell_list_by_type(self.LOWER):
            cell.targetVolume += 0.1
            cell.targetSurface = volume_to_surface(cell.targetVolume)
