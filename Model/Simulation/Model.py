from cc3d import CompuCellSetup

from .ModelSteppables import InitialiserSteppable

CompuCellSetup.register_steppable(steppable=InitialiserSteppable())

CompuCellSetup.run()
