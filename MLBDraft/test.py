import Game
import pybaseball as pyb
from tkinter import ttk
from tkinter import *
import pandas as pd
import sv_ttk
    
def main():

    while True:
        inputs = [3, "MLB", "ERA", 1980, 2024, '#39957b', "#1c1c1c", 'yellow', True]

        if inputs[0] == 2:
            names = ['Player 1', 'Player 2']
        elif inputs[0] == 3:
            names = ['Player 1', 'Player 2', 'Player 3']
        else:
            names = ['Player 1', 'Player 2', 'Player 3', 'Player 4']

        root = Tk()
        sv_ttk.set_theme('dark')
        game = Game.Game(root, inputs, names)

        print("Made it to the end")

        if game.exit:
            break
        elif game.play_again:
            continue

        root.destroy()
    
    return

main()



