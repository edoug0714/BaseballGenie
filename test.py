import Game
import gameSetup
import playerNames
import pybaseball as pyb
from tkinter import ttk
from tkinter import *
import pandas as pd
import sv_ttk
    
def main():

    while True:
        inputs = [2, "ALW", "H", 2020, 2024]
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
    data = pd.read_csv("C:\\Users\edoug\Code\Python\MLBDraft\merged_batter_data.csv").fillna(0)
    data.drop(columns=data.columns[0], axis=1, inplace=True)

    year = 1965
    franchise = 'LAA'

    #player_data = data[(data['Season'] == year) & (data['Name'] == name)]
    #player_data = player_data[player_data['G_by_pos'] / player_data['G'] >= 0.2]

    player_data = data[(data['Season'] == year) & (data['Franchise'] == franchise)]
    print(player_data)

    #pos = player_data['Pos'].tolist()

    #if (len(pos) == 0) or (pos == ['P']):
        #pos = ['DH']
    

    

#main()
#test()
test1()

