import flet as ft

from model.model import Model
from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        self._view.txt_result.controls = []
        self._view.update_page()
        nerc_str = self._view._ddNerc.value#possibile errore
        nerc = self._idMap.get(nerc_str)
        maxY = self._view._txtYears.value #possibile errore
        maxH = self._view._txtHours .value#possibile errore
        self._model.worstCase(nerc, maxY, maxH)
        personeCoinvolteSolBest = self._model._personeCoinvolteSolBest
        oreDiDisservizioSolBest = self._model._oreDiDisservizioSolBest
        solBest = self._model._solBest
        self._view.txt_result.controls.append(
            ft.Text(value=f"Tot people affected: {personeCoinvolteSolBest}\nTot hours of outage: {oreDiDisservizioSolBest}\n",
                    color="black",
                    text_align=ft.TextAlign.LEFT, width=300, weight=ft.FontWeight.BOLD))
        stampa = ""
        for i in solBest:
            #stampa += i.__str__ + "\n"
            self._view.txt_result.controls.append(ft.Text(value=i, color="black",
                                                      text_align=ft.TextAlign.LEFT, width=300))
        self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

