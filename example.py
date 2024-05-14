import pyLattice.pyLattice as pl

L = pl.Lattice.from_chain(5) * pl.Lattice.from_chain(3) * pl.Lattice.from_chain(2) 
L.hasse()
L.CongruenceLattice().hasse()