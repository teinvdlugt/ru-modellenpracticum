from cc3d import CompuCellSetup
from .Project2018Steppables import *

CompuCellSetup.register_steppable(steppable=ConstraintInitializerSteppable())
CompuCellSetup.register_steppable(steppable=GrowthSteppable())
CompuCellSetup.register_steppable(steppable=MitosisSteppable())
CompuCellSetup.register_steppable(steppable=FieldAdhesionSteppable())
CompuCellSetup.register_steppable(steppable=FieldStrenghtenSteppable())

CompuCellSetup.run()
