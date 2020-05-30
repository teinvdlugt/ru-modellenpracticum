from cc3d import CompuCellSetup
from .ModelSteppables import *  # You might need to remove the dot

CompuCellSetup.register_steppable(steppable=VolumeSurfaceSteppable())
CompuCellSetup.register_steppable(steppable=MitosisSteppable())
CompuCellSetup.register_steppable(steppable=MMPSecretionSteppable())
CompuCellSetup.register_steppable(steppable=MMPDegradationSteppable())
CompuCellSetup.register_steppable(steppable=OutputFieldsSteppable())
CompuCellSetup.register_steppable(steppable=CaterpillarSteppable())

# We could add the multiple CTP fields programmatically, to avoid duplicate code. E.g.:
# xml_root = CompuCellSetup.parseXML("./ModelSteppables.py").root
# chemotaxis_elt = xml_root.ElementCC3D("Plugin", {"Name": "Chemotaxis"})
# ...
# CompuCellSetup.setSimulationXMLDescription(cc3d)
# See also cc3d/CompuCellSetup/simulation_setup.py#getCoreSimulationObjects
# and https://pythonscriptingmanual.readthedocs.io/en/latest/replacing_cc3dml_with_equivalent_python_syntax.html


CompuCellSetup.run()
