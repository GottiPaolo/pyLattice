import pyLattice.pyLattice as pl
from random import randint
from time import time

Reticoli = [pl.Lattice.from_cw(randint(2,7),randint(2,7)) for n in range(2,11)]
print(len(Reticoli))
hasses = [pl.Hasse(*A.hasse_coordinate(), radius = 3) for A in Reticoli]

def get_color(vertex, con):
    return ['red' if con[a] == con[b] else 'black' for a,b in vertex]

for i in range(len(hasses)):
    c = Reticoli[i].calcola_congruenza(randint(0,len(Reticoli[i]) - 1), randint(0,len(Reticoli[i]) - 1))
    hasses[i].show_congruence(c)
    # hasses[i+1].nodes_color = ['black' if j in Reticoli[i+1].index_join_irriducibili() else 
    #                            'white' if j in Reticoli[i+1].index_meet_irriducibili() else
    #                            'grey'  for j in range(len(hasses[i+1].nodes))]

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


L = pl.Lattice.from_cw(2,2,3,2,4,2)
freq = [randint(0,10) for i in range(len(L))]
D = pl.DataSet(L,freq)
start = time()
D.fuzzy_dom()
D.fuzzy_sep()
clusters, separations = D.gerarchic_cluster()
print(f'Tempo: {time()-start}')
#pene



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



ConL = D.L.CongruenceLattice()
ConL.labels = [str(round(D.calcola_sep_cluster(con),2)) for con in ConL]

indici = [ConL.obj.index(c) for c in clusters]
vertexes = [(min(indici[i], indici[i+1]) ,max(indici[i], indici[i+1]))for i in range(len(clusters)-1)]
print(sorted(vertexes))
H1 = pl.Hasse(*D.L.hasse_coordinate(), radius = 3)
H2 = pl.Hasse(*ConL.hasse_coordinate(), radius = 3)
print(H1)
print(sorted(vertexes))
print(sorted(H2.vertex))
H2.vertex_color = ['orange' if a in vertexes else 'black' for a in H2.vertex]
print(H2.nodes, H2.vertex, H2.vertex_color, sep = '\n\n')
pl.Finestra(H1,H2, shape = (1400,800), show_labels = True, font_size = 15)

nblocchi = [pl.numero_blocchi(con) for con in clusters]

print(nblocchi,separations, sep = '\n\n')

hasses = []
for c in clusters:
    hasses.append(pl.Hasse(*D.L.hasse_coordinate(), radius = 3))
    hasses[-1].show_congruence(c)
pl.Finestra(*hasses, show_labels=False,shape = (1400,800))
#pl.Lattice.hasse(D.L,ConL)

