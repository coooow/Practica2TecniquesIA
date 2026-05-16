import random

N_BRONZE = 6
N_SILVER = 3
N_GOLD = 1

canSilver = False
canGold = False

bronzeCount = 0
silverCount = 0
goldCount = 0

current_row = 0
current_col = 0

hasGold = False

def play():
    print("Welcome to the Labyrinth Game!")

    rows, cols = 12, 12

    print("Llegenda:")
    print(". - Espai buit")
    print("P - Jugador")
    print("B - Anell bronze")
    print("S - Anell plata")
    print("G - Anell or")
    print("X - Barrera")

    #Creació del tauler buit
    board, current_row, current_col = generate_board(rows, cols)
        
    #MOVIMENT/OPCIONS
    while True:
        for row in board:
            print(row)
        print("Opcions:")
        print("W - Moure amunt")
        print("A - Moure esquerra")
        print("S - Moure avall")
        print("D - Moure dreta")
        print("Q - Moure amunt esquerra")
        print("E - Moure amunt dreta")
        print("Z - Moure avall esquerra")
        print("C - Moure avall dreta")
        
        move = input("Indica el teu moviment o acció: ").upper()
        if move in ["W", "A", "S", "D", "Q", "E", "Z", "C"]:
            # Aquí es processaria el moviment del jugador
            print(f"Has triat moure: {move}")
            # Implementar la lògica de moviment i interacció amb el tauler
            if checkValidMove(board, current_row, current_col, move):
                board, current_row, current_col = movePlayer(board, current_row, current_col, move)
                if(hasWon()):
                    print("Felicitats! Has guanyat el joc!")
                    break
            else:
                print("Moviment no vàlid. Intenta de nou.")
        else:
            print("Opció no reconeguda. Intenta de nou.")
            
            

#------------------CREACIO TAULELL------------------

def generate_board(rows, cols):
    #Creació del tauler buit
    board = [["." for i in range(cols)] for j in range(rows)]

    #------------------BARRERES------------------

    #Barrera 5x1
    direction = random.randint(0, 2)
    if direction == 0: #Vertical
        while True:
            random_row = random.randint(0, rows-5)
            random_col = random.randint(0, cols-1)
            if(board[random_row][random_col] == "." and board[random_row+1][random_col] == "." and board[random_row+2][random_col] == "." and board[random_row+3][random_col] == "." and board[random_row+4][random_col] == "."):
                break
        for i in range (5):
            board[random_row+i][random_col] = "X"
    elif direction == 1: #Horizontal
        while True:
            random_row = random.randint(0, rows-1)
            random_col = random.randint(0, cols-5)
            if(board[random_row][random_col] == "." and board[random_row][random_col+1] == "." and board[random_row][random_col+2] == "." and board[random_row][random_col+3] == "." and board[random_row][random_col+4] == "."):
                break
        for i in range (5):
            board[random_row][random_col+i] = "X"
    elif direction == 2: #Diagonal
        while True:
            random_row = random.randint(0, rows-5)
            random_col = random.randint(0, cols-5)
            if(board[random_row][random_col] == "." and board[random_row+1][random_col+1] == "." and board[random_row+2][random_col+2] == "." and board[random_row+3][random_col+3] == "." and board[random_row+4][random_col+4] == "."):
                break
        for i in range (5):
            board[random_row+i][random_col+i] = "X"     

    #Barrera 4x1
    direction = random.randint(0, 2)
    if direction == 0: #Vertical
        while(True):
            random_row = random.randint(0, rows-4)
            random_col = random.randint(0, cols-1)
            if(board[random_row][random_col] == "." and board[random_row+1][random_col] == "." and board[random_row+2][random_col] == "." and board[random_row+3][random_col] == "."):
                break
        for i in range (4):
            board[random_row+i][random_col] = "X"
    elif direction == 1: #Horizontal
        while True:
            random_row = random.randint(0, rows-1)
            random_col = random.randint(0, cols-4)
            if(board[random_row][random_col] == "." and board[random_row][random_col+1] == "." and board[random_row][random_col+2] == "." and board[random_row][random_col+3] == "."):
                break
        for i in range (4):
            board[random_row][random_col+i] = "X"
    elif direction == 2: #Diagonal
        while True:
            random_row = random.randint(0, rows-4)
            random_col = random.randint(0, cols-4)
            if(board[random_row][random_col] == "." and board[random_row+1][random_col+1] == "." and board[random_row+2][random_col+2] == "." and board[random_row+3][random_col+3] == "."):
                break
        for i in range (4):
            board[random_row+i][random_col+i] = "X"

    #Barreres 3x1
    for i in range (3):
        direction = random.randint(0, 2)
        if direction == 0: #Vertical
            while True:
                random_row = random.randint(0, rows-3)
                random_col = random.randint(0, cols-1)
                if(board[random_row][random_col] == "." and board[random_row+1][random_col] == "." and board[random_row+2][random_col] == "."):
                    break
            for j in range (3):
                board[random_row+j][random_col] = "X"
        elif direction == 1: #Horizontal
            while True:
                random_row = random.randint(0, rows-1)
                random_col = random.randint(0, cols-3)
                if(board[random_row][random_col] == "." and board[random_row][random_col+1] == "." and board[random_row][random_col+2] == "."):
                    break
            for j in range (3):
                board[random_row][random_col+j] = "X"
        elif direction == 2: #Diagonal
            while True:
                random_row = random.randint(0, rows-3)
                random_col = random.randint(0, cols-3)
                if(board[random_row][random_col] == "." and board[random_row+1][random_col+1] == "." and board[random_row+2][random_col+2] == "."):
                    break
            for j in range (3):
                board[random_row+j][random_col+j] = "X"


    #------------------PECES------------------

    #JUGADOR
    while(True):
        random_row = random.randint(0, rows-1)
        random_col = random.randint(0, cols-1)
        if board[random_row][random_col] == ".":
            break
    board[random_row][random_col] = "P"
    
    current_col = random_col
    current_row = random_row

    #ANELL BRONZE
    for i in range (6):
        while(True):
            random_row = random.randint(0, rows-1)
            random_col = random.randint(0, cols-1)
            if board[random_row][random_col] == ".":
                break
        board[random_row][random_col] = "B"

    #ANELL PLATA
    for i in range (3):
        while(True):
            random_row = random.randint(0, rows-1)
            random_col = random.randint(0, cols-1)
            if board[random_row][random_col] == ".":
                break
        board[random_row][random_col] = "S"

    #ANELL OR
    while(True):
        random_row = random.randint(0, rows-1)
        random_col = random.randint(0, cols-1)
        if board[random_row][random_col] == ".":
            break
    board[random_row][random_col] = "G"
    
    return board, current_row, current_col

def checkValidMove(board, current_row, current_col, move):
    # Implementar la lògica per verificar si el moviment és vàlid
    # Comprovar les coordenades de destinació segons el moviment i assegurar-se que no hi hagi barreres ni sortida del tauler
    if move == "W":  # Moure amunt
        new_row, new_col = current_row - 1, current_col
    elif move == "A":  # Moure esquerra
        new_row, new_col = current_row, current_col - 1
    elif move == "S":  # Moure avall
        new_row, new_col = current_row + 1, current_col
    elif move == "D":  # Moure dreta
        new_row, new_col = current_row, current_col + 1
    elif move == "Q":  # Moure amunt esquerra
        new_row, new_col = current_row - 1, current_col - 1
    elif move == "E":  # Moure amunt dreta
        new_row, new_col = current_row - 1, current_col + 1
    elif move == "Z":  # Moure avall esquerra
        new_row, new_col = current_row + 1, current_col - 1
    elif move == "C":  # Moure avall dreta
        new_row, new_col = current_row + 1, current_col + 1
    else:
        return False  # Moviment no reconegut
    
    # Comprovar si les coordenades de destinació estan dins del tauler
    if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
        # Comprovar si la casella de destinació no és una barrera
        if board[new_row][new_col] != "X":
            if board[new_row][new_col] == ".":
                return True
            elif board[new_row][new_col] == "B":
                print("Has recollit un anell de bronze!")
                global bronzeCount, canSilver
                bronzeCount += 1
                if bronzeCount == N_BRONZE:
                    canSilver = True
                    print("Ara pots recollir anells de plata!")
                return True
            elif board[new_row][new_col] == "S":
                if canSilver:
                    print("Has recollit un anell de plata!")
                    global silverCount, canGold
                    silverCount += 1
                    if silverCount == N_SILVER:
                        canGold = True
                        print("Ara pots recollir l'anell d'or!")
                    return True
                else:
                    print("No pots recollir aquest anell encara. Recull tots els anells de bronze primer.")
                    return False
            elif board[new_row][new_col] == "G":
                if canGold:
                    print("Has recollit l'anell d'or! Has guanyat el joc!")
                    global goldCount
                    goldCount += 1
                    return True
                else:
                    print("No pots recollir aquest anell encara. Recull tots els anells de bronze i plata primer.")
                    return False

def movePlayer(board, current_row, current_col, move):
    # Implementar la lògica per moure el jugador al tauler
    # Actualitzar les coordenades del jugador i el tauler segons el moviment
    if move == "W":  # Moure amunt
        new_row, new_col = current_row - 1, current_col
    elif move == "A":  # Moure esquerra
        new_row, new_col = current_row, current_col - 1
    elif move == "S":  # Moure avall
        new_row, new_col = current_row + 1, current_col
    elif move == "D":  # Moure dreta
        new_row, new_col = current_row, current_col + 1
    elif move == "Q":  # Moure amunt esquerra
        new_row, new_col = current_row - 1, current_col - 1
    elif move == "E":  # Moure amunt dreta
        new_row, new_col = current_row - 1, current_col + 1
    elif move == "Z":  # Moure avall esquerra
        new_row, new_col = current_row + 1, current_col - 1
    elif move == "C":  # Moure avall dreta
        new_row, new_col = current_row + 1, current_col + 1
    
    # Actualitzar el tauler amb la nova posició del jugador
    board[current_row][current_col] = "."  # Deixar la casella anterior buida
    board[new_row][new_col] = "P"  # Colocar el jugador en la nova casilla
    
    # Actualitzar les coordenades actuals del jugador
    current_row, current_col = new_row, new_col
    
    return board, current_row, current_col
    
def hasWon():
    # Implementar la lògica per verificar si el jugador ha guanyat el joc
    # Comprovar si el jugador ha recollit l'anell d'or
    return goldCount == N_GOLD