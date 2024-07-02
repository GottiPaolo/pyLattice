import numpy as np
#import p5
import tkinter as tk
from PIL import ImageGrab#Screeeeenshot fuck

#### Hasse functions
def get_riga_punto(cover_matrix,p,righe):
    """
    funzione per ottenere la riga di un punto in un diagramma di Hasse a partire dalle righe note e dalla matrice di copertura
    Questa funzione sfrutta la ricorsività,
    """
    if righe[p]:
        return righe[p]
    
    elif sum(cover_matrix[p]) == 0:
        righe[p] = 0
        return 0
    
    else:
        riga_temp = 0
        for i in range(len(cover_matrix)):
            if cover_matrix[p][i] == 1 and not righe[i]:
                righe[i] = get_riga_punto(cover_matrix,i,righe)
            if cover_matrix[p][i] == 1 and righe[i] >= riga_temp:
                riga_temp = righe[i] + 1
        righe[p] = riga_temp
        return riga_temp

def get_righe(cover_matrix):
    """
    Data una matrice di copertura ottiene una lista che alla cella i-esima contiene la riga
    in cui un punto si posiziona nel diagramma di hasse del PoSet.
    La riga si ottiene grazie ad una funzione d'appogio e si basa sulla formula:
    a.riga = max{b.riga |a\prec b} se \exits b: a\prec b; 0 altrimenti.
    """
    righe = [None for i in range(len(cover_matrix))]
    for j in range(len(cover_matrix)):
        righe[j] = get_riga_punto(cover_matrix,j,righe)
    return righe
   
def get_colonne(righe):
    """
    Data la lista di righe dei punti in un diagramma di hasse
    restituisce la loro colonnna.
    Si basa semplicemente sul fatto che la colonna corrisponde col numero di punti presenti fin'ora in quella riga
    (il primo punto è in colonna 0, il secondo in colonna 1 etc.)
    """
    return [righe[:p].count(righe[p]) for p in range(len(righe))]

def converti(riga,colonna,r,righe,min_x,max_x,min_y,max_y, hasse_mode = 4):
    """
    Questa funzione è ufficialmente obsoleta e inutilizzata, 
    Per ora voglio mantenerala per avere lo spunto per fare qualche improvmnet futur
    con diversi opzionoi di diagramma di Hasse, si basava sulla funzione mappa che ho rimosso ma semplicemente
    mappa(a,min,max,MIN,MAX) = (a - min) / (max - min) * (MAX - MIN) + MIN
    chiaramente con un attenzione per i casi estremi: if min == max reutrn 0.5 * (MAX - MIN) + MIN
    """
    if hasse_mode == 0:
        y = mappa(riga,-0.5,max(righe) + 0.5,min_y,max_y-r)
        x = mappa(colonna,-0.5,righe.count(riga) -0.5,min_x,max_x)
  
    elif hasse_mode == 1:
        gap_x = (max_x - min_x) / max([righe.count(r) for r in righe])
        gap_y = (max_y - min_y) / (max(righe) + 1)
        y = min_y + (riga + 0.5) * gap_y
        x = min_x + (colonna +0.5) * gap_x

    elif hasse_mode == 2:
        gap_x = (max_x - min_x) / max([righe.count(r) for r in righe])
        y = mappa(riga+0.5,0,max(righe)+1,min_y,max_y)
        x = min_x + (max_x-min_x)*0.5 + (colonna - righe.count(riga)/2+0.5)*gap_x

    elif hasse_mode == 3:
        max_n_righe = max([righe.count(r) for r in righe]) # numero massimo di elementi in una riga
        
        if max_n_righe == 1: 
            space_x =0  #se c'è al massimo un solo elemento per riga il gap è 0
        else:
            space_x = (max_x - min_x) / (4 * (max_n_righe-1))
        
        if max(righe) == 0:
            space_v = 0
        else:
            space_v = (max_y - min_y) / (4 * (max(righe)))
            
        y = mappa(riga,0,max(righe) ,min_y+space_v,max_y-space_v)
        x = mappa(colonna,-1,righe.count(riga),min_x-space_x,max_x+space_x)
        
    elif hasse_mode == 4:
        """
        Squadro i margini tenendo il maggiore
        """
        max_n_righe = max([righe.count(r) for r in righe]) # numero massimo di elementi in una riga
        
        if max_n_righe == 1: 
            space_x =0  #se c'è al massimo un solo elemento per riga il gap è 0
        else:
            space_x = (max_x - min_x) / (4 * (max_n_righe-1))
        
        if max(righe) == 0:
            space_y = 0
        else:
            space_y = (max_y - min_y) / (4 * (max(righe)))
            
        gap = max(space_x, space_y)
        y = mappa(riga,0,max(righe,),min_y+gap,max_y-gap)
        x = mappa(colonna,-1,righe.count(riga),min_x-gap,max_x+gap)
        
    elif hasse_mode == 5:
        n_points = max(max([righe.count(r) for r in righe]),(max(righe) + 1))#
        gap_x = (max_x - min_x) / n_points #(cons# idero come margine gap/2)
        gap_y = (max_y - min_y) / n_points
        #gap = max(gap_x, gap_y)
        
        y = min_y + gap_y*0.5 + riga*gap_y + (n_points - (max(righe) + 1)) *0.5* gap_y # devo centrare y se vince x , così come centro x se vince y
        x = min_x + gap_x * 0.5 + colonna*gap_x + (n_points - righe.count(riga)) *0.5* gap_x# + qualcosa legato a righe.count(riga) e max([righe.count(r) for r in righe])
   
    elif hasse_mode == 6:
        """
        Diagramma di hasse centrato in un riquadro
        tra gap_x e gap_y prendo il minore e lo rendo universale
        la distanza tra righe e coloenne è la stessa
        """
        gap_x = (max_x - min_x) / max([righe.count(r) for r in righe])
        gap_y = (max_y - min_y) / (max(righe) + 1)
        if gap_x > gap_y:
            x = min_x + colonna*gap_y + ((max_x-min_x) - (righe.count(riga)-1)*gap_y)*0.5
            y = min_y + riga*gap_y + ((max_y-min_y) - (max(righe))*gap_y)*0.5
       
        else:
            x = min_x + colonna*gap_x + ((max_x-min_x) - (righe.count(riga)-1)*gap_x)*0.5
            y = min_y + riga*gap_x + ((max_y-min_y) - (max(righe))*gap_x)*0.5
       
            
    else:
        raise ValueError('Hasse mode non definita')
      
    return x,y
     
def mappa(x,old_min,old_max,new_min,new_max):
    """
    Funzione per mappare un valore da un intervallo ad un altro
    Di fatto INUTILIZZATA mi serviva in "converti" che è obsoleta
    """
    if old_min==old_max:
        return 0.5 * (new_max - new_min) + new_min
    else:
        return (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
        
#### Congruence Function
def unisci(a,b,blocchi):
    """
    Questa funzione deve solo fare in modo che in una congruenza (blocchi) risulti che gli elementi a e b abbiano lo stesso valore
    (facciano parte della stessa classe d'eq) 
    Per uniformare il tutto faccio in modo che soppravvivi sempre l'indice più piccolo. 
    In questa maniera le congruenza sono definite unicamente, perchè ogni elemento finità per avere come indice della classe
    l'indice del più piccolo elemento presente
    
    (QUA HO GRANDISSIMO MARGINE DI IMPROVMENT, almeno la transitività posso completarla io senza cicli...)
    """
    blocchi[a] = min(blocchi[a],blocchi[b])
    blocchi[b] = min(blocchi[a],blocchi[b])
    #blocchi[max(a,b)] = blocchi[min(a,b)]
    return blocchi 

def confronta_blocchi(b1,b2):
    """
    Verifica se una cingruenza domina un'altra in ConL 
    
    Per come ho strutturato le congruenze b2 domina b1 se tutte le "identità" in b1 sono presenti anche in b2
    Quindi controllo tutte le coppie di b1, se incontro anche solo una coppia uguale in b1 e differente in b2 allora restituisco falso
    altrimenti restituisco vero
    
    ttudiando la matematica dietro la struttura che sto utilizzando probabilmente posso certamente renderlo più efficiente.
    """
    for i in range(len(b1)):
        for j in range(i+1,len(b1)):
            if b1[i] == b1[j] and b2[i] != b2[j]:
                return False
    return True

def replace_values_list(lista, oggetto, nuovo):
    """
    Da una lista geenera una nuova lista in cui gli elemtni "oggetto" sono sostituiti con gli elementi "nuovo"
    """
    return [nuovo if item == oggetto else item for item in lista]

def unisci_congruenze(C1,C2):
    """
    Unisce due congruenze, operatore "join" dentro ConL
    Ricordiamo che per come sto strutturando le congruenze le seguenti due sono identiche ma io incontrerò solo la prima:
    [0,1,0,1,2]
    [0,2,0,2,1]
    Poichè l'elemente della lista indica il gruppo di appartenenza, l'indice della lista indica l'elemento di riferimento
    Per evitare di avere congruenze concettualmente identiche ma sostanzialmente differenti (dato che poi devo anche confrontarle)
    Faccio sì che si propaghino in maniera costante, ovvero quando ne unisco due mantengo sempre il più piccolo
    
    Per ogni coppia di elementi se sono uguali in C1 ma diversi in C2 
    Questo algoritmo funziona (o almeno spero) anche se non so ancora bene come e perchè...
    Perchè non controllo il caso simmetrico a 
    C1[i] == C1[j] and C2[i] != C2[j] 
    ovvero
    C1[i] != C1[j] and C2[i] == C2[j]
    
    perchè mi basta scambiare max(C2[i],C2[j] con min(C2[i],C2[j]).
    se il minimo fosse in C1 ? -> penso che il punto sia che se il minimo
    Allora, usa la testa, per come ho strutturato le congruenze
    C
    """
    for i in range(len(C1)):
        for j in range(i+1,len(C1)):
            if C1[i] == C1[j] and C2[i] != C2[j]:
                C2 = replace_values_list(C2,max(C2[i],C2[j]),min(C2[i],C2[j]))
    return C2

def numero_blocchi(con):
    """
    Conta il numero di blocchi in una congruenza 
    coincide concettualmente con len(A.unique()) ma sfrutta la struttura della congruenze
    Non so se lo uso davvero ma sono sicuro che in caso si possa migliorare
    """
    n = 0
    for i,a in enumerate(con):
        if i==a:
            n+=1
    return n

#### FCA Function
def primes_o(oggetto,relation_matrix,nAtt):
    """
    Funzione ' su un gruppo di oggetti
    """
    att = list(range(nAtt))
    for g in oggetto:
        for a in range(nAtt):
            if a in att and relation_matrix[g][a] == 0:
                att.remove(a)
    return att

def primes_a(attributo,relation_matrix,nOgg):
    """
    Funzione ' su un gruppo di attributi    
    """
    ogg = list(range(nOgg))
    for a in attributo:
        for g in range(nOgg):
            if g in ogg and relation_matrix[g][a]==0:
                ogg.remove(g)
    return ogg

def close_o(oggetto,relation_matrix,nAtt,nOgg):
    return primes_a(primes_o(oggetto,relation_matrix,nAtt),relation_matrix,nOgg)

def close_a(attribbuto,relation_matrix,nOgg,nAtt):
    return primes_o(primes_a(attribbuto,relation_matrix,nOgg),relation_matrix,nAtt)

def fca(relation_matrix,incrementoPercentuale = 0.01):
    # thatsa difficult
    nOgg = len(relation_matrix)
    nAtt = len(relation_matrix[0])
    extent = []
    intent = []
    labelsO = []
    labelsA = []
    pr=0
    if nOgg<nAtt:
        for i in range(2**nOgg):
            if (i/2**nOgg)//incrementoPercentuale>pr:
                pr=i/2**nOgg
                print(round(pr,3))
            sub_set_ogg = []
            numero = i
            for k in range(numero):
                if numero%2==1:
                    sub_set_ogg.append(k)
                numero//=2
            close_obejct = close_o(sub_set_ogg,relation_matrix,nAtt,nOgg)
            if close_obejct not in extent:
                extent.append(close_obejct)
                intent.append(primes_o(close_obejct,relation_matrix,nAtt))
                labelsO.append([])
                labelsA.append([])
            if len(sub_set_ogg) == 1:
                labelsO[extent.index(close_obejct)].append(sub_set_ogg[0])

        for i in range(nAtt):
            fc = close_a([i],relation_matrix,nOgg,nAtt)
            labelsA[intent.index(fc)].append(i)
    else:
        for i in range(2**nAtt):
            if (i/2**nAtt)//incrementoPercentuale>pr//incrementoPercentuale:
                pr=i/2**nAtt
                print(round(pr,3))
            sub_set_att = []
            numero = i
            for k in range(numero):
                if numero%2==1:
                    sub_set_att.append(k)
                numero//=2
            close_att = close_a(sub_set_att,relation_matrix,nOgg,nAtt)
            if close_att not in intent:
                intent.append(close_att)
                extent.append(primes_a(close_att,relation_matrix,nOgg))
                labelsO.append([])
                labelsA.append([])
            if len(sub_set_att) == 1:
                labelsA[intent.index(close_att)].append(sub_set_att[0])

        for i in range(nOgg):
            fc = close_o([i],relation_matrix,nAtt,nOgg)
            labelsO[extent.index(fc)].append(i)
            
    return extent,intent,labelsO, labelsA

#### Support function
def fact(n):
    if n == 0:
        return 1
    for m in range(2,n):
        n*=m
    return n

def permutazioni(lista):
    dimensione_lista = len(lista)
    for indice in range(fact(dimensione_lista)):
        dati = [a for a in lista]
        permutazione = []
        for i in range(dimensione_lista):
            permutazione.append( dati[indice // fact(dimensione_lista-i-1)])
            indice %= fact(dimensione_lista-i-1)
            dati.remove(permutazione[-1])
        yield permutazione
        
def permutezione_esima(indice,lista):
    dimensione_lista = len(lista)
    permutazione = []
    for i in range(dimensione_lista):
        permutazione.append( lista[indice // fact(dimensione_lista-i-1)])
        indice %= fact(dimensione_lista-i-1)
        lista.remove(permutazione[-1])
    return permutazione

def matrix_from_sparse(sparse : list[tuple],n):
    """
    Data una matrice sparse di questo tipo: sparse = [(1,2), (2,2)] genero una matrice tale che:
    M[i][j] = 1 <-> (i,j) in sparse
    M[i][j] = 0 otherwise
    """
    matrix = [[0 for i in  range(n)] for j in range(n)]  
    for i,j in sparse:
        matrix[i][j] = 1
    return matrix
 
def component_wise(d1,d2):
    """
    funzione di confronto compoennt wise
    """
    one_win = False
    for a,b in zip(d1,d2):
        if b<a:
            return False
        elif b>a:
            one_win = True
    return one_win

def genera_cw(lista : list[int]) -> list[tuple]:
    """
    Funzione pergenerare tutti i possibili profili del cartesiano di n valori, ad esempio
    genera_cw([3,2]): -> [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
    """
    if len(lista) == 1:
        return [(i,) for i in range(lista[0])]
        
    risultato = []
    for i in range(lista[0]):
        for sotto_risultato in genera_cw(lista[1:]):
            risultato.append((i,) + sotto_risultato)
        
    return risultato

def permuta_matrice(matrice,nuovo_ordine):
    """
    riordina una matrice in maniera sensata scriverò dopo
    """
    new_m = [[0 for i in range(len(matrice))] for j in range(len(matrice))]
    
    for i in range(len(matrice)):
        for j in range(len(matrice)):
            new_m[i][j] = matrice[nuovo_ordine[i]][nuovo_ordine[j]]
    return new_m

def product(lista):
    """
    produttoria di una lista di numeri
    """
    p = 1
    
    for t in lista:
        p*=t
        
    return p

def join_irriducible_cw(*cw):
    """
    Questa funzione calcola le congruenza join-irriducibili in un reticolo component wise sfruttando molte proprietà
    I dettagli matematici li tratterò a parte, ma sono una generalizzazione dei cambi di base
    """
    ###### FUNZIONA CAZZO
    recurs = [product(cw[i+1:]) for i in range(len(cw)-1)]+[1]
    dati = genera_cw(cw)
    CON = []
    for i,v in enumerate(cw):
        for j in range(1,v):
            con = [ind if d[i]!= j else ind - recurs[i] for ind,d in enumerate(dati)]
            CON.append(con)
    return CON
        
        
#### PoSet Class
class PoSet:
    def __init__(self,domination_matrix, X = None, labels = None, blocchi = None):
        """
        Crea un bel PoSet:
        - domination_matrix: Matrice di dominanze
        - X elenco di oggetti, se non passatti verrano usati numeri progressivi
        """
        try:
            if X:
                self.obj = X
            else:
                self.obj = list(range(len(domination_matrix)))
        except ValueError: # Troverò un modo migliore ma se X è una lista di liste da problemi
            self.obj = X
            
        if type(domination_matrix) == list: 
            self.domination_matrix = np.array(domination_matrix)
        elif type(domination_matrix) == np.ndarray:
            self.domination_matrix = domination_matrix
              
        self.cover_matrix = self.domination_matrix - np.eye(len(domination_matrix)) - np.where((self.domination_matrix - np.eye(len(domination_matrix))) @ (self.domination_matrix - np.eye(len(domination_matrix))) > 0,1,0)

    def domination(self,a,b, from_index = False):
        """
        return TRUE if a > b
                False if not
        """
        if from_index:
            return bool(self.domination_matrix[b][a])
        return bool(self.domination_matrix[self.obj.index(b)][self.obj.index(a)])
    
    def cover(self,a,b, from_index = False):
        """
        return TRUE if a cover b
                False if not
        """
        if from_index:
            return bool(self.cover_matrix[b][a])
        return bool(self.cover_matrix[self.obj.index(b)][self.obj.index(a)])

    def upset(self,*a, from_index : bool = True, as_index  : bool= True) -> set :
        """
        Calcola l'upset di un insieme di elementi del poset
        restitusce l'insieme degli elementi che dominano tutti quelli passati
        i parametri 
        
        from_index e as_index sono due booleani che indicano sono stati forniti e come verrano restituiti gli elementi
        
        UpSet qua è inteso come l'insieme degli elementi che dominano TUTTI quelli indicati, 
        quindi l'intersezione dei subset dei singoli elementi
        """
        if not from_index:
            a = [self.obj.index(x) for x in a]

        if len(a) == 1:
            upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if r }
        else:
            upset = self.upset(a[0]) & self.upset(*a[1:])
 
        if as_index:
            return upset
        else:
            return {self[i] for i in upset}
    
    def downset(self,*a, from_index : bool = True, as_index  : bool= True) -> set :
        """
        Calcola il downset di un insieme di elementi del poset
        restitusce l'insieme degli elementi che sono dominati tutti quelli passati
        
        from_index e as_index sono due booleani che indicano sono stati forniti e come verrano restituiti gli elementi
        
        UpSet qua è inteso come l'insieme degli elementi che dominano TUTTI quelli indicati, 
        quindi l'intersezione dei subset dei singoli elementi
        """
        if not from_index:
            a = [self.obj.index(x) for x in a]
            
        if len(a) == 1:
            downset = { i for i,r in enumerate(self.domination_matrix) if r[a[0]] }
        else:
            downset = self.downset(a[0]) & self.downset(*a[1:])
            
        if as_index:
            return downset
        else:
            return {self[i] for i in downset}
        
    def max_sub_set(self,set, from_index : bool = True, as_index  : bool= True):
        """
        Restituisce l'insieme degli elementi che non sono dominati in un sottoinsieme degli elementi
        """
        if from_index:
            set = list(set)
        else:
            set = [self.obj.index(x) for x in set]
            
        upper = []
        for x in set:
            up = True
            for y in set:
                if x != y and self.domination_matrix[x][y]:
                    up = False
                    break
            if up:
                upper.append(x)
                
        if as_index:
            return upper
        else:
            return [self[i] for i in upper]
        
    def min_sub_set(self,set, from_index : bool = True, as_index  : bool= True):
        """
        Restituisce l'insieme degli elementi che sono dominati da tutti gli altri elementi di un sottoinsieme
        """
        # Sono sicuro che questa cosa degli indici possa essere fatta in maniera intelligente con un wrapper
        if from_index:
            set = list(set)
        else:
            set = [self.obj.index(x) for x in set]
            
        downer = []
        for x in set:
            down = True
            for y in set:
                if y != x and self.domination_matrix[y][x]:
                    down = False
                    break
            if down:
                downer.append(x)
                
        if as_index:
            return downer
        else:
            return [self[i] for i in downer]
            
    def join(self,*args, from_index = True, as_index=True, force = False):
        """
        calcla il join di due o più elementi, ovver il più piccolo elemento che li domina entrambi
        Se il join non è definito viene restituito
        se il parametro _force_ è True allora viene restituita una lista vuota se non esitte, 
        oppure contenente i possibili valori se non è unico
        
        Nel caso _force_ non venga specificato ed il join non è definito viene restituito un errore
        """
        min_up_set = self.min_sub_set(self.upset(*args, from_index=from_index))
        if len(min_up_set) == 1:
            if as_index:
                return min_up_set[0]
            else:
                return self[min_up_set[0]]
        
        elif len(min_up_set) == 0:
            return None
        
        elif force:
            if as_index:
                return min_up_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
            else:
                return [self[i] for i in min_up_set]
        else: 
            return None
            # raise ValueError("join non definito")
        
    def meet(self, *args, from_index = True, as_index=True, force = False):
        """
        calcla il meet di due o più elementi, ovver il più grande elemento che dominato da entrambi
        Se il meet non è definito viene restituito
        se il parametro _force_ è True allora viene restituita una lista vuota se non esitte, 
        oppure contenente i possibili valori se non è unico
        
        Nel caso _force_ non venga specificato ed il meet non è definito viene restituito un errore
        """
        max_down_set = self.max_sub_set(self.downset(*args, from_index = from_index))
        if len(max_down_set)==1:
            if as_index:
                return max_down_set[0]
            else:
                return self[max_down_set[0]]
            
        if len(max_down_set)==0:
            return None
        elif force:
            if as_index:
                return max_down_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
            else:
                return [self[i] for i in max_down_set] # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
        else:
            return None
            #raise ValueError("meet non definito") #devo guardare come si creano gli errori #devo differenziare tra "non esiste" e "ambiguo"
        
    def index_upset(self,*a, strict : bool = False):
        """
        Identica alla funzione upset ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if strict:
            if len(a) == 0:
                return {i for i in range(len(self))} # l'upset di un set vuoto è tutto
            if len(a) == 1: 
                upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if r and i!=a[0]}
                return upset
            else:
                return self.index_upset(a[0], strict = True) & self.index_upset(*a[1:], strict = True) #
        else:
            if len(a) == 0:
                return {i for i in range(len(self))} # l'upset di un set vuoto è tutto
            if len(a) == 1: 
                upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if r }
                return upset
            else:
                return self.index_upset(a[0]) & self.index_upset(*a[1:]) # Ma io allora non ho capito niente, io uso l'intersezione ma dovrei utilizzare l'unione
    
    def real_index_upset(self,*a, strict : bool = False):
        """
        Vero upset: ovvero UNIONE degli upset dei singoli elementi, non l'intersezione
        In più ho aggiunto un parametro booleano strict per indicare se usare la dominanza stretta o classica
        (utile per alcune funzioni di fuzzyficazione)
        """
        if strict:
            if len(a) == 0:
                return {i for i in range(len(self))} # l'upset di un set vuoto è tutto
            if len(a) == 1: 
                upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if (r and i!=a[0])}
                return upset
            else:
                return self.real_index_upset(a[0], strict = strict) | self.real_index_upset(*a[1:], strict = strict) # Ma io allora non ho capito niente, io uso l'intersezione ma dovrei utilizzare l'unione

        else:
            if len(a) == 0:
                return {i for i in range(len(self))} # l'upset di un set vuoto è tutto
            if len(a) == 1: 
                upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if r }
                return upset
            else:
                return self.real_index_upset(a[0], strict = strict) | self.real_index_upset(*a[1:], strict = strict) # Ma io allora non ho capito niente, io uso l'intersezione ma dovrei utilizzare l'unione
    
    def index_downset(self,*a, strict : bool = False):
        """
        Identica alla funzione downset ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if strict:
            if len(a) == 0:
                return {i for i in range(len(self))} # il down set di un set vuoto è tutto

            if len(a) == 1:
                downset = {i for i,r in enumerate(self.domination_matrix) if r[a[0]] and i != a[0]}
                return downset
            else:
                return self.index_downset(a[0], strict=True) & self.index_downset(*a[1:],strict=True)
        
        else:   
            if len(a) == 0:
                return {i for i in range(len(self))} # il down set di un set vuoto è tutto

            if len(a) == 1:
                downset = {i for i,r in enumerate(self.domination_matrix) if r[a[0]]}
                return downset
            else:
                return self.index_downset(a[0]) & self.index_downset(*a[1:])
        
    def index_max_sub_set(self,set):
        """
        Identica alla funzione max_sub_set ma invece che richiedere un elemento del poset chiede solo il suo indice
        
        Non posso super semplifcarla semplicemente sommando i valori della matrice di dominanza filtrata e vedere se c'è uno zero?
        """
        set = list(set)
        upper = []
        for i in set:
            up = True
            for j in set:
                if i!=j and self.domination_matrix[i][j]:
                    up = False
                    break
            if up:
                upper.append(i)
        return upper
    
    def index_min_sub_set(self,set):
        """
        Identica alla funzione min_sub_set ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        set = list(set)
        downer = []
        for i in set:
            down = True
            for j in set:
                if i!=j and self.domination_matrix[j][i]:
                    down = False
                    break
            if down:
                downer.append(i)
        return downer
             
    def index_join(self,*args):
        """
        Identica alla funzione join ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if len(args) == 2:
            if self.domination_matrix[args[0]][args[1]]:
                return args[1]
            elif self.domination_matrix[args[1]][args[0]]:
                return args[0]
            
        min_up_set = self.index_min_sub_set(self.index_upset(*args))
        if len(min_up_set) == 1:
            return min_up_set[0]
        else:
            return None
            # raise ValueError("join non definito")
        
    def index_meet(self, *args):
        """
        Identica alla funzione meet ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if len(args) == 2:
            if self.domination_matrix[args[0]][args[1]]:
                return args[0]
            elif self.domination_matrix[args[1]][args[0]]:
                return args[1]
            
        max_down_set = self.index_max_sub_set(self.index_downset(*args))
        if len(max_down_set)==1:
            return max_down_set[0]
        else:
            return None
            # raise ValueError("meet non definito")#devo guardare come si creano gli errori #devo differenziare tra "non esiste" e "ambiguo"
    
    def is_lattice(self):
        """
        Verifica che il poset sia un reticolo verificando che esista il join ed il meet per ogni coppia di elementi.
        """
        for i in range(len(self)):
            for j in range(i+1,len(self)):
                if  self.index_join(i,j) == None or self.index_meet(i,j) == None:
                    return False
        return True
    
    def to_lattice_fca(self):
        """
        Esegue il completamento di Dedekind tramite l'FCA
        (tutto sommato inutile)
        """
        extent,intent,labelsO, labelsA= fca(self.domination_matrix)
        labelsO = [self.labels[x[0]] if len(x)==1 else '' for x in labelsO]
        return Lattice.from_function(list(zip(extent,intent)),lambda x,y: set(x[0])<=set(y[0]),labelsO)
        #return Lattice.from_function(list(zip(extent,intent)),lambda x,y: set(x[0])<=set(y[0]),intent)
       
    def isomorphic(self,other) -> bool:
        """
        Verifica se due poset sono isomorfi, 
        per niente ottimizzata, dovrei studiarmi la teoria!
        """
        if len(self) != len(other):
            return False
        else:
            for indici in permutazioni(list(range(len(self)))):
                if ([[self.domination_matrix[i][j] for j in indici] for i in indici] == other.domination_matrix).all():
                    return True
        return False
          
    def __str__(self):
        """
        Come stringa viene restituita la matrice di dominanze
        """
        return str(self.domination_matrix)
    
    def __len__(self):
        """
        Come lunghezza viene restituito il numero di elementi
        """
        return len(self.obj)
        
    def __getitem__(self, indice):
        """
        pota
        """
        return self.obj[indice]
    
    def __iter__(self):
        """
        pota
        """
        return iter(self.obj)
    
    def __mul__(self,other):
        """
        Moltiplicazione definita da 
        L x W = Q : Q.obj = L.obj x W.obj 
        Q.i <_q Q.j  <==>  Q.i.l <_l Q.j.l <_l and  Q.i.w <_l Q.j.w <_w  
        """
        matrice = np.eye(len(self)*len(other))
        for i in range(len(self)*len(other)):
            for j in range(i+1,len(self)*len(other)):
                self_index_i = i // len(other)
                self_index_j = j // len(other)
                other_index_i = i % len(other)
                other_index_j = j % len(other)
                if self.domination_matrix[self_index_i][self_index_j] and other.domination_matrix[other_index_i][other_index_j]:
                    matrice[i][j] = 1
                elif self.domination_matrix[self_index_j][self_index_i] and other.domination_matrix[other_index_j][other_index_i]:
                    matrice[j][i] = 1

        self_  = [s if type(s) == tuple else (s,) for s in self]
        other_ = [s if type(s) == tuple else (s,) for s in other]
        x = [s + o for s in self_ for o in other_]
        return PoSet(matrice,x)
    
    def __add__(self,other):
        """
        Somma definita da 
        L + W = Q : Q.obj = L.obj + W.obj 
        Q.i <_q Q.j  <==>  (Q.i \in W and Q.j \in W) or (Q.i <_l Q.j) or (Q.i <_w Q.j) 
        """
        matrice = np.eye(len(self)+len(other))
        for i in range(len(self)+len(other)):
            for j in range(i+1,len(self)+len(other)):
                if i<len(self) and j<len(self):
                    matrice[i][j] = self.domination_matrix[i][j]
                    matrice[j][i] = self.domination_matrix[j][i]
                elif i>=len(self) and j>=len(self):
                    matrice[i][j] = other.domination_matrix[i-len(self)][j-len(self)]
                    matrice[j][i] = other.domination_matrix[j-len(self)][i-len(self)]
                else:
                    #matrice[i][j] = 0
                    matrice[i][j] = 1
        return PoSet(matrice,self.obj+other.obj)
    
    def __sub__(self,other):
        """
        Come differenza per ora ho definito la and component. sembra un casino ma è utile in certe costruizioni di reticoli
        Se io ho tre elementi 1,2,3. Se in un poset ho li ho ordinati come 1>2>3 ed in un altro 2>1>3. Allora posso costruire il poset
        allora posso costruire il poset in cui 1||2 ma 1,2 > 3. In altre parole il più piccolo PoSet che li rispetta entrambi
        
        Fun fact: per come ho definito la sottrazione è commuttativa!
        """
        assert len(self) == len(other)
        return PoSet(np.where(self.domination_matrix+other.domination_matrix > 1,1,0))
    
    def __neg__(self):
        """
        Non particolarmente essenziale (anzi rischia di fare danni) ma così posso calcolare il duale di P come -P
        Nonostatne ciò Q - P rimane quello che ho definito, non diventa: Q + (-P) = Q + P^d
        """
        return self.dual()
    
    def sort(self):
        lista = list(range(len(self)))
        dati = [(sum(self.cover_matrix[i]), sum([self.cover_matrix[k][i] for k in range(len(self))])) for i in range(len(self))]
        lista.sort(key = lambda i:dati[i])
        self.domination_matrix = permuta_matrice(self.domination_matrix,lista)
        self.cover_matrix = permuta_matrice(self.cover_matrix,lista)
        self.obj = [self.obj[i] for i in lista]
    
    def dual(self):
        """
        Restituisce il duale di un reticolo (semplicemente prendendo la trasposta della matrice di dominanze)
        """
        return PoSet(np.transpose(self.domination_matrix),self.obj,self.labels)
    
    def from_function(X,f ,labels = None):
        """
        Funzione per creare un PoSet da un insieme di elementi ed una funzione per confrontarli
        La funzione f deve essere del tipo f(a,b) --> bool: f(a,b) = True <==> a < b
        (Di base viene già inserità la riflessività, quindi si può trascurare nella funzione,
        può essere comodo in molti casi, ma può portare ad errori motlo difficili da identificare in altri.
        Dovrei inserire una parametro booleano ma ne parliamo in futuro)
        
        
        Ad esempio PoSet.from_function(list(range(20)), lambda a,b : a % b == 0)
        """
        domination_matrix = np.eye(len(X)) # Assumo che la funzione che mi viene passata sia giusta e quindi parto dall'indetità e skippo i valori uguali
        for i,a in enumerate(X):
            for j,b in enumerate(X[i+1:]):
                if f(a,b):
                    domination_matrix[i][j+i+1] = 1
                elif f(b,a):
                    domination_matrix[j+i+1][i] = 1
        #return PoSet(domination_matrix,labels = labels)
        return PoSet(domination_matrix,X,labels = labels)
    
    def from_cover_matrix(cover_matrix,X = None, labels = None):
        """
        Funzione per creare un PoSet dalla matrice di cooperture invece che dalle dominaze 
        Particolarmente comoda se dobbiamo "trascrivere" un disegno
        
        Si basa sull'identità
        Z = Bin((C+I)^{n-1})
        """
        if type(cover_matrix) == list: 
            cover_matrix = np.array(cover_matrix)
            
        domination_matrix = np.eye(len(cover_matrix))
        cover_matrix = cover_matrix + domination_matrix  # Sarebbe C + I ma sfrutto che inizializzo Z ad I per non calcolare due volte I
        
        for i in range(len(cover_matrix)-1):
            domination_matrix = domination_matrix @ cover_matrix
            
        domination_matrix = np.where( domination_matrix > 0, 1, 0)
        
        return PoSet(domination_matrix,X,labels)
    
    def from_antichain(n):
        return PoSet.from_function(list(range(n)), lambda a,b : a==b)
     
    def FCA(relation, oggetti=None, attributi=None):
        """
        FCA per niente ottimizzata, letteralmente scorrendo tutto il powerset di extent / intent
        """
        if not oggetti:
            oggetti=list(range(relation))
        if not attributi:
            attributi=list(range(relation[0]))
        # Bah si potrebbe fare MOooolto meglio
        extent,intent,labelsO, labelsA = fca(relation)

        Obj = []
        for exte, inte in zip (labelsO, labelsA):
            testo = '-'
            O = list(map(lambda i: oggetti[i], exte))
            A = list(map(lambda i: attributi[i], inte))
            for i in O:
                testo += f' {i}'
            testo+='\n='
            for i in A:
                testo += f' {i}'
            Obj.append(testo)
        return Lattice.from_function(list(zip(extent,intent)),lambda x,y: set(x[0])<=set(y[0]),Obj)

    def as_lattice(self):
        """
        funzione per convertire il poset in reticolo. I reticoli hanno alcune funzioni che i PoSet non hanno
        e soprattuto alcune funzioni vengono calcolate in maniera differente per questioni di efficienza, 
        MA se si tratta come un reticolo un poset si potrebbero ottenere risultati coerenti ma in realtà falsi.
        (Nel reticolo non verifico che il join sia unico perchè so che lo è!)
        """
        self.__class__ = Lattice
        
    def sub_poset(self,sub_set):
        """
        restituisce il PoSet di  una porzione del poSet di partenza, 
        particolarmente comodo per esplorare e rappresentare poset di grandi dimensioni
        
        Potrei ottimizzarlo prendendo un sottoinsieme della matrice di dominanze invece che utilizzando una funzione, ma non è urgnete
        """
        return PoSet.from_function([self[i] for i in sub_set],lambda x,y: self.domination_matrix[self.obj.index(x)][self.obj.index(y)])
          
    def dedekind_completetion(self, nice_labels = False):
        """
        Implementanto in versione stupida O(2**n)
        per ogni A \subset P, ovver per ogni A \in Poweset(P)
        calcoliamo A^u^l e poi ordiniamo i risultati per inclusione
        Dovrò capire la versione step wise
        
        Se nice_labels è True, come labels vengono utilizzate quelle del poset di partenza, esclusi i punti nuovi
        """   
        cuts = []
        for i in range(2**len(self)):
            # questo funziona print(i,[j for j in range(len(self)) if (i//2**j) %2 == 1])
            # SubSet = [j for j in range(len(self)) if (i//2**j) %2 == 1]
            # up_set = self.index_upset(*SubSet)
            # closed = self.index_downset(*list(up_set))
            closed = self.index_downset(*list(self.index_upset(*[j for j in range(len(self)) if (i//2**j) %2 == 1])))

            if closed not in cuts:
                cuts.append(closed)
        if nice_labels:
            obj = ['' for c in cuts]
            for j in range(len(self)):
                sub = self.index_downset(j)
                for i,c in enumerate(cuts):
                    if c == sub:
                        obj[i] = self.obj[j]
            L = Lattice.from_function(cuts,lambda a,b: a<= b,)
            L.obj = obj
            return L
        return Lattice.from_function(cuts,lambda a,b: a<= b)
      
    def restituiscimi_cover_matrix(self) -> None:
        for i,k in enumerate(self.cover_matrix):
            if i ==0 :
                print('[',[int(a) for a in k],',')
                
            elif i != len(self) - 1:
                print([int(a) for a in k],',')
                
            else:
                print([int(a) for a in k],']')
      
    def _simple(self):
        self.obj = [str(i) for i in range(len(self))]
        self.labels = [str(i) for i in range(len(self))]
        
        
    # Hasse semi-def     
    def get_hasse_variables(self,labels = None, radius = 3, font_size = 12, vertex_color = None,
                            nodes_color = None, stroke_weights = None):
        rows = get_righe(self.cover_matrix)
        cols = get_colonne(righe = rows)
        gaps_x = [rows.count(x) ** -1 for x in rows]
        gap_y = (max(rows)+1) ** -1
        self.nodes = [((c+0.5)*gap_x, (r+0.5)*gap_y) for r,c,gap_x in zip(rows,cols,gaps_x)]
        self.vertex = [(i,j)  for i in range(len(self)) for j in range(i+1,len(self)) if self.cover_matrix[i][j] or self.cover_matrix[j][i]]
        self.r = radius
        self.font_size = font_size
        
        if vertex_color:
            self.vertex_color = vertex_color
        else:
            self.vertex_color = ['black' for v in self.vertex]
        
        if nodes_color:
            self.nodes_color = nodes_color
        else:
            self.nodes_color = ['grey' for v in self.nodes]
            
        if stroke_weights:
            stroke_weights = [1 for v in self.vertex]
            
        if not labels:
            self.labels = [str(x) for x in self.obj]
        else:
            self.labels = labels
                 
    def hasse(*PoSets, shape : tuple = (500,500), grid: tuple = None, show_labels : bool = False, 
                   title = 'PoSet', init = True, radius = None, font_size = None):
        """
        Come distinguo tra l'aspetto grafico e quello concettuale
        """
        if init:
            for P in PoSets:
                P.get_hasse_variables()
        if radius:
            for P in PoSets:
                P.r = radius
        if font_size:
            for P in PoSets:
                P.font_size = font_size
        return Finestra(*PoSets, shape = shape, grid = grid, show_labels=show_labels, title = title)
 
    def show_percorso(self, nodes, color ='red'):
        self.vertex_color =[color if (x in nodes and x!= nodes[-1] and nodes[nodes.index(x)+1] == y) or (y in nodes and y!= nodes[-1] and nodes[nodes.index(y)+1] == x) else 'black' for x,y in self.vertex]
       
    def show_nodes(self, nodes, color = 'black', as_index = True):
        if as_index:
            self.nodes_color = [color if i in nodes else self.nodes_color[i] for i in range(len(self))]
        else:
            self.nodes_color = [color if i in nodes else self.nodes_color[i] for i in range(self)]
            
    def show_congruence(self, con, color = 'red'):
        self.vertex_color = [color if con[a] == con[b] else 'black' for a,b in self.vertex]
        
           
class Lattice(PoSet):
    ## Personal Function
    def join(self,*args):
        """
        Calcola il join tra uno o più elementi
        """
        return self.obj[self.index_join(*(self.obj.index(x) for x in args))]
        
    def meet(self, *args):
        """
        Calcola il meet tra uno o più elementi
        """
        return self.obj[self.index_meet(*(self.obj.index(x) for x in args))]

    def index_join(self,*args):
        """
        Calcola il join tra uno o più elementi a partire dall'indice degli'elementi 
        Anche l'output è l'indice dell'elemento
        """
        
        if len(args) < 2:
            raise ValueError("Inserire almeno due indici")
        elif len(args) == 2:
            if self.domination_matrix[args[0]][args[1]]:
                return args[1]
            elif self.domination_matrix[args[1]][args[0]]:
                return args[0]
            
        return self.index_min_sub_lattice(self.index_upset(*args))
        
    def index_meet(self, *args):
        """
        Calcola il meet tra uno o più elementi a partire dall'indice degli'elementi 
        Anche l'output è l'indice dell'elemento
        """
        if len(args) < 2:
            raise ValueError("Inserire almeno due indici")
        elif len(args) == 2:
            if self.domination_matrix[args[0]][args[1]]:
                return args[0]
            elif self.domination_matrix[args[1]][args[0]]:
                return args[1]
 
        return self.index_max_sub_lattice(self.index_downset(*args))

    def index_min_sub_lattice(self,set):
        """
        Restituisce il minimo, come indicem di un sotto reticolo del reticolo 
        Il minimo di un reticolo è più veloce da calcolare del minimo di un subset generico perchè è O(n) non O(n^2)!
        non devo controllare tutte le coppie se so già che è un reticolo, devo solo trovare quella che è dominata e non domina
        """
        set = list(set)
        minimo = set[0]
        for i in set[1:]:
            if self.domination_matrix[i][minimo]:
                minimo = i
        return minimo
    
    def index_max_sub_lattice(self,set):
        """
        Restituisce il massimo, come indicem di un sotto reticolo del reticolo 
        
        Il massimo di un reticolo è più veloce da calcolare del minimo di un subset generico perchè è O(n) non O(n^2)!
        non devo controllare tutte le coppie se so già che è un reticolo, devo solo trovare quella che domina e non è dominata
        """
        set = list(set)
        massimo = set[0]
        for i in set[1:]:
            if self.domination_matrix[massimo][i]:
                massimo = i
        return massimo
    
    def index_meet_irriducibili(self):
        """
        Calcola gli elementi (come indici) meet irriducibili: in un reticolo finito coincidono con quelli che sono coperti da un solo elemento
        """
        return [i for i in range(len(self))  if sum(self.cover_matrix[i]) == 1]
    
    def index_join_irriducibili(self):
        """
        Calcola gli elementi (come indici) join irriducibili: in un reticolo finito coincidono con quelli che coprono  un solo elemento
        """
        return [i for i in range(len(self))  if sum(np.transpose(self.cover_matrix)[i]) == 1]
    
    def get_one_index(self):
        """
        restituisce l'indice del "1" ovvero l'elemtno che domina tutti, o analogamente 
        non è dominato da nessunuo escluso se stesso
        """
        for i in range(len(self)):
            if sum(self.domination_matrix[i]) == 1: # dominato solo da un elemento (se stesso)
                return i
    
    def get_zero_index(self):
        """
        restituisce l'indice dello "0" ovvero l'elemtno che è dominato tutti, o analogamente 
        non domina da nessunuo escluso se stesso
        """
        for i in range(len(self)):
            if sum(self.domination_matrix[i]) == len(self): #dominato da tutti
                return i
    
    def from_function(X,f,labels = None):
        domination_matrix = np.eye(len(X)) # Assumo che la funzione che mi viene passata sia giusta e quindi parto dall'indetità e skippo i valori uguali
        for i,a in enumerate(X):
            for j,b in enumerate(X[i+1:]):
                if f(a,b):
                    domination_matrix[i][j+i+1] = 1
                elif f(b,a):
                    domination_matrix[j+i+1][i] = 1
        #return PoSet(domination_matrix,labels = labels)
        return Lattice(domination_matrix,X,labels = labels)
    
    def from_cover_matrix(cover_matrix,X = None, labels = None):
        """
        Z = Bin((C+I)^{n-1})
        """
        if type(cover_matrix) == list: 
            cover_matrix = np.array(cover_matrix)
            
        domination_matrix = np.eye(len(cover_matrix))
        cover_matrix = cover_matrix + domination_matrix  # Sarebbe C + I ma sfrutto che inizializzo Z ad I per non calcolare due volte I
        
        for i in range(len(cover_matrix)-1):
            domination_matrix = domination_matrix @ cover_matrix
            
        domination_matrix = np.where( domination_matrix > 0, 1, 0)
        
        return Lattice(domination_matrix,X,labels)
    
    def dual(self):
        """
        Restituisce il duale di un reticolo (semplicemente prendendo la trasposta della matrice di dominanze)
        """
        A = super().dual()
        A.as_lattice()
        return A
    
    #### Esoteric
    def __mul__(self,other):
        A = super().__mul__(other)
        A.as_lattice()
        return A

    def __add__(self,other):
        A = super().__add__(other)
        A.as_lattice()
        return A
    
    def glued_sum(self,other):
        """
        Calcola la glued-sum di due reticoli
        La glued sum coincide con la somma classica ma vengono accorpati il maggiore assoluto del primo reticolo 
        con il minore assoluto del secondo
        
        In teoria può essere calcolata anche per i PoSet ma bisogna verificare che esistano minimo e massimo nei rispettivi
        """
        top = self.get_one_index()
        d = [[ self.domination_matrix[i][j] for j in range(len(self)) if j!= top] for i in range(len(self)) if i!=top]
        return PoSet(d,[self.obj[i] for i in range(len(self)) if i!= top], [self.labels[i] for i in range(len(self)) if i!= top] ) + other
        
    #### Congruence Staff
    def apply_congruence(self,congruence):
        """
        Lemma 6.12 (i) $X \le Y \Longleftrightarrow \exists a \in X,b\in Y: a\le b$
        """
        blocks = {}
        for i,a in enumerate(congruence):
            #if i == a: Posso sfruttare questa roba ma non so come QUESTO FUNZIONA SOLO PER COME HO STRUTTURATO LA CONGRUENZA
            if a not in blocks:
                blocks[a] = [i]
            else:
                blocks[a].append(i)
        
        print(blocks.values())
        labels = list(map(lambda x:' '.join(map(lambda c:str(self.labels[c]),x)),blocks.values()))
        #labels = list(map(lambda x:' '.join(map(lambda c:str(self.obj[c]),x)),blocks.values())) #obj o labels ? 
        matrix = np.eye(len(blocks))
        
        for i,v in enumerate(blocks):
            for j,q in enumerate(list(blocks.keys())[i+1:]):
                 for a in blocks[v]:
                     for b in blocks[q]:
                        if self.domination_matrix[a][b]:
                            matrix[i][j+i+1] = 1
                        elif self.domination_matrix[b][a]:
                            matrix[j+i+1][i] = 1

        return Lattice(matrix,X = labels)
  
    def calcola_congruenza(self,a,b):
        """
        Calcola la più piccola congruenza che unisce a e b (intesi come indici)
        
        Probabilmente può essere ottimizzato ma non mi interessa adesso
        """
        ### A e B sono indici
        blocchi = list(range(len(self)))
        blocchi = unisci(a,b,blocchi)
        cambiamenti = True
        while cambiamenti:
            cambiamenti = False
            for i in range(len(self)):
                for j in range(i+1,len(self)):
                    if blocchi[i]==blocchi[j]: 
                        for k in range(len(self)):
                            # transitività (base delle congruenze)
                            # Se i e j sono in relazione
                            # allora tutto ciò con cui k è in relazione
                            # lo è anche con i, e viceversa
                            if blocchi[i] == blocchi[k] and blocchi[k] != blocchi[j]:
                                blocchi = unisci(j,k,blocchi)
                                cambiamenti = True

                            if blocchi[j] == blocchi[k] and blocchi[k] != blocchi[i]:
                                blocchi = unisci(i,k,blocchi)
                                cambiamenti = True

                            ## Lemma 6.6 (i)
                            join_i = self.index_join(i,k)
                            join_j = self.index_join(j,k)
                            if blocchi[join_i]!=blocchi[join_j]:
                                blocchi = unisci(join_i,join_j,blocchi)
                                cambiamenti = True

                            meet_i = self.index_meet(i,k)
                            meet_j = self.index_meet(j,k)
                            if blocchi[meet_i] != blocchi[meet_j]:
                                blocchi = unisci(meet_i,meet_j,blocchi)
                                cambiamenti = True
        # self.blocchi = blocchi Può sembrare comoda questa cosa ma mi porta ad un problema:
        # questa funzione la utilizzo OGNI VOLTA che creo ConL, e se lascio questa parte finisce che OGNI VOLTA viene rappresentata una
        # congruenza anche se non voluta
        return blocchi
    
    def congruenze_elementari(self):
        """UFFICIALMENTE DEPRECATO
        Deprecato perchè ho ristretto ancora l'insieme delle congruenze necessarie alle congruenze join_irriducibili!
        (non grazie a me, ahimé ma grazie a questo paper: COMPUTING CONGRUENCE LATTICES OF FINITE LATTICES RALPH FREESE)
        Calcola le congruenze che ho definito _elementari_ cioè quelle che uniscono i blocchi a e b, tali che a \prec b
        
        """
        elementar_congruenze = [] #NON INSERISCO L'identità: list(range(len(self))) potrei farlo ma allunga il calcolo di all
        for i in range(len(self)):
            for j in range(i+1,len(self)):
                if self.cover_matrix[i][j] or self.cover_matrix[j][i]: #SOLO QUELLE ELEMENTARI 
                    cong = self.calcola_congruenza(i,j)
                    if cong not in elementar_congruenze:
                        elementar_congruenze.append(cong)
        return elementar_congruenze
    
    def congruenze_join_irriducibili(self):
        """
        Calcola le congruenze join irriducibili cioè quelle che uniscono i blocchi a e b, tali che a \prec b ed a è join irriducibile
        """
        irr_congruenze = []
        for e in self.index_join_irriducibili():
            for i in range(len(self)):
                if self.cover_matrix[i][e]:
                    cong = self.calcola_congruenza(e,i)
                    if cong not in irr_congruenze:
                        irr_congruenze.append(cong)
        return irr_congruenze
    
    def all_congruenze(self):
        """
        Calcola tutte congruenze combinando quelle elementari (adesso combinando quelle join-irriducibili)
        """
        # all_congruenze = self.congruenze_elementari()
        all_congruenze = self.congruenze_join_irriducibili()
        inizio = 0 
        futuro_inizio = None
        while inizio != futuro_inizio:
            futuro_inizio = len(all_congruenze)
            for i,a in enumerate(all_congruenze[inizio:]):
                for b in all_congruenze[inizio+i+1:]:
                    new = unisci_congruenze(a,b)
                    if new not in all_congruenze:
                        all_congruenze.append(new)

            inizio = futuro_inizio
        all_congruenze.append(list(range(len(self)))) # AGGIUNGO ALLA FINE IDENTITÀ
        return all_congruenze

    def CongruenceLattice(self, labels = False):
        a = self.all_congruenze()
        if not labels:
            return Lattice.from_function(a,confronta_blocchi,labels = [str(numero_blocchi(c)) for c in a])
        else:
            return Lattice.from_function(a,confronta_blocchi)
         
    #### Hasse
    def show_irriducible(self):
        """
        Mostra tutti gli elementi join irriducibili
        """
        J_ = self.index_join_irriducibili()
        M_ = self.index_meet_irriducibili()
        self.show_nodes(J_,'yellow')
        self.show_nodes(M_,'red')
        self.show_nodes([i for i in J_ if i in M_],'orange') 
    
    def dinamic_congruences(self, shape : tuple = (500,500), grid: tuple = None, 
                                 show_labels : bool = False, title = 'PoSet', init = True, 
                                 ConL = None):    
        if not ConL:
            ConL = self.CongruenceLattice()
        
        if init:
            self.get_hasse_variables()
            ConL.get_hasse_variables()
        Finestra(self, ConL, shape = shape, grid = grid, show_labels = show_labels,  title = title, dinamic_con = True)
 
    #### Special Lattice
    def from_power_set(n):
        """
        Restituisce il reticolo di un powerset di ordine n ordinato per inclusione
        """
        PowerSet = []
        for i in range(2**n):
            s = set()
            for j in range(n):
                if i % 2 == 0:
                    s.add(j)
                i//=2
            PowerSet.append(s)
            
        return Lattice.from_function(PowerSet,lambda a,b: a <= b)
    
    def from_diamond(a,b=None):
        """
        Il diamond altro non è che un caso specifico del Component Wise, sarà presto deprecato
        """
        if not b:
            b = a
        dati = [(i,j) for i in range(a) for j in range(b)]
        return  Lattice.from_function(dati,lambda b,n: b[0] <= n[0] and b[1]<=n[1])
    
    def from_chain(n):
        """
        Catene
        """
        return Lattice.from_function(list(range(n)),lambda a,b: a <= b)
    
    def from_cw(*lista):
        """
        Componente wise (chain product)
        """
        return Lattice.from_function(genera_cw(lista),component_wise)

   
class CW(Lattice):
    def __init__(self, *cw):
        self.cw = cw
        self.obj = genera_cw(cw)
        self.domination_matrix = np.eye(len(self.obj))
        for i,a in enumerate(self.obj):
            for j,b in enumerate(self.obj[i+1:]):
                if component_wise(a,b):
                    self.domination_matrix[i][j+i+1] = 1
                elif component_wise(b,a):
                    self.domination_matrix[j+i+1][i] = 1
        self.cover_matrix = self.domination_matrix - np.eye(len(self.domination_matrix)) - np.where((self.domination_matrix - np.eye(len(self.domination_matrix))) @ (self.domination_matrix - np.eye(len(self.domination_matrix))) > 0,1,0)

    def congruenze_join_irriducibili(self):
        return join_irriducible_cw(*self.cw)
    
    
class Finestra():
    def __init__(self,*hasses,shape : tuple = (500,500), grid = None, show_labels = False, font_size = 12, title = 'PosetMagico', dinamic_con = False):
        # Definisci Griglia
        if not grid:
            self.grid = (1, len(hasses))
        else:
            self.grid = grid
        
        assert self.grid[0] * self.grid[1] >= len(hasses)
            
        # definisci var
        self.title = title
        self.hasses = hasses
        self.show_labels = show_labels
        self.font_size = font_size
        self.shape = shape
        self.W = self.shape[0] / self.grid[1]
        self.H = self.shape[1] / self.grid[0]
            
        # Crea Finestra
        self.root = tk.Tk()
        self.root.geometry(str(shape[0])+'x'+str(shape[1]))
        self.root.title(title)
        self.canvas = tk.Canvas(self.root, width=shape[0], height=shape[1], bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.disegna()
        self.canvas.bind("<B1-Motion>", self.gestisci_movimento_mouse)
        self.canvas.bind("<Configure>", self.resize)
        self.root.bind("j", self.show_all_irriducible)
        self.root.bind("r", self.reset)
        self.root.bind("<Up>", self.show_upset)
        self.root.bind("<Down>", self.show_downset)
        self.root.bind("s", self.save)
        self.root.bind("d", self.capture_window)
        if dinamic_con:
            self.canvas.bind('<Motion>',self.show_con)
            self.root.bind('<Button-2>', self.applica_con)
        self.root.mainloop()
               
    def resize(self, event):
        self.shape = (event.width,event.height)
        #self.root.geometry(str(self.shape[0])+'x'+str(self.shape[1]))
        self.W = self.shape[0] / self.grid[1]
        self.H = self.shape[1] / self.grid[0]
        # self.canvas.bind("<B1-Motion>", self.gestisci_movimento_mouse)
        self.disegna()
            
    def disegna(self):
        self.canvas.delete("all")
        for i,H in enumerate(self.hasses):
            row = i // self.grid[1]
            col = i % self.grid[1]

            # Disegna linee
            for i,(a,b) in enumerate(H.vertex):
                if H.vertex_color[i] != 'black': #Diverso spessore
                    self.canvas.create_line(((col + H.nodes[a][0]) * self.W, (row + H.nodes[a][1]) * self.H),
                                            ((col + H.nodes[b][0]) * self.W, (row + H.nodes[b][1]) * self.H),
                                            width = 2, fill = H.vertex_color[i]
                                            )
                else:
                    self.canvas.create_line(((col + H.nodes[a][0]) * self.W, (row + H.nodes[a][1]) * self.H),
                                            ((col + H.nodes[b][0]) * self.W, (row + H.nodes[b][1]) * self.H),
                                            width = 1, fill = H.vertex_color[i]
                        )
            
            # Disegna cerchi
            for i,(fx,fy) in enumerate(H.nodes):
                X = (col + fx) * self.W #X del cerchio
                Y = (row +fy) * self.H #Y del cerchio
                self.canvas.create_oval((X - H.r, Y - H.r),
                                        (X + H.r, Y + H.r),
                                        fill = H.nodes_color[i])
                
            # Aggiungi etichette
                if self.show_labels:
                    self.canvas.create_text(X,
                                            Y +  H.r*2 + H.font_size/2 ,
                                            font=f"Times {H.font_size}", text=H.labels[i])
                     
    def gestisci_movimento_mouse(self, evento):
        """Funzione per gestire il movimento del mouse"""
        # Individua punto nella griglia e conseguentemenete Hasse di riferimento
        row = int(evento.y  // self.H)
        col = int(evento.x  // self.W)
        hasse_index = row*self.grid[1] + col

        # relativizza posizione del mouse nel riquadro di interesse nella griglia 
        mouse_x = evento.x % (self.shape[0] / self.grid[1])
        mouse_y = evento.y % (self.shape[1] / self.grid[0])
        
        
        # Trova cerchio
        cerchio_selezionato = None
        for i,node in enumerate(self.hasses[hasse_index].nodes):
            node_x, node_y = node[0] * self.W, node[1] * self.H
            distanza_q = ((mouse_x - node_x)**2 + (mouse_y - node_y)**2)
            if distanza_q <= self.hasses[hasse_index].r ** 2 * 2:
                cerchio_selezionato = i
                break

        # Se un cerchio è stato selezionato, aggiorna la sua posizione
        if cerchio_selezionato != None:
          self.hasses[hasse_index].nodes[cerchio_selezionato] = (mouse_x / self.W, self.hasses[hasse_index].nodes[cerchio_selezionato][1])
          #self.hasses[hasse_index].nodes[cerchio_selezionato]
          self.disegna()
   
    def show_con(self, evento):
        row = int(evento.y  // self.H)
        col = int(evento.x  // self.W)
        hasse_index = row*self.grid[1] + col
        if hasse_index == 0:
            # Vogliamo farlo solo per CONL che è hasses[1]!!
            return
        # relativizza posizione del mouse nel riquadro di interesse nella griglia 
        mouse_x = evento.x % (self.shape[0] / self.grid[1])
        mouse_y = evento.y % (self.shape[1] / self.grid[0])
        
        # Trova cerchio
        cerchio_selezionato = None
        for i,node in enumerate(self.hasses[hasse_index].nodes):
            node_x, node_y = node[0] * self.W, node[1] * self.H
            distanza_q = ((mouse_x - node_x)**2 + (mouse_y - node_y)**2)
            if distanza_q <= self.hasses[hasse_index].r ** 2 * 2:
                cerchio_selezionato = i
                break

            
        # Se un cerchio è stato selezionato, mostra la relativa Congruenza
        if cerchio_selezionato != None: # figa e lo 0??
            self.hasses[0].show_congruence(self.hasses[1][cerchio_selezionato])
            self.disegna()
 
    def show_all_irriducible(self, skip):
        for h in self.hasses:
            h.show_irriducible()
        self.disegna()
        
    def reset(self, skip):
        for h in self.hasses:
            h.get_hasse_variables()
        self.disegna()
        
    def identifica_punto(self,x,y):
        """
        funzione che dalla x e dalla y del mouse restituisce l'indice del poset di riferimento e del punto di riferimento
        lo farl in futuro
        """
        row = int(y  // self.H)
        col = int(x  // self.W)
        hasse_index = row*self.grid[1] + col

        # relativizza posizione del mouse nel riquadro di interesse nella griglia 
        mouse_x = x % (self.shape[0] / self.grid[1])
        mouse_y = y % (self.shape[1] / self.grid[0])
        
        # Trova cerchio
        cerchio_selezionato = None
        for i,node in enumerate(self.hasses[hasse_index].nodes):
            node_x, node_y = node[0] * self.W, node[1] * self.H
            distanza_q = ((mouse_x - node_x)**2 + (mouse_y - node_y)**2)
            if distanza_q <= self.hasses[hasse_index].r ** 2 * 2:
                cerchio_selezionato = i
                return hasse_index, cerchio_selezionato

    def applica_con(self, evento):
        hasse_index,punto = self.identifica_punto(evento.x, evento.y)

        L = self.hasses[0].apply_congruence(self.hasses[hasse_index][punto])
        ConL = L.CongruenceLattice()

        L.get_hasse_variables()
        ConL.get_hasse_variables()
        
        self.hasses = [L,ConL]

        self.disegna()
        
    def show_upset(self,evento):
        hasse,punto = self.identifica_punto(evento.x,evento.y)
        self.hasses[hasse].show_nodes(self.hasses[hasse].upset(punto), 'red')    
        self.disegna()
    
    def show_downset(self,evento):
        hasse,punto = self.identifica_punto(evento.x,evento.y)
        self.hasses[hasse].show_nodes(self.hasses[hasse].downset(punto), 'red')  
        self.disegna()

    def save(self,evento):
        """
        Salva il contenuto del canvas come immagine PNG.

        Args:
          canvas: L'oggetto canvas Tkinter.
          filename: Il nome del file PNG da salvare.
        """
        self.canvas.postscript(file=f"PythonStuff/pyLattice/img/{self.title}.eps", colormode='color')
        
    def capture_window(self,evento):
        """
        Questa funzione mi serve letteralmente solo e soltanto per effettuare uno screensshot della finestra
        """
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()    #get details about window
        print(height,self.shape[1])
        
        takescreenshot = ImageGrab.grab(bbox=(x, y,x+ width,y+height))
        takescreenshot.save(f"PythonStuff/pyLattice/img/{self.title}.png")
# DataSet annd cluster class
class DataSet():
    def __init__(self, Lat:Lattice, freq, fuzzy_domination_function = 'BrueggemannLerche', t_norm_function = 'prod', t_conorm_function = None):
        """
        Un dataset è un reticolo ma con associata una distribuzione di frequenza per ogni punto.

        """
        assert len(freq) == len(Lat)
        self.L = Lat
        self.f = freq
        
        #Fuzzy dom
        if fuzzy_domination_function == 'BrueggemannLerche':
            self.fuz_dom = self.BrueggemannLerche()
            
        elif callable(fuzzy_domination_function):
            self.fuz_dom = fuzzy_domination_function(self.L)
            
        # T Norm
        if t_norm_function == 'prod':
            self.t_norm_func = lambda a,b: a*b
            self.t_conorm_func = lambda a,b: a+b - a*b
            
        elif t_norm_function == "min":
            self.t_norm_func = lambda a,b: min(a,b)
            self.t_conorm_func = lambda a,b: max(a,b)
            
        elif t_norm_function == 'hamacher':
            self.t_norm_func = lambda a,b: (a*b)/(a+b-a*b) if (a!=0 or b!=0) else 0
            self.t_conorm_func = lambda a,b: (a+b)/(1+a*b) #Einstein sum
  
        elif callable(t_norm_function):
            self.t_norm_func = t_norm_function
            self.t_conorm_func = lambda a,b: 1-self.t_norm_func(1-a,1-b)
            
        # T_conorm function
        if callable(t_conorm_function):
            self.t_conorm_func = t_conorm_function


        self.sep = self.compute_separation()
        
    # funzioni di fuzzy dominanza
    def BrueggemannLerche(self):
        fuz_dom = [[0 for i in range(len(self.L))] for j in range(len(self.L))] ###Strict dom (poi magari ne discutiamo)
        for i in range(len(self.L)):
            for j in range(i+1,len(self.L)):
                if self.L.domination_matrix[i][j]:
                    fuz_dom[i][j] = 1
                    fuz_dom[j][i] = 0
                elif self.L.domination_matrix[j][i]:
                    fuz_dom[i][j] = 0
                    fuz_dom[j][i] = 1
                else:
                    num_ij = len(self.L.index_upset(i, strict=True)  - self.L.index_upset(j, strict=True)) + 1
                    den_ij = len(self.L.index_downset(i, strict=True)  - self.L.index_downset(j,  strict=True)) + 1
                    a_ij = num_ij / den_ij
                    
                    num_ji = len(self.L.index_upset(j, strict = True)  - self.L.index_upset(i, strict = True)) + 1
                    den_ji =len(self.L.index_downset(j, strict = True) - self.L.index_downset(i, strict = True)) + 1
                    a_ji = num_ji / den_ji
                    
                    d_ij = a_ij / (a_ij + a_ji)
                    fuz_dom[i][j] = d_ij
                    fuz_dom[j][i] = 1 - d_ij
        return fuz_dom
         
    ## Costruire matrice di separation come 1 + \sum inb_{ikj}
    def in_beetwen(self, a,k,b):
        """
        Calcola la in_beetwen a < k < b
        """
        return self.t_conorm_func(
            self.t_norm_func(self.t_norm_func(self.fuz_dom[a][b],self.fuz_dom[a][k]),self.fuz_dom[k][b]),
            self.t_norm_func(self.t_norm_func(self.fuz_dom[b][a],self.fuz_dom[k][a]),self.fuz_dom[b][k])
        )
    
    def compute_separation(self):
        """
        Calcola la separation nel dataset, per ora è ottimizzata ma 
        In teoria sò già che sep_{ii} = 0, e che sep_{ij} = 1 - sep_{ji}
        """
        separation = [[0 for i in range(len(self.L))] for j in range(len(self.L))]
        for i in range(len(self.L)):
            for j in range(i+1,len(self.L)):
                sep = 1
                for k in range(len(self.L)):
                    sep += self.in_beetwen(i,k,j)
                separation[i][j] = sep
                separation[j][i] = sep
        if False:
            # Quella che segue è la versione di separation senza nessuna ottimizzazione teorica, ovvero:
            # - non assumo a priori che sep_ii = 0
            # - non assumo a priori che sep_ij = sep_ji
            # può essere molto utile per verificare che le funzioni che utilizzo rispettino certe premesse
            for i in range(len(self.L)):
                for j in range(len(self.L)):
                    sep = self.fuz_dom[i][j] + self.fuz_dom[j][i]
                    for k in range(len(self.L)):
                        sep += self.in_beetwen(i,k,j)
                    separation[i][j] = sep
        return separation
    
    def as_partition(con):
        """
        converte una congruenza in una partizione, mi semplifica parecchio i calcoli:
        una congruenza è una lista del tipo L[i] = k --> x_i \in k
        una partizione è una lista di liste P[i] = [i,k]
        """
        diz_indici = {}
        partizione = []
        for i,x in enumerate(con):
            if i == x:
                diz_indici[x] = len(partizione)
                partizione.append([i])
            else:
                partizione[diz_indici[x]].append(i)
        return partizione
            
    # Funzioni di disomogeneità di una partizione
    def total_separation(self,partition):
        """
        La separation totale di una partizione è definita come la somma delle separazioni internee ai gruppi, ovvero:
        sep_g = \sum_{a,b\in G} sep(a,b) * f_a * f_b
        """
        tot_sep = 0
        for gruppo in partition:
            for i,a in enumerate(gruppo):
                for b in gruppo[i+1:]:
                    tot_sep += self.sep[a][b] * self.f[a] * self.f[b]    
        return tot_sep
    
    def max_separation(self,partition):
        tot_sep = 0
        for gruppo in partition:
            sep_max = 0
            for i,a in enumerate(gruppo):
                for b in gruppo[i+1:]:
                    sep_max = max(sep_max, self.sep[a][b]) 
            tot_sep +=  sep_max * len(gruppo)
        return tot_sep
          
    # Support and estetic 
    def show_fuz_dom(self, decimal = 2):
        for riga in self.fuz_dom:
            print(*[f"{r:.{decimal}f}" for r in riga],sep = ' , ')
            
    def show_sep(self, decimal = 2):
        for riga in self.sep:
            print(*[f"{r:.{decimal}f}" for r in riga],sep = ' , ')
        
    def __len__(self):
        return len(self.L)
    
    def __getitem__(self,index):
        return self.L[index]

    def gerarchic_cluster(self, function_sep = "total_separation", irriducible_congru = None):
        """
        Calcoliamo una cluster gerarchica, questo comando restituisce due liste:
        - La prima è la lista di congruenze risultanti dalla cluster gerarchica
        - La seoncda è la lista di separation assocciata ad ogni congruenza
        
        L'algoritmo è valido ma devo formalizzarlo perchè non è totalmente scontato. non sto salendo sopra chi mi copre,
        potrei fare così ma secondo me questo è più efficiente perchè altrimenti dovrei calcolare tutto ConL per trovare chi mi copre
        Il disegno lo fa sembrare facile ma nella pratica è lentissimo
        """
        if function_sep == "total_separation":
            function_sep = lambda par: self.total_separation(par)
            
        elif function_sep == "max_separation":
            function_sep = lambda par: self.max_separation(par)

        else:
            assert callable(function_sep)
        if not irriducible_congru:
            irriducibile_con = self.L.congruenze_join_irriducibili()
        else:
            irriducibile_con = irriducible_congru
        actual_con = [i for i in range(len(self.L))]
        history_con = [actual_con]
        separations = [0]
        while sum(actual_con) != 0:
            best_next_con = None
            min_sep = 0
            for con in irriducibile_con:
                if not confronta_blocchi(con,actual_con):
                    nex_con = unisci_congruenze(con,actual_con)
                    nex_sep = function_sep(DataSet.as_partition(nex_con))
                    if best_next_con:
                        if nex_sep < min_sep:
                            best_next_con = nex_con
                            min_sep = nex_sep
                    else:
                        best_next_con = nex_con
                        min_sep = nex_sep
            actual_con = best_next_con
            history_con.append(actual_con)
            separations.append(min_sep)
        return history_con, separations

    def classic_gerarchic_cluster(self,function_sep = "total_separation"):
        if function_sep == "total_separation":
            function_sep = lambda par: self.total_separation(par)
            
        elif function_sep == "max_separation":
            function_sep = lambda par: self.max_separation(par)
        
        actual_cl = [[i] for i in range(len(self.L))]
        history_con = [actual_cl]
        separations = [0]
        for _ in range(len(self.L)-1):
            min_sep = 0
            best_cl = None
            for i,c1 in enumerate(actual_cl):
                for k,c2 in enumerate(actual_cl[i+1:]):
                    j = k + i + 1
                    next_cl = [c for l,c in enumerate(actual_cl) if l!=i and l!=j] 
                    next_cl.append(c1 + c2)
                    sep = function_sep(next_cl)
                    if best_cl:
                        if sep < min_sep:
                            min_sep = sep
                            best_cl = next_cl
                    else:
                        min_sep = sep
                        best_cl = next_cl
            actual_cl = best_cl
            separations.append(min_sep)
            history_con.append(actual_cl)
            
        return history_con,separations
        
    def estetic_rappresentation(self,gerarchic_cluster = None, function_sep = "total_separation"):
        if function_sep != "total_separation":
            raise ValueError("Non l'ho ancora implementato coglione")
        
        if not gerarchic_cluster:
            gerarchic_cluster = self.gerarchic_cluster(function_sep)[0]
        Con_L = self.L.CongruenceLattice()
        Con_L.get_hasse_variables()
        Con_L.show_percorso([Con_L.obj.index(x) for x in gerarchic_cluster], 'orange')
        if function_sep ==  "total_separation":
            Con_L.labels = [round(self.total_separation(DataSet.as_partition(con)),2) for con in Con_L]

        self.L.get_hasse_variables()
        self.L.labels = [str(_f) for _f in self.f]
        self.L.dinamic_congruences(ConL = Con_L,init = False, shape = (1400,700), show_labels=True)
        
        
def index_wrapper(self,*lista, from_index = False, to_index = False, func):
    if from_index and to_index:
        return self.func(*lista)

    elif from_index:
        return [self[x] for x in self.func(*lista)]
    
    elif to_index:
        return self.func(self.obj.index[x] for x in lista)
    
    else:
        return [self[x] for x in self.func(self.obj.index[x] for x in lista)]
       
class CWDataSet(DataSet):
    
    def __init__(self, cw, freq, fuzzy_domination_function = 'BrueggemannLerche', t_norm_function = 'prod', t_conorm_function = None):
        """
        Un dataset è un reticolo ma con associata una distribuzione di frequenza per ogni punto.

        """
        self.L = CW(*cw)
        
        assert len(freq) == len(self.L)
        self.f = freq
        
        #Fuzzy dom
        if fuzzy_domination_function == 'BrueggemannLerche':
            self.fuz_dom = self.BrueggemannLerche()
        
        elif fuzzy_domination_function == 'LLEs':
            self.fuz_dom = self.LLEs()
            
        elif callable(fuzzy_domination_function):
            self.fuz_dom = fuzzy_domination_function(self.L)
            
        # T Norm
        if t_norm_function == 'prod':
            self.t_norm_func = lambda a,b: a*b
            self.t_conorm_func = lambda a,b: a+b - a*b
            
        elif t_norm_function == "min":
            self.t_norm_func = lambda a,b: min(a,b)
            self.t_conorm_func = lambda a,b: max(a,b)
            
        elif t_norm_function == 'hamacher':
            self.t_norm_func = lambda a,b: (a*b)/(a+b-a*b) if (a!=0 or b!=0) else 0
            self.t_conorm_func = lambda a,b: (a+b)/(1+a*b) #Einstein sum
  
        elif callable(t_norm_function):
            self.t_norm_func = t_norm_function
            self.t_conorm_func = lambda a,b: 1-self.t_norm_func(1-a,1-b)
            
        # T_conorm function
        if callable(t_conorm_function):
            self.t_conorm_func = t_conorm_function


        self.sep = self.compute_separation()
        
    def BrueggemannLerche(self):
        fuz_dom = [[0 for i in range(len(self.L))] for j in range(len(self.L))] ###Strict dom (poi magari ne discutiamo)
        for p in range(len(self.L)):
            c_up_p = product([k - p_i   for k, p_i in zip(self.L.cw, self.L[p])]) # fuori dal ciclo risparmio ancora di più
            c_down_p  = product([p_i + 1 for p_i in self.L[p]])  
            for q in range(p+1,len(self.L)):
                valore_p = self.L[p] # per il debug
                valore_q = self.L[q] # per il debug
                if self.L.domination_matrix[p][q]:
                    fuz_dom[p][q] = 1
                    fuz_dom[q][p] = 0
                elif self.L.domination_matrix[q][p]:
                    fuz_dom[p][q] = 0
                    fuz_dom[q][p] = 1
                else:
                    c_up_pq = product([k - max(p_i,q_i)  for k, p_i, q_i in zip(self.L.cw, self.L[p], self.L[q])])
                    up_pq = c_up_p - c_up_pq
                    
                    c_down_pq = product([min(p_i,q_i) + 1 for p_i,q_i in zip(self.L[p], self.L[q])])
                    down_pq = c_down_p - c_down_pq
                    
                    
                    c_up_q = product([k - q_i  for k, q_i in zip(self.L.cw, self.L[q])]) 
                    up_qp = c_up_q - c_up_pq
                    
                    c_down_q  = product([q_i + 1 for q_i in self.L[q]]) 
                    down_qp = c_down_q - c_down_pq
                    
                    a_pq = up_pq / down_pq
                    a_qp = up_qp / down_qp
                    d_pq = a_pq / (a_pq + a_qp)
                    fuz_dom[p][q] = d_pq
                    fuz_dom[q][p] = 1 - d_pq
        return fuz_dom      
    
    def LLEs(self):
        """
        Solo per reticoli CW, infatti dovrei spostarlo
        """
        fuz_dom = [[0 for i in range(len(self.L))] for j in range(len(self.L))] ###Strict dom (poi magari ne discutiamo)
        k = len(self.L[0])
        
        if True:
            for i,a in enumerate(self.L):
                for _,b in enumerate(self.L[i+1:]):
                    j = _ + i + 1
                    k1 = sum([1 for x,y in zip(a,b) if x < y])
                    k2 = sum([1 for x,y in zip(a,b) if x == y])
                    
                    fuzzy_dom_ab = 0
                    for s in range(k2 + 1):
                        primo_termine = product(range(k2 - s + 1, k2 + 1))
                        secondo_termine = product(range(k-s,k))
                        fuzzy_dom_ab += primo_termine/secondo_termine
                    fuzzy_dom_ab *= k1/k
                    fuz_dom[i][j] = fuzzy_dom_ab
                    fuz_dom[j][i] = 1 - fuzzy_dom_ab
        else:
            # Versione estesa
            for i,a in enumerate(self.L):
                for j,b in enumerate(self.L):
                    if i == j :
                        continue
                    k1 = sum([1 for x,y in zip(a,b) if x < y])
                    k2 = sum([1 for x,y in zip(a,b) if x == y])
                    
                    fuzzy_dom_ab = 0
                    for s in range(k2 + 1):
                        primo_termine = product(range(k2 - s + 1, k2 + 1))
                        secondo_termine = product(range(k-s,k))
                        fuzzy_dom_ab += primo_termine/secondo_termine
                    fuzzy_dom_ab *= k1/k
                    fuz_dom[i][j] = fuzzy_dom_ab
                    
        return fuz_dom
   
"""
SFIDE FUTURE
 1. [ ] Uniformare tutte le funzioni. probabilmente si può fare in maniera intelligente con i wrapper, quello che è importante però è questo:
    - Non devo avere funzioni diverse per fare le cose in base all'indice o all'oggetto. Devonono solo essere parametri
 5. [ ] Migliorare l'aspetto grafico:
    Non devo avere funzioni complesse ed illegibili, dovrei poter fare questa cosa
    - [ ] Una cazzo di griglia costumizzabile dai... L'equivalente di subplots in matplot lib per multigrafici
    - [ ] Funzioni per evidenziare un insieme di punti o edge:
        Non devo avere la funzione apposta per evidenziare una congruenze, semplicemente devo calcolare 
        gli edge che la riguardano e passarli ad una funzione del tipo _evidenzia_edges(edges, color =(255,0,0), weight = 3_ 
        
        Analogalmente con i punti.
        
        Questo renderebbe incredibilmente semplice, elegante e divertente giocare con subset, elementi join-dense, catene etc. etc.

    - [ ]Studiare un cazzo di algoritmo (mi suiciderò prima di farlo) che ottimizzi la grafica di un poset
        Riordinare i punti in maniera tale di avere meno sovrapposizioni possibili e edges più corti possibili
        
    - Upgradare l'algoritmo. So che c'è una mappa per gli elementi join-irriducibili in L to gli elementi join irriducibibli in ConL
        Devo eseguire i seguenti due step ma dopo credo (cioè è ovvio) sia più conveniente passare a questo metodo:
        - Accertarmi che la mia tecnica per trovare gli elementi join irriducibili sia corretta
        - Identificare gli step per ottenere ConL dai suoi elementi join irriducibili.
            Ovvero, esiste un modo migliore che prendere tutti i suoi possibili sottoinsiemi?
            L'algoritmo che ho studiato ora funziona
            
6. [x] Implementare Dedekind Completetion
    - [ ]  impmlementarlo stepwise invece che stupi one...
    
7. definire altre operazioni tra PoSet e Lattices.
    - [ ] PoSet: glued sum verificando che abbiano massimo e minimo
    - [ ] test di verifica di isomorfismi ed omomorfismi (sarebbe carino sfruttare funzioni built in come __is__) 
    - [ ] Potrebbe essere carino (ma non particolarmente essenziale) definire __floordiv__ per calcolare Reticoli quoziente: L // theta = ...
    
8. ottimizzare cluster:
    - Una volta dimostrato che ConL è colo l'insieme di possibili gap da rimuovere posso calcolare con L con molta più semplicità
Problema teorico:
Sò che |C_4 X C_3| = 12. ed in generale che il reticolo CW ottenuto come 
prodotto di n catene di elementi k_1, k_2, ..., k_n  = k_1 * k_2 ... k_n

Quanto è invece |ConL(C_4 X C_3)|  ed in generale |ConL(\Pi_{i=o}^n C_{k_i})| ?
Segue direttamente da: a cosa è siomorfo ConL(C_4 X C_3)?
C'è un legame tra ConL(C_4 X C_3) e ConL(C_4) X ConL(C_3)... spoiler sono uguali, ma va dimostrato
A questo punto diventa tutto più semplice (credo) 

S_n x S_m = S_{n*m}

Dato che ConL(C_n) == S_n
|ConL(C_n)| = |S_n| = 2**n

|ConL(C_n) x ConL(C_n)| = |S_n| = 2**n

Devo lavorare solo ad un interfaccia grafica!
In maniera intelligente, su un file nuovo, una nuova classe

"""
