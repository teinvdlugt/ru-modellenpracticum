from cc3d import CompuCellSetup

from .PressureDemonstrationSteppables import *

CompuCellSetup.register_steppable(steppable=GrowthSteppable())

CompuCellSetup.run()
