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
P.hasse()

### From a cover matrix
                    #  a  b  d  e  f  h  i  j  k  l
cover_matrix      = [ [0, 1, 0, 0, 0, 0, 0, 0, 0, 0] , # a
                      [0, 0, 1, 0, 0, 1, 0, 0, 0, 0] , # b
                      [0, 0, 0, 0, 1, 0, 0, 1, 0, 0] , # d
                      [0, 0, 0, 0, 1, 0, 0, 0, 1, 0] , # e
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] , # f
                      [0, 0, 0, 0, 1, 0, 0, 1, 0, 0] , # h
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0] , # i
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] , # j
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] , # k
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ] # l

P = pl.PoSet.from_cover_matrix(cover_matrix=cover_matrix, X = ['a','b','d','e','f','h','i','j','k','l'])
P.hasse(labels=True)
print(P.is_lattice())

### From a function
Q = pl.PoSet.from_function(list(range(1,20)),lambda a,b: a%b == 0)
Q.hasse(labels=True)


## Operation on a PoSet
print(P.upset('e'))                   # {'e', 'f', 'l', 'k'}
print(P.upset('e','i'))               # {'k', 'l'}
print(P.downset('k'))                 # {'k', 'e', 'i'}
print(P.join('d','h'))                # None
print(P.join('d','h', force = True))  # ['j', 'f']
print(P.meet('i','d', force = True))  # None
P.hasse(labels = True)

## Operation beetwen PoSet
### sum
H = Q+P
pl.PoSet.hasse(P,Q,H,shape = (700,300), radius = 3)

### product
Q = pl.PoSet.from_function([0,1,2], lambda a,b: a>b)
H = Q * Q
Q.hasse(Q,H,shape = (700,300), radius = 3, labels = True)




