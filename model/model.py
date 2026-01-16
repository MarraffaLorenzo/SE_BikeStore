import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.lista_categorie=[]
        self.lista_nodi=[]
        self.dict_nodi={}
        self.G=nx.DiGraph()
        self.top5=[]
        self.percorso_migliore=[]
        self.peso_migliore=0

    def get_date_range(self):
        return DAO.get_date_range()

    def get_categorie(self):
        categorie=DAO.get_category()
        for categoria in categorie:
            self.lista_categorie.append(categoria)
        return self.lista_categorie

    def build_graph(self,id_categoria,data_inizio,data_fine):
        self.G.clear()
        self.lista_nodi = []
        self.dict_nodi = {}

        nodi=DAO.get_prodotti_per_categoria(id_categoria)
        for nodo in nodi:
            self.lista_nodi.append(nodo)
            self.dict_nodi[nodo.id]=nodo
        self.G.add_nodes_from(self.lista_nodi)

        connessioni=DAO.get_connessioni(data_inizio,data_fine)
        for id1,peso1 in connessioni:
            for id2,peso2 in connessioni:
                if id1!=id2:
                    nodo1=self.dict_nodi.get(id1)
                    nodo2=self.dict_nodi.get(id2)
                    peso_tot=peso1+peso2
                    if nodo1 and nodo2:
                        if peso1>peso2:
                            self.G.add_edge(nodo1,nodo2,weight=peso_tot)
                        elif peso1<peso2:
                            self.G.add_edge(nodo2,nodo1,weight=peso_tot)
                        elif peso1==peso2:
                            self.G.add_edge(nodo1, nodo2, weight=peso_tot)
                            self.G.add_edge(nodo2, nodo1, weight=peso_tot)

    def get_topfive(self):
        self.top5=[]
        for nodo in self.G.nodes():
            somme_uscenti=self.G.out_degree(nodo,weight="weight")
            somme_entranti=self.G.in_degree(nodo,weight="weight")
            peso_tot=somme_uscenti-somme_entranti
            self.top5.append((nodo,peso_tot))
        self.top5.sort(key=lambda x: x[1], reverse=True)
        return self.top5[:5]

    def get_percorso(self,lunghezza,id_inizale,id_finale):
        self.percorso_migliore = []
        self.peso_migliore = 0
        prodotto_iniziale=self.dict_nodi.get(id_inizale)
        prodotto_finale=self.dict_nodi.get(id_finale)
        self.ricorsione([prodotto_iniziale],prodotto_finale,lunghezza,0)
        return self.percorso_migliore,self.peso_migliore

    def ricorsione(self,parziale,prodotto_finale,lunghezza_max,peso_tot):
        ultimo=parziale[-1]
        if len(parziale)==lunghezza_max:
            if ultimo==prodotto_finale:
                if peso_tot> self.peso_migliore:
                    self.peso_migliore=peso_tot
                    self.percorso_migliore=parziale.copy()
            return

        vicini=self.G.neighbors(ultimo)
        for vicino in vicini:
            peso_arco=self.G[ultimo][vicino]["weight"]
            if vicino in parziale:
                continue
            parziale.append(vicino)
            self.ricorsione(parziale,prodotto_finale,lunghezza_max,peso_tot+peso_arco)
            parziale.pop()




























