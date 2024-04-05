import math
import time

class Node:
    def __init__(self, ul, ur, dl, dr, num, level, hashcode):
        self.ul = ul            #upper left cell
        self.ur = ur            #upper right cell
        self.dl = dl            #down left cell
        self.dr = dr            #down right cell
        self.num = num          #number of living cells
        self.level = level      #level of the node
        self.hash = hashcode    #hash of the node
    def __hash__(self):
        return self.hash

live = Node(None, None, None, None, 1, 0, 2)
dead = Node(None, None, None, None, 0, 0, 1)
calculated = {}
row_num = 64
col_num = 64

def combine(ul, ur, dl, dr):
    num = ul.num + ur.num + dl.num + dr.num
    level = ul.level + 1
    hashcode = ((14621 * ul.hash + 33889 * ur.hash + 26921 * dl.hash + 41413 * dr.hash)
            % (pow(2, 31) - 1))
    return Node(ul, ur, dl, dr, num, level, hashcode)

def rule(ul, u, ur, ml, m, mr, dl, d, dr):
    counter = ul.num + u.num + ur.num + ml.num + mr.num + dl.num + d.num + dr.num
    if counter == 3:
        return live
    elif counter == 2:
        return m
    return dead

def get_empty(level):
    if level == 0:
        return dead
    else:
        temp = get_empty(level - 1)
        return combine(temp, temp, temp, temp)

def step(m):
    '''if m.num == 0:
        return m.dl'''
    if hash(m) in calculated:
        return calculated[hash(m)]
    elif m.level == 2:
        ul = rule(m.ul.ul, m.ul.ur, m.ur.ul,
                  m.ul.dl, m.ul.dr, m.ur.dl,
                  m.dl.ul, m.dl.ur, m.dr.ul)
        ur = rule(m.ul.ur, m.ur.ul, m.ur.ur,
                  m.ul.dr, m.ur.dl, m.ur.dr,
                  m.dl.ur, m.dr.ul, m.dr.ur)
        dl = rule(m.ul.dl, m.ul.dr, m.ur.dl,
                  m.dl.ul, m.dl.ur, m.dr.ul,
                  m.dl.dl, m.dl.dr, m.dr.dl)
        dr = rule(m.ul.dr, m.ur.dl, m.ur.dr,
                  m.dl.ur, m.dr.ul, m.dr.ur,
                  m.dl.dr, m.dr.dl, m.dr.dr)
        result = combine(ul, ur, dl, dr)
    else:
        ul = step(m.ul)
        u = step(combine(m.ul.ur, m.ur.ul, m.ul.dr, m.ur.dl))
        ur = step(m.ur)
        ml = step(combine(m.ul.dl, m.ul.dr, m.dl.ul, m.dl.ur))
        M = step(combine(m.ul.dr, m.ur.dl, m.dl.ur, m.dr.ul))
        mr = step(combine(m.ur.dl, m.ur.dr, m.dr.ul, m.dr.ur))
        dl = step(m.dl)
        d = step(combine(m.dl.ur, m.dr.ul, m.dl.dr, m.dr.dl))
        dr = step(m.dr)
        result = combine( combine(ul.dr, u.dl, ml.ur, M.ul),
                          combine(u.dr, ur.dl, M.ur, mr.ul),
                          combine(ml.dr, M.dl, dl.ur, d.ul),
                          combine(M.dr, mr.dl, d.ur, dr.ul))
    calculated[hash(m)] = result
    return result

def change_cell_state(m, x, y):
    if m.level == 0:
        return live if m.num == 0 else dead
    else:
        side = pow(2, m.level - 1)
        x_remain = x % side
        y_remain = y % side
        if x // side == 0 and y // side == 0:
            return combine(change_cell_state(m.ul, x_remain, y_remain), m.ur, m.dl, m.dr)
        elif x // side == 1 and y //side == 0:
            return combine(m.ul, change_cell_state(m.ur, x_remain, y_remain), m.dl, m.dr)
        elif x // side == 0 and y //side == 1:
            return combine(m.ul, m.ur, change_cell_state(m.dl, x_remain, y_remain), m.dr)
        elif x // side == 1 and y // side == 1:
            return combine(m.ul, m.ur, m.dl, change_cell_state(m.dr, x_remain, y_remain))

def to_list(m):
    if m.level == 0:
        return [['_']] if m.num == 0 else [['#']]
    else:
        result = []
        for i in range(0, pow(2, m.level - 1)):
            result.append(to_list(m.ul)[i] + to_list(m.ur)[i])
        for i in range(0, pow(2, m.level - 1)):
            result.append(to_list(m.dl)[i] + to_list(m.dr)[i])
        return result

if __name__ == '__main__':
    while(True):
        print('Input the filename or type "QUIT" to stop:')
        filename = input()
        if filename == 'QUIT':
            break
        
        input_file = open(filename, mode="r", encoding="utf-8")
        line = input_file.readline()
        col_num = int(input_file.readline()[:-1])
        row_num = int(input_file.readline()[:-1])
        level = math.log2(max(col_num, row_num))
        level = int(level) + 1 if level == int(level) else int(level) + 2
        node = get_empty(level)
        
        line = input_file.readline()
        while line != '//END\n':
            element = line[:-1].split(' ')
            node = change_cell_state(node, pow(2, level - 2) + int(element[1]),
                              pow(2, level - 2) + int(element[0]))
            line = input_file.readline()
        
        print('Input number of steps')
        step_num = int(input())
        start = time.perf_counter()
        for i in range(0, step_num):
            node = step(node)
            temp = get_empty(level - 2)
            node = combine( combine(temp, temp, temp, node.ul),
                            combine(temp, temp, node.ur, temp),
                            combine(temp, node.dl, temp, temp),
                            combine(node.dr, temp, temp, temp))
        end = time.perf_counter()
        print(end - start)