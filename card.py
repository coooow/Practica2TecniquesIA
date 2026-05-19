import random
import copy
from enum import Enum
###NORMES PREVIES####
#1. El jugador només pot alliberar una carta descoberta o reservada en cada torn.
#2. Per alliberar una carta de plata, el jugador ha de tenir 6 cartes de bronze alliberades.
#3. Per alliberar una carta d'or, el jugador ha de tenir 3 cartes de plata alliberades.
#4. Un jugador no pot reservar una carta si ja té una carta reservada.

####Funcions de la IA adversial search Minimax
def utilitat(maquina, huma): ##son de la clase Jugador
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

def accions_possibles(jugador, rival):
    accions=[]

    if jugador.cartaDescoberta is not None:
        print("ALLIBERAR_CARTA")
        accions.append("alliberar_carta_descoberta")

    if jugador.cartaReservada is None:
        print("RESERVAR_CARTA")
        accions.append("reservar_carta")

    accions_possibles.append("Retornar_carta_descoberta")

    if jugador.cartaReservada is not None:
        print("ALLIBERAR_CARTA_RESERVADA")
        accions.append("alliberar_carta_reservada")
    if rival.bloquejat:
        print("BLOQUEJAR_RIVAL")
        accions.append("bloquejar_rival")

    if len(accions) == 0:
        print("PASSAR_TORN")
        accions.append("passar_torn")

    return accions

## TOTES LES CLASSES

#### Classe Card
class Carta:
    def __init__(self, tipusCarta):
        self.tipus = tipusCarta
    
    def __str__(self):
        return self.tipus.value
    
class TipusCarta(Enum):
    BRONZE = "Bronze"
    PLATA = "Plata"
    OR = "Or"

### Classe jugador
class Jugador:
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
    
##Llògia del joc
def play():
    print ("Benvingut al joc de cartes!")
    nomJugador =input("Introdueix el nom del jugador 1:")
    nomMaquina =input("Introdueix el nom de la máquina:")

    jugador = Jugador(nomJugador)
    jugador.crearBaralla()
    maquina = Jugador(nomMaquina)
    maquina.crearBaralla()

    guanyador = False
    while guanyador ==False:
