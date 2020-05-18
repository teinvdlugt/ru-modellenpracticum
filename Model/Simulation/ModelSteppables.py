from cc3d.core.PySteppables import *
import math

# Collagen parameters
collagen_length = 100
collagen_thickness = 1

# Volume, surface, growth and mitosis parameters
tumor_initial_volume = 64.0  # must agree with PIF file
tumor_lambda_volume = 10.0  # from Scianna et al.
tumor_initial_surface = 8 * sqrt(tumor_initial_volume / math.pi)  # See also volume_to_surface function
tumor_lambda_surface = 2.0  # TODO what does Scianna say?


tumor_growth_rate = 0.01  # per MCS -- be sure to keep this a float


mitosis_threshold = 2 * tumor_initial_volume  # cell divides if volume > mitosis_threshold
volume_steppable_frequency = 20  # Maybe change this frequency. I have set it to 10 to reduce computation
mmpdegradation_steppable_frequency = 10 # mmpdegradation turns out te be extremely expensive

collagen_lambda_volume = 11.0  # from Scianna et al.

mmp_offset = 50 # The amount of mmp constantly secreted

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
                print(cell.volume)
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


class MMPSecretionSteppable(SecretionBasePy):
    # Docs: https://compucell3dreferencemanual.readthedocs.io/en/latest/secretion.html
    def __init__(self, frequency=1):
        SecretionBasePy.__init__(self, frequency)

    def step(self, mcs):
        secretor = self.get_field_secretor("MMP")
        for cell in self.cell_list:
            if cell.type == self.TUMOR:
                # Secretion rate depends on cell confinement
                delta_volume = cell.targetVolume - cell.volume
                #delta_surface = cell.targetSurface - cell.surface
                delta_surface = 0 # I think we decided on leaving out the surface term in the secretion of the mmp field
                delta_volume = 0 if delta_volume < 0 else delta_volume
                delta_surface = 0 if delta_surface < 0 else delta_surface
                
                confinement_energy = tumor_lambda_volume * delta_volume ** 2 \
                                     + tumor_lambda_surface * delta_surface ** 2 # Why should this be quadratic?
                
                secr_rate = (confinement_energy+mmp_offset) * 5e-5 # How should secretion rate depend on contact area?
                secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, secr_rate, [self.COLLAGEN])


class MMPDegradationSteppable(SteppableBasePy):
    def __init__(self, frequency=mmpdegradation_steppable_frequency):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Find medium cell object (to replace collagen pixels with)  # TODO only once?
        for cell in self.cell_list:
            if cell.type == self.MEDIUM:
                self.medium_cell = cell
                break

    def step(self, mcs):
        
        mmp = CompuCell.getConcentrationField(self.simulator, "MMP")

        for cell in self.cell_list_by_type(self.COLLAGEN):
            for pixel in self.get_copy_of_cell_pixels(cell):
                if mmp.get(pixel) >= 1: # Maybe add some stochastic factor into this?
                    # Replace Collagen by Medium:
                    self.cell_field[pixel.x, pixel.y, pixel.z] = self.medium_cell
                    # Remove MMP:
                    mmp.set(pixel, 0)
