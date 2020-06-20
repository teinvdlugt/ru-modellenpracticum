from cc3d.core.PySteppables import *
import math
import os
import time
import zlib
import numpy as np

# Toggles
_3d = False  # 3D toggle. To toggle 3D, set to True and change some lines in Model.xml
mmp_enabled = True  # NOTE: also comment out MMP DiffusionField tag in XML! Rest is handled in Model.py
growth_mitosis_enabled = True  # Handled in Model.py
OutputField_enable = False
leader_follower_enabled = True

# Volume, surface, growth and mitosis parameters
tumor_lambda_volume = 10.0  # from Scianna et al.
tumor_lambda_surface = 2.0  # TODO what does Scianna say?
tumor_growth_rate = 0.15  # per MCS -- be sure to keep this a float
collagen_lambda_volume = 0.0  # from Scianna et al.
collagen_volume_energy = -100.0
mmp_offset = 10  # The amount of mmp constantly secreted
mmp_offset_leader = 100  # The amount of mmp constantly secreted
mmp_scale_factor = 1e-5  # Conversion factor from confinement energy to secretion rate
mmp_scale_factor_leader = 10e-5
leader_percentage = 0.10 if leader_follower_enabled else 0  # Value between 0 and 1

# Steppable frequencies
growth_mitosis_steppable_frequency = 10  # The higher the cheaper computation
mmpdegradation_steppable_frequency = 10  # mmpdegradation turns out te be extremely expensive
OutputField_frequency = 10  # Outputs all chemical fields into a CSV file


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


class VolumeSurfaceInitialiserSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Initialise cell volumes
        for cell in self.cellList:
            if cell.type == self.TUMOR:
                cell.targetVolume = cell.volume
                cell.targetSurface = volume_to_surface(cell.volume)
                cell.lambdaVolume = tumor_lambda_volume
                cell.lambdaSurface = tumor_lambda_surface

            if cell.type == self.COLLAGEN:
                cell.targetVolume = cell.volume
                cell.lambdaVolume = collagen_lambda_volume
                cell.volumeEnergy = collagen_volume_energy

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


class GrowthMitosisSteppable(MitosisSteppableBase):
    # Docs: https://pythonscriptingmanual.readthedocs.io/en/latest/mitosis.html
    def __init__(self, frequency=growth_mitosis_steppable_frequency):  # Maybe change this frequency. I have set it to 10 to reduce computation
        MitosisSteppableBase.__init__(self, frequency)
        # Randomise where the 'parent' will end up and where the 'child' will end up (see docs):
        self.set_parent_child_position_flag(0)

    def step(self, mcs):
        # Growth
        for cell in self.cell_list_by_type(self.TUMOR):
            cell.targetVolume += tumor_growth_rate * growth_mitosis_steppable_frequency
            cell.targetSurface = volume_to_surface(cell.targetVolume)

        # Mitosis
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

        leader = np.random.random() < leader_percentage
        self.child_cell.dict["MMP_OFFSET"] = mmp_offset_leader if leader else mmp_offset
        self.child_cell.dict["MMP_SCALE_FACTOR"] = mmp_scale_factor_leader if leader else mmp_scale_factor


class MMPSecretionSteppable(SecretionBasePy):
    # Docs: https://compucell3dreferencemanual.readthedocs.io/en/latest/secretion.html
    def __init__(self, frequency=1):
        SecretionBasePy.__init__(self, frequency)

    def start(self):
        for cell in self.cell_list_by_type(self.TUMOR):
            leader = np.random.random() < leader_percentage
            print("leader" if leader else "follower")
            cell.dict["MMP_OFFSET"] = mmp_offset_leader if leader else mmp_offset
            cell.dict["MMP_SCALE_FACTOR"] = mmp_scale_factor_leader if leader else mmp_scale_factor

    def step(self, mcs):
        secretor = self.get_field_secretor("MMP")
        for cell in self.cell_list_by_type(self.TUMOR):
            # Secretion rate depends on cell confinement
            # Secretion rate should be increasing function of "cell.targetVolume - cell.volume" but
            # should be 0 when  cell.targetVolume - cell.volume < 0.

            # The following expression is quadratic because it was inspired by the volume-energy term
            # The surface energy contribution is commented out.
            confinement_energy = tumor_lambda_volume * max(cell.targetVolume - cell.volume, 0) ** 2
            # + tumor_lambda_surface * max(cell.targetSurface - cell.surface, 0) ** 2

            # Add offset and scale appropriately
            secr_rate = (confinement_energy + cell.dict["MMP_OFFSET"]) * cell.dict["MMP_SCALE_FACTOR"]

            # MMP is secreted at secr_rate at all pixels that are neighbour of a collagen pixel.
            secretor.secreteOutsideCellAtBoundaryOnContactWith(cell, secr_rate, [self.COLLAGEN])


class MMPDegradationSteppable(SteppableBasePy):
    def __init__(self, frequency=mmpdegradation_steppable_frequency):
        SteppableBasePy.__init__(self, frequency)

    def start(self):
        # Find medium cell object (to replace collagen pixels with)
        for cell in self.cell_list:
            if cell.type == self.MEDIUM:
                self.medium_cell = cell
                break

    def step(self, mcs):
        mmp = CompuCell.getConcentrationField(self.simulator, "MMP")

        for cell in self.cell_list_by_type(self.COLLAGEN):
            for pixel in self.get_copy_of_cell_pixels(cell):
                if mmp.get(pixel) >= 1: # TODO Maybe add some stochastic factor into this?
                    # Replace Collagen by Medium:
                    self.cell_field[pixel.x, pixel.y, pixel.z] = self.medium_cell
                    # Remove MMP:
                    mmp.set(pixel, 0)


class OutputFieldsSteppable(SteppableBasePy):
    def __init__(self, frequency=OutputField_frequency):
        SteppableBasePy.__init__(self, frequency)

    def step(self,mcs):
        start = time.time()
        compression_save_frequency = 10*OutputField_frequency
        if OutputField_enable:
            python_path = os.path.dirname(os.path.abspath(__file__))
            path = python_path+"/Fields_output"
            if not os.path.exists(path):
                os.makedirs(path)
            fields = ["CTP"]
            number_of_fields = len(fields)
            f = []
            field_data= []
            if _3d:
                size = (number_of_fields,200,200,200)
            else:
                size = (number_of_fields,200,200,1)
            data= np.zeros(size)

            for field in fields:
                f.append(open("".join((path,"/Output_",field,"{:04d}".format(mcs),"unc",".txt")),"wb"))
                field_data.append(CompuCell.getConcentrationField(self.simulator, field))
            for i in range(0,200):
                for j in range(0,200):
                    for k in range (0,size[-1]):
                       for l in range (0,number_of_fields):
                           data[l,i,j,k] = field_data[l][i,j,k]
            for i in range(0,number_of_fields):
                data[i].astype("float16").tofile(f[i])
                f[i].close()
            print("Saving all chemical fields took %f seconds" % (time.time()-start))


            if (mcs+10)%compression_save_frequency == 0:
                for field in fields:
                    uncompressed = []
                    for filename in sorted(os.listdir(path)):
                        if (filename.endswith("unc.txt") and field in filename):
                            file = open(os.path.join(path,filename),"rb")
                            uncompressed.append(file.read())
                            file.close()
                            os.remove(os.path.join(path,filename))

                    compressed = zlib.compress(np.array(b"".join(uncompressed)),1)
                    g = open("".join((path,"/Output_",field,"{:04d}".format(mcs+10-compression_save_frequency),".txt")),"wb")
                    g.write(compressed)
                    g.close()
