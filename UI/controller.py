from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def set_dd_categorie(self):
        categorie=self._model.get_categorie()
        self._view.dd_category.options.clear()
        for id_c,name in categorie:
            self._view.dd_category.options.append(ft.dropdown.Option(key=str(id_c),text=str(name)))
        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        id_categoria=self._view.dd_category.value
        data_inizio=self._view.dp1.value
        data_fine=self._view.dp2.value
        self._view.dd_prodotto_iniziale.options.clear()
        self._view.dd_prodotto_finale.options.clear()
        self._model.build_graph(int(id_categoria),data_inizio.strftime('%Y-%m-%d'),data_fine.strftime('%Y-%m-%d'))
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f"Date selezionate:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Start date: {data_inizio.strftime('%Y-%m-%d')}"))
        self._view.txt_risultato.controls.append(ft.Text(f"End date: {data_fine.strftime('%Y-%m-%d')}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di nodi: {self._model.G.number_of_nodes()}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Numero di archi: {self._model.G.number_of_edges()}"))
        for nodo in self._model.G.nodes():
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(key=str(nodo.id),text=str(nodo.product_name)))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(key=str(nodo.id), text=str(nodo.product_name)))
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        top_five=self._model.get_topfive()
        self._view.txt_risultato.controls.append(ft.Text(f""))
        self._view.txt_risultato.controls.append(ft.Text(f"I cinque prodotti più venduti sono:"))
        for nodo,peso in top_five:
            self._view.txt_risultato.controls.append(ft.Text(f"{nodo.product_name} with score {peso}"))
        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._view.txt_risultato.controls.clear()
        id_iniziale=self._view.dd_prodotto_iniziale.value
        id_finale=self._view.dd_prodotto_finale.value
        lunghezza_massima=int(self._view.txt_lunghezza_cammino.value)
        percorso,peso=self._model.get_percorso(lunghezza_massima,int(id_iniziale),int(id_finale))
        self._view.txt_risultato.controls.append(ft.Text(f"Cammino migliore:"))
        for nodo in percorso:
            self._view.txt_risultato.controls.append(ft.Text(f"{nodo.product_name}"))
        self._view.txt_risultato.controls.append(ft.Text(f"Score: {peso}"))
        self._view.update()