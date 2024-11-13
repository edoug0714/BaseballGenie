import Game
import gameSetup
import playerNames
import pybaseball as pyb
from tkinter import ttk
from tkinter import *
import sv_ttk
    
def main():

    while True:
        inputs = [2, "ALW", "W", 2020, 2024]
        #inputs = gameSetup.gameSetup()
        #if inputs[0] == -1:
            #break

        names = ['Player 1', 'Player 2']
        #names = playerNames.playerNames(inputs)
        #if names[0] == -1:
            #break

        root = Tk()
        game = Game.Game(root, inputs, names)

        print("Made it to the end")

        if game.exit:
            break
        elif game.play_again:
            continue

        root.destroy()
    
    return
    
def test():
    season_pitching_stats = pyb.pitching_stats(2024, qual = 1)
    season_pitching_stats.to_csv('output.csv')

def test1():
    root = Tk()
    root.geometry("300x200")

    # Apply the theme
    sv_ttk.set_theme("dark")  # Options: "dark" or "light"

    frame = ttk.Frame(root, borderwidth = 1)
    frame.pack()

    # Create a sample button to show the theme
    btn = ttk.Button(frame, text="Click Me")
    btn.pack(pady=20)

    root.mainloop()
    

main()
#test()
#test1()

