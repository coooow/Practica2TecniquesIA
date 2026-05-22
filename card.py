import random
import copy
from enum import Enum


# ============================================================
# NORMES DEL JOC
# ============================================================
# 1. Cada jugador té una baralla amb:
#    - 6 cartes de Bronze
#    - 3 cartes de Plata
#    - 1 carta d'Or
#
# 2. En cada torn, el jugador descobreix una carta i fa UNA acció.
#
# 3. Només es pot alliberar una carta de Plata si abans
#    s'han alliberat 6 cartes de Bronze.
#
# 4. Només es pot alliberar una carta d'Or si abans
#    s'han alliberat 3 cartes de Plata.
#
# 5. El jugador només pot tenir una carta reservada.
#
# 6. Si el jugador allibera una carta reservada o bloqueja el rival,
#    la carta descoberta del torn torna a la baralla.
#
# 7. Guanya el primer jugador que allibera la carta d'Or.


# ============================================================
# TIPUS DE CARTA
# ============================================================

class TipusCarta(Enum):
    BRONZE = "Bronze"
    PLATA = "Plata"
    OR = "Or"


# ============================================================
# CLASSE CARTA
# ============================================================

class Carta:
    def __init__(self, tipusCarta):
        self.tipus = tipusCarta

    def __str__(self):
        return self.tipus.value


# ============================================================
# CLASSE JUGADOR
# ============================================================

class Jugador:
    def __init__(self, nom):
        self.nom = nom

        # Baralla pròpia del jugador
        self.baralla = []

        # Comptadors de cartes alliberades
        self.bronzes = 0
        self.platas = 0
        self.ors = 0

        # Carta descoberta en el torn actual
        self.cartaDescoberta = None

        # Carta reservada del jugador
        self.cartaReservada = None

        # Estat de bloqueig
        self.bloquejat = False

        # Última acció feta.
        # Serveix per evitar que la màquina bloquegi infinitament.
        self.ultimaAccio = None

    # --------------------------------------------------------
    # Crear i barrejar la baralla
    # --------------------------------------------------------
    def crearBaralla(self):
        self.baralla = []

        for _ in range(6):
            self.baralla.append(Carta(TipusCarta.BRONZE))

        for _ in range(3):
            self.baralla.append(Carta(TipusCarta.PLATA))

        self.baralla.append(Carta(TipusCarta.OR))

        random.shuffle(self.baralla)

    # --------------------------------------------------------
    # Descobrir una carta de la baralla
    # --------------------------------------------------------
    def descobrirCarta(self):
        if len(self.baralla) > 0:
            self.cartaDescoberta = self.baralla.pop(0)
            return self.cartaDescoberta

        return None

    # --------------------------------------------------------
    # Reservar la carta descoberta
    # --------------------------------------------------------
    def reservarCarta(self):
        if self.cartaDescoberta is not None and self.cartaReservada is None:
            self.cartaReservada = self.cartaDescoberta
            self.cartaDescoberta = None
            return True

        return False

    # --------------------------------------------------------
    # Comprovar si una carta es pot alliberar
    # --------------------------------------------------------
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

    # --------------------------------------------------------
    # Alliberar una carta descoberta o reservada
    # --------------------------------------------------------
    def alliberarCarta(self, carta):
        if not self.potAlliberar(carta):
            return False

        if carta.tipus == TipusCarta.BRONZE:
            self.bronzes += 1

        elif carta.tipus == TipusCarta.PLATA:
            self.platas += 1

        elif carta.tipus == TipusCarta.OR:
            self.ors += 1

        # Eliminem la carta del lloc on estava guardada
        if carta == self.cartaReservada:
            self.cartaReservada = None

        elif carta == self.cartaDescoberta:
            self.cartaDescoberta = None

        return True

    # --------------------------------------------------------
    # Retornar una carta a la baralla i barrejar
    # --------------------------------------------------------
    def retornarCarta(self, carta):
        if carta is None:
            return False

        self.baralla.append(carta)
        random.shuffle(self.baralla)

        if carta == self.cartaReservada:
            self.cartaReservada = None

        elif carta == self.cartaDescoberta:
            self.cartaDescoberta = None

        return True


# ============================================================
# FUNCIÓ D'UTILITAT
# ============================================================
# Aquesta funció avalua si l'estat actual és bo o dolent
# per a la màquina.
#
# Valor positiu  -> avantatge per a la màquina
# Valor negatiu  -> avantatge per al jugador humà

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

    # Valorem tenir una carta important reservada
    if maquina.cartaReservada is not None:
        if maquina.cartaReservada.tipus == TipusCarta.PLATA:
            valor_maquina += 5
        elif maquina.cartaReservada.tipus == TipusCarta.OR:
            valor_maquina += 20

    if huma.cartaReservada is not None:
        if huma.cartaReservada.tipus == TipusCarta.PLATA:
            valor_huma += 5
        elif huma.cartaReservada.tipus == TipusCarta.OR:
            valor_huma += 20

    # Bloquejar ajuda, però no ha de valer més que progressar
    if huma.bloquejat:
        valor_maquina += 8

    if maquina.bloquejat:
        valor_maquina -= 20

    # Penalització per evitar bloquejos infinits
    if maquina.ultimaAccio == "bloquejar_rival":
        valor_maquina -= 8

    return valor_maquina - valor_huma


# ============================================================
# ACCIONS POSSIBLES
# ============================================================
# Retorna una llista amb les accions legals que pot fer
# un jugador en l'estat actual.

def accions_possibles(jugador, rival):
    accions = []

    # Prioritat: si es pot alliberar carta descoberta, és una acció possible
    if jugador.cartaDescoberta is not None:
        if jugador.potAlliberar(jugador.cartaDescoberta):
            accions.append("alliberar_carta_descoberta")

    # També pot alliberar carta reservada si compleix la jerarquia
    if jugador.cartaReservada is not None:
        if jugador.potAlliberar(jugador.cartaReservada):
            accions.append("alliberar_carta_reservada")

    # Si pot alliberar alguna carta, no afegim bloqueig.
    # Això evita que la màquina bloquegi quan pot progressar.
    if len(accions) > 0:
        return accions

    # Si no pot alliberar, pot reservar o retornar la carta descoberta
    if jugador.cartaDescoberta is not None:
        if jugador.cartaReservada is None:
            accions.append("reservar_carta")

        accions.append("retornar_carta_descoberta")

    # Bloquejar només si el rival no està ja bloquejat
    # i si el jugador no acaba de bloquejar en el torn anterior
    if not rival.bloquejat and jugador.ultimaAccio != "bloquejar_rival":
        accions.append("bloquejar_rival")

    if len(accions) == 0:
        accions.append("passar_torn")

    return accions


# ============================================================
# APLICAR ACCIÓ
# ============================================================
# Executa una acció sobre un jugador i modifica l'estat
# del jugador o del rival.

def aplicar_accio(jugador, rival, accio):
    jugador.ultimaAccio = accio

    if accio == "alliberar_carta_descoberta":
        jugador.alliberarCarta(jugador.cartaDescoberta)

    elif accio == "reservar_carta":
        jugador.reservarCarta()

    elif accio == "retornar_carta_descoberta":
        jugador.retornarCarta(jugador.cartaDescoberta)

    elif accio == "alliberar_carta_reservada":
        if jugador.alliberarCarta(jugador.cartaReservada):
            # Si allibera la reservada, la carta descoberta torna a la baralla
            if jugador.cartaDescoberta is not None:
                jugador.retornarCarta(jugador.cartaDescoberta)

    elif accio == "bloquejar_rival":
        rival.bloquejat = True

        # Si bloqueja, la carta descoberta no es queda a la mà
        if jugador.cartaDescoberta is not None:
            jugador.retornarCarta(jugador.cartaDescoberta)

    elif accio == "passar_torn":
        # Si passa torn, retorna la carta descoberta si n'hi ha
        if jugador.cartaDescoberta is not None:
            jugador.retornarCarta(jugador.cartaDescoberta)


# ============================================================
# MINIMAX
# ============================================================
# Algorisme d'Adversarial Search.
#
# La màquina és MAX:
#   intenta maximitzar la utilitat.
#
# El jugador humà és MIN:
#   es considera que intentarà reduir l'avantatge de la màquina.

def minimax(maquina, huma, tornMaquina, profunditat):
    # Cas base: arribem al límit de profunditat o algú ha guanyat
    if profunditat == 0 or maquina.ors >= 1 or huma.ors >= 1:
        return utilitat(maquina, huma), None

    # Determinem qui juga en aquest nivell de l'arbre
    jugador = maquina if tornMaquina else huma
    rival = huma if tornMaquina else maquina

    # Si el jugador està bloquejat, perd el torn
    if jugador.bloquejat:
        jugador.bloquejat = False
        valor, _ = minimax(maquina, huma, not tornMaquina, profunditat - 1)
        return valor, "passar_torn"

    # Si no té carta descoberta, en descobreix una
    if jugador.cartaDescoberta is None and len(jugador.baralla) > 0:
        jugador.descobrirCarta()

    accions = accions_possibles(jugador, rival)

    # Torn de la màquina: busca el valor màxim
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

    # Torn del jugador humà: busca el valor mínim per a la màquina
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


# ============================================================
# MOSTRAR ACCIÓ DE LA MÀQUINA
# ============================================================

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


# ============================================================
# TORN DE LA MÀQUINA
# ============================================================

def tornMaquina(maquina, jugador):
    print(f"\nTorn de {maquina.nom}")

    if maquina.bloquejat:
        print(f"{maquina.nom} està bloquejada i perd el torn")
        maquina.bloquejat = False
        return

    # La màquina descobreix una carta si no en té cap
    if maquina.cartaDescoberta is None:
        cartaDescoberta = maquina.descobrirCarta()
    else:
        cartaDescoberta = maquina.cartaDescoberta

    if cartaDescoberta is not None:
        print(f"{maquina.nom} ha descobert una carta: {cartaDescoberta}")
    else:
        print(f"{maquina.nom} no té més cartes per descobrir.")

    # Fem còpies per simular amb Minimax sense modificar la partida real
    maquinaCopia = copy.deepcopy(maquina)
    jugadorCopia = copy.deepcopy(jugador)

    _, millorAccio = minimax(maquinaCopia, jugadorCopia, True, 3)

    if millorAccio is None:
        millorAccio = "passar_torn"

    # Guardem la carta abans d'aplicar l'acció, perquè pot desaparèixer
    cartaUsada = maquina.cartaDescoberta

    if millorAccio == "alliberar_carta_reservada":
        cartaUsada = maquina.cartaReservada

    aplicar_accio(maquina, jugador, millorAccio)
    mostrar_accio_maquina(millorAccio, cartaUsada)

    print(f"{maquina.nom} té {maquina.bronzes} bronzes, {maquina.platas} platas i {maquina.ors} ors")


# ============================================================
# TORN DEL JUGADOR HUMÀ
# ============================================================

def tornJugador(jugador, maquina):
    print(f"\nTorn de {jugador.nom}")

    if jugador.bloquejat:
        print(f"{jugador.nom} està bloquejat i no pot jugar aquest torn.")
        jugador.bloquejat = False
        return

    # El jugador descobreix carta si encara no en té cap
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
                jugador.ultimaAccio = "alliberar_carta_descoberta"
                print(f"{jugador.nom} ha alliberat la carta descoberta.")
                opcio_valida = True
            else:
                print("No pots alliberar aquesta carta. Revisa les normes.")

        elif accio == "2":
            cartaReservada = jugador.cartaReservada

            if jugador.alliberarCarta(cartaReservada):
                jugador.ultimaAccio = "alliberar_carta_reservada"

                if jugador.cartaDescoberta is not None:
                    jugador.retornarCarta(jugador.cartaDescoberta)

                print(f"{jugador.nom} ha alliberat la carta reservada: {cartaReservada}")
                print("La carta descoberta ha tornat a la baralla.")
                opcio_valida = True
            else:
                print("No pots alliberar aquesta carta reservada. Revisa les normes.")

        elif accio == "3":
            if jugador.reservarCarta():
                jugador.ultimaAccio = "reservar_carta"
                print(f"{jugador.nom} ha reservat la carta descoberta.")
                opcio_valida = True
            else:
                print("No pots reservar aquesta carta. Revisa les normes.")

        elif accio == "4":
            if jugador.retornarCarta(jugador.cartaDescoberta):
                jugador.ultimaAccio = "retornar_carta_descoberta"
                print(f"{jugador.nom} ha retornat la carta descoberta a la baralla i l'ha barrejada.")
                opcio_valida = True
            else:
                print("No tens cap carta descoberta per retornar.")

        elif accio == "5":
            if jugador.ultimaAccio == "bloquejar_rival":
                print("No pots bloquejar dues vegades seguides.")

            elif maquina.bloquejat:
                print(f"{maquina.nom} ja està bloquejada.")

            else:
                maquina.bloquejat = True
                jugador.ultimaAccio = "bloquejar_rival"

                if jugador.cartaDescoberta is not None:
                    jugador.retornarCarta(jugador.cartaDescoberta)

                print(f"{jugador.nom} ha bloquejat a {maquina.nom}.")
                print("La carta descoberta ha tornat a la baralla.")
                opcio_valida = True

        elif accio == "6":
            jugador.ultimaAccio = "passar_torn"

            if jugador.cartaDescoberta is not None:
                jugador.retornarCarta(jugador.cartaDescoberta)

            print(f"{jugador.nom} passa el torn.")
            opcio_valida = True

        else:
            print("Acció no vàlida. Intenta-ho de nou.")

    print(f"{jugador.nom} té {jugador.bronzes} bronzes, {jugador.platas} platas i {jugador.ors} ors")


# ============================================================
# FUNCIÓ PRINCIPAL DEL JOC DE CARTES
# ============================================================

def play():
    print("Benvingut al joc de cartes!")
    print("Normes:")
    print("1. Cada jugador només pot fer una acció per torn.")
    print("2. Per alliberar una carta de Plata, cal tenir 6 cartes de Bronze alliberades.")
    print("3. Per alliberar una carta d'Or, cal tenir 3 cartes de Plata alliberades.")
    print("4. Un jugador només pot tenir una carta reservada.")
    print("5. Guanya el primer jugador que allibera la carta d'Or.")

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


# Aquesta part només s'executa si fem:
# python card.py
#
# Si el fitxer s'importa des de main.py amb:
# import card
# no s'executa automàticament.
if __name__ == "__main__":
    play()