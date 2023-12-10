import random
import math
import os
import tkinter as tk
from tkinter import simpledialog
import asyncio
import concurrent.futures

root = tk.Tk()
root.withdraw()

class TicTacToe:
    def __init__(self):
        self.board = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humanPlayer = 'X'
            self.botPlayer = "O"
        else:
            self.humanPlayer = "O"
            self.botPlayer = "X"

    def show_board(self):
        print("")
        for i in range(3):
            print("  ", self.board[0 + (i * 3)], " | ", self.board[1 + (i * 3)], " | ", self.board[2 + (i * 3)])
            print("")

    def is_board_filled(self, state):
        return not "-" in state

    def is_player_win(self, state, player):
        if state[0] == state[1] == state[2] == player: return True
        if state[3] == state[4] == state[5] == player: return True
        if state[6] == state[7] == state[8] == player: return True
        if state[0] == state[3] == state[6] == player: return True
        if state[1] == state[4] == state[7] == player: return True
        if state[2] == state[5] == state[8] == player: return True
        if state[0] == state[4] == state[8] == player: return True
        if state[2] == state[4] == state[6] == player: return True

        return False

    def check_winner(self, state):
        if self.is_player_win(state, self.humanPlayer):
            os.system("cls")
            print(f"   Player {self.humanPlayer} wins the game!")
            return True

        if self.is_player_win(state, self.botPlayer):
            os.system("cls")
            print(f"   Player {self.botPlayer} wins the game!")
            return True

        if self.is_board_filled(state):
            os.system("cls")
            print("   Match Draw!")
            return True
        return False

    def start(self):
        bot = ComputerPlayer(self.botPlayer)
        human = HumanPlayer(self.humanPlayer)
        asyncio.run(self.async_start(human, bot))

    async def async_start(self, human, bot):
        while True:
            os.system("cls")
            print(f"   Player {self.humanPlayer} turn")
            self.show_board()

            square = await human.async_human_move(self.board)
            self.board[square] = self.humanPlayer
            if self.check_winner(self.board):  # Pasa el estado del tablero como argumento
                break

            square = await bot.async_machine_move(self.board)
            self.board[square] = self.botPlayer
            if self.check_winner(self.board):  # Pasa el estado del tablero como argumento
                break

        print()
        self.show_board()

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    async def async_human_move(self, state):
        while True:
            square_str = simpledialog.askstring("Input", "Enter the square to fix spot(1-9): ")
            square = int(square_str)
            print()
            if state[square - 1] == "-":
                break
        return square - 1

class ComputerPlayer(TicTacToe):
    def __init__(self, letter):
        super().__init__()
        self.botPlayer = letter
        self.humanPlayer = "X" if letter == "O" else "O"

    async def async_machine_move(self, state):
        square = (await self.minimax_async(state, self.botPlayer, float('-inf'), float('inf')))['position']
        return square

    async def minimax_async(self, state, player, alfa, beta):
        if self.terminal(state):
            return {'position': None, 'score': self.evaluate(state, player)}

        if player == self.botPlayer:
            return await self.max_value(state, player, alfa, beta)
        else:
            return await self.min_value(state, player, alfa, beta)

    async def max_value(self, state, player, alfa, beta):
        best = {'position': None, 'score': float('-inf')}

        for move in self.actions(state):
            new_state = self.result(state, move, player)
            child = await self.minimax_async(new_state, self.humanPlayer, alfa, beta)
            child['position'] = move

            best = max(best, child, key=lambda x: x['score'])

            if best['score'] >= beta:
                return best

            alfa = max(alfa, best['score'])

        return best

    async def min_value(self, state, player, alfa, beta):
        best = {'position': None, 'score': float('inf')}

        for move in self.actions(state):
            new_state = self.result(state, move, player)
            child = await self.minimax_async(new_state, self.botPlayer, alfa, beta)
            child['position'] = move

            best = min(best, child, key=lambda x: x['score'])

            if best['score'] <= alfa:
                return best

            beta = min(beta, best['score'])

        return best

    def actions(self, state):
        return [i for i, x in enumerate(state) if x == "-"]

    def result(self, state, action, player):
        new_state = state.copy()
        new_state[action] = player
        return new_state

    def evaluate(self, state, player):
        if self.is_player_win(state, self.botPlayer):
            return 1  # La computadora gana
        elif self.is_player_win(state, self.humanPlayer):
            return -1  # El jugador humano gana
        elif self.is_board_filled(state):
            return 0  # Empate
        else:
            return 0.5 
        pass

    def terminal(self, state):
        return self.check_winner(state) or self.is_board_filled(state)

if __name__ == "__main__":
    tic_tac_toe = TicTacToe()
    tic_tac_toe.start()
