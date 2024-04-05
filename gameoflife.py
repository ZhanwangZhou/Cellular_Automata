import random

life = set()            #set of live cells
life_counter = {}       #counter of cells
row_num = 64            #row number of the canvas
col_num = 64            #column number of the canvas
mode = 'Game of Life 2' #mode of cellular automata


def add_counter(y: int, x: int, count: int):
    '''
    Add count to counter to cell at (y, x)
    '''
    if (y, x) not in life_counter:
        life_counter[(y, x)] = 0
    life_counter[(y, x)] += count
    if life_counter[(y, x)] == 0 and (y, x) not in life:
        life_counter.pop((y, x))

def enlighten_unit(y, x, enlighten=True):
    '''
    Set a dead cell to live or a live cell to dead
    Modify life_counter of surrounding cells
    '''
    global life, life_counter
    if type(mode) == int:
        if y >= row_num:
            return 1
        if enlighten:
            life.add((y, x))
            add_counter(y+1, x-1, 1)
            add_counter(y+1, x, 2)
            add_counter(y+1, x+1, 4)
        else:
            life.remove((y, x))
            add_counter(y+1, x-1, -1)
            add_counter(y+1, x, -2)
            add_counter(y+1, x+1, -4)
    elif mode == 'Game of Life 1':
        if enlighten:
            life.add((y, x))
            add_counter(y-1, x-1, 1)
            add_counter(y-1, x, 1)
            add_counter(y-1, x+1, 1)
            add_counter(y, x-1, 1)
            add_counter(y, x, 0)
            add_counter(y, x+1, 1)
            add_counter(y+1, x-1, 1)
            add_counter(y+1, x, 1)
            add_counter(y+1, x+1, 1)
        else:
            life.remove((y, x))
            add_counter(y-1, x-1, -1)
            add_counter(y-1, x, -1)
            add_counter(y-1, x+1, -1)
            add_counter(y, x-1, -1)
            add_counter(y, x, 0)
            add_counter(y, x+1, -1)
            add_counter(y+1, x-1, -1)
            add_counter(y+1, x, -1)
            add_counter(y+1, x+1, -1)
    elif mode == 'Game of Life 2':
        if enlighten:
            life.add((y, x))
            add_counter((y-1)%row_num, (x-1)%col_num, 1)
            add_counter((y-1)%row_num, x, 1)
            add_counter((y-1)%row_num, (x+1)%col_num, 1)
            add_counter(y, (x-1)%col_num, 1)
            add_counter(y, x, 0)
            add_counter(y, (x+1)%col_num, 1)
            add_counter((y+1)%row_num, (x-1)%col_num, 1)
            add_counter((y+1)%row_num, x, 1)
            add_counter((y+1)%row_num, (x+1)%col_num, 1)
        else:
            life.remove((y, x))
            add_counter((y-1)%row_num, (x-1)%col_num, -1)
            add_counter((y-1)%row_num, x, -1)
            add_counter((y-1)%row_num, (x+1)%col_num, -1)
            add_counter(y, (x-1)%col_num, -1)
            add_counter(y, x, 0)
            add_counter(y, (x+1)%col_num, -1)
            add_counter((y+1)%row_num, (x-1)%col_num, -1)
            add_counter((y+1)%row_num, x, -1)
            add_counter((y+1)%row_num, (x+1)%col_num, -1)
        

def initialize_life(rate=0):
    '''
    Reset the canvas with random live cells
    The proportion of live cell equal to rate
    '''
    global life
    life = set()
    life_counter.clear()
    for i in range(row_num):
        for j in range(col_num):
            if random.random() < rate:
                enlighten_unit(i, j)

def set_canvas_size(y: int, x: int):
    '''
    Set row and column number of the canvas
    '''
    global row_num, col_num
    if 1000 >= y >= 3:
        row_num = y
    if 1000 >= x >= 3:
        col_num = x

def change_mode(m):
    '''
    Change mode of cellular automata
    int for Sierpinski Triangle, string for Conway's Game of Life
    '''
    global mode
    if type(m) == int or m in ('Game of Life 1', 'Game of Life 2'):
        mode = m

def rule(num: int, state: bool)->bool:
    '''
    Return whether state of the cell need to be updated
    "state" is whether the cell is live or dead
    "num" is counter stored in "live_cell"
    '''
    if type(mode) == int:
        temp = '%08d' % int(bin(mode)[2:])
        if temp[7-num] == '1':
            return not state
        else:
            return state
    elif mode in ('Game of Life 2', 'Game of Life 1'):
        if num == 3:
            return not state
        elif num == 2:
            return False
        else:
            return state

def step_life():
    '''
    Simulate one step
    '''
    global life, life_counter
    cells_to_be_updated = []
    for i, j in life_counter:
        state = True if (i, j) in life else False
        if rule(life_counter[(i, j)], state):
            cells_to_be_updated.append((i, j, not state))
    for i, j, k in cells_to_be_updated:
        enlighten_unit(i, j, k)
    