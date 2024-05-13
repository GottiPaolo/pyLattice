import numpy as np
from p5 import *
import tkinter as tk
#### Hasse
dinamic_congruence = False

def mappa(x,a,b,A,B):
    """
    Funzione per convertire in maniera lineare un valore x assunto in un range (a,b) in un valore in range (A,B)
    Secondo la formual : (x-a)/(b-a) = (X-A)/(B-A) --> X = (x-a)/(b-a)*(B-A)+A
    
    """
    if a==b:
        return (A+B)/2
    return (x-a)/(b-a)*(B-A)+A

def get_riga_punto(cover_matrix,p,righe):
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

def converti(riga,colonna,r,righe,min_x,max_x,min_y,max_y, hasse_mode = 0):
    """
    funzoine per convertire i punti da righe e colonna discretizzate a coordinate nella finestra
    """
    if hasse_mode == 0:
        y = mappa(riga,0,max(righe),min_y+r*2,max_y-r * 2)
        x = mappa(colonna,-1,righe.count(riga),min_x-r*2,max_x+r*2)
        
    elif hasse_mode == 1:
        y = mappa(riga,0,max(righe),min_y+r*2,max_y-r * 2)
        x = mappa(colonna,-1,max(righe),min_x-r*2,max_x+r*2)
        
    elif hasse_mode == 2:
        max_n_righe = max([righe.count(r) for r in righe])
        y = mappa(riga,0,max(righe),min_y+r*2,max_y-r * 2)
        x = max_x/2 + (colonna - righe.count(riga)//2)*(max_x-min_x)/max_n_righe
        
    elif hasse_mode == 3:
        max_n_righe = max([righe.count(r) for r in righe])
        y = mappa(riga,0,max(righe),min_y+r*2,max_y-r * 2)
        x = max_x/2 + (colonna - righe.count(riga)//2 +((righe.count(riga)+1)%2)*0.5 )*(max_x-min_x)/(max_n_righe)
    return x,y
     
def get_coor(righe,colonne,r,min_x,max_x,min_y,max_y):
    """
    Dai dati elementari di un PoSet (righe, colonne e margini della finestra)
    restituiscee un dizionario con le coordinate dei punti
    """
    dizCoor = {}
    for i,(riga,colonna) in enumerate(zip(righe,colonne)):
        dizCoor[i] = converti(riga,colonna,r,righe,min_x,max_x,min_y,max_y)
    return dizCoor

def PoSet_to_show(*PoSet):
    """
    Funzione che globalizza i dati dei PoSet da mostrare
    WIDTH, HEIGHT non sono utilizzati solo perchè sono un pirla (o forse c'era un motivo)
    La griglia è calcolata per essere alta due e lunga n//2 escluso il caso in cui vengano passati due PoSet, in quel caso
    Sono affiancati orizzontalemnte
    """
    global PoSets, Griglia, WIDTH, HEIGHT
    PoSets = PoSet
    if len(PoSet) > 2:
        Griglia = ((len(PoSet)+1)//2 , 2)
    else: 
        Griglia = (len(PoSet) , 1)

        
    WIDTH, HEIGHT = 500,500

def get_dati(Pi,min_x,max_x,min_y,max_y):
    """
    Funzione compatta per ottenere tutti i dati da un PoSet ed i margini della finestra in cui mostrarlo
    """
    righe = get_righe(Pi.cover_matrix)
    colonne = get_colonne(righe)
    radius = min(((max_y-min_y))/(max(righe)+1),(max_x-min_x)/(max(colonne)+1))
    radius *= 0.5 * 0.8
    t_size = radius *0.5 # *0.3
    dizCoor = get_coor(righe,colonne,radius,min_x,max_x,min_y,max_y)
    return radius, t_size, dizCoor

def rappresenta(Pi):
    """
    Funzione che rappresenta un PoSet partando dal dizionario globalizzato dei dati dizPi
    """
    radius, t_size, dizCoor = dizPi[Pi]
    for p in range(len(Pi.cover_matrix)):
        for b in range(len(Pi.cover_matrix)):
            if Pi.cover_matrix[p][b]:
                if not Pi.blocchi:
                    stroke(255)
                    strokeWeight(1)
                    line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                elif Pi.blocchi[p] == Pi.blocchi[b]:
                    stroke(255,0,0)
                    strokeWeight(3)
                    line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                else:
                    stroke(255)
                    strokeWeight(1)
                    line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                    
    for p in range(len(Pi.cover_matrix)):
        noStroke()
        fill(170)
        ellipse(dizCoor[p][0],dizCoor[p][1],radius,radius)
        fill(220,0,0)
        text_size(t_size)
        text(Pi.labels[p],dizCoor[p][0]-(len(Pi.labels[p])//4*t_size),dizCoor[p][1]-radius/2)

def setup():
    """
    Funzione di base di p5 dei calcoli da fare per generare la finestra
    """
    global dizPi, selected, WIDTH, HEIGHT
    background(0)
    size(WIDTH, HEIGHT)
    dizPi = {}
    selected = False
    for i,Pi in enumerate(PoSets):    
        min_x = (i %  Griglia[0]) * width / Griglia[0] 
        min_y = (i //  Griglia[0]) * height / Griglia[1] 
        max_x = min_x + width / Griglia[0] 
        max_y = min_y + height / Griglia[1] 
        #radius, t_size, dizCoor = get_dati(Pi.cover_matrix,min_x,min_x+500,min_y,min_y+500)
        dizPi[Pi] = get_dati(Pi,min_x,max_x,min_y, max_y)
        rappresenta(Pi)

def draw():
    global selected, dinamic_congruence
    """
    Funzione di base di p5 che defiinisce il loop dell'animazione
    """
    background(0)
    for Pi in PoSets:
        rappresenta(Pi)

    ### MUOVI IN MANIERA DINAMICA
    if mouse_is_pressed:
        griglia_x = mouse_x // (width / Griglia[0])
        griglia_y = mouse_y // (height / Griglia[1])
        indice = int(griglia_y*Griglia[0] + griglia_x)
        for p in range(len(dizPi[PoSets[indice]][2])):
            if dist((mouse_x,mouse_y),dizPi[PoSets[indice]][2][p]) * 2< dizPi[PoSets[indice]][0]:
                noFill()
                strokeWeight(4)
                stroke(255,0,0)
                ellipse(*dizPi[PoSets[indice]][2][p], 
                        dizPi[PoSets[indice]][0],dizPi[PoSets[indice]][0])
                dizPi[PoSets[indice]][2][p] = (mouse_x,dizPi[PoSets[indice]][2][p][1])
                break
        
    if dinamic_congruence:
        for i,c in enumerate(PoSets[1]):
            if dist((mouse_x,mouse_y),dizPi[PoSets[1]][2][i]) * 2 < dizPi[PoSets[1]][0]:
                PoSets[0].blocchi = c #Questa struttura non mi piace, devo separare la rappresentazione dalla variabile.
                #i blocchi non devono essere un'entità del PoSet!
      
def mouse_pressed():
    """
    funzione di p5 da azionare quando premo il mouse
    la uso solo per applicare le congruenze
    """
    global PoSets, WIDTH, HEIGHT, dizPi, selected
    if dinamic_congruence and mouse_button == RIGHT and PoSets[0].blocchi:
        Pi = PoSets[0].apply_congruence(PoSets[0].blocchi)
        ConL = Pi.CongruenceLattice()
        PoSets = (Pi, ConL)
        WIDTH, HEIGHT = width / 2, height / 2
        # Duplico il contenuto di setup perchè per ora non ho modi migliori, ma non va bene. 
        # Ci deve essere un modo intelligente per chiamarlo. Ho pure creato le variabili WIDTH, HEIGHT apposta
        dizPi = {}
        selected = False
        for i,Pi in enumerate(PoSets):    
            min_x = (i %  Griglia[0]) * width / Griglia[0] 
            min_y = (i //  Griglia[0]) * height / Griglia[1] 
            max_x = min_x + width / Griglia[0] 
            max_y = min_y + height / Griglia[1] 
            #radius, t_size, dizCoor = get_dati(Pi.cover_matrix,min_x,min_x+500,min_y,min_y+500)
            dizPi[Pi] = get_dati(Pi,min_x,max_x,min_y, max_y)
            rappresenta(Pi)

def hasse_diagram(cover_matrix, shape:tuple = None, radius = None, hasse_mode = 2, title = 'PoSet'):
    """
    Crea una finestra tk-inter con il diagramma di hasse non dinamico di un poset.
    """
    if shape:
        WIDTH,HEIGHT = shape
    else:
        WIDTH,HEIGHT = 500,500
        
    if radius:
        RADIUS = radius
    else:
        RADIUS = 5 #troverò un metodo migliore
    righe = get_righe(cover_matrix)
    colonne = get_colonne(righe)
    coordinate = [converti(r,c,RADIUS,righe,0,WIDTH,0,HEIGHT,hasse_mode = hasse_mode) for i,(r,c) in enumerate(zip(righe,colonne))]

    #Crea finestra
    root = tk.Tk()
    root.geometry(str(WIDTH)+'x'+str(HEIGHT))
    root.title('PoSet')
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
    canvas.pack(anchor=tk.CENTER, expand=True)

    for i, riga in enumerate(cover_matrix):
        for j, value in enumerate(riga):
            if value:
                canvas.create_line(coordinate[i],coordinate[j])

    for x,y in coordinate:
        canvas.create_oval((x - RADIUS, y - RADIUS),
                           (x + RADIUS, y + RADIUS),
                           fill = 'grey')


    
    root.mainloop()


#### Congruence Function
def unisci(a,b,blocchi):
    """
    Unisce due elementi di una congruenza, 
    Ricordiamo che per come sto strutturando le congruenze le seguenti due sono identiche:
    [0,1,0,1,2]
    [0,2,0,2,1]
    Poichè l'elemente della lista indica il gruppo di appartenenza, l'indice della lista indica l'elemento di riferimento
    Per evitare di avere congruenze concettualmente identiche ma sostanzialmente differenti (dato che poi devo anche confrontarle)
    Faccio sì che si propaghino in maniera costante, ovvero quando ne unisco due mantengo sempre il più piccolo 
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
    
    studiando la matematica dietro la struttura che sto utilizzando probabilmente posso renderlo più efficiente.
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
    Ricordiamo che per come sto strutturando le congruenze le seguenti due sono identiche:
    [0,1,0,1,2]
    [0,2,0,2,1]
    Poichè l'elemente della lista indica il gruppo di appartenenza, l'indice della lista indica l'elemento di riferimento
    Per evitare di avere congruenze concettualmente identiche ma sostanzialmente differenti (dato che poi devo anche confrontarle)
    Faccio sì che si propaghino in maniera costante, ovvero quando ne unisco due mantengo sempre il più piccolo 
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

def matrix_from_sparse(sparse,n):
    matrix = [[0 for i in  range(n)] for j in range(n)]  
    for i,j in sparse:
        matrix[i][j] = 1
    return matrix
 
def component_wise(d1,d2):
    one_win = False
    for a,b in zip(d1,d2):
        if b<a:
            return False
        elif b>a:
            one_win = True
    return one_win

def genera_cw(lista):

    if len(lista) == 1:
        return [(i,) for i in range(lista[0])]
        
    risultato = []
    for i in range(lista[0]):
        for sotto_risultato in genera_cw(lista[1:]):
            risultato.append((i,) + sotto_risultato)
        
    return risultato

#### PoSet Class
class PoSet:
    def __init__(self,domination_matrix, X = None, labels = None, blocchi = None):
        """
        Crea un bel PoSet:
        - domination_matrix: Matrice di dominanze
        - X elenco di oggetti, se non passatti verrano usati numeri progressivi
        - Labels: etichette da mostrare nella rappresentazione del poset, se non specificare verrà utilizzato la stringa degli oggeti
        - blocchi = indicare se si vuole evidenziare nella rappresentazione una particolare equivalenza
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
            
        if labels:
            self.labels = labels
        else:
            self.labels = [str(x) for x in self.obj]
            
        self.cover_matrix = self.domination_matrix - np.eye(len(domination_matrix)) - np.where((self.domination_matrix - np.eye(len(domination_matrix))) @ (self.domination_matrix - np.eye(len(domination_matrix))) > 0,1,0)
        self.blocchi = blocchi

    def domination(self,a,b):
        """
        return TRUE if a > b
                False if not
        """
        return bool(self.domination_matrix[self.obj.index(b)][self.obj.index(a)])
    
    def cover(self,a,b):
        """
        return TRUE if a cover b
                False if not
        """
        return bool(self.cover_matrix[self.obj.index(b)][self.obj.index(a)])

    def upset(self,*a):
        """
        Calcola l'upset di un insieme di elementi del poset
        restitusce l'insieme degli elementi che dominano tutti quelli passati
        """
        if len(a) == 1:
            index_a = self.obj.index(a[0]) 
            upset = {self.obj[i] for i,r in enumerate(self.domination_matrix[index_a]) if r }
            return upset
        else:
            return self.upset(a[0]) & self.upset(*a[1:])
    
    def downset(self,*a):
        """
        Calcola il downset di un insieme di elementi del poset
        restitusce l'insieme degli elementi che sono dominati tutti quelli passati
        """
        if len(a) == 1:
            index_a = self.obj.index(a[0])
            downset = { self.obj[i] for i,r in enumerate(self.domination_matrix) if r[index_a] }
            return downset
        else:
            return self.downset(a[0]) & self.downset(*a[1:])
        
    def max_sub_set(self,set):
        """
        Restituisce l'insieme degli elementi che non sono dominati in un sottoinsieme degli elementi
        """
        set = list(set)
        upper = []
        for x in set:
            index_x = self.obj.index(x)
            up = True
            for y in set:
                index_y = self.obj.index(y)
                if index_y != index_x and self.domination_matrix[index_x][index_y]:
                    up = False
                    break
            if up:
                upper.append(x)
        return upper
        
    def min_sub_set(self,set):
        """
        Restituisce l'insieme degli elementi che sono dominati da tutti gli altri elementi di un sottoinsieme
        """
        set = list(set)
        downer = []
        for x in set:
            index_x = self.obj.index(x)
            down = True
            for y in set:
                index_y = self.obj.index(y)
                if index_y != index_x and self.domination_matrix[index_y][index_x]:
                    down = False
                    break
            if down:
                downer.append(x)
        return downer
        
    def join(self,*args, force = False):
        """
        calcla il join di due o più elementi, ovver il più piccolo elemento che li domina entrambi
        Se il join non è definito viene restituito
        se il parametro _force_ è True allora viene restituita una lista vuota se non esitte, 
        oppure contenente i possibili valori se non è unico
        
        Nel caso _force_ non venga specificato ed il join non è definito viene restituito un errore
        """
        min_up_set = self.min_sub_set(self.upset(*args))
        if len(min_up_set) == 1:
            return min_up_set[0]
        elif force:
            return min_up_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
        else: 
            raise ValueError("join non definito") #devo guardare come si creano gli errori
        
    def meet(self, *args, force = False):
        """
        calcla il meet di due o più elementi, ovver il più grande elemento che dominato da entrambi
        Se il meet non è definito viene restituito
        se il parametro _force_ è True allora viene restituita una lista vuota se non esitte, 
        oppure contenente i possibili valori se non è unico
        
        Nel caso _force_ non venga specificato ed il meet non è definito viene restituito un errore
        """
        max_down_set = self.max_sub_set(self.downset(*args))
        if len(max_down_set)==1:
            return max_down_set[0]
        elif force:
            return max_down_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
        else:
            raise ValueError("meet non definito") #devo guardare come si creano gli errori #devo differenziare tra "non esiste" e "ambiguo"
        
    def index_upset(self,*a):
        """
        Identica alla funzione upset ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if len(a) == 1: 
            upset = {i for i,r in enumerate(self.domination_matrix[a[0]]) if r }
            return upset
        else:
            return self.index_upset(a[0]) & self.index_upset(*a[1:])
    
    def index_downset(self,*a):
        """
        Identica alla funzione downset ma invece che richiedere un elemento del poset chiede solo il suo indice
        """
        if len(a) == 1:
            downset = {i for i,r in enumerate(self.domination_matrix) if r[a[0]]}
            return downset
        else:
            return self.index_downset(a[0]) & self.index_downset(*a[1:])
        
    def index_max_sub_set(self,set):
        """
        Identica alla funzione max_sub_set ma invece che richiedere un elemento del poset chiede solo il suo indice
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
        
    def rappresenta(*PoSets):
        """
        Funzione per creare la finestra interattiva che rappresenta il poset
        (giuro che le cambiero nome)
        """
        PoSet_to_show(*PoSets)
        #get_dati(self.cover_matrix,list(map(lambda x: str(x),self.obj)))
        run(renderer="skia")
        
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
            raise ValueError("join non definito")
        
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
            raise ValueError("meet non definito")#devo guardare come si creano gli errori #devo differenziare tra "non esiste" e "ambiguo"
    
    def is_lattice(self):
        """
        Verifica che il poset sia un reticolo verificando che esista il join ed il meet per ogni coppia di elementi.
        """
        for i in range(len(self)):
            for j in range(i+1,len(self)):
                try:
                    self.index_join(i,j)
                    self.index_meet(i,j)
                except:
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
            domination_matrix @= cover_matrix
            
        domination_matrix = np.where( domination_matrix > 0, 1, 0)
        
        return PoSet(domination_matrix,X,labels)
    
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
        return PoSet.from_function(sub_set,lambda x,y: self.domination_matrix[self.obj.index(x)][self.obj.index(y)])
        
    def dedekind_completetion(self):
        """
        NON FUNZIONA, Meglio non l'ho ancora implementato, ma a breve, promesso
        """
        # Inizializza il set di tutti i cut del poset
        # Proviamo in maniera ingenua
        cuts = []
        for i in range(len(self)):
            index = 0
            cut_find = False
            down_set = {i}
            up_set = self.index_upset(i)

            while not cut_find:
                if index % 2 == 0:
                    if up_set == {}:
                        down_set_ip = set(range(len(self)))
                    else:
                        down_set_ip = self.index_downset(*list(up_set))
                    if down_set == down_set_ip:
                        cut_find = True
                    down_set = down_set_ip
                    
                else:
                    if down_set == {}:
                        up_set_ip = set(range(len(self)))
                    else:
                        up_set_ip = self.index_upset(*list(down_set))
                    if up_set == up_set_ip:
                        cut_find = True
                    up_set = up_set_ip
                    
                    index +=1
            if up_set not in cuts:     
                cuts.append(up_set)
 
        return PoSet.from_function(cuts, lambda a,b: a>=b)
        
    def hasse(self, shape:tuple = None, radius = None, hasse_mode = 0, title = 'PoSet'):
        #hasse_diagram(self.cover_matrix)
        hasse_diagram(self.cover_matrix,shape,radius,hasse_mode,title)    
     
    def restituiscimi_cover_matrix(self):
        for i,k in enumerate(self.cover_matrix):
            if i ==0 :
                print('[',[int(a) for a in k],',')
                
            elif i != len(self) - 1:
                print([int(a) for a in k],',')
                
            else:
                print([int(a) for a in k],']')
                
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
            domination_matrix @= cover_matrix
            
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
                
        labels = list(map(lambda x:' '.join(map(lambda c:self.labels[c],x)),blocks.values()))
        matrix = np.eye(len(blocks))
        
        for i,v in enumerate(blocks):
            for j,q in enumerate(list(blocks.keys())[i+1:]):
                 for a in blocks[v]:
                     for b in blocks[q]:
                        if self.domination_matrix[a][b]:
                            matrix[i][j+i+1] = 1
                        elif self.domination_matrix[b][a]:
                            matrix[j+i+1][i] = 1

        return Lattice(matrix,labels = labels)
  
    def calcola_congruenza(self,a,b):
        """
        Calcola la più piccola congruenza che unisce a e b
        
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
                            if blocchi[i]==blocchi[k] and blocchi[k]!=blocchi[j]:
                                blocchi = unisci(j,k,blocchi)
                                cambiamenti = True

                            if blocchi[j]==blocchi[k] and blocchi[k]!=blocchi[i]:
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
                            if blocchi[meet_i]!=blocchi[meet_j]:
                                blocchi = unisci(meet_i,meet_j,blocchi)
                                cambiamenti = True
        # self.blocchi = blocchi Può sembrare comoda questa cosa ma mi porta ad un problema:
        # questa funzione la utilizzo OGNI VOLTA che creo ConL, e se lascio questa parte finisce che OGNI VOLTA viene rappresentata una
        # congruenza anche se non voluta
        return blocchi
    
    def congruenze_elementari(self):
        """UFFICIALMENTE DEPRECATO
        Calcola le congruenze che ho definito _elementari_ cioè quelle che uniscono i blocchi a e b, tali che a \prec b
        
        Ora credo di poterlo migliorare passando alle congruenze join_irriducibili
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
        Calcola tutte congruenze combinando quelle elementari (adesso in beta combinando quelle join-irriducibili)
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

    def CongruenceLattice(self, labels = None):
        a = self.all_congruenze()
        if not labels:
            return Lattice.from_function(a,confronta_blocchi,labels = [str(numero_blocchi(c)) for c in a])
        else:
            return Lattice.from_function(a,confronta_blocchi,labels = labels)
        
    def dinamic_congruences(self,labels = None):
        global dinamic_congruence
        dinamic_congruence = True
        self.rappresenta(self.CongruenceLattice(labels))
        dinamic_congruence = False 
        
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
        Componente wise
        """
        return Lattice.from_function(genera_cw(lista),component_wise)
    
    
    """
    SFIDE FUTURE
    1. [x] Sistemare le parentesi nel prodotto di Reticoli / Poset. è una cosa sbatti utile ma problematica 
        - Porta però a creare problemi quando moltiplico reticoli che hanno come oggetti delle tuple, anche se queste non derivano da prodotti
    2. [x] Implementare le funzioni per estrarre gli elementi meet-dense e join-dense
        Dalla teoria risulta che preso a in L: a\in J(L) <==> \exists ! b: b\prec a
        Quindi in realtà se faccio scorrere la matrice di copertura e sommo righe / colonne ottengo meet dense e join dense quando le somme fanno 1 giusto??
    3. [ ] Studiare la rappresentazione. p5 rimane l'opzione migliore come libreria, 
        devo studiare come differenziare diversi Canvas, separare le funzioni etc.
    4. [x] Calcolare il duale: Cosa semplice e veloce in realtà
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
                
    6. [ ] Implementare Dedekind Completetion
            
            
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
    
    """
    