import random
import time

life = set()            #set of live cells
life_counter = {}       #counter of cells
row_num = 1000          #row number of the canvas
col_num = 1000          #column number of the canvas
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
    if -2 <= y <= row_num + 1 and -2 <= x <= col_num + 1:
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
    cells_to_be_updated = []
    for i, j in life_counter:
        state = True if (i, j) in life else False
        if rule(life_counter[(i, j)], state):
            cells_to_be_updated.append((i, j, not state))
    for i, j, k in cells_to_be_updated:
        enlighten_unit(i, j, k)
        
if __name__ == '__main__':
    while(True):
        print('Input the filename or type "QUIT" to stop:')
        filename = input()
        if filename == 'QUIT':
            break
        
        input_file = open(filename, mode="r", encoding="utf-8")
        line = input_file.readline()
        row_num = int(input_file.readline()[:-1])
        col_num = int(input_file.readline()[:-1])
        
        line = input_file.readline()
        while line != '//END\n':
            element = line[:-1].split(' ')
            enlighten_unit(int(element[0]), int(element[1]))
            line = input_file.readline()
        
        print('Input number of steps')
        step_num = int(input())
        start = time.perf_counter()
        for i in range(0, step_num):
            step_life()
        end = time.perf_counter()
        print(end - start)