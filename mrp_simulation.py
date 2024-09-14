import pyLattice.pyLattice as pl
import tkinter as tk


def linear_extension(P,exte):
    P.get_hasse_variables()
    for i,j in enumerate(exte[:-1]):
        k = exte[i+1]
        P.vertex.append((j,k)) 
        P.vertex_color.append('red')
#A = pl.Lattice.from_power_set(3)
def get_all_linear_ex(A):
    all_ = []
    elementi = list(range(len(A)))
    estensione = []
    indice = 0
    step_back = False
    reset_index = False
    while True:
        possibilie_scelte =  sorted(A.max_sub_set(elementi))
        if step_back:
            indice = possibilie_scelte.index(max_)
            if indice < len(possibilie_scelte)-1:
                indice += 1
                step_back = False
                reset_index = True
            else:
                if len(estensione) == 0:
                    break
                elementi.insert(estensione[-1],estensione[-1])
                max_ = estensione[-1]
                estensione=estensione[:-1]
                continue
        max_ = possibilie_scelte[indice]
        if reset_index:
            reset_index = False
            indice = 0
        estensione.append(max_)
        elementi.remove(max_)
        if len(elementi) == 0:
            all_.append(estensione)
            step_back = True
            estensione=estensione[:-1]
            elementi.insert(max_,max_)
    return all_


def compute_fuz_dom_mrp(P):
    n = 0
    matrice = pl.np.array([[0 for i in range(len(P))] for j in range(len(P))])
    for est in get_all_linear_ex(P):
        n+=1
        for i in range(len(P)):
            for j in range(i,len(P)):
                if est.index(i) >= est.index(j):
                    matrice[i][j] +=1
                else:
                    matrice[j][i]+=1
    return matrice/n
        
def count_linear_ex(A):
    n = 0
    elementi = list(range(len(A)))
    estensione = []
    indice = 0
    step_back = False
    reset_index = False
    while True:
        possibilie_scelte =  sorted(A.max_sub_set(elementi))
        if step_back:
            indice = possibilie_scelte.index(max_)
            if indice < len(possibilie_scelte)-1:
                indice += 1
                step_back = False
                reset_index = True
            else:
                if len(estensione) == 0:
                    break
                elementi.insert(estensione[-1],estensione[-1])
                max_ = estensione[-1]
                estensione=estensione[:-1]
                continue
        max_ = possibilie_scelte[indice]
        if reset_index:
            reset_index = False
            indice = 0
        estensione.append(max_)
        elementi.remove(max_)
        if len(elementi) == 0:
            n+=1
            step_back = True
            estensione=estensione[:-1]
            elementi.insert(max_,max_)
    return n

c = [
[0, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0],
[0, 1, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0]
]




P = pl.Lattice.from_chain(7) * pl.Lattice.from_chain(2)
print(count_linear_ex(P))
print(P.domination_matrix)
m = compute_fuz_dom_mrp(P)
print()
for riga in m:
    print([round(x,3) for x in riga])
# print(compute_fuz_dom_mrp(P))