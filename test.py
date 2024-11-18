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
        inputs = [2, "AL", "ERA", 1990, 2024]
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

def set_division(year, division):
    if division == "ALW":
        if (year < 1970):
            division = ['CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'SEA']
        elif (year > 1969) & (year < 1972):
            division = ['CAL', 'CHW', 'KCR', 'MIN', 'MIL', 'OAK']
        elif (year > 1971) & (year < 1977):
            division = ['CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'TEX']
        elif (year > 1976) & (year < 1994):
            division = ['CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'SEA', 'TEX']
        elif (year > 1993) & (year < 1997):
            division = ['CAL', 'OAK', 'SEA', 'TEX']
        elif (year > 1996) & (year < 2005):
            division = ['ANA', 'OAK', 'SEA', 'TEX']
        elif (year > 2004) & (year < 2013):
            division = ['LAA', 'OAK', 'SEA', 'TEX']
        elif (year > 2012):
            division = ['HOU', 'LAA', 'OAK', 'SEA', 'TEX']
    elif division == "ALC":
        if (year < 1998):
            division = ['CHW', 'CLE', 'KCR', 'MIL', 'MIN']
        elif (year > 1997):
            division = ['CHW', 'CLE', 'DET', 'KCR', 'MIN']
    elif division == "ALE":
        if (year < 1972):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'NYY', 'WAS']
        elif (year > 1971) & (year < 1977):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY']
        elif (year > 1976) & (year < 1994):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY', 'TOR']
        elif (year > 1993) & (year < 1998):
            division = ['BAL', 'BOS', 'DET', 'NYY', 'TOR']
        elif (year > 1997) & (year < 2008):
            division = ['BAL', 'BOS', 'NYY', 'TBD', 'TOR']
        elif (year > 2007):
            division = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR']
    elif division == "NLW":
        if (year < 1993):
            division = ['ATL', 'CIN', 'HOU', 'LAD', 'SDP', 'SFG']
        elif (year > 1992) & (year < 1994):
            division = ['ATL', 'CIN', 'COL', 'HOU', 'LAD', 'SDP', 'SFG']
        elif (year > 1993) & (year < 1998):
            division = ['COL', 'LAD', 'SDP', 'SFG']
        elif (year > 1997):
            division = ['ARI', 'COL', 'LAD', 'SDP', 'SFG']
    elif division == "NLC":
        if (year < 1998):
            division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
        if (year > 1997) & (year < 2013):
            division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
        if (year > 2012):
            division = ['CHC', 'CIN', 'MIL', 'PIT', 'STL']
    elif division == "NLE":
        if (year < 1993):
            division = ['CHC', 'MON', 'NYM', 'PHI', 'PIT', 'STL']
        elif (year > 1992) & (year < 1994):
            division = ['CHC', 'FLA', 'MON', 'NYM', 'PHI', 'PIT', 'STL']
        elif (year > 1993) & (year < 2005):
            division = ['ATL', 'FLA', 'MON', 'NYM', 'PHI']
        elif (year > 2004) & (year < 2012):
            division = ['ATL', 'FLA', 'NYM', 'PHI', 'WSN']
        elif (year > 2011):
            division = ['ATL', 'MIA', 'NYM', 'PHI', 'WSN']
    elif division == "AL":
        if (year < 1902):
            division = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'MIL', 'PHA', 'WAS']
        elif (year > 1901) & (year < 1903):
            division = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'PHA', 'SLB', 'WAS'] 
        elif (year > 1902) & (year < 1913):
            division = ['BOS', 'CHW', 'CLE', 'DET', 'NYH', 'PHA', 'SLB', 'WAS']
        elif (year > 1912) & (year < 1954):
            division = ['BOS', 'CHW', 'CLE', 'DET', 'NYY', 'PHA', 'SLB', 'WAS']
        elif (year > 1953) & (year < 1955):
            division = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'NYY', 'PHA', 'WAS']
        elif (year > 1954) & (year < 1961):
            division = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'KCA', 'NYY', 'WAS']
        elif (year > 1960) & (year < 1965):
            division = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'KCA', 'LAA', 'MIN', 'NYY', 'WAS']
        elif (year > 1964) & (year < 1968):
            division = ['BAL', 'BOS', 'CAL', 'CHW', 'CLE', 'DET', 'KCA', 'MIN', 'NYY', 'WAS'] 
        elif (year > 1967) & (year < 1969):
            division = ['BAL', 'BOS', 'CAL', 'CHW', 'CLE', 'DET', 'MIN', 'NYY', 'OAK', 'WAS']
        elif (year > 1968) & (year < 1970):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'NYY', 'WAS', 'CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'SEA']
        elif (year > 1969) & (year < 1972):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'NYY', 'WAS', 'CAL', 'CHW', 'KCR', 'MIN', 'MIL', 'OAK']
        elif (year > 1971) & (year < 1977):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY', 'CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'TEX']
        elif (year > 1976) & (year < 1997):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY', 'TOR', 'CAL', 'CHW', 'KCR', 'MIN', 'OAK', 'SEA', 'TEX']
        elif (year > 1996) & (year < 1998):
            division = ['BAL', 'BOS', 'DET', 'NYY', 'TOR', 'CHW', 'CLE', 'KCR', 'MIL', 'MIN', 'ANA', 'OAK', 'SEA', 'TEX']
        elif (year > 1997) & (year < 2005):
            division = ['BAL', 'BOS', 'NYY', 'TBD', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'ANA', 'OAK', 'SEA', 'TEX']
        elif (year > 2004) & (year < 2008):
            division = ['BAL', 'BOS', 'NYY', 'TBD', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'LAA', 'OAK', 'SEA', 'TEX']
        elif (year > 2007) & (year < 2013):
            division = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'LAA', 'OAK', 'SEA', 'TEX']
        elif (year > 2012):
            division = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'LAA', 'OAK', 'SEA', 'TEX']
    elif division == "NL":
        if year < 1903:
            division = ['BSN', 'BRO', 'CHI', 'CIN', 'NYG', 'PHI', 'PIT', 'STL']
        if (year > 1902) & (year < 1953):
            division = ['BSN', 'BRO', 'CHC', 'CIN', 'NYG', 'PHI', 'PIT', 'STL']
        if (year > 1952) & (year < 1958):
            division = ['BRO', 'CHC', 'CIN', 'MIL', 'NYG', 'PHI', 'PIT', 'STL']
        if (year > 1957) & (year < 1962):
            division = ['CHC', 'CIN', 'LAD', 'MIL', 'PHI', 'PIT', 'STL', 'SFG']
        if (year > 1961) & (year < 1966):
            division = ['CHC', 'CIN', 'HOU', 'LAD', 'MIL', 'PHI', 'NYM', 'PIT', 'STL', 'SFG']
        if (year > 1965) & (year < 1969):
            division = ['ATL', 'CHC', 'CIN', 'HOU', 'LAD', 'PHI', 'NYM', 'PIT', 'STL', 'SFG']
        if (year > 1968) & (year < 1993):
            division = ['CHC', 'MON', 'NYM', 'PHI', 'PIT', 'STL', 'ATL', 'CIN', 'HOU', 'LAD', 'SDP', 'SFG']
        if (year > 1992) & (year < 1994):
            division = ['CHC', 'FLA', 'MON', 'NYM', 'PHI', 'PIT', 'STL', 'ATL', 'CIN', 'COL', 'HOU', 'LAD', 'SDP', 'SFG']
        if (year > 1993) & (year < 1998):
            division = ['ATL', 'FLA', 'MON', 'NYM', 'PHI', 'CHC', 'CIN', 'HOU', 'PIT', 'STL', 'COL', 'LAD', 'SDP', 'SFG']
        if (year > 1997) & (year < 2005):
            division = ['ATL', 'FLA', 'MON', 'NYM', 'PHI', 'CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
        if (year > 2004) & (year < 2012):
            division = ['ATL', 'FLA', 'NYM', 'PHI', 'WSN', 'CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
        if (year > 2011) & (year < 2013):
            division = ['ATL', 'MIA', 'NYM', 'PHI', 'WSN', 'CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
        if (year > 2012):
            division = ['ATL', 'MIA', 'NYM', 'PHI', 'WSN', 'CHC', 'CIN', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
    else:
        division = []

    return(division)

def test1():
    year = 1901

    tf = False
    while (year < 2025) & (tf == False):
        data = pd.read_csv('\\Users\edoug\Code\Python\MLBDraft\merged_batter_data.csv')
        data = data[data['Season'] == year]

        if year < 1969:
            division = set_division(year, 'AL')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NL')
            print(division)
            data = data[~data['Team'].isin(division)]
        elif year < 1994:
            division = set_division(year, 'ALW')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NLW')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'ALE')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NLE')
            print(division)
            data = data[~data['Team'].isin(division)]

        else:
            division = set_division(year, 'ALW')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NLW')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'ALC')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NLC')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'ALE')
            print(division)
            data = data[~data['Team'].isin(division)]

            division = set_division(year, 'NLE')
            print(division)
            data = data[~data['Team'].isin(division)]

        data = data[['Season', 'Team', 'Franchise']]
        unique_teams = data['Team'].unique()
        if len(unique_teams) > 0:
            tf = True
        else:
            year += 1
    
    print(data)
    print(year)
    print(unique_teams)

def test2():
    root = Tk()
    sv_ttk.set_theme('dark')
    root.title("Autocomplete Dropdown")
    root.geometry("400x300")

    player_list = [
        "2024 Shohei Ohtani", "2024 Mike Trout", "2024 Aaron Judge",
        "2024 Mookie Betts", "2024 Freddie Freeman"
    ]

    autocomplete = AutoCompleteDropdown(root, player_list)
    root.mainloop()

class AutoCompleteDropdown:
    def __init__(self, root, options):
        # Full list of options
        self.options = options
        self.filtered_options = []

        self.frame = ttk.Frame(root)
        self.frame.pack()

        # Entry widget for user input
        self.entry = ttk.Entry(self.frame, width=30)
        self.entry.grid(row = 0, column = 0, pady = 10)
        self.entry.bind("<KeyRelease>", self.update_list)  # Update dropdown on key release

        # Listbox for dropdown options
        self.listbox = Listbox(self.frame, width=30, height = 3, activestyle="dotbox", bd = 0)
        self.listbox.pack_forget()  # Initially hide the listbox
        self.listbox.bind("<<ListboxSelect>>", self.select_option)  # Bind selection event

        # Style the Listbox to match ttk themes
        self.listbox.configure(background="white", foreground="black", selectbackground="#0078d7", selectforeground="white")

        # Confirm button
        self.confirm_button = ttk.Button(self.frame, text="Confirm", command=self.confirm_selection)

    def update_list(self, event=None):
        # Get current text in entry widget
        typed_text = self.entry.get().lower()

        # Only start showing options after 8 characters are typed
        if len(typed_text) >= 8:
            # Filter options based on input
            self.filtered_options = [
                option for option in self.options if typed_text in option.lower()
            ]

            # Update listbox
            self.listbox.delete(0, END)  # Clear existing items
            for option in self.filtered_options:
                self.listbox.insert(END, option)  # Add filtered options

            # Show listbox only if there are matching options
            if self.filtered_options:
                self.listbox.grid(row = 1, column = 0, pady = 10)
                self.confirm_button.grid(row = 2, column = 0, pady = 10)
            else:
                self.listbox.grid_forget()  # Hide if no matches
        else:
            self.listbox.grid_forget()  # Hide listbox if fewer than 8 characters are typed
            self.confirm_button.grid_forget()

    def select_option(self, event):
        # Get selected option
        selection = self.listbox.curselection()
        if selection:
            selected_option = self.listbox.get(selection[0])  # Get first selected item
            self.entry.delete(0, END)  # Clear entry
            self.entry.insert(0, selected_option)  # Populate entry with selected item
            self.listbox.grid_forget()  # Hide dropdown after selection

    def confirm_selection(self):
        # Print the selected player's name
        selected_player = self.entry.get()
        if selected_player:
            print(f"Confirmed selection: {selected_player}")
        else:
            print("No player selected")

main()
#test()
#test1()
#test2()

