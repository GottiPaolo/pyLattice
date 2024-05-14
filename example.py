import pyLattice.pyLattice as pl

## Construct a PoSet
### From a domination matrix
                    #  a  b  c  d  e 
domination_matrix = [ [1, 0, 0, 0, 0], # a
                      [1, 1, 0, 0, 0], # b
                      [1, 0, 1, 0, 0], # c
                      [1, 0, 0, 1, 0], # d
                      [1, 1, 1, 1, 1]  # e   
                     ]

P = pl.PoSet(domination_matrix, X = ['a','b','c','d','e'])
P.hasse(labels=True)

### From a cover matrix
                    #  a  b  c  d  e 
cover_matrix      = [ [0, 0, 0, 0, 0], # a
                      [1, 0, 0, 0, 0], # b
                      [1, 0, 0, 0, 0], # c
                      [1, 0, 0, 0, 0], # d
                      [0, 1, 1, 1, 1]  # e   
                     ]
P = pl.PoSet.from_cover_matrix(cover_matrix=cover_matrix)

P.hasse(labels=True)


### From a function
P = pl.PoSet.from_function(list(range(1,20)),lambda a,b: a%b == 0)

P.hasse(labels=True)


pl.Lattice.from_power_set(3).hasse(labels = True, radius = 2)
P = pl.PoSet.from_function(list(range(1,20)), lambda a,b: a%b == 0)
print(P.is_lattice())

P.hasse(labels = True)