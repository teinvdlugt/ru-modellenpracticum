from cc3d.core.PySteppables import *


class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self, _frequency=1):
        SteppableBasePy.__init__(self, _frequency)

    def start(self):
        for cell in self.cellList:
            cell.targetVolume = 25
            cell.lambdaVolume = 2.0


class GrowthSteppable(SteppableBasePy):
    def __init__(self, _frequency=1):
        SteppableBasePy.__init__(self, _frequency)

    def step(self, mcs):
        for cell in self.cellList:
            cell.targetVolume += 0.05  # Cell growth rate


class MitosisSteppable(MitosisSteppableBase):
    def __init__(self, _frequency=1):
        MitosisSteppableBase.__init__(self, _frequency)

    def step(self, mcs):
        cells_to_divide = []
        for cell in self.cellList:
            if cell.volume > 50:  # Size at which the cell divides
                cells_to_divide.append(cell)
        for cell in cells_to_divide:
            self.divide_cell_random_orientation(cell)

    def updateAttributes(self):
        self.parentCell.targetVolume /= 2.0  # reducing parent target volume
        self.cloneParent2Child()

        if self.parentCell.type == 1:
            self.childCell.type = 1
        else:
            self.childCell.type = 1


class FieldAdhesionSteppable(SteppableBasePy):
    def __init__(self, _frequency=1):
        SteppableBasePy.__init__(self, _frequency)

    def step(self, mcs):
        if mcs % 100 == 0:
            collagen = CompuCell.getConcentrationField(self.simulator, "Collagen")
            difference = CompuCell.getConcentrationField(self.simulator, "Difference")
            collagenDense = CompuCell.getConcentrationField(self.simulator, "CollagenDense")
            for pt in self.everyPixel():
                x = pt[0]
                y = pt[1]
                z = pt[2]
                # Calculate the boundary of the soft collagen for cell-matrix adhesion
                ptl = CompuCell.Point3D(x - 1, y, z)
                ptr = CompuCell.Point3D(x + 1, y, z)
                ptu = CompuCell.Point3D(x, y + 1, z)
                ptd = CompuCell.Point3D(x, y - 1, z)
                variance = abs(collagen.get(ptl) - collagen.get(pt)) + abs(collagen.get(ptr) - collagen.get(pt)) + abs(
                    collagen.get(ptu) - collagen.get(pt)) + abs(collagen.get(ptd) - collagen.get(pt))
                difference.set(pt, variance)
                # Remove hard collagen that cells accidentally placed behind them
                if collagen.get(pt) < 0.1:
                    collagenDense.set(pt, 0)


class FieldStrenghtenSteppable(SteppableBasePy):
    def __init__(self, _frequency=1):
        SteppableBasePy.__init__(self, _frequency)

    def step(self, mcs):
        if mcs % 10 == 0:
            degradationFactor = 0.0  # Amount of collagen that a cell leaves behind each step (0 = instant
            # degradation, 1 = no degradation)
            range = 2  # How far away from the cell the hard collagen gets placed (1 = cell radius)
            collagen = CompuCell.getConcentrationField(self.simulator, "Collagen")
            collagenDense = CompuCell.getConcentrationField(self.simulator, "CollagenDense")
            for cell in self.cellList:
                pixels = self.getCopyOfCellPixels(cell)
                xCOM = cell.xCOM  # Center of mass
                yCOM = cell.yCOM
                zCOM = cell.zCOM
                xtotal = 0  # Average movement
                ytotal = 0
                ztotal = 0
                totalCollagen = 0  # Total collagen removed
                count = 0  # Number of lattice points where collagen is removed
                # Remove soft collagen
                for pt in pixels:
                    c = collagen.get(pt)
                    if c > 0:
                        x = pt.x
                        y = pt.y
                        z = pt.z
                        xtotal = xtotal + (pt.x - xCOM)
                        ytotal = ytotal + (pt.y - yCOM)
                        ztotal = ztotal + (pt.z - zCOM)
                        totalCollagen = totalCollagen + c
                        count = count + 1
                    collagen.set(pt, collagen.get(pt) * degradationFactor)  # Degrade soft collagen
                    collagenDense.set(pt, 0)
                # Place hard collagen
                if count != 0:
                    xtotal = xtotal / count  # A vector that approximates the direction of movement (and thus the front of the cell)
                    ytotal = ytotal / count
                    ztotal = ztotal / count
                    boundaryPixels = self.getCopyOfCellBoundaryPixels(cell)
                    collagenPerCell = totalCollagen / len(boundaryPixels)  # Collagen to be placed at each cell
                    for pt in boundaryPixels:
                        deltax = pt.x - cell.xCOM  # The relative position of the point to the center of mass
                        deltay = pt.y - cell.yCOM
                        deltaz = pt.z - cell.zCOM
                        pt.x = int(cell.xCOM + range * deltax)  # The point at which the hard collagen will be placed
                        pt.y = int(cell.yCOM + range * deltay)
                        pt.z = int(cell.zCOM + range * deltaz)
                        totalNorm = sqrt((xtotal ** 2 + ytotal ** 2 + ztotal ** 2))
                        deltaNorm = sqrt(deltax ** 2 + deltay ** 2 + deltaz ** 2)
                        dotProduct = xtotal * deltax + ytotal * deltay + ztotal * deltaz
                        if totalNorm != 0 and deltaNorm != 0:
                            cos = dotProduct / (totalNorm * deltaNorm)
                            if -1 / sqrt(2) < cos < 1 / sqrt(
                                    2):  # Check if the point is at the sides of the cell
                                if collagen.get(pt) != 0:
                                    collagenDense.set(pt, collagenPerCell)  # Place the hard collagen
