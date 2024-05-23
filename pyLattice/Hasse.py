import tkinter as tk
import pyLattice as pl


class Hasse():
    def __init__(self, nodes, vertex, labels, radius = 2):
        self.nodes = nodes
        self.vertex = vertex
        self.r = radius
        self.labels = labels

class Finestra():
    def __init__(self,*hasses,shape : tuple = (500,500), grid = None, show_labels = False, font_size = 10):
        # Definisci Griglia
        if not grid:
            self.grid = (1, len(hasses))
        else:
            self.grid = grid
            
        # definisci var
        self.hasses = hasses
        self.show_labels = show_labels
        self.font_size = font_size
        self.shape = shape
            
        # Crea Finestra
        self.root = tk.Tk()
        self.root.geometry(str(shape[0])+'x'+str(shape[1]))
        self.root.title('PoSet magicooooo')
        self.canvas = tk.Canvas(self.root, width=shape[0], height=shape[1], bg='white')
        self.canvas.pack(anchor=tk.CENTER, expand=True)
        self.disegna()
        self.canvas.bind("<B1-Motion>", self.gestisci_movimento_mouse)
        self.root.mainloop()
            
    def disegna(self):
        self.canvas.delete("all")
        for i,H in enumerate(self.hasses):
            row = i // self.grid[1]
            col = i % self.grid[1]
            upper_left = (col * self.shape[0] / self.grid[1], row * self.shape[1] / self.grid[0])
            
            # Disegna linee
            for a,b in H.vertex:
                self.canvas.create_line((H.nodes[a][0] + upper_left[0], H.nodes[a][1] + upper_left[1]),
                                        (H.nodes[b][0] + upper_left[0], H.nodes[b][1] + upper_left[1]),
                                        )
            
            # Disegna cerchi
            for i,(x,y) in enumerate(H.nodes):
                self.canvas.create_oval((x - H.r + upper_left[0], y - H.r + upper_left[1]),
                                        (x + H.r + upper_left[0], y + H.r + upper_left[1]),
                                        fill = 'grey')
                
            # Aggiungi etichette
                if self.show_labels:
                    self.canvas.create_text(x + upper_left[0],
                                            y + upper_left[1] +  H.r*2 + self.font_size/2 ,
                                            font=f"Times {self.font_size}", text=H.labels[i])
                    

        
# Funzione per gestire il movimento del mouse
    def gestisci_movimento_mouse(self, evento):
        # Individua punto nella griglia e conseguentemenete Hasse di riferimento
        row = evento.x * self.grid[1] // self.shape[0]
        col = evento.y * self.grid[0] // self.shape[1]
        hasse_index = row*self.grid[0] + col
        
        # relativizza posizione del mouse nel riquadro di interesse nella griglia 
        mouse_x = evento.x % (self.shape[0] / self.grid[1])
        mouse_y = evento.y % (self.shape[1] / self.grid[0])
        
        
        # Trova cerchio
        cerchio_selezionato = None
        for i,node in enumerate(self.hasses[hasse_index].nodes):
            if type(node) != tuple:
                break
            node_x, node_y = node
            distanza_q = ((mouse_x - node_x)**2 + (mouse_y - node_y)**2)
            if distanza_q <= self.hasses[hasse_index].r ** 2 * 2:
                cerchio_selezionato = i
                break

        # Se un cerchio è stato selezionato, aggiorna la sua posizione
        if cerchio_selezionato:
          self.hasses[hasse_index].nodes[cerchio_selezionato] = (mouse_x, self.hasses[hasse_index].nodes[cerchio_selezionato][1])
          #self.hasses[hasse_index].nodes[cerchio_selezionato]
          self.disegna()


# Reticoli = [pl.Lattice.from_power_set(n) for n in range(2,6)]
# print(len(Reticoli))
# hasses = [Hasse(*A.hasse_coordinate(700/4,500),A.labels, radius = 5) for A in Reticoli]
# Finestra(*hasses, shape = (700,500))



"""
Con questo ho tutte le conoscenze per migrare in maniera unica e definitiva su TkInter.
Devo implementare tutte queste funzionalità:
- Rappresentare un poset (sarebbe carino includere diverse modalità)
- Rappresentare più poset specificando la disposizione della griglia
- Rappresentare più poset specificando quanto spazio deve occupare ciascuno
- Evidenziare con diversi colori certi legami o certi Pallini (da inserire nella classe Hasse)
- Inserire una modalità specifica per le congruenze dinamiche
- Rendere la finestra dinamica (poterla rimodificare)

"""