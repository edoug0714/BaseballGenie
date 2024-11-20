from tkinter import *
import playerNames
import gameSetup
import sv_ttk
import Game
import os
import sys

CURR_YEAR = 2024
REQUIRED_FILES = ['Game.py', 'gameSetup.py', 'helper.py', 'playerNames.py', 'merged_batter_data.csv', 'merged_pitcher_data.csv', 'season_name_batters.csv', 'season_name_pitchers.csv']


def check_files():
    curr = os.path.dirname(os.path.abspath(__file__))
    missing_files = [file for file in REQUIRED_FILES if not os.path.isfile(os.path.join(curr, file))]
    if missing_files:
        print(f"Error: The following required files are missing: {', '.join(missing_files)}")
        sys.exit(1)

def main():
    root = Tk()
    sv_ttk.set_theme('dark')
    window_destroy = False
    while True:
        print('NEW GAME!')
        inputs = gameSetup.gameSetup(root)
        if inputs[0] == -1:
            window_destroy = True
            break
        names = playerNames.playerNames(root, inputs)
        if names[0] == -1:
            window_destroy = True
            break
        game = Game.Game(root, inputs, names)

        print("Made it to the end")

        if game.exit:
            break
        elif game.play_again:
            continue

    if window_destroy:
        return
    else:
        root.destroy()
        return

check_files()
main()



