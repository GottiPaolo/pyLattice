import pyLattice.pyLattice as pl
from random import randint
import time as t

def count_unique(con):
    s = 0
    for i,j in enumerate(con):
        if i==j:
            s+=1
    return s


# C = A.CongruenceLattice()
# D = pl.DinamicCongruences(pl.Hasse(*A.hasse_coordinate(),radius=10),  pl.Hasse(*C.hasse_coordinate(), radius = 10),
#                           congruence_lattice =C, shape = (800,800), show_labels= True, font_size= 15)
# pene
mostra_grafici = True
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
if mostra_grafici:
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
if mostra_grafici:
    P.hasse(show_labels=True)
    P.sort()
    P.hasse(show_labels=True)
print(P.is_lattice())

### From a function
Q = pl.PoSet.from_function(list(range(1,20)),lambda a,b: a%b == 0)
if mostra_grafici:
    Q.hasse(show_labels=True)


## Operation on a PoSet
if mostra_grafici:
    P.hasse(show_labels = True)
print(P.upset('e',from_index=False))                    # {'e', 'f', 'l', 'k'}
print(P.upset('e','i', from_index=False))               # {'k', 'l'}
print(P.downset('k', from_index=False))                 # {'k', 'e', 'i'}
print(P.join('d','h',from_index=False))                # None
print(P.join('d','h',from_index=False, force = True))  # ['j', 'f']
print(P.meet('i','d',from_index=False, force = True))  # None

if mostra_grafici:
    P.sub_poset(['a','b','d','h','j','l']).hasse(show_labels = True)

## Operation beetwen PoSet
### sum
H = Q+P
if mostra_grafici:
    pl.PoSet.hasse(P,Q,H,shape = (300,100))

### product
Q = pl.PoSet.from_function([0,1,2], lambda a,b: a>b)
H = Q * Q
if mostra_grafici:
    H.hasse()

#Hasse diagram
if mostra_grafici:
    P.hasse(shape = (200,200), show_labels = True, font_size=12)
    pl.PoSet.hasse(Q,Q,H)
    pl.PoSet.hasse(Q,Q,H, grid = (1,3))


# Lattice
## powersets
if mostra_grafici:
    pl.Lattice.from_power_set(3).hasse(show_labels = True)
    pl.PoSet.hasse(*[pl.Lattice.from_power_set(i) for i in range(2,8)],
               grid = (2,3), title='Power Sets', show_labels = 3, shape = (600,400))

# chain and product beetwen chain
C_2 = pl.Lattice.from_chain(2)
C_3 = pl.Lattice.from_chain(3)
CW = C_2 * C_3
if mostra_grafici:
    C_2.hasse(C_3,CW)
    CW.hasse(pl.Lattice.from_cw(2,3),shape = (400,200),  show_labels = True, font_size=12)

#Chek if a poset is a lattice
n = 390
P = pl.PoSet.from_function([i for i in range(1,n+1) if n%i == 0], lambda a,b: b%a == 0)
print(P.is_lattice())
print(type(P))
P.as_lattice()
print(type(P))
if mostra_grafici:
    P.hasse(shape = (200,400), show_labels = True, font_size=12)


## Dedekind completition of a PoSet (beta)
c = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 1, 0, 0]
]

P = pl.PoSet.from_cover_matrix(c)
if mostra_grafici:
    P.hasse(P.dedekind_completetion(nice_labels=True),shape=(400,200), show_labels= True)


### Congruencens

L = pl.Lattice.from_cw(2,3,4)

print(L.calcola_congruenza(10,15)) # [0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2]
if mostra_grafici:
    L.hasse(L.CongruenceLattice(),shape = (500,250))

L.dinamic_congruences()




