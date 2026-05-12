import random

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

    #IMPRIMIR TAULER
    for row in board:
        print(row)
