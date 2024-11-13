from tkinter import *
import sv_ttk
import ctypes

def throw_error(error_label, message, row = 0):
    error_label.config(text = message)
    error_label.grid(row = row, column = 0, padx = 5, pady = 5)

def quit(root):
    root.destroy()

def on_close(var, root, var2 = 0):
    print('Helper called')

    if isinstance(var2, bool):
        print('var2 exists')
        var2 = True

    if isinstance(var, list):
        var.append(-1)
    elif isinstance(var, bool):
        print('bool')
        var = True
    elif isinstance(var, BooleanVar):
        print('boolean')
        var.set(True)
        print('before destroy')
    else:
        print('else')
        var = -1

    print("returning")
    quit(root)
    #root.destroy()
    