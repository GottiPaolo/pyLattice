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




n_righe = 10
for j in range(2,n_righe + 2):
    #print("riga",j-1)
    b= [f'{i,j-i}' for i in range(1,j//2+1)]
    a = [ count_linear_ex(pl.Lattice.from_cw(i,j-i)) for i in range(1,j//2+1)]
    if  j % 2 == 1:
        a += a[::-1]
    else:
        a += a[:-1][::-1]
    #print(b)
    print(a)
    continue
    for i in  range(1,j//2 + 1):
        D = pl.Lattice.from_cw(i,j-i)
        print(i,j-i)
        print(count_linear_ex(D))

quit()
A = pl.Lattice.from_cw(5,4)
exs = get_all_linear_ex(A)
print(*exs,sep = '\n\n')

for i in range(len(A)):
    for j in range(i+1, len(A)):
        if A.domination_matrix[i][j] or A.domination_matrix[j][i]:
            continue
        n=0
        for ex in exs:
            if ex.index(i) > ex.index(j):
                n+=1
        print(A[i],A[j],round(n/len(exs),4),n)
        
print(len(exs))
A.hasse(show_labels=True,font_size=20)
## Generiamo il codice per printare in mermaid l'albero