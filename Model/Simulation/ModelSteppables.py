from cc3d.core.PySteppables import *
import math

_3d = False

# Volume, surface, growth and mitosis parameters
tumor_lambda_volume = 10.0  # from Scianna et al.
tumor_lambda_surface = 1.0  # TODO what does Scianna say?
tumor_growth_rate = 0.05  # per MCS -- be sure to keep this a float
collagen_lambda_volume = 11.0  # from Scianna et al.
volume_steppable_frequency = 20  # Maybe change this frequency.
mitosis_threshold = None  # Initialised in VolumeSurfaceSteppable. Cell divides if volume > mitosis_threshold


# To increase speed, consider changing every call to this function to the appropriate function (2d or 3d)
def volume_to_surface(volume):
    if _3d:
        return volume_to_surface3d(volume)
    else:
        return volume_to_surface2d(volume)


_8oversqrtpi = 8 / sqrt(math.pi)
def volume_to_surface2d(volume):
    """ Calculates perimeter(="surface") of a pixelated disk having the specified area(="volume").
        This stems from: vol = pi r^2, surface = 8 * r = 8 * sqrt(vol/pi). """
    return _8oversqrtpi * sqrt(volume)


_24_3_4pi_23 = 24 * (3/4/math.pi)**(2/3.)
def volume_to_surface3d(volume):
    """ Calculates surface of a pixelated ball having the specified volume.
        This stems from: vol = 4/3 pi r^3, surface = 6*(2r)^2 = _24_3_4pi_23 * vol^(2/3). """
    return _24_3_4pi_23 * (volume ** (2 / 3.))


class VolumeSurfaceSteppable(SteppableBasePy):
    def __init__(self, frequency=volume_steppable_frequency):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Initialise cell volumes
        for cell in self.cellList:
            if cell.type == self.TUMOR:
                cell.targetVolume = cell.volume
                cell.targetSurface = volume_to_surface(cell.targetVolume)
                cell.lambdaVolume = tumor_lambda_volume
                cell.lambdaSurface = tumor_lambda_surface

            if cell.type == self.COLLAGEN:
                cell.targetVolume = cell.volume
                cell.lambdaVolume = collagen_lambda_volume

        # Initialise mitosis threshold. Find random tumor cell:
        tumor_cell = None
        for cell in self.cell_list:
            if cell.type == self.TUMOR:
                tumor_cell = cell
                break
        # Set mitosis threshold to twice the tumor cell size:
        global mitosis_threshold
        mitosis_threshold = tumor_cell.volume * 2
        # This assumes that all cells have the same size!

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
