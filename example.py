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
P.hasse() # show Hasse diagram

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
P.hasse(labels = True)
print(P.upset('e'))                   # {'e', 'f', 'l', 'k'}
print(P.upset('e','i'))               # {'k', 'l'}
print(P.downset('k'))                 # {'k', 'e', 'i'}
print(P.join('d','h'))                # None
print(P.join('d','h', force = True))  # ['j', 'f']
print(P.meet('i','d', force = True))  # None
P.sub_poset(['a','b','d','h','j','l']).hasse(labels = True)

## Operation beetwen PoSet
### sum
H = Q+P
pl.PoSet.hasse(P,Q,H,shape = (300,100), radius = 3)

### product
Q = pl.PoSet.from_function([0,1,2], lambda a,b: a>b)
H = Q * Q
H.hasse()

#Hasse diagram
P.hasse(shape = (200,200), radius = 2, labels = True, t_size=12)
pl.PoSet.hasse(Q,Q,H)
pl.PoSet.hasse(Q,Q,H, grid = (1,3))


# Lattice
pl.Lattice.from_power_set(3).hasse(labels = True)
C_2 = pl.Lattice.from_chain(2)
C_3 = pl.Lattice.from_chain(3)
CW = C_2 * C_3
C_2.hasse(C_3,CW)

CW.hasse(pl.Lattice.from_cw(2,3),shape = (400,200), radius = 2, labels = True, t_size=12)

n = 390
P = pl.PoSet.from_function([i for i in range(1,n+1) if n%i == 0], lambda a,b: b%a == 0)
print(P.is_lattice())
print(type(P))
P.as_lattice()
print(type(P))
P.hasse(shape = (200,400), radius = 2, labels = True, t_size=12)


## Dedekind completition of a PoSet
c = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 0, 0]
]

P = pl.PoSet.from_cover_matrix(c)
P.hasse(P.dedekind_completetion(nice_labels=True),shape=(400,200), radius = 3, labels= True)
