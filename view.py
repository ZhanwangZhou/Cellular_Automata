import tkinter as tk
import gameoflife
import threading, os.path, copy
from tkinter import BOTH, HORIZONTAL, LEFT
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showerror

life_initial_state = set()  #list of initial states of all units
initialized = 0             #whether the window is being initialized

running = False             #whether the simulation is running
drawing = True              #whether the user is drawing
have_run = False            #whether the simulation have run

window_height = 700         #height of the window
window_width = 700          #width of the window
unit_length = 10.0          #length of a single unit

unit_drawn = []             #tuple of x and y of units drawn in one mouse motion
co_x = 0                    #x coordinate of the field
co_y = 0                    #y coordinate of the field

step_num = 0                #number of steps simulated
delay = 125                 #delayed time of animation in millisecond

view_proportion = 1

#Initialize Window
window = tk.Tk()
window.title('Cellular Automata')
window.geometry('717x717')
window.iconbitmap(bitmap=r'icons/icon2.ico')

canvas = tk.Canvas(window, width=700,height=700,bg="#222222")




def thread_func(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

def save_initial_state():
    global life_initial_state
    if life_initial_state == set():
        life_initial_state = copy.deepcopy(gameoflife.life)

def read_initial_state():
    global running, step_num, drawing
    running = False
    drawing = True
    step_num = 0
    gameoflife.initialize_life()
    if life_initial_state != set():
        gameoflife.life = copy.deepcopy(life_initial_state)
        for i, j in life_initial_state:
            gameoflife.enlighten_unit(i, j)
    life_initial_state.clear()

def run_and_stop():
    global running, have_run, drawing
    if running:
        running = False
        drawing = True
    else:
        running = True

def reset(rate=0):
    global life_initial_state, running, drawing, step_num
    running = False
    drawing = True
    life_initial_state = set()
    step_num = 0
    gameoflife.initialize_life(rate)

def run():
    global step_num
    save_initial_state()
    thread_func(gameoflife.step_life)
    step_num += 1

def step():
    global running, drawing
    run()
    drawing = True
    running = False

def zoom(temp, x, y):
    global unit_length, co_x, co_y, drawing, window_height, window_width, view_proportion
    window_height = window.winfo_height()
    window_width = window.winfo_width()
    drawing = True
    if temp > 0:
        unit_length *= 2
    else:
        unit_length /= 2
    co_x = (window_width - unit_length * gameoflife.col_num) / 2
    co_y = (window_height - unit_length * gameoflife.row_num) / 2
    view_proportion =  gameoflife.row_num * unit_length / canvas.winfo_height()

def set_delay(temp: int):
    global delay, drawing
    drawing = True
    if temp < 0:
        delay = (2 * delay if delay != 50 else 125)
    else:
        if delay == 125:
            delay =50
        else:
            delay = (25 if delay == 25 else int(delay / 2))

def set_mode(m):
    gameoflife.change_mode(m)
    read_initial_state()

def view_move(command: str):
    global co_x, co_y, drawing
    drawing = True
    if co_x < 0 and command == 'left':
        co_x += 20
    if co_x + gameoflife.col_num * unit_length > window_width and command == 'right':
        co_x -= 20
    if co_y < 0 and command == 'up':
        co_y += 20
    if co_y + gameoflife.row_num * unit_length > window_height and command == 'down':
        co_y -= 20

def mouseclick(x, y):
    global unit_drawn, drawing
    unit_drawn = []
    drawing = True
    width = int((x - co_x)/unit_length)
    height = int((y - co_y)/unit_length)
    if gameoflife.row_num > height >=0 and gameoflife.col_num > width >= 0:
        gameoflife.enlighten_unit(height, width, (height, width) not in gameoflife.life)

def mousemotion(x, y):
    global unit_drawn, drawing
    drawing = True
    width = int((x - co_x)/unit_length)
    height = int((y - co_y)/unit_length)
    if (width, height) not in unit_drawn and gameoflife.row_num > height >= 0 and gameoflife.col_num > width >= 0:
        unit_drawn.append((width, height))
        gameoflife.enlighten_unit(height, width, (height, width) not in gameoflife.life)

def refresh_window():
    global window_height, window_width, drawing, unit_length, co_x, co_y, view_proportion
    drawing = True
    window_height = canvas.winfo_height()
    window_width = canvas.winfo_width()
    unit_length = min(window_height/gameoflife.row_num, window_width/gameoflife.col_num)
    co_x = (window_width - unit_length * gameoflife.col_num) / 2
    co_y = (window_height - unit_length * gameoflife.row_num) / 2
    view_proportion = gameoflife.row_num * unit_length / canvas.winfo_height()

def set_unit_num(height, width):
    gameoflife.set_canvas_size(height, width)
    reset()
    refresh_window()

def write_file(temp=False):
    global life_initial_state, running
    running = False
    if temp:
        life_initial_state = set()
    save_initial_state()
    filename = asksaveasfilename(defaultextension='.cellauto', filetypes=[('Cell Automata files', '.cellauto')])
    if os.path.isfile(filename):
        os.remove(filename)
    temp = open(filename, mode="w", encoding="utf-8")
    temp.write('//CELL AUTOMATA FILE\n')
    temp.write(str(gameoflife.row_num) + '\n')
    temp.write(str(gameoflife.col_num) + '\n')
    for i, j in life_initial_state:
        temp.write(str(i) + ' ' + str(j) + '\n')
    temp.write('//END\n')
    temp.close()

def read_file():
    global running, life_initial_state
    running = False
    try:
        filename = askopenfilename(defaultextension='.cellauto', filetypes=[('Cell Automata files', '.cellauto')])
        temp = open(filename, mode="r", encoding="utf-8")
        line = temp.readline()
        if line == '//CELL AUTOMATA FILE\n':
            height = int(temp.readline()[:-1])
            width = int(temp.readline()[:-1])
            set_unit_num(height, width)
            line = temp.readline()
            while line != '//END\n':
                element = line[:-1].split(' ')
                life_initial_state.add((int(element[0]), int(element[1])))
                line = temp.readline()
            read_initial_state()
        else:
            raise Exception
    except:
        showerror(message='Failed to Read')
    finally:
        temp.close()
    

def input_unit_num():
    global running
    input_window = tk.Toplevel(window)
    input_window.resizable(0, 0)
    input_window.title('Input Unit Number')
    running = False
    window.withdraw()
    #Set Frames
    frame = tk.Frame(input_window)
    frame.pack()
    frame_left = tk.Frame(frame)
    frame_right = tk.Frame(frame)
    frame_left.pack(side='left')
    frame_right.pack(side='right')
    frame_right_left = tk.Frame(frame_right)
    frame_right_right = tk.Frame(frame_right)
    frame_right_left.pack(side='left')
    frame_right_right.pack(side='right')
    #Set Labels
    tk.Label(frame_left, text='Width:').pack()
    tk.Label(frame_left, text='Height:').pack()
    #Read width
    width = tk.IntVar()
    input_width = tk.Entry(frame_right_right, textvariable=width, width=4)
    tk.Scale(frame_right_left, from_=0, to=1000, resolution=1, length=200, troughcolor='white',
             showvalue=0, orient=HORIZONTAL, variable=width).pack()
    width.set(gameoflife.col_num)
    input_width.pack()
    #Read Height
    height = tk.IntVar()
    input_height = tk.Entry(frame_right_right, textvariable=height, width=4)
    tk.Scale(frame_right_left, from_=0, to=1000, resolution=1, length=200, troughcolor='white',
             showvalue=0, orient=HORIZONTAL, variable=height).pack()
    height.set(gameoflife.row_num)
    input_height.pack()
    #Set Buttons
    def action_confirm():
        window.deiconify()
        input_window.destroy()
        set_unit_num(height.get(), width.get())
    confirm_button = tk.Button(input_window, text='Confirm', width=19, command=action_confirm)
    confirm_button.pack(side='right')
    def action_cancel():
        window.deiconify()
        input_window.destroy()
    cancel_button = tk.Button(input_window, text='Cancel', width=19, command=action_cancel)
    cancel_button.pack(side='left')
    input_window.protocol('WM_DELETE_WINDOW', action_cancel)
    input_window.mainloop()

#Read Rule Number of Sierpinski Triangle
def input_rule_num():
    global running
    input_window = tk.Toplevel(window)
    input_window.resizable(0, 0)
    input_window.title('Input Rule Number')
    running = False
    window.withdraw()
    #Set Frames
    frame = tk.Frame(input_window)
    frame.pack()
    frame_left = tk.Frame(frame)
    frame_right = tk.Frame(frame)
    frame_left.pack(side='left')
    frame_right.pack(side='right')
    frame_right_left = tk.Frame(frame_right)
    frame_right_right = tk.Frame(frame_right)
    frame_right_left.pack(side='left')
    frame_right_right.pack(side='right')
    #Set Labels
    tk.Label(frame_left, text='Rule ').pack()
    #Read rule
    rule = tk.IntVar()
    input_rule = tk.Entry(frame_right_left, textvariable=rule, width=4)
    rule.set(30)
    #Set Canvas
    input_canvas = tk.Canvas(input_window, width=280,height=36,bg="#ffffff")
    temp1 = [0,0,1,1,1,0,1,1,2,0,1,2,1,0,1,2,2,0,2,1,1,0,2,1,2,0,2,2,1,0,2,2,2,0,0]
    def display_input_canvas():
        temp2 = '%08d' % int(bin(rule.get())[2:])
        for i in range(len(temp1)):
            if temp1[i] == 1:
                input_canvas.create_polygon(i * 8, 8,
                                      i * 8, 16,
                                      i * 8 + 8, 16,
                                      i * 8 + 8, 8,
                                      outline='#888888', fill='black')
            if temp1[i] == 2:
                input_canvas.create_polygon(i * 8, 8,
                                      i * 8, 16,
                                      i * 8 + 8, 16,
                                      i * 8 + 8, 8,
                                      outline='#888888', fill='white')
        for i in range(len(temp2)):
            if temp2[i] == '1':
                input_canvas.create_polygon(i * 32 + 24, 20,
                                      i * 32 + 24, 28,
                                      i * 32 + 32, 28,
                                      i * 32 + 32, 20,
                                      outline='#888888', fill='black')
            if temp2[i] == '0':
                input_canvas.create_polygon(i * 32 + 24, 20,
                                      i * 32 + 24, 28,
                                      i * 32 + 32, 28,
                                      i * 32 + 32, 20,
                                      outline='#888888', fill='white')
        input_canvas.pack()
    input_rule.bind('<Return>', lambda event: display_input_canvas())
    input_rule.pack()
    scale = tk.Scale(frame_right_right, from_=0, to=255, resolution=1, length=200, troughcolor='white',
             showvalue=0, orient=HORIZONTAL, variable=rule)
    scale.bind('<ButtonRelease>', lambda event: display_input_canvas())
    scale.pack()
    display_input_canvas()
    #Set Buttons
    def action_confirm():
        window.deiconify()
        input_window.destroy()
        set_mode(rule.get())
    confirm_button = tk.Button(input_window, text='Confirm', width=19, command=action_confirm)
    confirm_button.pack(side='right')
    def action_cancel():
        window.deiconify()
        input_window.destroy()
    cancel_button = tk.Button(input_window, text='Cancel', width=19, command=action_cancel)
    cancel_button.pack(side='left')
    input_window.protocol('WM_DELETE_WINDOW', action_cancel)
    input_window.mainloop()


#Setting Menubar
menubar = tk.Menu(window)

filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', accelerator='Ctrl+O', command=read_file)
filemenu.add_command(label='Save Initial', accelerator='Ctrl+S', command=write_file)
filemenu.add_command(label='Save Current', accelerator='Ctrl+Shift+S', command=lambda: write_file(True))

imagemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Canvas', menu=imagemenu)
imagemenu.add_command(label='Clear', accelerator='Ctrl+Tab', command=reset)
imagemenu.add_command(label='Random', command=lambda: reset(0.2))
imagemenu.add_command(label='Turn Back', command=read_initial_state)
unitnummenu = tk.Menu(imagemenu, tearoff=0)
imagemenu.add_cascade(label='Set Unit Number', menu=unitnummenu)
unitnummenu.add_command(label='50x50', command=lambda:set_unit_num(50, 50))
unitnummenu.add_command(label='100x100', command=lambda:set_unit_num(100, 100))
unitnummenu.add_command(label='200x200', command=lambda:set_unit_num(200, 200))
unitnummenu.add_command(label='400x400', command=lambda:set_unit_num(400, 400))
unitnummenu.add_command(label='Customize', command=input_unit_num)

viewmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=viewmenu)
zoommenu = tk.Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label='Zoom', menu=zoommenu)
zoommenu.add_command(label='Zoom In', command=lambda:zoom(1, window_width/2, window_height/2))
zoommenu.add_command(label='Zoom Out', command=lambda:zoom(-1, window_width/2, window_height/2))
viewmenu.add_command(label='Fit Pattern', accelerator='Ctrl+F', command=refresh_window)

runmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Control', menu=runmenu)
runmenu.add_command(label='Run/Stop', accelerator='Space', command=run_and_stop)
runmenu.add_command(label='Step', accelerator='Return', command=step)
runmenu.add_command(label='Faster', accelerator=']', command=lambda: set_delay(1))
runmenu.add_command(label='Slower', accelerator='[', command=lambda: set_delay(-1))

modemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Mode', menu=modemenu)
modemenu.add_command(label='Game of Life 1', command=lambda: set_mode('Game of Life 1'))
modemenu.add_command(label='Game of Life 2', command=lambda: set_mode('Game of Life 2'))
modemenu.add_command(label='Rule 30', command=lambda: set_mode(30))
modemenu.add_command(label='Rule 90', command=lambda: set_mode(90))
modemenu.add_command(label='Rule 110', command=lambda: set_mode(110))
modemenu.add_command(label='Customize Rule', command=input_rule_num)

window.config(menu=menubar)

#Setting Mouse and Keyboard Event
canvas.bind("<ButtonRelease>", lambda event: mouseclick(event.x, event.y))
canvas.bind("<B1-Motion>", lambda event: mousemotion(event.x, event.y))
canvas.bind("<MouseWheel>", lambda event: zoom(event.delta, event.x, event.y))
window.bind("<Control-s>", lambda event: write_file())
window.bind("<Control-S>", lambda event: write_file(True))
window.bind("<Control-o>", lambda event: read_file())
window.bind("<Control-Tab>", lambda event: reset())
window.bind("<Control-f>", lambda event: refresh_window())
window.bind("<space>", lambda event: run_and_stop())
window.bind("<Return>", lambda event: step())
window.bind("<Left>", lambda event: view_move('left'))
window.bind("<Right>", lambda event: view_move('right'))
window.bind("<Up>", lambda event: view_move('up'))
window.bind("<Down>", lambda event: view_move('down'))
window.bind("<]>", lambda event: set_delay(1))
window.bind("<[>", lambda event: set_delay(-1))


def initialize():
    global initialized
    if initialized < 5:
        initialized += 1
        refresh_window()

def display():
    global canvas, rectangle_list
    canvas.delete('all')
    canvas.create_polygon(co_x, co_y,
                          co_x, co_y + gameoflife.row_num * unit_length,
                          co_x + gameoflife.col_num * unit_length, co_y + gameoflife.row_num * unit_length,
                          co_x + gameoflife.col_num * unit_length, co_y,
                          outline='white', fill='black')
    for j, i in gameoflife.life:
        canvas.create_polygon(i*unit_length + co_x, j*unit_length + co_y,
                            (i+1)*unit_length + co_x, j*unit_length + co_y,
                            (i+1)*unit_length + co_x, (j+1)*unit_length + co_y,
                            i*unit_length + co_x, (j+1)*unit_length + co_y,
                            outline='#888888', fill='white')
    text_content = 'Population=' + str(len(gameoflife.life)) + '\tStep Num=' + str(step_num) + '\tDelay=' + str(delay)
    if type(gameoflife.mode) == int:
        text_content += '\tMode: Rule ' + str(gameoflife.mode)
    else:
        text_content += '\tMode: ' + gameoflife.mode
    #if maximized:
    if view_proportion > 1:
        w = gameoflife.col_num * 60 / gameoflife.row_num
        cw = unit_length * gameoflife.col_num
        ch = unit_length * gameoflife.row_num
        canvas.create_line(canvas.winfo_width() - 100, canvas.winfo_height() - 100,
                           canvas.winfo_width() - 100, canvas.winfo_height() - 40, fill='#888888')
        canvas.create_line(canvas.winfo_width() - 100, canvas.winfo_height() - 100,
                           canvas.winfo_width() - 100 + w, canvas.winfo_height() - 100, fill='#888888')
        canvas.create_line(canvas.winfo_width() - 100 + w, canvas.winfo_height() - 40,
                           canvas.winfo_width() - 100, canvas.winfo_height() - 40, fill='#888888')
        canvas.create_line(canvas.winfo_width() - 100 + w, canvas.winfo_height() - 40,
                           canvas.winfo_width() - 100 + w, canvas.winfo_height() - 100, fill='#888888')
        canvas.create_line(canvas.winfo_width()-100-co_x*w/cw, canvas.winfo_height()-100-co_y*60/ch,
                           canvas.winfo_width()-100+(canvas.winfo_width()-co_x)*w/cw, canvas.winfo_height()-100-co_y*60/ch,
                           fill='white')
        canvas.create_line(canvas.winfo_width()-100-co_x*w/cw, canvas.winfo_height()-100-co_y*60/ch,
                           canvas.winfo_width()-100-co_x*w/cw, canvas.winfo_height()-100+(canvas.winfo_height()-co_y)*60/ch,
                           fill='white')
        canvas.create_line(canvas.winfo_width()-100+(canvas.winfo_width()-co_x)*w/cw, canvas.winfo_height()-100+(canvas.winfo_height()-co_y)*60/ch,
                           canvas.winfo_width()-100-co_x*w/cw, canvas.winfo_height()-100+(canvas.winfo_height()-co_y)*60/ch,
                           fill='white')
        canvas.create_line(canvas.winfo_width()-100+(canvas.winfo_width()-co_x)*w/cw, canvas.winfo_height()-100+(canvas.winfo_height()-co_y)*60/ch,
                           canvas.winfo_width()-100+(canvas.winfo_width()-co_x)*w/cw, canvas.winfo_height()-100-co_y*60/ch,
                           fill='white')
        canvas.create_text(canvas.winfo_width()-100+w/2, canvas.winfo_height()-30, text='1:%.1f' %view_proportion,font=('consolas', 10),
                           fill='#888888')
    
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()-15, text=text_content, font=('consolas', 10),
                       fill='#888888')
    canvas.pack(side=LEFT,expand=True,fill=BOTH)

def repeater(root):
    global drawing
    #update_window()
    initialize()
    if running:
        display()
        run()
        root.after(delay, repeater, root)
    else:
        if drawing or initialized < 5:
            display()
            drawing = False
        root.after(100, repeater, root)
