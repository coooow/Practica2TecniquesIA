import random
import copy
from enum import Enum

### NORMES PREVIES
# 1. El jugador només pot fer una acció per torn.
# 2. Per alliberar una carta de plata, el jugador ha de tenir 6 cartes de bronze alliberades.
# 3. Per alliberar una carta d'or, el jugador ha de tenir 3 cartes de plata alliberades.
# 4. Un jugador no pot reservar una carta si ja té una carta reservada.


class Carta:
    def __init__(self, tipusCarta):
        self.tipus = tipusCarta

    def __str__(self):
        return self.tipus.value


class TipusCarta(Enum):
    BRONZE = "Bronze"
    PLATA = "Plata"
    OR = "Or"


class Jugador:
    def __init__(self, nom):
        self.nom = nom
        self.baralla = []

        self.bronzes = 0
        self.platas = 0
        self.ors = 0

        self.cartaDescoberta = None
        self.cartaReservada = None

        self.bloquejat = False

    def crearBaralla(self):
        self.baralla = []

        for _ in range(6):
            self.baralla.append(Carta(TipusCarta.BRONZE))

        for _ in range(3):
            self.baralla.append(Carta(TipusCarta.PLATA))

        self.baralla.append(Carta(TipusCarta.OR))

        random.shuffle(self.baralla)

    def descobrirCarta(self):
        if len(self.baralla) > 0:
            self.cartaDescoberta = self.baralla.pop(0)
            return self.cartaDescoberta
        return None

    def reservarCarta(self):
        if self.cartaDescoberta is not None and self.cartaReservada is None:
            self.cartaReservada = self.cartaDescoberta
            self.cartaDescoberta = None
            return True
        return False

    def potAlliberar(self, carta):
        if carta is None:
            return False

        if carta.tipus == TipusCarta.BRONZE:
            return True

        elif carta.tipus == TipusCarta.PLATA:
            return self.bronzes == 6

        elif carta.tipus == TipusCarta.OR:
            return self.platas == 3

        return False

    def alliberarCarta(self, carta):
        if not self.potAlliberar(carta):
            return False

        if carta.tipus == TipusCarta.BRONZE:
            self.bronzes += 1

        elif carta.tipus == TipusCarta.PLATA:
            self.platas += 1

        elif carta.tipus == TipusCarta.OR:
            self.ors += 1

        if carta == self.cartaReservada:
            self.cartaReservada = None

        elif carta == self.cartaDescoberta:
            self.cartaDescoberta = None

        return True

    def RetornarCarta(self, carta):
        if carta is None:
            return False

        self.baralla.append(carta)
        random.shuffle(self.baralla)

        if carta == self.cartaReservada:
            self.cartaReservada = None

        elif carta == self.cartaDescoberta:
            self.cartaDescoberta = None

        return True
    def __init__(self, nom):
        self.nom = nom
        self.baralla = []

        self.bronzes=0
        self.platas=0
        self.ors=0

        self.cartaDescoberta = None
        self.cartaReservada = None

        self.bloquejat = False

    #Crear la baralla del jugador
    def crearBaralla(self):
        for i in range(6):
            self.baralla.append(Carta(TipusCarta.BRONZE))
        for i in range(3):
            self.baralla.append(Carta(TipusCarta.PLATA))
        for i in range(1):
            self.baralla.append(Carta(TipusCarta.OR))
        random.shuffle(self.baralla)

    #Treure les cartes de la baralla
    def descobrirCarta(self):
        if(len(self.baralla) > 0):
            self.cartaDescoberta = self.baralla.pop(0)
            return self.cartaDescoberta 
        return None
    #Reservar la carta descoberta
    def reservarCarta(self):
        if(self.cartaDescoberta !=None and self.cartaReservada == None):
            self.cartaReservada = self.cartaDescoberta
            self.cartaDescoberta = None
            return True
        return False
    
    #Comprovar si es pot alliberar la carta descoberta o reservada
    def potAlliberar(self, carta):
        if carta is None:
            return False

        if carta.tipus == TipusCarta.BRONZE:
            return True

        elif carta.tipus == TipusCarta.PLATA:
            return self.bronzes == 6

        elif carta.tipus == TipusCarta.OR:
            return self.platas == 3
        return False
    
    #Alliberar la carta reservada o descoberta
    def alliberarCarta(self, carta):
        if not self.potAlliberar(carta):
            return False

        if carta.tipus == TipusCarta.BRONZE:
            self.bronzes += 1

        elif carta.tipus == TipusCarta.PLATA:
            self.platas += 1

        elif carta.tipus == TipusCarta.OR:
            self.ors += 1

        if carta == self.cartaReservada:
            self.cartaReservada = None

        elif carta == self.cartaDescoberta:
            self.cartaDescoberta = None
            
        
        return True
    

    #Retorna la carta a la baralla i la barreja
    
    def RetornarCarta(self, carta):
        if (carta is None):
            return False
        
        self.baralla.append(carta)
        random.shuffle(self.baralla)

        if(carta==self.cartaReservada):
            self.cartaReservada = None

        if(carta==self.cartaDescoberta):
            self.cartaDescoberta = None
        return True
    

def utilitat(maquina, huma):
    valor_maquina = (
        maquina.bronzes * 10 +
        maquina.platas * 40 +
        maquina.ors * 1000
    )

    valor_huma = (
        huma.bronzes * 10 +
        huma.platas * 40 +
        huma.ors * 1000
    )

    if huma.bloquejat:
        valor_maquina += 25

    if maquina.bloquejat:
        valor_maquina -= 25

    return valor_maquina - valor_huma

##accions_possibles() calcula las acciones legals.

def accions_possibles(jugador, rival):
    accions = []

    if jugador.cartaDescoberta is not None:
        if jugador.potAlliberar(jugador.cartaDescoberta):
            accions.append("alliberar_carta_descoberta")

        if jugador.cartaReservada is None:
            accions.append("reservar_carta")

        accions.append("retornar_carta_descoberta")

    if jugador.cartaReservada is not None:
        if jugador.potAlliberar(jugador.cartaReservada):
            accions.append("alliberar_carta_reservada")

    if not rival.bloquejat:
        accions.append("bloquejar_rival")

    if len(accions) == 0:
        accions.append("passar_torn")

    return accions


def aplicar_accio(jugador, rival, accio):
    if accio == "alliberar_carta_descoberta":
        jugador.alliberarCarta(jugador.cartaDescoberta)

    elif accio == "reservar_carta":
        jugador.reservarCarta()

    elif accio == "retornar_carta_descoberta":
        jugador.RetornarCarta(jugador.cartaDescoberta)

    elif accio == "alliberar_carta_reservada":
        if jugador.alliberarCarta(jugador.cartaReservada):
            if jugador.cartaDescoberta is not None:
                jugador.RetornarCarta(jugador.cartaDescoberta)

    elif accio == "bloquejar_rival":
        rival.bloquejat = True

        if jugador.cartaDescoberta is not None:
            jugador.RetornarCarta(jugador.cartaDescoberta)

    elif accio == "passar_torn":
        if jugador.cartaDescoberta is not None:
            jugador.RetornarCarta(jugador.cartaDescoberta)

##Simula torns futurs i retorna el valor de la millor acció per a la màquina.
def minimax(maquina, huma, tornMaquina, profunditat):
    if profunditat == 0 or maquina.ors >= 1 or huma.ors >= 1:
        return utilitat(maquina, huma), None

    jugador = maquina if tornMaquina else huma
    rival = huma if tornMaquina else maquina

    if jugador.bloquejat:
        jugador.bloquejat = False
        valor, _ = minimax(maquina, huma, not tornMaquina, profunditat - 1)
        return valor, "passar_torn"

    if jugador.cartaDescoberta is None and len(jugador.baralla) > 0:
        jugador.descobrirCarta()

    accions = accions_possibles(jugador, rival)

    if tornMaquina:
        millorValor = float("-inf")
        millorAccio = None

        for accio in accions:
            maquinaCopia = copy.deepcopy(maquina)
            humaCopia = copy.deepcopy(huma)

            aplicar_accio(maquinaCopia, humaCopia, accio)

            valor, _ = minimax(maquinaCopia, humaCopia, False, profunditat - 1)

            if valor > millorValor:
                millorValor = valor
                millorAccio = accio

        return millorValor, millorAccio

    else:
        pitjorValor = float("inf")
        pitjorAccio = None

        for accio in accions:
            maquinaCopia = copy.deepcopy(maquina)
            humaCopia = copy.deepcopy(huma)

            aplicar_accio(humaCopia, maquinaCopia, accio)

            valor, _ = minimax(maquinaCopia, humaCopia, True, profunditat - 1)

            if valor < pitjorValor:
                pitjorValor = valor
                pitjorAccio = accio

        return pitjorValor, pitjorAccio
    
def mostrar_accio_maquina(accio, carta):
    if accio == "alliberar_carta_descoberta":
        print(f"La màquina ha alliberat la carta descoberta: {carta}")

    elif accio == "alliberar_carta_reservada":
        print(f"La màquina ha alliberat la carta reservada: {carta}")

    elif accio == "reservar_carta":
        print(f"La màquina ha reservat la carta descoberta: {carta}")

    elif accio == "retornar_carta_descoberta":
        print("La màquina ha retornat la carta descoberta a la baralla")

    elif accio == "bloquejar_rival":
        print("La màquina ha bloquejat el jugador")

    elif accio == "passar_torn":
        print("La màquina passa el torn")

#Utilitza minimax per decidir la millor acció de la màquina i l'aplica al torn de la màquina. 
# També mostra les accions realitzades i l'estat actual de la màquina després del torn.
def tornMaquina(maquina, jugador):
    print(f"\nTorn de {maquina.nom}")

    if maquina.bloquejat:
        print(f"{maquina.nom} està bloquejada i perd el torn")
        maquina.bloquejat = False
        return

    if maquina.cartaDescoberta is None:
        cartaDescoberta = maquina.descobrirCarta()
    else:
        cartaDescoberta = maquina.cartaDescoberta

    if cartaDescoberta is not None:
        print(f"{maquina.nom} ha descobert una carta: {cartaDescoberta}")
    else:
        print(f"{maquina.nom} no té més cartes per descobrir.")

    maquinaCopia = copy.deepcopy(maquina)
    jugadorCopia = copy.deepcopy(jugador)

    _, millorAccio = minimax(maquinaCopia, jugadorCopia, True, 3)

    if millorAccio is None:
        millorAccio = "passar_torn"

    cartaUsada = maquina.cartaDescoberta

    if millorAccio == "alliberar_carta_reservada":
        cartaUsada = maquina.cartaReservada

    aplicar_accio(maquina, jugador, millorAccio)
    mostrar_accio_maquina(millorAccio, cartaUsada)

    print(f"{maquina.nom} té {maquina.bronzes} bronzes, {maquina.platas} platas i {maquina.ors} ors")


def tornJugador(jugador, maquina):
    print(f"\nTorn de {jugador.nom}")

    if jugador.bloquejat:
        print(f"{jugador.nom} està bloquejat i no pot jugar aquest torn.")
        jugador.bloquejat = False
        return

    if jugador.cartaDescoberta is None:
        cartaDescoberta = jugador.descobrirCarta()
    else:
        cartaDescoberta = jugador.cartaDescoberta

    if cartaDescoberta is not None:
        print(f"{jugador.nom} ha descobert una carta: {cartaDescoberta}")
    else:
        print(f"{jugador.nom} no té més cartes per descobrir.")

    if jugador.cartaReservada is not None:
        print(f"Carta reservada actual: {jugador.cartaReservada}")

    opcio_valida = False

    while not opcio_valida:
        print("\nAccions disponibles:")
        print("1. Alliberar carta descoberta")
        print("2. Alliberar carta reservada")
        print("3. Reservar carta descoberta")
        print("4. Retornar carta descoberta a la baralla i barrejar")
        print("5. Bloquejar rival")
        print("6. Passar torn")

        accio = input("Selecciona una acció (1-6): ")

        if accio == "1":
            if jugador.alliberarCarta(jugador.cartaDescoberta):
                print(f"{jugador.nom} ha alliberat la carta descoberta.")
                opcio_valida = True
            else:
                print("No pots alliberar aquesta carta. Revisa les normes.")

        elif accio == "2":
            cartaReservada = jugador.cartaReservada

            if jugador.alliberarCarta(cartaReservada):
                if jugador.cartaDescoberta is not None:
                    jugador.RetornarCarta(jugador.cartaDescoberta)

                print(f"{jugador.nom} ha alliberat la carta reservada: {cartaReservada}")
                print("La carta descoberta ha tornat a la baralla.")
                opcio_valida = True
            else:
                print("No pots alliberar aquesta carta reservada. Revisa les normes.")

        elif accio == "3":
            if jugador.reservarCarta():
                print(f"{jugador.nom} ha reservat la carta descoberta.")
                opcio_valida = True
            else:
                print("No pots reservar aquesta carta. Revisa les normes.")

        elif accio == "4":
            if jugador.RetornarCarta(jugador.cartaDescoberta):
                print(f"{jugador.nom} ha retornat la carta descoberta a la baralla i l'ha barrejada.")
                opcio_valida = True
            else:
                print("No tens cap carta descoberta per retornar.")

        elif accio == "5":
            if maquina.bloquejat:
                print(f"{maquina.nom} ja està bloquejada.")
            else:
                maquina.bloquejat = True

                if jugador.cartaDescoberta is not None:
                    jugador.RetornarCarta(jugador.cartaDescoberta)

                print(f"{jugador.nom} ha bloquejat a {maquina.nom}.")
                print("La carta descoberta ha tornat a la baralla.")
                opcio_valida = True

        elif accio == "6":
            if jugador.cartaDescoberta is not None:
                jugador.RetornarCarta(jugador.cartaDescoberta)
            print(f"{jugador.nom} passa el torn.")
            opcio_valida = True

        else:
            print("Acció no vàlida. Intenta-ho de nou.")

    print(f"{jugador.nom} té {jugador.bronzes} bronzes, {jugador.platas} platas i {jugador.ors} ors")
##Llògia del joc
def play():
    print("Benvingut al joc de cartes!")
    print("Normes:")
    print("1. El jugador només pot fer una acció per torn.")
    print("2. Per alliberar una carta de plata, el jugador ha de tenir 6 cartes de bronze alliberades.")
    print("3. Per alliberar una carta d'or, el jugador ha de tenir 3 cartes de plata alliberades.")
    print("4. Un jugador no pot reservar una carta si ja té una carta reservada.")
    print("5. Guanya el primer jugador que alliberi la carta d'or.")

    nomJugador = input("Introdueix el nom del jugador: ")

    jugador = Jugador(nomJugador)
    jugador.crearBaralla()

    maquina = Jugador("Magnus_Carlsen.exe")
    maquina.crearBaralla()

    guanyador = False

    while not guanyador:
        print("\n-------------------------")
        print(f"Jugador: {jugador.nom} - Bronzes: {jugador.bronzes}, Platas: {jugador.platas}, Ors: {jugador.ors}")
        print(f"Rival: {maquina.nom} - Bronzes: {maquina.bronzes}, Platas: {maquina.platas}, Ors: {maquina.ors}")
        print("-------------------------")

        tornJugador(jugador, maquina)

        if jugador.ors >= 1:
            print(f"\n{jugador.nom} ha guanyat!")
            guanyador = True
            break

        tornMaquina(maquina, jugador)

        if maquina.ors >= 1:
            print(f"\n{maquina.nom} ha guanyat!")
            guanyador = True
            break



    print("Benvingut al joc de cartes!")
    print("Normes:")
    print("1. El jugador només pot fer una acció per torn.")
    print("2. Per alliberar una carta de plata, el jugador ha de tenir 6 cartes de bronze alliberades.")
    print("3. Per alliberar una carta d'or, el jugador ha de tenir 3 cartes de plata alliberades.")
    print("4. Un jugador no pot reservar una carta si ja té una carta reservada.")
    print("5. Guanya el primer jugador que alliberi la carta d'or.")

    nomJugador = input("Introdueix el nom del jugador: ")

    jugador = Jugador(nomJugador)
    jugador.crearBaralla()

    maquina = Jugador("Magnus_Carlsen.exe")
    maquina.crearBaralla()

    guanyador = False

    while not guanyador:
        print("\n-------------------------")
        print(f"Jugador: {jugador.nom} - Bronzes: {jugador.bronzes}, Platas: {jugador.platas}, Ors: {jugador.ors}")
        print(f"Rival: {maquina.nom} - Bronzes: {maquina.bronzes}, Platas: {maquina.platas}, Ors: {maquina.ors}")
        print("-------------------------")

        tornJugador(jugador, maquina)

        if jugador.ors >= 1:
            print(f"\n{jugador.nom} ha guanyat!")
            guanyador = True
            break

        tornMaquina(maquina, jugador)

        if maquina.ors >= 1:
            print(f"\n{maquina.nom} ha guanyat!")
            guanyador = True
            break