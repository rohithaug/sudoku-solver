from random import sample
from math import sqrt

#size = int(input("Enter Size : ")
def Sudoku(size):
    len = int(sqrt(size))
    cells = list(range(len))

    rows  = [x*len+w for x in sample(cells, len) for w in sample(cells, len)]
    cols  = [y*len+h for y in sample(cells, len) for h in sample(cells, len)]
    nums = sample(list(range(1, size+1)), size)

    def pattern(x, y):
        return (x + y//len + len*(y%len))%size

    board = [[nums[pattern(row, col)] for col in cols] for row in rows]

    squares = size*size
    empties = int(squares * 0.6)

    for square in sample(range(squares), empties):
        board[square//size][square%size] = 0

    return board

print("\nSudoku creator for different size variants such as: \n")
for i in range(2, 11):
    print(i*i, "x", i*i)
size = int(input("\nEnter size of board : "))

board = Sudoku(size)

print(size)
print("\nSudoku created:\n")
for i in board:
    print(i)
