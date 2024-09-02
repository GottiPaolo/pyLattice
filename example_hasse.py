import pyLattice.pyLattice as pl
from random import randint,seed
from time import time
import copy
seed(6)
cw = (3,3)
df = pl.CWDataSet(cw,[randint(0,10) for i in range(pl.product(cw))])
print(df.L)
print(df.f)

df.L.labels = df.f
df.L.hasse(show_labels=True)
    
partitions, sep = df.gerarchic_cluster()

print('\nClusters a')
for c in partitions:
    print(len(pl.DataSet.as_partition(c)))
    for cluster in pl.DataSet.as_partition(c):
        print('\t',[df.L[i] for i in cluster])
    print()
    
# df.estetic_rappresentation(partitions)



"""
Verifichiamo uno dei più grandi dubbi attuali, ovvero che se prendo a metà della cluster il 
reticolo quoziente di una congruenza scelta e ricomincio da capo ottengo lo stesso risultato, questo non è affato scontato
"""
df_2 = df.get_dataset(clusters=partitions[1])

partitions, sep = df_2.gerarchic_cluster()

print('\nClusters b')
for c in partitions:
    print(len(pl.DataSet.as_partition(c)))
    for cluster in pl.DataSet.as_partition(c):
        print('\t',[df_2.L[i] for i in cluster])
    print()


df.estetic_rappresentation()
df_2.estetic_rappresentation()




for b in df.fuz_dom:
    print(b)

    
print()
print(*df_2.L.obj,sep = '\n')
for b in df_2.sep:
    print([round(_,2) for _ in b])
    
