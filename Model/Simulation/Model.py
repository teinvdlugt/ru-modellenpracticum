from cc3d import CompuCellSetup
from .ModelSteppables import *  # You might need to remove the dot

CompuCellSetup.register_steppable(steppable=InitialiserSteppable())
CompuCellSetup.register_steppable(steppable=VolumeSurfaceSteppable())
CompuCellSetup.register_steppable(steppable=MitosisSteppable())

CompuCellSetup.run()
