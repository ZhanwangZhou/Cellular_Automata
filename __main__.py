import view
import gameoflife
import ctypes

if __name__ == '__main__':
    '''whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)'''
    gameoflife.initialize_life()
    view.repeater(view.window)
    view.window.mainloop()