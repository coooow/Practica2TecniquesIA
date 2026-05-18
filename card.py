import random
from enum import Enum
###NORMES PREVIES####
#1. El jugador només pot alliberar una carta descoberta o reservada en cada torn.
#2. Per alliberar una carta de plata, el jugador ha de tenir 6 cartes de bronze alliberades.
#3. Per alliberar una carta d'or, el jugador ha de tenir 3 cartes de plata alliberades.
#4. Un jugador no pot reservar una carta si ja té una carta reservada.

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
        #Comprobem el tipus i si compleix la norma
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
    
    #Bloqueja al jugador
    def bloquejarJugador(jugador):
        if(jugador.bloquejat):
            print(f"{jugador.nom} ja està bloquejat")
            return False
        jugador.bloquejat= True
        return True
    #Retorna la carta a la baralla i la barreja
    
    def RetornarCarta(self, carta):
        self.baralla.append(carta)
        random.shuffle(self.baralla)
        if(carta==self.cartaReservada):
            self.cartaReservada = None

        if(carta==self.cartaDescoberta):
            self.cartaDescoberta = None
    
##Llògia del joc
def play():
    print ("Benvingut al joc de cartes!")
    nomJugador1 =input("Introdueix el nom del jugador 1:")
    nomJugador2 =input("Introdueix el nom del jugador 2:")

    jugador1 = Jugador(nomJugador1)
    jugador1.crearBaralla()
    jugador2 = Jugador(nomJugador2)
    jugador2.crearBaralla()

    guanyador = False
    while guanyador ==False:
        for jugador in [jugador1, jugador2]:
            print(f"Torn de {jugador.nom}")
            cartaDescoberta = jugador.descobrirCarta()
            if cartaDescoberta is not None:
                print(f"{jugador.nom} ha descobert un/a {cartaDescoberta}")

                opció_valida = False
                while not opció_valida:
                    print(f"{jugador.nom} quina acció vols fer?")
                    print(f"1: Alliberar carta descoberta")
                    print(f"2: Alliberar carta reservada")
                    print(f"3: Reservar carta")
                    print(f"4: Retornar carta i barrejar")
                    print(f"5: Bloquejar jugador")
                    accio=input("Opció: ")
                    if accio =="1":
                        if jugador.alliberarCarta(cartaDescoberta):
                            print(f"{jugador.nom} ha alliberat un/a {cartaDescoberta}")
                            print(f"{jugador.nom} té {jugador.bronzes} bronzes, {jugador.platas} platas i {jugador.ors} ors")
                            opció_valida = True
                        else:
                            print(f"{jugador.nom} no pot alliberar un/a {cartaDescoberta}")

                    elif accio =="2":
                        if jugador.cartaReservada is not None and jugador.alliberarCarta(jugador.cartaReservada):
                            print(f"{jugador.nom} ha alliberat un/a {jugador.cartaReservada}")
                            print(f"{jugador.nom} té {jugador.bronzes} bronzes, {jugador.platas} platas i {jugador.ors} ors")
                            opció_valida = True
                        else:
                            print(f"{jugador.nom} no pot alliberar la carta reservada")
                        
                    elif accio =="3":
                        if jugador.reservarCarta():
                            print(f"{jugador.nom} ha reservat un/a {cartaDescoberta}")
                            opció_valida = True
                        else:
                            print(f"{jugador.nom} no pot reservar un/a {cartaDescoberta}")

                    elif accio =="4":
                        jugador.RetornarCarta(cartaDescoberta)
                        print(f"{jugador.nom} ha retornat la carta i ha barrejat la baralla")
                        opció_valida = True
                    
                    elif accio =="5":
                        if jugador.bloquejarJugador(jugador):
                            print(f"{jugador.nom} ha bloquejat al jugador")
                            opció_valida = True
                        else:
                            print(f"{jugador.nom} no pot bloquejar al jugador")
                    else:
                        print("Opció no vàlida, torna a intentar-ho.")
                ##FI WHILE OPCIÓ_VÀLIDA
                if(jugador.ors == 1):
                    guanyador = True
                    print(f"{jugador.nom} ha guanyat el joc!")
                
                    
