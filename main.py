import gameSetup
import playerNames
import Game
from tkinter import *

CURR_YEAR = 2024
STATS_LIST = ["WAR", "Batter WAR", "Pitcher WAR"]

def main():
    while True:
        inputs = gameSetup.gameSetup()
        if inputs[0] == -1:
            break
        names = playerNames.playerNames(inputs)
        if names[0] == -1:
            break

        root = Tk()
        game = Game.Game(root, inputs, names)

        print("Made it to the end")

        if game.exit:
            break
        elif game.play_again:
            continue

        root.destroy()
    
    return

main()

