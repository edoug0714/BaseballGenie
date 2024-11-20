from tkinter import *

def throw_error(error_label, message, row = 0):
    error_label.config(text = message)
    error_label.grid(row = row, column = 0, padx = 5, pady = 5)

def quit(root):
    root.destroy()

def on_close(var, root):
    print('On close called')
    var.append(-1)

    quit(root)
    