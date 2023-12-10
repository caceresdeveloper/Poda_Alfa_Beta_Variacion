import numpy as np
import pygame
import sys
import math

# Definición de colores
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Define el número de filas y columnas
ROW_COUNT = 6
COLUMN_COUNT = 7

# Se inicializa una matriz de ceros para representar el tablero
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Coloca una pieza (1 para jugador 1, 2 para jugador 2 en la posición especificada)
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Verifica si la columna aún tiene espacio para agregar una pieza
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Devuelve la fila disponible más baja en una columna específica
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Imprime el tablero en la consola
def print_board(board):
    print(np.flip(board, 0))

# Verifica si hay una jugada ganadora para el jugador actual
def winning_move(board, piece):
    # ... (código existente para verificar jugadas ganadoras)
    return False

# Dibuja el tablero y las fichas en la ventana de Pygame
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

# Implementación de la poda alfa-beta
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over:
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                eval = minimax(board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                board[row][col] = 0  # Deshacer el movimiento
                if beta <= alpha:
                    break  # Poda alfa-beta
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                eval = minimax(board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                board[row][col] = 0  # Deshacer el movimiento
                if beta <= alpha:
                    break  # Poda alfa-beta
        return min_eval

# Función para evaluar la posición del tablero (heurística simple)
def evaluate_board(board):
    # Implementa tu propia función de evaluación aquí
    return 0

# Resto del código (bucle principal, manejo de eventos, etc.)
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)

board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            col = int(math.floor(posx / SQUARESIZE))

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                print_board(board)
                draw_board(board)

                if game_over:
                    pygame.time.wait(3000)
                else:
                    # Movimiento de la IA (jugador 2)
                    best_move = -1
                    best_eval = float('-inf')
                    for col in range(COLUMN_COUNT):
                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)
                            eval = minimax(board, 3, float('-inf'), float('inf'), False)
                            board[row][col] = 0  # Deshacer el movimiento
                            if eval > best_eval:
                                best_eval = eval
                                best_move = col

                    if best_move != -1:
                        row = get_next_open_row(board, best_move)
                        drop_piece(board, row, best_move, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                        print_board(board)
                        draw_board(board)

                        turn += 1
                        turn = turn % 2

                        if game_over:
                            pygame.time.wait(3000)