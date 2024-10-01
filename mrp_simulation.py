import pyLattice.pyLattice as pl
import tkinter as tk
import random as r
import copy
from fractions import Fraction

L = pl.Lattice.from_cw(3,3)
exs = L.get_all_linear_ex()
den = len(exs)
for i,x in enumerate(L):
    for j,y in enumerate(L[i+1:]):
        if L.domination_matrix[i][j+i+1] or L.domination_matrix[j+i+1][i]:
            continue
        u,d = len(L.upset(i)), len(L.downset(i))
        u_,d_ = len(L.upset(i+j+1)), len(L.downset(i+j+1))
        num =len([a for a in exs if a.index(i) < a.index(j+i+1)])
        fraction = Fraction(num, den)
        print(x,y,u,d,u_,d_,num,fraction)
    


quit()
def unisci(a,b):
    M = [[0 for j in range(a+b)] for k in range(a+b)]
    for i in range(a-1):
        M[i][i+1] = 1
    for j in range(b-1):
        i = a + j
        M[i][i+1] = 1
    return M

values = [len(pl.Lattice.from_cover_matrix(unisci(3,k)).get_all_linear_ex()) for k in range(1,20)]
print(values)
for a in range(2,5):
    for b in range(a,a+20):
        L = pl.Lattice.from_cover_matrix(unisci(a,b))
        L.hasse()
        print(a,b,'size',len(L.get_all_linear_ex()))
quit()
L = pl.Lattice.from_cw(3,2,3)
L.get_hasse_variables()
con = L.all_congruenze()
ConL = L.CongruenceLattice()
ConL.get_hasse_variables()
for c in con:
    L.show_congruence(c)
    ConL.get_hasse_variables()
    ConL.show_nodes([c], color = 'red', as_index = False)
    L.hasse(ConL,init=False)
L.dinamic_congruences()
D = pl.CWDataSet((3,3),[r.randint(0,10) for i in range(9)])
lles = D.LLEs()
mrp = D.mutual_ranking_probability()
bls = D.BrueggemannLerche()
for i in range(9):
    for j in range(9):
        if  not (D.L.domination_matrix[i][j] or D.L.domination_matrix[j][i]):
            # print(D.L[i],D.L[j])
            # print('mrp',mrp[i][j])
            # print('bls',bls[i][j])
            # print('lles',lles[i][j])
            print('\\hline')
            print(D.L[i], D.L[j], f'{mrp[i][j]:.2f}', f'{bls[i][j]:.2f}', f'{lles[i][j]:.2f}', sep=' & ')
            #print()
L.hasse(show_labels = True, font_size = 27)
exte = [pl.PoSet.from_function([L[i] for i in e],lambda x,y : e.index(L.obj.index(x)) > e.index(L.obj.index(y))) for e in L.get_all_linear_ex()]
L.hasse(*exte, show_labels = True, font_size = 27,grid = (1,(len(exte)+1)))

D = pl.CWDataSet((2,2,3),[r.randint(0,10) for i in range(12)])
D.estetic_rappresentation(labels_freq = False, font_size = 20,)





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
