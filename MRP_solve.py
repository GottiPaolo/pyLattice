from fractions import Fraction
import pyLattice.pyLattice as pl
import pandas as pd

# ora facciamo una cosa figa
# Sono certo (non è vero) che si possa trovare una formula operativi per reticoli cw
# Qua iniziero a creare degli esempi, partirò da matrici di dominanza e 
# calcolerò la matrice di fuzzy dominanza con l'mrp
# Cercherò di utilizzare frazioni per far emergere delle regolarità,
# e sopratutto devo ordinare la matrice con una qualche regola
def estensioni_lineari(self):
    all_ = []
    elementi = list(range(len(self)))
    estensione = []
    indice = 0
    step_back = False
    reset_index = False
    while True:
        possibilie_scelte =  sorted(self.max_sub_set(elementi))
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

def mutual_ranking_probability(self):
    matrice = pl.np.array([[Fraction(0,1) for i in range(len(self))] for j in range(len(self))])
    estensioni_lineari_ = estensioni_lineari(self)
    n = len(estensioni_lineari_)
    for est in estensioni_lineari_:
        for i in range(len(self)):
            for j in range(i+1,len(self)):
                if est.index(i) >= est.index(j):
                    matrice[i][j] +=Fraction(1,n)
                else:
                    matrice[j][i]+=Fraction(1,n)
    return matrice

def mostra_matrice(M):
    for row in M:
        print(" ".join(f"{elem.numerator}/{elem.denominator}" for elem in row))

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def prod(lista):
    p = 1
    for i in lista:
        p *= i
    return p

def get_tree_n(p_a,p_b,cw):
    a_ = prod([c-a for a,c in zip(p_a,cw)])
    b_ = prod([c-b for b,c in zip(p_b,cw)])
    ab_ = prod([c-max(a,b) for a,b,c in zip(p_a,p_b,cw)])
    _a = prod([a+1 for a in p_a])
    _b = prod([b+1 for b in p_b])
    _ab = prod([min(a,b)+1 for a,b in zip(p_a,p_b)])

    return a_ ,b_,ab_,_a,_b,_ab

def sort_matrix(m):
    # Calculate the sum of 1s for each row
    row_sums = [(sum(row), idx) for idx, row in enumerate(m)]
    # Sort rows based on the sum of 1s
    row_sums.sort()
    sorted_indices = [idx for _, idx in row_sums]

    # Reorder rows and columns simultaneously
    sorted_matrix = [[m[i][j] for j in sorted_indices] for i in sorted_indices]

    return sorted_matrix

def column_indices_with_sum_one(matrix):
    indices = []
    for col_idx in range(len(matrix[0])):
        col_sum = sum(matrix[row_idx][col_idx] for row_idx in range(len(matrix)))
        if col_sum == 1:
            indices.append(col_idx)
    return indices

def row_indices_with_sum_one(matrix):
    indices = []
    for row_idx in range(len(matrix)):
        row_sum = sum(matrix[row_idx])
        if row_sum == 1:
            indices.append(row_idx)
    return indices

def remove_row_and_column(matrix, index):
    # Remove the specified row
    if index ==len(matrix)-1:
        new_matrix = [row[:-1]  for row in enumerate(matrix[:-1])]

    elif index == 0:
        new_matrix = [row[1:]  for row in matrix[1:]]

    else:
        new_matrix = [row for i, row in enumerate(matrix) if i != index]
        new_matrix = [[elem for j, elem in enumerate(row) if j != index] for row in new_matrix]
    return new_matrix

def phi(dom_matrix):
    if len(dom_matrix) == 1:
        return 1
    n = 0
    for a in column_indices_with_sum_one(dom_matrix):
        n += phi(remove_row_and_column(dom_matrix,a))
    return n
    
D = pl.Lattice.from_cw(5,5).domination_matrix
print('phi',phi(D))
quit()
diz ={ 
    'a' : [],
    'b' : [],
    'a_upset' :[],
    'b_upset' :[],
    'a_b_upset' :[],
    'a_downset' :[],
    'b_downset' :[],
    'a_b_downset' :[],
    'mrp a_b' : [],
    'L_shape' : [],
    'n_estensioni' : []
}
# Example usage

# for i in (2,3,4,5):
#     for j in (2,3,4,5):
#         if j>= i:
#             A = pl.Lattice.from_cw(i,j)
#             n = len(estensioni_lineari(A))
#             print(i,j,n,prime_factors(n))

print(prime_factors(1680384))
for D in [(3,),(3,3),(3,3,3)]:   
    A = pl.Lattice.from_cw(*D)
    M = mutual_ranking_probability(A)
    n_estensioni = len(estensioni_lineari(A))
    print(D)
    #n_estensioni = 1680384
    for i in range(len(A)):
        for j in range(i+1,len(A)):
            if not A.domination_matrix[i][j] and not A.domination_matrix[i][j]:
                diz['a'].append(A[i])
                diz['b'].append(A[j])
                a_ ,b_,ab_,_a,_b,_ab = get_tree_n(A[i],A[j],D)
                diz['a_upset'].append(a_)
                diz['b_upset'].append(b_)
                diz['a_b_upset'].append(ab_)
                diz['a_downset'].append(_a)
                diz['b_downset'].append(_b)
                diz['a_b_downset'].append(_ab)
                diz['mrp a_b'].append(M[i][j])
                diz['L_shape'].append(D)
                diz['n_estensioni'].append(n_estensioni)
                print(A[i],A[j])
                print(get_tree_n(A[i],A[j],D))
                print(M[i][j])
                print()

pd.DataFrame(diz).to_csv('mrp.csv')
A.hasse(show_labels=True)





