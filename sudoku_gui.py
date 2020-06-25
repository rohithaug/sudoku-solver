from random import sample
from math import sqrt

from pygame.locals import *
import pygame
import sys

def create_sudoku(size):
    len = int(sqrt(size))
    cells = list(range(len))

    rows  = [x*len+w for x in sample(cells, len) for w in sample(cells, len)]
    cols  = [y*len+h for y in sample(cells, len) for h in sample(cells, len)]
    nums = sample(list(range(1, size+1)), size)

    def pattern(x, y):
        return (x + y//len + len*(y%len))%size

    board = [[nums[pattern(row, col)] for col in cols] for row in rows]

    squares = size*size
    empties = int(squares * 0.75)

    for square in sample(range(squares), empties):
        board[square//size][square%size] = 0

    return board

class Sudoku:
    def __init__(self, screen, width, height, rows, cols, array):
        self.screen = screen
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.array = array
        self.values = None
        self.cells = [[Cell(screen, width, height, rows, cols, row, col, array[row][col]) for col in range(cols)] for row in range(rows)]
        self.selected_cell = None

    def update_values(self):
        self.values = [[self.cells[row][col].value for col in range(self.cols)] for row in range(self.rows)]

    def draw(self):
        w = self.width/self.cols
        h = self.height/self.rows
        for row in range(self.rows+1):
            if row%3 == 0 and row != 0:
                thickness = 3
                color = (0, 0, 0)
            else:
                thickness = 1
                color = (160, 160, 160)
            pygame.draw.lines(self.screen, color, False, [(row*w, 0), (row*w, self.height)], thickness)
            pygame.draw.lines(self.screen, color, False, [(0, row*h), (self.width, row*h)], thickness)

        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].draw()

    def click_cell(self, pos):
        if pos[0] > self.width and pos[1] > self.height:
            return None
        else:
            w = self.width/self.cols
            h = self.height/self.rows
            col = int(pos[0]//w)
            row = int(pos[1]//h)
            return(row, col)

    def unselect_cell(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].selected = False

    def select_cell(self, cell):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].selected = False

        self.cells[cell[0]][cell[1]].selected = True
        self.selected_cell = (cell[0], cell[1])

    def write_value(self, value):
        row, col = self.selected_cell
        self.cells[row][col].set_temp_value(value)

    def place_value(self, value):
        row, col = self.selected_cell
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(value)
            self.update_values()

            if self.correct_pos(value, (row,col)) and self.solve():
                return True
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp_value(0)
                self.update_values()
                return False

    def delete_value(self):
        row, col = self.selected_cell
        self.cells[row][col].set_value(0)
        self.cells[row][col].set_temp_value(0)
        self.update_values()

    def solution(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].value == 0:
                    return False
        return True

    def find_empty(self):
        for row in range(len(self.values)):
            for col in range(len(self.values)):
                if self.values[row][col] == 0:
                    return(row, col)
        return None

    def correct_pos(self, num, pos):
        #check rows
        for row in range(self.rows):
            if self.values[pos[0]][row] == num and pos[1] != row:
                return False
        #check columns
        for col in range(self.cols):
            if self.values[col][pos[1]] == num and pos[0] != col:
                return False
        #check 3*3 boxes
        box_x = (pos[0]//3)*3
        box_y = (pos[1]//3)*3
        for row in range(box_x, box_x+3):
            for col in range(box_y, box_y+3):
                if self.values[row][col] == num and pos != (row, col):
                    return False
        return True

    def solve(self):
        pos = self.find_empty()
        if pos is None:
            return True
        for i in range(1, self.rows+1):
            if self.correct_pos(i, pos):
                self.values[pos[0]][pos[1]] = i
                if self.solve():
                    return True
                self.values[pos[0]][pos[1]] = 0
        return False

    def solve_sudoku(self):
        pos = self.find_empty()
        if pos is None:
            return True
        for i in range(1, self.rows+1):
            if self.correct_pos(i, pos):
                self.values[pos[0]][pos[1]] = i
                self.cells[pos[0]][pos[1]].set_value(i)
                self.cells[pos[0]][pos[1]].draw_entry(True)
                self.update_values()
                pygame.display.update()
                pygame.time.delay(20)

                if self.solve_sudoku():
                    return True

                self.values[pos[0]][pos[1]] = 0
                self.cells[pos[0]][pos[1]].set_value(0)
                self.cells[pos[0]][pos[1]].draw_entry(False)
                self.update_values()
                pygame.display.update()
                pygame.time.delay(20)

        return False

class Cell:
    def __init__(self, screen, width, height, rows, cols, row, col, value):
        self.screen = screen
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.row = row
        self.col = col
        self.w = width/self.cols
        self.h = height/self.rows
        self.x = col * (width/self.cols)
        self.y = row * (height/self.rows)
        self.value = value
        self.temp_value = 0
        self.selected = False

    def set_value(self, value):
        self.value = value

    def set_temp_value(self, value):
        self.temp_value = value

    def draw(self):
        cell_font = pygame.font.SysFont("cambria", 40)

        if self.value == 0 and self.temp_value != 0:
            cell_text = cell_font.render(str(self.temp_value), 1, (128, 128, 128))
            self.screen.blit(cell_text, (self.x+5, self.y+5))

        elif self.value != 0:
            cell_text = cell_font.render(str(self.value), 1, (0, 0, 0))
            self.screen.blit(cell_text, (self.x + (self.w/2 - cell_text.get_width()/2), self.y + (self.h/2 - cell_text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(self.screen, (255,0,0), (self.x, self.y, self.w, self.h), 4)

    def draw_entry(self, valid):
        cell_font = pygame.font.SysFont("cambria", 40)

        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 0)

        cell_text = cell_font.render(str(self.value), 1, (64, 64, 64))
        self.screen.blit(cell_text, (self.x + (self.w/2 - cell_text.get_width()/2), self.y + (self.h/2 - cell_text.get_height()/2)))

        if valid:
            pygame.draw.rect(self.screen, (0, 255, 0), (self.x+2, self.y+2, self.w, self.h), 4)
        else:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x+2, self.y+2, self.w, self.h), 4)

def main():
    pygame.init()

    sudoku_size = 9
    array = create_sudoku(sudoku_size)
    rows = sudoku_size
    cols = sudoku_size

    screen = pygame.display.set_mode((600, 640), HWSURFACE|DOUBLEBUF|RESIZABLE)
    screen.fill((255, 255, 255))
    pygame.display.set_caption("SUDOKU SOLVER \u00A9 ROHITH")

    board = Sudoku(screen, 600, 600, rows, cols, array)
    board.update_values()

    key = None

    while True:
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==VIDEORESIZE:
                screen=pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
                pygame.display.flip()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_BACKSPACE:
                    board.delete_value()
                    key = None

                if event.key == pygame.K_RETURN:
                    cell = board.selected_cell
                    if board.cells[cell[0]][cell[1]].temp_value != 0:
                        if board.place_value(board.cells[cell[0]][cell[1]].temp_value):
                            print("Yes")
                        else:
                            print("No")
                        key = None

                        if board.solution():
                            print("Game over")

                if event.key == pygame.K_SPACE:
                    board.update_values()
                    board.unselect_cell()
                    board.solve_sudoku()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = board.click_cell(pos)
                if cell:
                    board.select_cell(cell)
                    key = None

        if board.selected_cell and key != None:
            board.write_value(key)

        screen.fill((255,255,255))
        board.draw()
        font = pygame.font.SysFont("cambria", 18)
        text = font.render("Type your ans and press Enter | Hit spacebar to solve automatically", 1, (0, 0, 0))
        screen.blit(text, (15, 607))
        pygame.display.update()

if __name__=='__main__':
    main()
    pygame.quit()
