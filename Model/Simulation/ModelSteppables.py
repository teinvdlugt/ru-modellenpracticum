from cc3d.core.PySteppables import *
import math


# Volume, surface, growth and mitosis parameters
# tumor_initial_volume = 64.0  # Is now automatically set from PIF file, see InitialiserSteppable
tumor_lambda_volume = 10.0  # from Scianna et al.
# tumor_initial_surface = 8 * sqrt(tumor_initial_volume / math.pi)  # See also volume_to_surface function
tumor_lambda_surface = 1.0  # TODO what does Scianna say?
tumor_growth_rate = 0.05  # per MCS -- be sure to keep this a float

tumor_initial_volume = 64.0
mitosis_threshold = 2 * tumor_initial_volume  # cell divides if volume > mitosis_threshold
volume_steppable_frequency = 20  # Maybe change this frequency. I have set it to 10 to reduce computation

# Proteolysis parameters
collagen_lambda_volume = 100.0  # The lower(?) this value, the easier proteolysis. In Scianna et al.: 11.0


_8oversqrtpi = 8 / sqrt(math.pi)
def volume_to_surface(volume):
    """ Calculates surface of a pixelated sphere having the specified volume.
        This stems from: vol = pi r^2, surface = 8 * r = 8 * sqrt(vol/pi). """
    return _8oversqrtpi * sqrt(volume)


class InitialiserSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Nothing here.
        return


class VolumeSurfaceSteppable(SteppableBasePy):
    def __init__(self, frequency=volume_steppable_frequency):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Initialise cell volumes
        for cell in self.cellList:
            if cell.type == self.TUMOR:
                cell.targetVolume = cell.volume  # Set targetVolume equal to actual volume of initial condition
                cell.lambdaVolume = tumor_lambda_volume
                cell.targetSurface = volume_to_surface(cell.targetVolume)
                cell.lambdaSurface = tumor_lambda_surface

            if cell.type == self.COLLAGEN:
                cell.targetVolume = cell.volume  # collagen_length * collagen_thickness
                cell.lambdaVolume = collagen_lambda_volume

    # Growth:
    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.TUMOR:
                cell.targetVolume += tumor_growth_rate * volume_steppable_frequency
                cell.targetSurface = volume_to_surface(cell.targetVolume)


class MitosisSteppable(MitosisSteppableBase):
    # Docs: https://pythonscriptingmanual.readthedocs.io/en/latest/mitosis.html
    def __init__(self, frequency=10):  # Maybe change this frequency. I have set it to 10 to reduce computation
        MitosisSteppableBase.__init__(self, frequency)
        # Randomise where the 'parent' will end up and where the 'child' will end up (see docs):
        self.set_parent_child_position_flag(0)

    def step(self, mcs):
        cells_to_divide = []
        for cell in self.cell_list:
            if cell.type == self.TUMOR and cell.volume > mitosis_threshold:
                cells_to_divide.append(cell)
        for cell in cells_to_divide:
            self.divide_cell_random_orientation(cell)  # for other orientations, see docs

    def update_attributes(self):
        # Called after mitosis has occurred.
        # Set new target volumes:
        self.parent_cell.targetVolume /= 2.0
        self.parent_cell.targetSurface = volume_to_surface(self.parent_cell.targetVolume)
        self.clone_parent_2_child()  # Copy parent cell parameters to daughter cell


# The following steppable makes sure that collagen targetVolume is always the same as its actual volume,
# to make sure that the collagen is really eaten and cannot 'grow back'.
class ProteolysisSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.cell_type == self.COLLAGEN:
                cell.targetVolume = cell.volume
