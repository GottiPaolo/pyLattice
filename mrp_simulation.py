import pyLattice.pyLattice as pl
import tkinter as tk
import random as r
import copy


D = pl.CWDataSet((2,2,3),[r.randint(0,10) for i in range(12)])
D.estetic_rappresentation(labels_freq = False, font_size = 20)





r.seed(9)

def matrix_to_latex(matrix, label='matrice'):
    if label:
        s = f'{label}: '
    else:
        s = ''
    s += '\[\n\\begin{bmatrix}\n'
    for i in matrix:
        s += ' & '.join([f'{_: .2f}' for _ in i]) + '\\\\\n'
    s += '\\end{bmatrix}\n\]'
    return s

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


m = [
[0, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0],
[0, 1, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 1, 0]
]



D = pl.CWDataSet((2,2,3),[r.randint(0,10) for i in range(12)])

for ob,n in zip(D.L.obj,D.f):
    print(ob,'&',n,'\\\\')
print(*sorted(list(zip(D.L.obj,D.f))),sep = '\n')
D.L.get_hasse_variables()

D.L.hasse(init = False, show_labels = True, font_size = 20)

D.estetic_rappresentation(labels_freq = False, font_size = 20)
con,B = D.gerarchic_cluster()


# con  = D.L.congruenze_join_irriducibili()
# con = D.L.all_congruenze()
T = [copy.deepcopy(D.L) for i in con]
for L,c in zip(T,con):
    L.get_hasse_variables()
    L.show_congruence(c)
    
pl.PoSet.hasse(*T, init = False, radius = 4) #, grid = (4,len(T)//4))
print(pl.np.array(D.fuz_dom))
print(pl.np.array(D.sep))




print(matrix_to_latex(D.L.domination_matrix))
print()
D.fuz_dom = D.mutual_ranking_probability()
print(matrix_to_latex(D.fuz_dom, label = 'fuz_dom - mrp'))
print(matrix_to_latex(D.compute_separation(), label = 'SEP - mrp'))
print()
D.fuz_dom = D.BrueggemannLerche()

print(matrix_to_latex(D.fuz_dom, label = 'fuz_dom - bls'))
print(matrix_to_latex(D.compute_separation(), label = 'SEP - bls'))
print()
D.fuz_dom = D.LLEs()
print(matrix_to_latex(D.fuz_dom, label = 'fuz_dom - LLEs'))
print(matrix_to_latex(D.compute_separation(), label = 'SEP - LLEs'))

D.L.get_hasse_variables(labels =[i+1 for i in range(len(D.L))],
                        font_size = 15)
D.L.hasse(show_labels = True, init = False)
