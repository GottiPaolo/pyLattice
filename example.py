import pyLattice.pyLattice as pl
from random import randint
import time as t
import copy

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
    P.sub_poset([P.obj.index(_a) for _a in ['a','b','d','h','j','l']]).hasse(show_labels = True)

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
    pl.PoSet.hasse(Q,Q,H, shape = (450, 150))
    pl.PoSet.hasse(Q,Q,H, grid = (1,3),shape = (450, 150))

# Dedekind completion of a PoSet
domination_matrix= [[1, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [0, 1, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [1, 1, 1, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [1, 1, 0, 1,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
  
                    [0, 0, 0, 0,   1, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [0, 0, 0, 0,   0, 1, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [0, 0, 0, 0,   1, 1, 1, 0,   0, 0, 0, 0,   0, 0, 0, 0], 
                    [0, 0, 0, 0,   1, 1, 0, 1,   0, 0, 0, 0,   0, 0, 0, 0], 
  
                    [1, 1, 1, 1,   1, 1, 1, 1,   1, 0, 0, 0,   0, 0, 0, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   0, 1, 0, 0,   0, 0, 0, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 1, 0,   0, 0, 0, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   1, 1, 0, 1,   0, 0, 0, 0],  
                  
                    [1, 1, 1, 1,   1, 1, 1, 1,   0, 0, 0, 0,   1, 0, 0, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   0, 0, 0, 0,   0, 1, 0, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   0, 0, 0, 0,   1, 1, 1, 0], 
                    [1, 1, 1, 1,   1, 1, 1, 1,   0, 0, 0, 0,   1, 1, 0, 1]
              ]

P = pl.PoSet(domination_matrix)
L = P.dedekind_completion(nice_labels=True)
if mostra_grafici:
    P.get_hasse_variables(radius = 3, font_size=12)
    pl.Lattice.hasse(P,L, show_labels = True, init = False)

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
    C_2.hasse(C_3,CW,shape = (450, 150))
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


### Congruencens

#### All congruences on 3 pwst
L = pl.Lattice.from_power_set(3)
congs = L.all_congruenze()
alls = [pl.Lattice.from_power_set(3) for c in congs]
for a,c in zip(alls,congs):
    a.get_hasse_variables()
    a.show_congruence(c)

if mostra_grafici:  
    pl.Lattice.hasse(*alls,init = False, shape = (400,800), grid = (4,2))

L = pl.Lattice.from_cw(2,3,4)

print(L.calcola_congruenza(10,15)) # [0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2]
if mostra_grafici:
    L.hasse(L.CongruenceLattice(),shape = (500,250))

if mostra_grafici:
    L.dinamic_congruences(shape=(700,350))
    

### DataSet
cw = (2,3,3)
D = pl.CWDataSet(cw,[randint(0,20) for i in range(pl.product(cw))])
print('\nBLS')
D.show_fuz_dom()
D.fuz_dom = D.LLEs()
print('\nLLES')
D.show_fuz_dom()

print('\nGerarchia delle partizioni')
print(*[pl.DataSet.as_partition(x) for x in D.gerarchic_cluster()[0]],sep = '\n')
if mostra_grafici:
    D.estetic_rappresentation()



## All approches
cw = (3,2,2)
A = pl.Lattice.from_cw(*cw)
frequenze = [randint(0,20) for a in A]
D = pl.DataSet(A,frequenze)

hasses = [A]
ConL_a = A.CongruenceLattice()

D.L.get_hasse_variables(radius = 3, font_size=12, labels = [str(f) for f in frequenze])

for fuzzy_d in ('BrueggemannLerche', 'LLEs'):
    for agg_function in ("total_separation","max_separation"):
        for t_n in ('hamacher', 'min', 'prod'):
            print('\n',fuzzy_d,t_n,agg_function)
            D = pl.CWDataSet(cw,freq=frequenze,t_norm_function=t_n,fuzzy_domination_function=fuzzy_d)

            start = t.time()
            clusters, separations = D.gerarchic_cluster()
            print(f'Tempo gerarchic_cluster: {t.time()-start}')
            
            clusters, separations = D.gerarchic_cluster(function_sep=agg_function)
            hasses.append(copy.deepcopy(ConL_a))
            hasses[-1].get_hasse_variables(radius = 3, font_size=11)
            hasses[-1].show_percorso([ConL_a.obj.index(c) for c in clusters], color ='orange')
            if agg_function == "total_separation":
                hasses[-1].labels = ([str(round(D.total_separation(pl.DataSet.as_partition(con)),2)) for con in ConL_a])
            else:
                hasses[-1].labels = ([str(round(D.max_separation(pl.DataSet.as_partition(con)),2)) for con in ConL_a])
             
            #hasses[-1].hasse(init = False, show_labels = True, title = f"{fuzzy_d} {t_n} {agg_function}", 
            #                 shape = (800,800))
            hasses[-1].labels = ['' for i in ConL_a]
            hasses[-1].labels[-1] = f"{fuzzy_d} {t_n} {agg_function}"
            
if mostra_grafici:       
    pl.Lattice.hasse(*hasses[1:],show_labels=True, shape = (1200,900), 
                 grid = (4,3), title = 'All', init = False)
    
if mostra_grafici:
    D.list_of_quotient_relative_con(normalize_costant=0.2, temp_radius_f=lambda x: x**0.5, n_rows=1,)
