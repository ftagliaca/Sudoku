import os

import numpy as np


class Board:

    def __init__(self, file, board_n = -1):

        sudoku_path = os.path.join("puzzles",file)
        self.board, self.solution = self.load(sudoku_path, n = board_n)

        self.max_idx = 0
        self.solved = False

        # pg.init()
        # self.xmax = 800
        # self.ymax = 600
        # self.res = (self.xmax, self.ymax)
        #
        # self.white = (255,255,255)
        # self.cyan = (0,255,255)
        # self.red = (255,0,0)
        # self.black = (0,0,0)
        #
        # scr = pg.display.set_mode(self.res)
        # pg.display.set_caption("Sudoku")


    def load(self, file, n = -1):

        if n == 'custom':
            return np.zeros((9,9),dtype='int64'), np.zeros((9,9),dtype='int64')


        boards = np.genfromtxt(file,skip_header=1,delimiter=',',dtype='str')
        n = np.random.randint(boards.shape[0]) if n == -1 else n
        board = boards[n,0]
        solution = boards[n,1]
        board = np.array(list(board),dtype='int64').reshape(9,9)
        solution = np.array(list(solution),dtype='int64').reshape(9,9)

        return board, solution

    def set_board(self):
        self.board = np.abs(self.board)

    def unset_board(self):
        self.board = -np.abs(self.board)

    def solve_board(self, idx):
        
        self.max_idx = max(idx, self.max_idx)

        col_idx = idx  % 9
        row_idx = idx // 9

        if self.board[row_idx, col_idx] == 0:
            values = []

            for value in range(1,10):
                values.append(value) if not self.check_cell(idx, value) else 0
            

        else:
            values =  [self.board[row_idx, col_idx]]
        
        #print(f'Index: {idx}, column: {col_idx}, row: {row_idx}')
        #print(f'Possible values {values}')
        #print('='*30)
        #print(self.max_idx, end='\r')

        if len(values) == 1 and idx == 80:
            self.board[row_idx, col_idx] = -values[0] if self.board[row_idx, col_idx]<=0 else self.board[row_idx, col_idx]
            return True
        
        elif len(values) == 0:
            self.board[row_idx, col_idx] = 0 if self.board[row_idx, col_idx]<=0 else self.board[row_idx, col_idx]
            return False


        for value in values:
            
            self.board[row_idx, col_idx] = -value if self.board[row_idx, col_idx]<=0 else self.board[row_idx, col_idx]

            if self.solve_board(idx+1):
                return True

        self.board[row_idx, col_idx] = 0 if self.board[row_idx, col_idx]<=0 else self.board[row_idx, col_idx]
        return False

    def check_cell(self, idx: int, val: int) -> bool:
        """[summary]

        Args:
            idx (int): [description]
            val (int): [description]

        Returns:
            bool: True if value is present False otherwise 
        """
        col_idx = idx  % 9
        row_idx = idx // 9 

        row = self.board[row_idx, :]
        col = self.board[:, col_idx]
        square = self.board[(row_idx//3)*3:(row_idx//3+1)*3, (col_idx//3)*3:(col_idx//3+1)*3]

        return True if (np.abs(val) in np.abs(row)) or (np.abs(val) in np.abs(col)) or (np.abs(val) in np.abs(square)) else False

    def zero_cell(self, idx):

        col = idx % 9
        row = idx // 9

        val = self.board[row, col]

        self.board[row, col] = 0

        return val

if __name__ == '__main__':
    testBoard = Board('sudoku.csv')
    print(testBoard.board)
    print(testBoard.solution)
