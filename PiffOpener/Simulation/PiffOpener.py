
from cc3d import CompuCellSetup
        

from PiffOpenerSteppables import PiffOpenerSteppable

CompuCellSetup.register_steppable(steppable=PiffOpenerSteppable(frequency=1))


CompuCellSetup.run()
