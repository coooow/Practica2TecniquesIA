import random
from aima3.search import Problem, astar_search


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

# Variables de puntuació 
movementCount = 0
minCostToGold = 0

# Classe per al problema de cerca
class LabyrinthProblem(Problem):
    def __init__(self, initial, goal, board, can_silver, can_gold):
        super().__init__(initial, goal)
        self.board = board
        self.can_silver = can_silver
        self.can_gold = can_gold
        self.rows = len(board)
        self.cols = len(board[0])

    def actions(self, state):
        row, col = state
        possible_actions = []
        # Mapa de moviments i els seus offsets (8 direccions)
        moves = {
            "W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1),
            "Q": (-1, -1), "E": (-1, 1), "Z": (1, -1), "C": (1, 1)
        }
        
        for action, (dr, dc) in moves.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                char = self.board[nr][nc]
                if char != "X":
                    # Restriccions jeràrquiques
                    if char == "S" and not self.can_silver: continue
                    if char == "G" and not self.can_gold: continue
                    possible_actions.append(action)
        return possible_actions

    def result(self, state, action):
        row, col = state
        moves = {
            "W": (-1, 0), "S": (1, 0), "A": (0, -1), "D": (0, 1),
            "Q": (-1, -1), "E": (-1, 1), "Z": (1, -1), "C": (1, 1)
        }
        dr, dc = moves[action]
        return (row + dr, col + dc)

    #Distancia de Chebyshev com a heurística
    def h(self, node):
        r1, c1 = node.state
        r2, c2 = self.goal
        return max(abs(r1 - r2), abs(c1 - c2))

def play():
    global movementCount, minCostToGold, bronzeCount, silverCount, goldCount, canSilver, canGold
    
    print("Benvingut/da al Joc del Laberint!")

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
    
    print("Calculant cost mínim fins a l'anell d'or...")
    minCostToGold = calculate_total_min_cost(board, (current_row, current_col))
    print(f"Cost mínim estimat: {minCostToGold}")
        
    #MOVIMENT/OPCIONS
    while True:
        for row in board:
            print(row)
        
        print(f"\nMoviments: {movementCount} | Cost Mínim: {minCostToGold} | Limit: {minCostToGold + 5}")
        
        print("Opcions:")
        print("W/A/S/D - Moviment Bàsic | Q/E/Z/C - Diagonals")
        print("H - Hint (A*) | G - God Mode (Full Path)")
        
        move = input("Indica el teu moviment o acció: ").upper()
        
        if move == "H":
            action = get_next_best_move(board, (current_row, current_col))
            if action:
                print(f"\n>>> PISTA: Hauries de moure cap a: {action} <<<")
            else:
                print("\n>>> No s'ha trobat un camí possible! <<<")
            continue
            
        elif move == "G":
            print("\n--- ACTIVANT GOD MODE (FULL PATH) ---")
            sequence = get_full_solution_sequence(board, (current_row, current_col), bronzeCount, silverCount, canSilver, canGold)
            if sequence:
                print(f"\n>>> SEQUENCIA DE MOVIMENTS FINS AL FINAL: {', '.join(sequence)} <<<")
                print(f">>> Total moviments: {len(sequence)} <<<")
            else:
                print("\n>>> No s'ha trobat un camí possible fins al final! <<<")
            continue

        if move in ["W", "A", "S", "D", "Q", "E", "Z", "C"]:
            if checkValidMove(board, current_row, current_col, move):
                board, current_row, current_col = movePlayer(board, current_row, current_col, move)
                movementCount += 1 # Incrementar comptador

                if(hasWon()):
                    print("Felicitats! Has guanyat el joc!")
                    break
                elif(hasLost()):
                    break
            else:
                print("Moviment no vàlid. Intenta de nou.")
        else:
            print("Opció no reconeguda. Intenta de nou.")

# --- Funcions auxiliars per a A* ---

# Calcula el millor moviment seguent cap a l'objectiu actual (Bronze, Plata o Or) utilitzant A*
def get_next_best_move(board, current_pos):
    target_char = "B"
    if bronzeCount == N_BRONZE: target_char = "S"
    if silverCount == N_SILVER: target_char = "G"
    
    # Busquem objectius del tipus actual
    targets = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == target_char:
                targets.append((r, c))
    
    if not targets: return None

    # Trobem el camí al més proper
    best_action = None
    shortest_len = float('inf')
    
    for goal in targets:
        prob = LabyrinthProblem(current_pos, goal, board, canSilver, canGold)
        node = astar_search(prob)
        if node:
            solution = node.solution()
            if len(solution) < shortest_len:
                shortest_len = len(solution)
                best_action = solution[0]
                
    return best_action

#Calcula el cost total mínim per recollir tots els anells en ordre (Bronze -> Plata -> Or) utilitzant A* per simular la recollida
def calculate_total_min_cost(board, start_pos):
    temp_board = [row[:] for row in board]
    current = start_pos
    total_cost = 0
    
    rows = len(board)
    cols = len(board[0])
    
    # 1. Cost per recollir tots els de Bronze
    for _ in range(N_BRONZE):
        targets = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "B"]
        best_path_len, next_pos = find_closest_target_cost(temp_board, current, targets, False, False)
        if next_pos:
            total_cost += best_path_len
            temp_board[next_pos[0]][next_pos[1]] = "."
            current = next_pos
        else: return 999 # Tauler impossible

    # 2. Cost per recollir tots els de Plata
    for _ in range(N_SILVER):
        targets = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "S"]
        best_path_len, next_pos = find_closest_target_cost(temp_board, current, targets, True, False)
        if next_pos:
            total_cost += best_path_len
            temp_board[next_pos[0]][next_pos[1]] = "."
            current = next_pos
        else: return 999

    # 3. Cost per recollir l'Or
    gold_target = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "G"]
    best_path_len, next_pos = find_closest_target_cost(temp_board, current, gold_target, True, True)
    if next_pos:
        total_cost += best_path_len
    else: return 999

    return total_cost

def find_closest_target_cost(board, start, targets, can_s, can_g):
    min_len = float('inf')
    target_pos = None
    for t in targets:
        prob = LabyrinthProblem(start, t, board, can_s, can_g)
        node = astar_search(prob)
        if node:
            if len(node.solution()) < min_len:
                min_len = len(node.solution())
                target_pos = t
    return min_len, target_pos

def find_closest_target_path(board, start, targets, can_s, can_g):
    min_len = float('inf')
    best_path = None
    target_pos = None
    for t in targets:
        prob = LabyrinthProblem(start, t, board, can_s, can_g)
        node = astar_search(prob)
        if node:
            sol = node.solution()
            if len(sol) < min_len:
                min_len = len(sol)
                best_path = sol
                target_pos = t
    return best_path, target_pos

def get_full_solution_sequence(board, start_pos, b_count, s_count, can_s, can_g):
    temp_board = [row[:] for row in board]
    current = start_pos
    all_moves = []
    
    temp_b_count = b_count
    temp_s_count = s_count
    temp_can_s = can_s
    temp_can_g = can_g
    
    rows = len(board)
    cols = len(board[0])
    
    # 1. Cost per recollir tots els de Bronze restants
    while temp_b_count < N_BRONZE:
        targets = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "B"]
        if not targets: break
        path, next_pos = find_closest_target_path(temp_board, current, targets, temp_can_s, temp_can_g)
        if next_pos:
            all_moves.extend(path)
            temp_board[next_pos[0]][next_pos[1]] = "."
            current = next_pos
            temp_b_count += 1
            if temp_b_count == N_BRONZE:
                temp_can_s = True
        else: return None

    # 2. Cost per recollir tots els de Plata restants
    while temp_s_count < N_SILVER:
        targets = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "S"]
        if not targets: break
        path, next_pos = find_closest_target_path(temp_board, current, targets, temp_can_s, temp_can_g)
        if next_pos:
            all_moves.extend(path)
            temp_board[next_pos[0]][next_pos[1]] = "."
            current = next_pos
            temp_s_count += 1
            if temp_s_count == N_SILVER:
                temp_can_g = True
        else: return None

    # 3. Cost per recollir l'Or
    gold_target = [(r, c) for r in range(rows) for c in range(cols) if temp_board[r][c] == "G"]
    if gold_target:
        path, next_pos = find_closest_target_path(temp_board, current, gold_target, temp_can_s, temp_can_g)
        if next_pos:
            all_moves.extend(path)
        else: return None

    return all_moves

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

def hasLost():
    # Implementar la lògica per verificar si el jugador ha perdut el joc
    # Comprovar si el jugador ha superat el límit de moviments o si no hi ha camí possible cap a l'anell d'or
    if movementCount > minCostToGold + 5:
        print("Has superat el límit de moviments! Has perdut el joc.")
        return True
    return False