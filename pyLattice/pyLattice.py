import numpy as np
import p5
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

def converti(riga,colonna,r,righe,min_x,max_x,min_y,max_y, hasse_mode = 4):
    """
    funzoine per convertire i punti da righe e colonna discretizzate a coordinate nella finestra
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
     
## p5

def get_coor(righe,colonne,r,min_x,max_x,min_y,max_y,hasse_mode = 4):
    """
    Dai dati elementari di un PoSet (righe, colonne e margini della finestra)
    restituiscee un dizionario con le coordinate dei punti
    """
    dizCoor = {}
    for i,(riga,colonna) in enumerate(zip(righe,colonne)):
        dizCoor[i] = converti(riga,colonna,r,righe,min_x,max_x,min_y,max_y, hasse_mode=hasse_mode)
    return dizCoor

def PoSet_to_show(*PoSet, grid = None, hasse_mode = 4, show_labels = True):
    """
    Funzione che globalizza i dati dei PoSet da mostrare
    WIDTH, HEIGHT non sono utilizzati solo perchè sono un pirla (o forse c'era un motivo)
    La griglia è calcolata per essere alta due e lunga n//2 escluso il caso in cui vengano passati due PoSet, in quel caso
    Sono affiancati orizzontalemnte
    """
    global PoSets, Griglia, WIDTH, HEIGHT, HASSE_MODE, Show_labels
    PoSets = PoSet
    HASSE_MODE = hasse_mode
    if not grid:
        Griglia = (1 , len(PoSet))
    else:
        Griglia = grid
    Show_labels = show_labels
        
    WIDTH, HEIGHT = 500,500

def get_dati(Pi,min_x,max_x,min_y,max_y):
    """
    Funzione compatta per ottenere tutti i dati da un PoSet ed i margini della finestra in cui mostrarlo
    """
    righe = get_righe(Pi.cover_matrix)
    colonne = get_colonne(righe)
    radius = min(((max_y-min_y))/(max(righe)+1),(max_x-min_x)/(max(colonne)+1))
    radius *= 0.4
    t_size = radius *0.5 # *0.3
    if radius > 15:
        radius = 15
    if radius < 7:
        radius = 7
    if t_size < 20:
        t_size = 20
    elif t_size > 40:
        t_size = 40
    dizCoor = get_coor(righe,colonne,radius,min_x,max_x,min_y,max_y, hasse_mode=HASSE_MODE)
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
                    p5.stroke(0)
                    p5.strokeWeight(1)
                    p5.line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                elif Pi.blocchi[p] == Pi.blocchi[b]:
                    p5.stroke(255,0,0)
                    p5.strokeWeight(3)
                    p5.line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                    p5.strokeWeight(1)
                else:
                    p5.stroke(0)
                    p5.strokeWeight(1)
                    p5.line(dizCoor[p][0],dizCoor[p][1],dizCoor[b][0],dizCoor[b][1])
                    
    for p in range(len(Pi.cover_matrix)):
        #p5.noStroke()
        p5.stroke(0)
        p5.fill(130)
        p5.ellipse(dizCoor[p][0],dizCoor[p][1],radius,radius)
        p5.fill(0)
        if Show_labels:
            p5.text_size(t_size)
            p5.text(Pi.labels[p],dizCoor[p][0]-(len(Pi.labels[p])//2*t_size*0.5),
                    dizCoor[p][1]+radius*2+t_size/2)

def setup():
    """
    Funzione di base di p5 dei calcoli da fare per generare la finestra
    """
    global dizPi, selected, WIDTH, HEIGHT
    p5.background(255)
    p5.size(WIDTH, HEIGHT)
    dizPi = {}
    selected = False
    for i,Pi in enumerate(PoSets):    
        min_x = (i %  Griglia[1]) * width / Griglia[1] 
        min_y = (i //  Griglia[1]) * height / Griglia[0] 
        max_x = min_x + width / Griglia[1] 
        max_y = min_y + height / Griglia[0] 
        #radius, t_size, dizCoor = get_dati(Pi.cover_matrix,min_x,min_x+500,min_y,min_y+500)
        dizPi[Pi] = get_dati(Pi,min_x,max_x,min_y, max_y)
        rappresenta(Pi)

def draw():
    global selected, dinamic_congruence
    """
    Funzione di base di p5 che defiinisce il loop dell'animazione
    """
    p5.background(255)
    for Pi in PoSets:
        rappresenta(Pi)

    ### MUOVI IN MANIERA DINAMICA
    if mouse_is_pressed and mouse_button == p5.LEFT:
        griglia_x = mouse_x // (width / Griglia[0])
        griglia_y = mouse_y // (height / Griglia[1])
        indice = int(griglia_y*Griglia[0] + griglia_x)
        for p in range(len(dizPi[PoSets[indice]][2])):
            if p5.dist((mouse_x,mouse_y),dizPi[PoSets[indice]][2][p]) < dizPi[PoSets[indice]][0]:
                p5.noFill()
                p5.strokeWeight(4)
                p5.stroke(255,0,0)
                p5.ellipse(*dizPi[PoSets[indice]][2][p], 
                        dizPi[PoSets[indice]][0],dizPi[PoSets[indice]][0])
                dizPi[PoSets[indice]][2][p] = (mouse_x,dizPi[PoSets[indice]][2][p][1])
                break
        
    if dinamic_congruence:
        for i,c in enumerate(PoSets[1]):
            if p5.dist((mouse_x,mouse_y),dizPi[PoSets[1]][2][i]) * 2 < dizPi[PoSets[1]][0]:
                PoSets[0].blocchi = c #Questa struttura non mi piace, devo separare la rappresentazione dalla variabile.
                #i blocchi non devono essere un'entità del PoSet!
      
def mouse_pressed():
    """
    funzione di p5 da azionare quando premo il mouse
    la uso solo per applicare le congruenze
    """
    global PoSets, WIDTH, HEIGHT, dizPi, selected
    if dinamic_congruence and mouse_button == p5.RIGHT and PoSets[0].blocchi:
        Pi = PoSets[0].apply_congruence(PoSets[0].blocchi)
        ConL = Pi.CongruenceLattice()
        PoSets = (Pi, ConL)
        WIDTH, HEIGHT = width / 2, height / 2
        # Duplico il contenuto di setup perchè per ora non ho modi migliori, ma non va bene. 
        # Ci deve essere un modo intelligente per chiamarlo. Ho pure creato le variabili WIDTH, HEIGHT apposta
        dizPi = {}
        selected = False
        for i,Pi in enumerate(PoSets):    
            min_x = (i %  Griglia[1]) * width / Griglia[1] 
            min_y = (i //  Griglia[1]) * height / Griglia[0] 
            max_x = min_x + width / Griglia[1] 
            max_y = min_y + height / Griglia[0] 
            #radius, t_size, dizCoor = get_dati(Pi.cover_matrix,min_x,min_x+500,min_y,min_y+500)
            dizPi[Pi] = get_dati(Pi,min_x,max_x,min_y, max_y)
            rappresenta(Pi)

# tk
def single_hasse_diagram(cover_matrix, canvas, rect, radius = None, hasse_mode = 4,
                         labels = None, t_size = None):
    if radius:
        RADIUS = radius
    else:
        RADIUS = 5 #troverò un metodo migliore
        
    if t_size:
        fontSize = t_size
    else:
        fontSize = 10
    
    # Lo farò ma quando trovero un modo intelligente. Non a cazzo di cane
    # if not colors:
    #     colors = ['grey' for i in cover_matrix]
    # else:
    #     colors = [("grey", "yellow", "cyan", "magenta", "red", "blue", "black")[i] for i in colors]
               
    righe = get_righe(cover_matrix)
    colonne = get_colonne(righe)
    coordinate = [converti(r,c,RADIUS,righe,*rect,hasse_mode = hasse_mode) for i,(r,c) in enumerate(zip(righe,colonne))]

    for i, riga in enumerate(cover_matrix):
        for j, value in enumerate(riga):
            if value:
                canvas.create_line(coordinate[i],coordinate[j])

    for i,(x,y) in enumerate(coordinate):
        canvas.create_oval((x - RADIUS, y - RADIUS),
                           (x + RADIUS, y + RADIUS),
                           fill = 'grey')
        if labels:
            canvas.create_text(x,y + RADIUS*2 + fontSize/2 ,font=f"Times {fontSize}",
                            text=labels[i])
        
def hasse_diagram(PoSets , grid = None, shape:tuple = None, radius = None, hasse_mode = 2, 
                  title = 'PoSet', labels = False, t_size = None, save_ps = False):
    """
    Crea una finestra tk-inter con il diagramma di hasse non dinamico di un poset.
    """
    if shape:
        WIDTH,HEIGHT = shape
    else:
        WIDTH,HEIGHT = 500,500
        
    if not grid:
        grid = (1,len(PoSets))
    #Crea finestra
    root = tk.Tk()
    root.geometry(str(WIDTH)+'x'+str(HEIGHT))
    root.title(title)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
    canvas.pack(anchor=tk.CENTER, expand=True)
    
    for i,P in enumerate(PoSets):
        riga = i // grid[1]
        col  = i % grid[1]
        if labels:
            single_hasse_diagram(P.cover_matrix,canvas, rect = (col  * WIDTH / grid[1], (col  + 1) * WIDTH / grid[1],
                                                            riga * HEIGHT / grid[0], (riga + 1) * HEIGHT / grid[0]), 
                             radius = radius, hasse_mode = hasse_mode, labels = P.labels, t_size=t_size)
        else:
            single_hasse_diagram(P.cover_matrix,canvas, rect = (col  * WIDTH / grid[1], (col  + 1) * WIDTH / grid[1],
                                                            riga * HEIGHT / grid[0], (riga + 1) * HEIGHT / grid[0]), 
                             radius = radius, hasse_mode = hasse_mode, t_size=t_size)

    if save_ps:
        canvas.postscript(file = f'{title}.ps',colormode = 'color')
    
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
        
        elif len(min_up_set) == 0:
            return None
        
        elif force:
            return min_up_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
        else: 
            return None
            # raise ValueError("join non definito")
        
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
        if len(max_down_set)==0:
            return None
        elif force:
            return max_down_set # devo decidere se restituire lista vuota/multipla nel caso non sia definito il meet, oppure errore
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
        return PoSet.from_function(sub_set,lambda x,y: self.domination_matrix[self.obj.index(x)][self.obj.index(y)])
          
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
            labels = ['' for c in cuts]
            for j in range(len(self)):
                sub = self.index_downset(j)
                for i,c in enumerate(cuts):
                    if c == sub:
                        labels[i] = self.labels[j]
            return Lattice.from_function(cuts,lambda a,b: a<= b, labels=labels)
        return Lattice.from_function(cuts,lambda a,b: a<= b)

    def hasse(*PoSets, grid = None, shape:tuple = None, radius = None, hasse_mode = 3, title = 'PoSet', 
              labels = False, t_size = None, save_ps = False):
        
        hasse_diagram(PoSets, grid = grid, shape = shape, radius = radius, hasse_mode=hasse_mode, title = title, 
                      labels=labels, t_size = t_size, save_ps = save_ps)
                    #  shape,radius,hasse_mode,title)   
        # assert grid[1] * grid[0] >= len(self)
        # for P in PoSets:
        #     hasse_diagram(P.cover_matrix,shape,radius,hasse_mode,title)    
     
    def hasse_p5(*PoSets, grid = None, hasse_mode = 4, labels = True):
        """
        Funzione per creare la finestra interattiva che rappresenta il poset
        (giuro che le cambiero nome)
        """
        PoSet_to_show(*PoSets, grid = grid,hasse_mode = hasse_mode ,show_labels = labels)
        #get_dati(self.cover_matrix,list(map(lambda x: str(x),self.obj)))
        p5.run(renderer="skia",sketch_setup=setup,sketch_draw=draw)
       
     
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
        
    def hasse_coordinate(self,W = 1,H = 1):
        """
        Questa funzione restituisce i dati per rappresentare un diagramma 
        di hasse del poset in una finestra di ampiezza W x H
        
        restituisce due elementi: 
        - _nodes_: Lista tuple con le coordinate dei pallina della finestra [(x_0,y_0), (x_1,y_1),...]
        - _vertex_Lista di tuple dei vertici da collegare : [(0,1), (0,2),...]
        
        
        Voglio trovare un modo intelligente per rendererlo customizzarbile, attualmente il diagramma di hasse è costruito con i seguenti step logici
        - le righe dei punti vengono individuate nella seguente maniera:
            - se non ti copre nessuno -> 0
            - altrimenti --> max(righe di chi ti copre) + 1
        - le colonne sono semplici numeri progressivi non ripetuti a parità di riga
        - La disposizione nella finestra segue queste regole 
            - Lungo l'asse verticale i punti hanno una distanza uguale più mezza di questa distanza dai bordi
            - Lungo l'asse orizzontale come sopra, con la differenza che la distanza (gap) cambia in base al numero di punti 
        
        """
        
        rows = get_righe(self.cover_matrix)
        cols = get_colonne(righe = rows)
        gaps_x = [W/rows.count(x) for x in rows]
        gap_y = H / (max(rows)+1) # più uno perchè conto da 0
        nodes = [((c+0.5)*gap_x, (r+0.5)*gap_y) for r,c,gap_x in zip(rows,cols,gaps_x)]
        vertex = [(i,j)  for i in range(len(self)) for j in range(i+1,len(self)) if self.cover_matrix[i][j] or self.cover_matrix[j][i]]
        
        return nodes, vertex, self.labels

           
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

    def CongruenceLattice(self, labels = False):
        a = self.all_congruenze()
        if not labels:
            return Lattice.from_function(a,confronta_blocchi,labels = [str(numero_blocchi(c)) for c in a])
        else:
            return Lattice.from_function(a,confronta_blocchi)
        
    def dinamic_congruences(self,Con_labels = False, labels = True, p_con_labels = None):
        global dinamic_congruence
        dinamic_congruence = True
        if not p_con_labels:
            self.hasse_p5(self.CongruenceLattice(Con_labels), labels = labels)
        else:
            ConL = self.CongruenceLattice()
            ConL.labels = p_con_labels
            self.hasse_p5(ConL, labels = labels)
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
        Componente wise (chain product)
        """
        return Lattice.from_function(genera_cw(lista),component_wise)
   
#### Rappresentation class   
class Hasse():
    def __init__(self, nodes, vertex, labels, radius = 2, vertex_color = None, nodes_color = None):
        self.nodes = nodes
        self.vertex = vertex
        self.r = radius
        self.labels = labels
        if not nodes_color:
            self.nodes_color = ['grey' for i in self.nodes]
        else:
            self.nodes_color = nodes_color
            
        if not vertex_color:
            self.vertex_color = ['black' for i in self.vertex]
        else:
            self.vertex_color = vertex_color
            
    def show_congruence(self, con, color = 'red'):
        self.vertex_color = [color if con[a] == con[b] else 'black' for a,b in self.vertex]
        
    def show_percorso(self, nodes, color ='red'):
        self.vertex_color =[color if (x in nodes and x!= nodes[-1] and nodes[nodes.index(x)+1] == y) or (y in nodes and y!= nodes[-1] and nodes[nodes.index(y)+1] == x) else 'black' for x,y in self.vertex]


class Finestra():
    def __init__(self,*hasses,shape : tuple = (500,500), grid = None, show_labels = False, font_size = 12, title = 'PosetMagico'):
        # Definisci Griglia
        if not grid:
            self.grid = (1, len(hasses))
        else:
            self.grid = grid
        
        assert self.grid[0] * self.grid[1] >= len(hasses)
            
        # definisci var
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
            upper_left = (col * self.shape[0] / self.grid[1], row * self.shape[1] / self.grid[0])
            
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
                                            Y +  H.r*2 + self.font_size/2 ,
                                            font=f"Times {self.font_size}", text=H.labels[i])
                     
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
   

class DinamicCongruences(Finestra):  
    def __init__(self,*hasses,shape : tuple = (500,500), congruence_lattice, grid = None, show_labels = False, font_size = 12, title = 'PoSet'):
        # Definisci Griglia
        if not grid:
            self.grid = (1, len(hasses))
        else:
            self.grid = grid
        
        assert self.grid[0] * self.grid[1] >= len(hasses)
            
        # definisci var
        self.ConL = congruence_lattice
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
        self.canvas.bind('<Motion>',self.show_con)
        self.canvas.bind("<Configure>", self.resize)
        self.root.mainloop()
        
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
            self.hasses[0].show_congruence(self.ConL[cerchio_selezionato])
            self.disegna()
                 
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
                    num_ij = len(self.L.index_upset(i) & ({k for k in range(len(self.L))} - self.L.index_upset(j))) + 1
                    den_ij = len(self.L.index_downset(i) & ({k for k in range(len(self.L))} - self.L.index_downset(j))) + 1
                    a_ij = num_ij / den_ij
                    
                    num_ji = len(self.L.index_upset(j) & ({k for k in range(len(self.L))} - self.L.index_upset(i))) + 1
                    den_ji =len(self.L.index_downset(j) & ({k for k in range(len(self.L))} - self.L.index_downset(i))) + 1
                    a_ji = num_ji / den_ji
                    
                    d_ij = a_ij / (a_ij + a_ji)
                    fuz_dom[i][j] = d_ij
                    fuz_dom[j][i] = 1 - d_ij
        return fuz_dom
        
    def LLEs(self):
        """
        Da implementare, non è così semplice
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
                        primo_termine = 1
                        for pt in range(k2 - s + 1, k2 + 1):
                            primo_termine*=pt
                            
                        secondo_termine = 1
                        for pt in range(k-s,k):
                            secondo_termine*=pt
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
                        primo_termine = 1
                        for pt in range(k2 - s + 1, k2 + 1):
                            primo_termine*=pt
                            
                        secondo_termine = 1
                        for pt in range(k-s,k):
                            secondo_termine*=pt
                        fuzzy_dom_ab += primo_termine/secondo_termine
                    fuzzy_dom_ab *= k1/k
                    fuz_dom[i][j] = fuzzy_dom_ab
                    
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
    
    def gerarchic_cluster(self, function_sep = "total_separation"):
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
        irriducibile_con = self.L.congruenze_join_irriducibili()
 
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
    
    """
    SFIDE FUTURE
    1. [x] Sistemare le parentesi nel prodotto di Reticoli / Poset. è una cosa sbatti utile ma problematica 
        - Porta però a creare problemi quando moltiplico reticoli che hanno come oggetti delle tuple, anche se queste non derivano da prodotti
    2. [x] Implementare le funzioni per estrarre gli elementi meet-dense e join-dense
        Dalla teoria risulta che preso a in L: a\in J(L) <==> \exists ! b: b\prec a
        Quindi in realtà se faccio scorrere la matrice di copertura e sommo righe / colonne ottengo meet dense e join dense quando le somme fanno 1 giusto??
    3. [x] Studiare la rappresentazione. p5 rimane l'opzione migliore come libreria, 
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
                
    6. [x] Implementare Dedekind Completetion
        - [ ]  impmlementarlo stepwise invece che stupi one...
        
    7. definire altre operazioni tra PoSet e Lattices.
        - [ ] PoSet: glued sum verificando che abbiano massimo e minimo
        - [ ] test di verifica di isomorfismi ed omomorfismi (sarebbe carino sfruttare funzioni built in come __is__) 
        - [ ] Potrebbe essere carino (ma non particolarmente essenziale) definire __floordiv__ per calcolare Reticoli quoziente: L // theta = ...
        
            
            
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
    