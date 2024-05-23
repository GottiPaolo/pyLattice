import pyLattice as pl
import Hasse as h

class DataSet:
    def __init__(self, Lattice : pl.Lattice, freq):
        assert len(freq) == len(Lattice)
        self.L = Lattice
        self.f = freq
        
    ## Costruire matrice di dominanze fuzzificate
    def fuzzy_dom(self, func = 'boh'):
        if type(func) == 'function':
            self.fuz_dom = [[func(i,j,self.L) for i in range(len(self.L))] for j in range(len(self.L))]
        elif func == 'boh':
            self.fuz_dom = [[self.fuzzy_func_culo(i,j) for i in range(len(self.L))] for j in range(len(self.L))]
            
        else:
            """
            da definire
            """
    
    ## Costruire matrice di separation come 1 + \sum inb_{ikj}
    ## dove inb_{ijk} = 
    # ( a_i < a_j ^ a_k < a_j ^ a_i < a_k ) V ( a_i > a_j ^ a_k > a_j ^ a_i > a_k )
    # però fuzzyficando tutto, la dominanza lo si vede sopra
    # gli "and" ed "or" si
    def fuzzy_sep(self,t_norm = 'boh', t_conorm = None):
        if t_norm == 'boh':
            t_norm_func = DataSet.t_norm_func
            if not t_conorm:
                t_conorm_func = DataSet.recupera_t_con(t_norm_func)
                # è simmetrica la separation? nel dubbio calcoliamola in generale
                
            self.sep = [[0 for i in range(len(self.L))] for j in range(len(self.L))]
            for i in range(len(self.L)):
                for j in range(len(self.L)):
                    self.sep[i][j] = 1
                    for k in range(len(self.L)):
                        self.sep[i][j] +=t_conorm_func(
                            (t_norm_func(t_norm_func(self.fuz_dom[i][j],self.fuz_dom[k][j]),self.fuz_dom[i][k])), # t_norm io suppongo sia assocciativa
                            (t_norm_func(t_norm_func(self.fuz_dom[j][i],self.fuz_dom[k][i]),self.fuz_dom[j][k]))
                        )
                            
    def fuzzy_func_culo(self,i,j):
        if self.L.domination_matrix[i][j]:
            return 1
        
        elif self.L.domination_matrix[j][i]:
            return 0
        
        else:
            return len(self.L.index_downset(i) & self.L.index_downset(j)) / len(self.L.index_downset(j))
        

    def t_norm_func(a,b):
        return a*b
    
    def recupera_t_con(t_norm_func):
        func = lambda a,b: 1 - t_norm_func(1-a,1-b)
        return func
    
    
L = pl.Lattice.from_power_set(2)
L.hasse_p5()
D = DataSet(L,[i for i in range(len(L))])
D.fuzzy_dom()
D.fuzzy_sep()

print('fuz_dom')
for a in D.fuz_dom:
    print([round(i,2) for i in a]) # DIO FUNZIONA C'È da capire perchè D.sep[i][i] != 0
print()
print('fuz_sep')
for a in D.sep:
    print([round(i,2) for i in a]) # DIO FUNZIONA C'È da capire perchè D.sep[i][i] != 0
# Quello che è certo è che se separation_{ij} = 1 +sum... allora separation_{ii} >= 1.
# c'è qualcosa che non va sicuro. . . 

