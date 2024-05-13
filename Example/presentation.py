import sys
sys.path.append( '/Users/paologotti/Library/CloudStorage/OneDrive-Personale/Tesi/pyLattice/' )
import pyLattice as pl

L = pl.Lattice.from_chain(5)
L.dinamic_congruences()
L.rappresenta()