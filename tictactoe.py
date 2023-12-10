import random
import math
import os
import tkinter as tk
from tkinter import simpledialog
#X is max = 1
#O in min = -1
# Crear una ventana de diálogo simple
root = tk.Tk()
root.withdraw()

class TicTacToe:
    
    def __init__(self):
        #primero se crea el tablero con - ademas se elegige de forma aleatoria si el jugador humano es la x o es la
        self.board = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humanPLayer = 'X'
            self.botPlayer = "O"
        else:
            self.humanPLayer = "O"
            self.botPlayer = "X"

    #funcion para mostrar el tablero 
    def show_board(self):
        print("")
        for i in range(3):
            print("  ",self.board[0+(i*3)]," | ",self.board[1+(i*3)]," | ",self.board[2+(i*3)])
            print("")

    #funcion para buscar que no quede un hueco vacio
    def is_board_filled(self,state):
        return not "-" in state

    #funcion para comprobar si un jugador ha echo 3 en raya o ha ganado
    def is_player_win(self,state,player):
        if state[0]==state[1]==state[2] == player: return True
        if state[3]==state[4]==state[5] == player: return True
        if state[6]==state[7]==state[8] == player: return True
        if state[0]==state[3]==state[6] == player: return True
        if state[1]==state[4]==state[7] == player: return True
        if state[2]==state[5]==state[8] == player: return True
        if state[0]==state[4]==state[8] == player: return True
        if state[2]==state[4]==state[6] == player: return True

        return False

    #llama las dos funciones para saber si un juego ha acabado 
    def checkWinner(self):
        if self.is_player_win(self.board,self.humanPLayer):
            os.system("cls")
            print(f"   Player {self.humanPLayer} wins the game!")
            return True

        if self.is_player_win(self.board,self.botPlayer):
            os.system("cls")
            print(f"   Player {self.botPlayer} wins the game!")
            return True

        # checking whether the game is draw or not
        if self.is_board_filled(self.board):
            os.system("cls")
            print("   Match Draw!")
            return True
        return False


    def start(self):
        #se crea el jugador humano y el jugador player 
        #se pasa la letra con la que juega el jugador humano 
        bot = ComputerPlayer(self.botPlayer)
        human = humanPLayer(self.humanPLayer)
        while True:
            os.system("cls")
            print(f"   Player {self.humanPLayer} turn")
            self.show_board()

            #Human
            square = human.human_move(self.board)
            self.board[square] = self.humanPLayer
            if self.checkWinner():
                break

            #Bot
            square = bot.machine_move(self.board)
            self.board[square] = self.botPlayer
            if self.checkWinner():
                break

        # showing the final view of board
        print()
        self.show_board()

class humanPLayer:
    #se pasa la letra con la que se juega la partida 
    def __init__(self,letter):
        self.letter = letter

    #funcion para realizar el movimiento que se desea realizar y si la casilla esta vacia se valida o si no se vuelve a pedir 
    def human_move(self,state):
        # taking user input
        while True:
            #se pide donde se va a colocar 
            square_str = simpledialog.askstring("Input", "Enter the square to fix spot(1-9): ")

            # Convertir la entrada a entero
            square = int(square_str)
            print()
            if state[square-1] == "-":
                break
        return square-1

##crea la clase computer y se hereda tictactoe
class ComputerPlayer(TicTacToe):
    ##botplayer va a ser la letra que se le pase y el humanplayer va a ser la letra contraria 
    def __init__(self,letter):
        self.botPlayer = letter
        self.humanPlayer = "X" if letter == "O" else "O"

    #esta funcion nos permite decidir quien va a jugar si la maquina o el humano 
    def players(self,state):
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if(state[i] == "X"):
                x = x+1
            if(state[i] == "O"):
                o = o+1

        if(self.humanPlayer == "X"):
            return "X" if x==o else "O"
        if(self.humanPlayer == "O"):
            return "O" if x==o else "X"

    ##funcion que se le pasa un tablero devuelve que opciones tenemos de movimiento 
    def actions(self,state):
        return [i for i, x in enumerate(state) if x == "-"]

    #esta funcion devulve un tablero njuevo en el que se ha producido un nuevo movimiento 
    def result(self,state,action):
        newState = state.copy()
        player = self.players(state)
        newState[action] = player
        return newState

    ##funcion que indica si hay un tres en raya e indica si ha ganado la x o si por el contrario ha ganado la o 
    def terminal(self,state):
        if(self.is_player_win(state,"X")):
            return True
        if(self.is_player_win(state,"O")):
            return True
        return False


    def minimax(self, state, player):
        max_player = self.humanPlayer  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # Se verifica si el estado actual del juego es terminal. Si es terminal, se devuelve un diccionario con la posición None y un puntaje basado en el jugador que hizo el movimiento.
        if self.terminal(state):
            return {'position': None, 'score': 1 * (len(self.actions(state)) + 1) if other_player == max_player else -1 * (
                        len(self.actions(state)) + 1)}
        #Si el tablero está lleno pero el juego no es terminal, se devuelve un diccionario con la posición None y un puntaje de empate (0).
        elif self.is_board_filled(state):
            return {'position': None, 'score': 0}

        #Se inicializa la mejor jugada posible (best) con un puntaje inicial extremo para maximizar o minimizar, según el jugador actual.
        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        #Se itera sobre todas las acciones posibles que el jugador puede tomar en el estado actual.
        for possible_move in self.actions(state):
            #Se realiza una simulación recursiva del juego después de realizar el movimiento actual. newState es el nuevo estado del juego después de hacer possible_move, y sim_score contiene el resultado de la llamada recursiva a minimax con el jugador oponente.
            newState = self.result(state,possible_move)
            sim_score = self.minimax(newState, other_player)  # simulate a game after making that move


            #Se actualiza best si la puntuación obtenida en la simulación es mejor que la mejor puntuación actual.
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        #Al final de la función, se devuelve el diccionario que contiene la mejor posición y su puntaje asociado.
        return best

    #Se utiliza el método minimax para calcular el mejor movimiento para la máquina (self.botPlayer) dado el estado actual del juego (state). El resultado es un diccionario que contiene la posición del mejor movimiento.
    def machine_move(self,state):
        square = self.minimax(state,self.botPlayer)['position']
        #Se devuelve la posición del mejor movimiento calculado por el algoritmo Minimax
        return square

# starting the game
tic_tac_toe = TicTacToe()
tic_tac_toe.start()