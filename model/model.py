import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._personeCoinvolteSolBest = 0
        self._oreDiDisservizioSolBest = 0
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.DAO = DAO()
        self.lenListEvents = 0




    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self._personeCoinvolteSolBest = 0
        self._oreDiDisservizioSolBest = 0
        self.loadEvents(nerc)
        self.lenListEvents = len(self._listEvents)
        print(f"La lista di eventi è: {[evento.__str__() for evento in self._listEvents]}\n")
        parziale = []
        self.ricorsione(parziale, int(maxY), int(maxH), 0)

    def ricorsione(self, parziale, maxY, maxH, livello):
        personeCoinvolte = self.calcolaPersoneCoinvolte(parziale)
        if personeCoinvolte > self._personeCoinvolteSolBest:
            self._personeCoinvolteSolBest = personeCoinvolte
            self._oreDiDisservizioSolBest = self.calcolaOreDiDisservizio(parziale)
            self._solBest = copy.deepcopy(parziale)  # Usa deepcopy per evitare riferimenti
            print(f"La soluzione migliore ora è: {[evento.__str__() for evento in self._solBest]}\n")

        for i in range(livello, self.lenListEvents):
            evento = self._listEvents[i]
            if self.isAdmissible(evento, maxY, maxH, parziale) and evento not in parziale:
                parziale.append(evento)
                print(f"chiamo la ricorsione con i = {i+ 1}\n")

                """
                Se ho capito bene pyton è in grado di capire autonomamente
                che se i ad esempio è uguale a 5 e la lista è lunga 5 non può chiamare
                la funzione ricorsione con (i+1) perché altrimenti uscirebbe fuori dal range
                """
                self.ricorsione(parziale, maxY, maxH, i + 1) #modifica: i + 1 al posto di livello + 1, PS il problema grosso era qui, pensaci perchè non lo hai capito
                print("\n Gestiamo un altro ramo delle possibilità")
                parziale.pop()
        print(f"La soluzione finale è: {[evento.__str__() for evento in self._solBest]}\n")

    def isAdmissible(self, possibileNuovoEvento, maxY, maxH, parziale):
        totaleOreDiDisservizio = 0

        # Crea una lista temporanea che include il nuovo evento
        parziale_temp = parziale + [possibileNuovoEvento]

        # Calcola il massimo e il minimo degli anni con l'evento aggiunto
        annoPiuRecente = max(evento.date_event_began.year for evento in parziale_temp)
        annoPiuVecchio = min(evento.date_event_began.year for evento in parziale_temp)

        # Calcola le ore di disservizio per tutti gli eventi inclusi il nuovo evento
        for evento in parziale_temp:
            secondiDiDisservizio = abs((evento.date_event_began - evento.date_event_finished).total_seconds())
            totaleOreDiDisservizio += secondiDiDisservizio // 3600

        if totaleOreDiDisservizio <= maxH and (annoPiuRecente - annoPiuVecchio) <= maxY:
            print(f"Evento con id: {possibileNuovoEvento.id} ammissibile con ore di disservizio totali: {totaleOreDiDisservizio}, e differenza: {annoPiuRecente - annoPiuVecchio}")
            return True
        else:
            print(f"Evento con id: {possibileNuovoEvento.id} NON ammissibile con ore di disservizio totali: {totaleOreDiDisservizio}, e differenza: {annoPiuRecente - annoPiuVecchio}")
            return False

    def calcolaPersoneCoinvolte(self, parziale):
        personeCoinvolteParziale = 0
        for evento in parziale:
            personeCoinvolteParziale += evento.customers_affected
        return personeCoinvolteParziale

    def calcolaOreDiDisservizio(self, parziale):
        totaleOreDiDisservizio = 0
        for evento in parziale:
            secondiDiDisservizio = abs((evento.date_event_began - evento.date_event_finished).total_seconds())
            totaleOreDiDisservizio += secondiDiDisservizio // 3600
        return totaleOreDiDisservizio


    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()

    @property
    def listNerc(self):
        return self._listNerc



