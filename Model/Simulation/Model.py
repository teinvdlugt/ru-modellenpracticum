from cc3d import CompuCellSetup
from .ModelSteppables import *  # You might need to remove the dot

# STEPPABLES
CompuCellSetup.register_steppable(steppable=VolumeSurfaceInitialiserSteppable())
if growth_mitosis_enabled:
    CompuCellSetup.register_steppable(steppable=GrowthMitosisSteppable())
if mmp_enabled:
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




# # XML STUFF
# # Find pathname of Model.xml:
# import os, inspect
# modeldotpy = inspect.getframeinfo(inspect.currentframe()).filename
# xml_file = os.path.join(os.path.dirname(os.path.abspath(modeldotpy)), "Model.xml")
# # Parse XML file:
# xml_root = CompuCellSetup.parseXML(xml_file).root
# diffusion_solve_fe = xml_root.ElementCC3D("Steppable", {"Name" : "DiffusionSolverFE"})
# diffusion_field = diffusion_solve_fe.ElementCC3D("DiffusionField",{"Name":"MMP"})
# diffusion_data = diffusion_field.ElementCC3D("DiffusionData")
# diffusion_data.ElementCC3D("FieldName",{},"MMP")
# diffusion_data.ElementCC3D("GlobalDiffusionConstant",{},"1.6e-03")
# diffusion_data.ElementCC3D("GlobalDecayConstant",{},"2e-04")
#
# CompuCellSetup.set_simulation_xml_description(xml_root)
