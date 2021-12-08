import sys
import random
from time import sleep, time
from tkinter import Frame, Label, CENTER

SIZE = 400
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

BACKGROUND_COLOR_DICT = {
    2:      "#f1d9e1",
    4:      "#e3b4c4",
    8:      "#e3b4c4",
    16:     "#c76a8a",
    32:     "#b9456d",
    64:     "#943757",
    128:    "#4a1b2b",
    256:    "#923655",
    512:    "#e56e74",
    1024:   "#e0020d",
    2048:   "#e8555d",
    4096:   "#bfce4c",
    8192:   "#c18f03",
    16384:  "#f2b179",
    32768:  "#f59563",
    65536:  "#1f4df4",
}

CELL_COLOR_DICT = {
    2:      "#776e65",
    4:      "#776e65",
    8:      "#f9f6f2",
    16:     "#f9f6f2",
    32:     "#f9f6f2",
    64:     "#f9f6f2",
    128:    "#f9f6f2",
    256:    "#f9f6f2",
    512:    "#f9f6f2",
    1024:   "#f9f6f2",
    2048:   "#f9f6f2",
    4096:   "#776e65",
    8192:   "#f9f6f2",
    16384:  "#776e65",
    32768:  "#776e65",
    65536:  "#f9f6f2",
}

FONT = ("Helvetica", 50, "bold")

KEY_QUIT = "Escape"

KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_LEFT = "Left"
KEY_RIGHT = "Right"


def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix


def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat


def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'

    for i in range(len(mat)-1):
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'


def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new


def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new


def cover_up(mat):
    new = []
    for j in range(GRID_LEN):
        partial_new = []
        for i in range(GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(GRID_LEN):
        count = 0
        for j in range(GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done


def merge(mat, done):
    for i in range(GRID_LEN):
        for j in range(GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                done = True
    return mat, done


def down(game):
    print("down")
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    return game, done


def up(game):
    print("up")
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    return game, done


def left(game):
    print("left")
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    return game, done


def right(game):
    print("right")
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    return game, done


def gen():
    return random.randint(0, GRID_LEN - 1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048 by Deepak Meena')
        self.master.bind("<Key>", self.key_down)

        self.commands = {
            KEY_UP: up,
            KEY_DOWN: down,
            KEY_LEFT: left,
            KEY_RIGHT: right,
        }

        self.grid_cells = []
        self.init_grid()
        self.matrix = new_game(GRID_LEN)
        self.update_grid_cells()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME,
                           width=SIZE, height=SIZE)
        background.grid()

        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(
                    background,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    width=SIZE / GRID_LEN,
                    height=SIZE / GRID_LEN
                )
                cell.grid(
                    row=i,
                    column=j,
                    padx=GRID_PADDING,
                    pady=GRID_PADDING
                )
                t = Label(
                    master=cell,
                    text="",
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=FONT,
                    width=5,
                    height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(
                        text=str(new_number),
                        bg=BACKGROUND_COLOR_DICT[new_number],
                        fg=CELL_COLOR_DICT[new_number]
                    )
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        if key == KEY_QUIT:
            exit()
        if key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                # record last move
                self.update_grid_cells()
                if game_state(self.matrix) == 'win':
                    print("You Win!")
                    sleep(5)
                    end = time()
                    print('time:', round(end - start, 2), 'seconds')
                    sys.exit()
                if game_state(self.matrix) == 'lose':
                    print("You Lose!")
                    sleep(5)
                    end = time()
                    print('time:', round(end - start, 2), 'seconds')
                    sys.exit()

    def generate_next(self):
        index = (gen(), gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (gen(), gen())
        self.matrix[index[0]][index[1]] = 2


start = time()
game_grid = GameGrid()
