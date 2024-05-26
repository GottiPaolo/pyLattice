import pyLattice.pyLattice as pl
from random import randint
from time import time
c = [
    [0,0,0,0],
    [1,0,0,0], 
    [1,0,0,0],
    [0,0,1,0]
]
P = pl.PoSet.from_cover_matrix(c)

P = P * P
L = P.dedekind_completetion()
L = L + pl.Lattice([[1]]) + L
L = pl.Lattice.from_cw(3,2,2)
L.hasse()
colors = ['yellow' if (i in L.index_join_irriducibili() and i in L.index_meet_irriducibili()) else "black" if i in L.index_join_irriducibili() else "white" if i in L.index_meet_irriducibili() else "grey" for i in range(len(L))]
H = pl.Hasse(*L.hasse_coordinate(),nodes_color = colors, radius = 5)
C = L.CongruenceLattice()
colors_b = ['yellow' if (i in C.index_join_irriducibili() and i in C.index_meet_irriducibili()) else "black" if i in C.index_join_irriducibili() else "white" if i in C.index_meet_irriducibili() else "grey" for i in range(len(C))]

F = pl.DinamicCongruences(H, pl.Hasse(*C.hasse_coordinate(),nodes_color = colors_b, radius = 5), congruence_lattice=C, shape = (1500,800), show_labels=True)
# H.nodes_color = ['yellow' if i in L.index_upset(5) else 'red' if i in L.index_downset(5) else 'grey' for i in range(len(L))]
L = pl.Lattice.from_cw(3,3)
H = pl.Hasse(*L.hasse_coordinate(),nodes_color = colors, radius = 5)
for j in range(min(len(L),5)):
    H.nodes_color = ['blue' if  (i in L.index_downset(j) and i in L.index_join_irriducibili()) else 'red' if i == j else 'grey' for i in range(len(L))]
    F = pl.Finestra(H)
    
D = pl.DataSet(L,[1 for i in L])
print(D.gerarchic_cluster()[0])
## è perfetto, ho tutte le potenzialità, dovrò solo trovare un'interfacia dinamica carina
def get_color(vertex, con):
    return ['red' if con[a] == con[b] else 'black' for a,b in vertex]

for i in range(len(hasses)):
    c = Reticoli[i].calcola_congruenza(randint(0,len(Reticoli[i]) - 1), randint(0,len(Reticoli[i]) - 1))
    hasses[i].show_congruence(c)
    # hasses[i+1].nodes_color = ['black' if j in Reticoli[i+1].index_join_irriducibili() else 
    #                            'white' if j in Reticoli[i+1].index_meet_irriducibili() else
    #                            'grey'  for j in range(len(hasses[i+1].nodes))]

if False:
    pl.Finestra(*hasses, shape = (1200,800), grid = (3,3), show_labels=False)


    A = pl.Lattice.from_cw(2,3,2)
    pl.Finestra(pl.Hasse(*A.hasse_coordinate()),
               pl.Hasse(*A.CongruenceLattice().hasse_coordinate()),
               shape = (700,700), show_labels=True)



###### LETS GO

from random import randint   



L = pl.Lattice.from_cw(4,2,2)
freq = [randint(0,10) for i in range(len(L))]
L.labels = [f'{f}' for l,f in zip(L,freq)]


cover = [
    [0, 0, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0]
]
L = pl.Lattice.from_cw(2,10) 
freq = [1 for i in range(len(L))]
L.labels = [str(f) for f in freq]
D = pl.DataSet(L,freq)
start = time()
D.fuzzy_dom()
D.fuzzy_sep()
clusters, separations = D.gerarchic_cluster()
print(f'Tempo gerarchico: {time()-start}')
#pene
C = L.CongruenceLattice()
A = pl.DinamicCongruences(pl.Hasse(*L.hasse_coordinate()), pl.Hasse(*C.hasse_coordinate()),congruence_lattice=C,shape =(1200,800) )


# print('dom')
# for a in D.L.domination_matrix:
#     print('\t'.join([f"{round(i, 2):.2f}" for i in a])) # DIO FUNZIONA C'È da capire perchè D.sep[i][i] != 0
# print()
# print('fuz_dom')
# for a in D.fuz_dom:
#     print('\t'.join([f"{round(i, 2):.2f}" for i in a])) # DIO FUNZIONA C'È da capire perchè D.sep[i][i] != 0
# print()
# print('fuz_sep')
# for a in D.sep:
#     print('\t'.join([f"{round(i, 2):.2f}" for i in a])) # DIO FUNZIONA C'È da capire perchè D.sep[i][i] != 0
# Quello che è certo è che se separation_{ij} = 1 +sum... allora separation_{ii} >= 1.
# c'è qualcosa che non va sicuro. . . 



start = time()
ConL = D.L.CongruenceLattice()
ConL.labels = [str(round(D.calcola_sep_cluster(con),2)) for con in ConL]

indici = [ConL.obj.index(c) for c in clusters]
vertexes = [(min(indici[i], indici[i+1]) ,max(indici[i], indici[i+1]))for i in range(len(clusters)-1)]

H1 = pl.Hasse(*D.L.hasse_coordinate(), radius = 3)
H2 = pl.Hasse(*ConL.hasse_coordinate(), radius = 3)

H2.vertex_color = ['orange' if a in vertexes else 'black' for a in H2.vertex]
print(f'Tempo complessivo: {time()-start}')
pl.Finestra(H1,H2, shape = (1400,800), show_labels = True, font_size = 15)

nblocchi = [pl.numero_blocchi(con) for con in clusters]


print(nblocchi,separations, sep = '\n\n')

hasses = []
for c in clusters:
    hasses.append(pl.Hasse(*D.L.hasse_coordinate(), radius = 3))
    hasses[-1].show_congruence(c)
pl.Finestra(*hasses, show_labels=False,shape = (1400,800))
#pl.Lattice.hasse(D.L,ConL)

