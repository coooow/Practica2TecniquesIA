import random
from enum import Enum
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
    
    #Alliberar la carta reservada
    def alliberarCarta(self, carta):
        #Comprovar que la carta a alliberar es la reservada o la descoberta
        if (carta.tipus == TipusCarta.BRONZE):
            self.bronzes += 1
        
        elif (carta.tipus == TipusCarta.PLATA and self.bronzes == 6):
            self.platas += 1
        elif (carta.tipus == TipusCarta.OR and self.platas == 3):
            self.ors += 1
        else:
            return False
        #Si la carta a alliberar es la reservada o la descoberta, alliberar-la
        if(carta==self.cartaReservada):
            self.cartaReservada = None

        if(carta==self.cartaDescoberta):
            self.cartaDescoberta = None
        
        return True        
    
##Llògia del joc
def play():
    print ("Welcome to the Card Game!")
    nomJugador1 =input("Enter the name of player 1:")
    nomJugador2 =input("Enter the name of player 2:")

    jugador1 = Jugador(nomJugador1)
    jugador1.crearBaralla()
    jugador2 = Jugador(nomJugador2)
    jugador2.crearBaralla()

    guanyador = False
    while guanyador ==False:
