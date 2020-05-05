from cc3d.core.PySteppables import *
import math

# Collagen parameters
collagen_length = 100
collagen_thickness = 1

# Volume, growth and mitosis parameters
tumor_initial_volume = 64.0  # must agree with PIF file
tumor_lambda_volume = 10.0  # from Scianna et al.
tumor_initial_surface = 36.0    #This stems from the relation between the volume and the surface of a voxel sphere, ie
                                #vol = pi r^2, surface = 8 * sqrt(vol/pi)
tumor_lambda_surface = 1.0

tumor_growth_rate = 0.05  # per MCS -- keep this a float


mitosis_threshold = 2*tumor_initial_volume  # cell divides if volume > mitosis_threshold
volume_steppable_frequency = 20  # Maybe change this frequency. I have set it to 10 to reduce computation

collagen_lambda_volume = 11.0  # from Scianna et al.


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
                cell.targetVolume = tumor_initial_volume
                cell.lambdaVolume = tumor_lambda_volume
                cell.targetSurface = tumor_initial_surface
                cell.lambdaSurface = tumor_lambda_surface
                
            if cell.type == self.COLLAGEN:
                cell.targetVolume = collagen_length * collagen_thickness
                cell.lambdaVolume = collagen_lambda_volume

    def step(self, mcs):
        for cell in self.cell_list:
            if cell.type == self.TUMOR:
                cell.targetVolume += tumor_growth_rate * volume_steppable_frequency
                cell.targetSurface = 4.5 * math.sqrt(cell.targetVolume) #The 4.5 \approx 8/sqrt(pi)


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
        self.parent_cell.targetSurface = 4.5 * math.sqrt(self.parent_cell.targetVolume)
        self.clone_parent_2_child()  # Copy parent cell parameters to daughter cell
