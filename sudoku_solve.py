class sudoku:
    def __init__(self, board):
        self.board = board

    def find_empty(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                if self.board[row][col] == 0:
                    return(row, col)
        return None

    def correct_pos(self, num, pos):
        #check rows
        for row in range(len(self.board)):
            if self.board[pos[0]][row] == num and pos[1] != row:
                return False
        #check columns
        for col in range(len(self.board)):
            if self.board[col][pos[1]] == num and pos[0] != col:
                return False
        #check 3*3 boxes
        box_x = (pos[0]//3)*3
        box_y = (pos[1]//3)*3
        for row in range(box_x, box_x+3):
            for col in range(box_y, box_y+3):
                if self.board[row][col] == num and pos[1] != row and pos[0] != col:
                    return False
        return(True)

    def solver(self):
        pos = self.find_empty()
        if pos is None:
            return True
        for i in range(1, rows):
            if self.correct_pos(i, pos):
                self.board[pos[0]][pos[1]] = i
                if self.solver():
                    return True
                self.board[pos[0]][pos[1]] = 0
        return False

    def solution(self):
        if self.solver():
            for row in range(len(self.board)):
                for col in range(len(self.board)):
                    print(self.board[row][col], end=' ')
                print('')
        else:
            print("Solution does not exists")

array =  [[3, 0, 6, 5, 0, 8, 4, 0, 0],
          [5, 2, 0, 0, 0, 0, 0, 0, 0],
          [0, 8, 7, 0, 0, 0, 0, 3, 1],
          [0, 0, 3, 0, 1, 0, 0, 8, 0],
          [9, 0, 0, 8, 6, 3, 0, 0, 5],
          [0, 5, 0, 0, 9, 0, 6, 0, 0],
          [1, 3, 0, 0, 0, 0, 2, 5, 0],
          [0, 0, 0, 0, 0, 0, 0, 7, 4],
          [0, 0, 5, 2, 0, 6, 3, 0, 0]]

board = sudoku(array)
board.solution()
