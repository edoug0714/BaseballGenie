from tkinter import ttk
from tkinter import *
import pandas as pd
import numpy as np
import random
import helper

CURR_YEAR = 2024

class Pick:
    def __init__(self, name, position, total):
        self.name = name
        self.position = position
        self.total = total

class Player:
    def __init__(self, name):
        self.rem_turns = 9
        self.player_objects = []
        self.total = 0
        self.ab = 0
        self.ip = 0
        self.num_sp = 0
        self.num_rp = 0
        self.name = name
        self.teams_needed = []

        self.catcher = Pick("", "C", 0)
        self.first_base = Pick("", "1B", 0)
        self.second_base = Pick("", "2B", 0)
        self.third_base = Pick("", "3B", 0)
        self.short_stop = Pick("", "SS", 0)
        self.left_field = Pick("", "LF", 0)
        self.center_field = Pick("", "CF", 0)
        self.right_field = Pick("", "RF", 0)
        self.hitter = Pick("", "DH", 0)

        self.sp1 = Pick("", "SP", 0)
        self.sp2 = Pick("", "SP", 0)
        self.sp3 = Pick("", "SP", 0)
        self.sp4 = Pick("", "SP", 0)
        self.sp5 = Pick("", "SP", 0)
        self.sp6 = Pick("", "SP", 0)
        self.sp7 = Pick("", "SP", 0)
        self.sp8 = Pick("", "SP", 0)
        self.sp9 = Pick("", "SP", 0)
        self.rp1 = Pick("", "RP", 0)
        self.rp2 = Pick("", "RP", 0)
        self.rp3 = Pick("", "RP", 0)
        self.rp4 = Pick("", "RP", 0)

        self.total = 0

class Game:
    def __init__(self, root, inputs, names):
        self.root = root
        self.play_again = BooleanVar(value = False)
        self.prev_player = ""
        self.prev_division = []
        self.picked_players = []
        self.numPlayers = inputs[0]
        self.division = inputs[1]
        self.stat = inputs[2]
        self.start_year = inputs[3]
        self.end_year = inputs[4]
        self.textcolor = inputs[5]
        self.backgroundcolor = inputs[6]
        self.errorcolor = inputs[7]
        self.teamscar = inputs[8]
        self.cumstats = False

        #Read correct datafile depending on batter/pitcher
        if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
            self.data = pd.read_csv("../data/merged_batter_data.csv").fillna(0)
            self.data.drop(columns=self.data.columns[0], axis=1, inplace=True)
            self.season_name = pd.read_csv("../data/season_name_batters.csv").fillna(0)
            self.season_name = self.season_name['x'].tolist()
        else:
            self.data = pd.read_csv("../data/merged_pitcher_data.csv").fillna(0)
            self.season_name = pd.read_csv("../data/season_name_pitchers.csv").fillna(0)
            self.season_name = self.season_name['x'].tolist()

        #Finish game setup
        self.create_players(names)
        self.set_division_tf()
        self.startGame()

    def create_players(self, names):
        #If random order was enabled, shuffle
        if names[0].get():
            names.pop(0)
            random.shuffle(names)
        else:
            names.pop(0)

        self.player1 = Player(names[0])
        self.player1.teams_needed = self.set_division(CURR_YEAR, self.division)
        self.player2 = Player(names[1])
        self.player2.teams_needed = self.set_division(CURR_YEAR, self.division)
        if self.numPlayers > 2:
            self.player3 = Player(names[2])
            self.player3.teams_needed = self.set_division(CURR_YEAR, self.division)
            if self.numPlayers > 3:
                self.player4 = Player(names[3])
                self.player4.teams_needed = self.set_division(CURR_YEAR, self.division)

    def set_division_tf(self):
        #Check if game is for specific division
        if self.division in ['MLB', 'AL', 'NL']:
            self.division_tf = False
        else:
            self.division_tf = True

    def startGame(self):
        if self.numPlayers == 2:
            self.root.geometry("1200x620")
        elif self.numPlayers == 3:
            self.root.geometry("1500x620")
        else:
            self.root.geometry("1800x620")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close)

        self.objects = [] #Stores all tkinter objects for easy clearing of screen
        self.objects.append(ttk.Frame(self.root))
        self.objects[-1].pack(fill = 'both', expand = 'True')
        self.objects[-1].columnconfigure(0, weight = 1)
        self.objects[-1].columnconfigure(1, weight = 1)
        self.objects[-1].columnconfigure(2, weight = 1)

        #Pack the 3 columns used for game screen
        self.objects.append(ttk.Frame(self.objects[0])) #WAS LEFT FRAME NOW self.objects[1]
        self.objects[-1].grid(row = 0, column = 0, sticky = "nsw", padx = (10, 5), pady = 10)
        self.objects.append(ttk.Frame(self.objects[0])) #WAS RIGHT FRAME NOW self.objects[2]
        self.objects[-1].grid(row = 0, column = 2, sticky = "nse", padx = (5, 10), pady = 10)
        self.objects.append(ttk.Frame(self.objects[0])) #WAS CENTER FRAME NOW self.objects[3]
        self.objects[-1].grid(row = 0, column = 1)

        draft_order, player = self.orient_screen(self.objects[1], self.objects[2])
        player_objects = self.paste_player(self.objects[1], self.objects[2])

        self.player1.player_objects = player_objects[0]
        self.player2.player_objects = player_objects[1]
        if self.numPlayers > 2:
            self.player3.player_objects = player_objects[2]
            if self.numPlayers > 3:
                self.player4.player_objects = player_objects[3]

        #If team scarcity is on, set remteams to correct division
        if (self.division == 'AL') or (self.division == 'NL') or (self.division == 'MLB'):
            if self.teamscar:
                if self.division == 'AL': self.remteams = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'LAA', 'OAK', 'SEA', 'TEX']
                elif self.division == 'NL': self.remteams = ['ATL', 'MIA', 'NYM', 'PHI', 'WSN', 'CHC', 'CIN', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']
                else: self.remteams = ['BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'LAA', 'OAK', 'SEA', 'TEX', 'ATL', 'MIA', 'NYM', 'PHI', 'WSN', 'CHC', 'CIN', 'MIL', 'PIT', 'STL', 'ARI', 'COL', 'LAD', 'SDP', 'SFG']

                #If there are more picks in draft than length of remteams, double remteams (each team can be picked twice)
                while self.numPlayers * 9 > len(self.remteams):
                    self.remteams += self.remteams
        #If specific division is selected, ensure team scarcity is False
        else:
            self.teamscar = False

        #START OF MAIN GAME LOOP
        self.exit = False
        for i in draft_order:
            objects = []
            print(f'Loop {i}: {self.exit}')
            if self.exit:
                break
            if i < len(player):
                self.turn(self.objects[3], player[i], objects)
            
            #Clear screen after each turn
            if not self.exit:
                for obj in objects:
                    obj.destroy
                objects.clear()

        if self.exit:
            return

        #Clear screen before displaying results
        for obj in objects:
            obj.destroy()
        objects.clear()

        #Display finishing order
        if self.numPlayers == 2:
            players = [self.player1, self.player2]
        elif self.numPlayers == 3:
            players = [self.player1, self.player2, self.player3]
        else:
            players = [self.player1, self.player2, self.player3, self.player4]
        if self.stat == 'AVG':
            sorted_players = sorted(players, key=lambda player: player.total / player.ab, reverse=True)
        if self.stat == 'ERA':
            sorted_players = sorted(players, key=lambda player: 9 * player.total / player.ip, reverse=False)
        else:
            sorted_players = sorted(players, key=lambda player: player.total, reverse=True)
        objects.append(Label(self.objects[3], text = f'1st: {sorted_players[0].name}', font = ('System', 50), fg = '#FFD700'))
        objects[-1].grid(row = 0, column = 0, padx = 5, pady = 0)
        objects.append(Label(self.objects[3], text = f'2nd: {sorted_players[1].name}', font = ('System', 40), fg = '#9e9d8f'))
        objects[-1].grid(row = 1, column = 0, padx = 5, pady = 10)
        if self.numPlayers > 2:
            objects.append(Label(self.objects[3], text = f'3rd: {sorted_players[2].name}', font = ('System', 30), fg = '#915e25'))
            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
            if self.numPlayers > 3:
                objects.append(Label(self.objects[3], text = f'4th: {sorted_players[3].name}', font = ('System', 20), fg = 'white'))
                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)

        self.top_remaining(self.objects[3], self.objects)

        #Display play again button and hold screen until it is pressed or game is exited
        objects.append(ttk.Button(self.objects[3], text = "Play Again", command = lambda: (self.play_again.set(True))))
        objects[-1].grid(row = 9, column = 0, padx = 5, pady = 25)

        self.root.wait_variable(self.play_again)

        #Clear rankings from screen
        for obj in objects:
            obj.destroy()
        objects.clear()

        #Destroy frame and grid objects
        for obj in self.objects:
            obj.destroy()
        self.objects.clear()

    def orient_screen(self, left_frame, right_frame):
        if self.numPlayers == 2:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = self.textcolor)
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(right_frame, text = self.player2.name, font=('System', 18), fg = self.textcolor)
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            draft_order = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            player = [self.player1, self.player2]
        elif self.numPlayers == 3:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = self.textcolor)
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(left_frame, text = self.player2.name, font=('System', 18), fg = self.textcolor)
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            player3_label = Label(right_frame, text = self.player3.name, font=('System', 18), fg = self.textcolor)
            player3_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            draft_order = [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 3]
            player = [self.player1, self.player2, self.player3]
        elif self.numPlayers == 4:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = self.textcolor)
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(left_frame, text = self.player2.name, font=('System', 18), fg = self.textcolor)
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            player3_label = Label(right_frame, text = self.player3.name, font=('System', 18), fg = self.textcolor)
            player3_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player4_label = Label(right_frame, text = self.player4.name, font=('System', 18), fg = self.textcolor)
            player4_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            draft_order = [0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3]
            player = [self.player1, self.player2, self.player3, self.player4]

        return draft_order, player

    def paste_player(self, left_frame, right_frame):
        #Player 2 on right
        if self.numPlayers == 2:
            player1_frame = left_frame
            player2_frame = right_frame
        #Players 3/4 on right
        else:
            player1_frame = left_frame
            player2_frame = left_frame

        #Determine which layout to use based on stat
        if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
            pos = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH', 'Total']
        elif self.stat == 'W':
            pos = ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'Total']
        else:
            pos = ['SP', 'SP', 'SP', 'SP', 'SP', 'RP', 'RP', 'RP', 'RP', 'Total']

        #Create objects to display each player's draft selections and score
        player1_obj = []
        player2_obj = []
        player3_obj = []
        player4_obj = []
        for i in range(len(pos)):
            player1_obj.append(ttk.Label(player1_frame, text = f'{pos[i]}:'))
            player1_obj[i].grid(row = i + 1, column = 0, padx = 25, pady = 5)
            player2_obj.append(ttk.Label(player2_frame, text = f'{pos[i]}:'))
            player2_obj[i].grid(row = i + 1, column = 1, padx = 25, pady = 5)
            if self.numPlayers > 2:
                player3_obj.append(ttk.Label(right_frame, text = f'{pos[i]}:'))
                player3_obj[i].grid(row = i + 1, column = 0, padx = 25, pady = 5)
                if self.numPlayers > 3:
                    player4_obj.append(ttk.Label(right_frame, text = f'{pos[i]}:'))
                    player4_obj[i].grid(row = i + 1, column = 1, padx = 25, pady = 5)
            
        #Add teams needed objects if divisional game
        if self.division_tf:
            player1_obj.append(Label(player1_frame, text = 'Teams Needed', font = ('Fixedsys', 10), fg = self.textcolor))
            player1_obj[10].grid(row = 11, column = 0, padx = 25, pady = 5)
            player1_obj.append(Label(player1_frame, text = f'{", ".join(self.player1.teams_needed)}', font = ('Fixedsys', 10), fg = self.textcolor))
            player1_obj[11].grid(row = 12, column = 0, padx = 25, pady = 5)
            player2_obj.append(Label(player2_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = self.textcolor))
            player2_obj[10].grid(row = 11, column = 1, padx = 25, pady = 5)
            player2_obj.append(Label(player2_frame, text = f'{", ".join(self.player2.teams_needed)}', font = ('Fixedsys', 10), fg = self.textcolor))
            player2_obj[11].grid(row = 12, column = 1, padx = 25, pady = 5)
            if self.numPlayers > 2:
                player3_obj.append(Label(right_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = self.textcolor))
                player3_obj[10].grid(row = 11, column = 0, padx = 25, pady = 5)
                player3_obj.append(Label(right_frame, text = f'{", ".join(self.player3.teams_needed)}', font = ('Fixedsys', 10), fg = self.textcolor))
                player3_obj[11].grid(row = 12, column = 0, padx = 25, pady = 5)
                if self.numPlayers > 3:
                    player4_obj.append(Label(right_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = self.textcolor))
                    player4_obj[10].grid(row = 11, column = 1, padx = 25, pady = 5)
                    player4_obj.append(Label(right_frame, text = f'{", ".join(self.player4.teams_needed)}', font = ('Fixedsys', 10), fg = self.textcolor))
                    player4_obj[11].grid(row = 12, column = 1, padx = 25, pady = 5)

        player_objects = [player1_obj, player2_obj, player3_obj, player4_obj]
        return player_objects

    def turn(self, center_frame, player, objects):
        #Class that handles the dropdown search menu for player selection
        class AutoCompleteDropdown(Game):
            def __init__(self, game_instance, frame, options):
                self.game = game_instance
                self.options = options
                self.filtered_options = []
                objects.append(ttk.Entry(frame, width=30)) #SELF.ENTRY NOW OBJECTS[4]
                objects[4].grid(row = 4, column = 0, pady = 10)
                objects[4].bind("<KeyRelease>", self.update_list)
                objects.append(Listbox(frame, width=30, height = 3, activestyle="dotbox", bd = 0)) #SELF.LISTBOX NOW OBJECTS[5]
                objects[5].grid(row = 5, column = 0, pady = 10)
                objects[5].bind("<<ListboxSelect>>", self.select_option)
                objects[5].configure(background=self.game.backgroundcolor, selectbackground=self.game.backgroundcolor, selectforeground="white")
                objects.append(ttk.Button(frame, text="Confirm", command = lambda: (self.confirm_selection()))) #SELF.CONFIRM_BUTTON NOW OBJECTS[6]
                objects[6].grid(row = 6, column = 0, pady = 10)

            #Every time user types a character, update list to show matches
            def update_list(self, event=None):
                typed_text = objects[4].get().lower()

                #Do not start displaying matches until 4 characters (year) have been typed
                if len(typed_text) >= 4:
                    self.filtered_options = [option for option in self.options if typed_text in option.lower()]
                    objects[5].delete(0, END) 
                    for option in self.filtered_options:
                        objects[5].insert(END, option)
                #If less than 4 characters, do not show matches
                else:
                    objects[5].delete(0, END)

            #Allows users to click on player they want
            def select_option(self, event):
                selection = objects[5].curselection()
                if selection:
                    selected_option = objects[5].get(selection[0])
                    objects[4].delete(0, END)
                    objects[4].insert(0, selected_option)
                    objects[5].grid_forget()

            #Displays confirm button
            def confirm_selection(self):
                if len(objects[4].get().split()) >= 2:
                    year = objects[4].get().split(' ', 1)[0]
                    name = objects[4].get().split(' ', 1)[1]
                    player.temp_name = name
                    player.temp_year = int(year)
                    self.game.loop1.set(True)

        #Start of each individual turn
        #print(f'Called turn() - Player {player.name}\'s Turn')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.loop1 = BooleanVar(self.root)
        self.loop2 = BooleanVar(self.root)
        self.loop3 = BooleanVar(self.root)
        self.loop1.set(False)
        self.loop2.set(False)
        self.loop3.set(False)

        #Filter season_name list so that only correct years show up in listbox
        self.season_name = [item for item in self.season_name if str(self.start_year) < item < str(self.end_year + 1)]

        self.errorcode = -1
        while self.loop1.get() == False:
            #print('While loop 1 called')
            self.loop1.set(False)
            self.loop2.set(False)
            self.loop3.set(False)

            #Create and pack center display objects
            objects.append(Label(center_frame, text = f'{self.start_year}-{self.end_year} {self.division} {self.stat_disp()}', font=('System', 28)))
            objects.append(Label(center_frame, text = f'{player.name}\'s Selection', font=('System', 28), fg = self.textcolor))
            objects.append(Label(center_frame, text = "Select Player", font=('Helvetica', 20)))
            objects.append(Label(center_frame, text = "EX: (1994 Michael Jordan)", font=('Helvetica', 10)))
            for i, obj in enumerate(objects):
                if i == 0:
                    obj.grid(row = i, column = 0, padx = 5, pady = 10)
                elif i == 1:
                    obj.grid(row = i, column = 0, padx = 5, pady = 10)
                else:
                    obj.grid(row = i, column = 0, padx = 5, pady = 5)

            #Dropdown menu object
            self.acd = AutoCompleteDropdown(self, center_frame, self.season_name)

            #Display previous selection's top 3 seasons in division and year range
            self.prev_player_stats(center_frame, objects)
            #Display remaining teams
            self.remaining_teams(center_frame, objects)

            #Display errors if error has been flagged
            if self.errorcode == 0:
                helper.throw_error(objects[-1], message = "Error: Player does not exist.", row = 12)
            elif self.errorcode == 1:
                helper.throw_error(objects[-1], message = "Error: Player is not from correct division.", row = 12)
            elif self.errorcode == 2:
                helper.throw_error(objects[-1], message = f'Error: Must select a player from {", ".join(player.teams_needed)}.', row = 12)
            elif self.errorcode == 3:
                helper.throw_error(objects[-1], message = f'Error: {", ".join(franchises)} are not available.', row = 12)
            elif self.errorcode == 4:
                helper.throw_error(objects[-1], message = f'Error: Year is out of range.', row = 12)
            elif self.errorcode == 5:
                helper.throw_error(objects[-1], message = f'Error: Player already selected.', row = 12)
            self.errorcode = -1

            #Wait variable that holds screen until player is selected
            center_frame.wait_variable(self.loop1)

            while self.loop2.get() == False:
                #print('While loop 2 called')
                
                #Get division layout from selected year
                division = self.set_division(player.temp_year, self.division)
                self.multiple_positions = False
                player_stats = self.data
                player_stats = player_stats[player_stats['Name'] == player.temp_name]
                season_stats = player_stats[player_stats['Season'] == player.temp_year]
                teams = season_stats['Team'].unique()
                franchises = season_stats['Franchise'].unique()
                common_teams_div = np.intersect1d(teams, division)
                if self.teamscar:
                    common_teams_fra = np.intersect1d(franchises, self.remteams)
                else:
                    common_teams_fra = []
                common_teams_need = np.intersect1d(teams, player.teams_needed)

                #Throw errors
                skiploop2 = False
                if (player.temp_year < self.start_year) or (player.temp_year > self.end_year):
                    self.errorcode = 4
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                elif len(player_stats) == 0:
                    self.errorcode = 0
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                elif player.temp_name in self.picked_players:
                    self.errorcode = 5
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                elif (len(common_teams_div) == 0) & (not self.teamscar):
                    self.picked_players.append(player.temp_name)
                    self.errorcode = 1
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                elif (len(common_teams_need) == 0) & (player.rem_turns == len(player.teams_needed)) & (not self.teamscar):
                    self.picked_players.append(player.temp_name)
                    self.errorcode = 2
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                elif (len(common_teams_fra) == 0) & (self.teamscar):
                    self.picked_players.append(player.temp_name)
                    self.errorcode = 3
                    skiploop2 = True
                    self.loop2.set(True)
                    self.loop1.set(False)
                else:
                    self.picked_players.append(player.temp_name)

                #Batting stats
                    if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
                        season_stats = season_stats[season_stats['Team'].isin(common_teams_div)]
                        if player.rem_turns == len(player.teams_needed):
                            season_stats = season_stats[season_stats['Team'].isin(common_teams_need)]
                        if self.stat == "AVG":
                            season_stats = season_stats.sort_values(by = ['H'], ascending = False)
                            val = season_stats['H'].iloc[0]
                        else:
                            season_stats = season_stats.sort_values(by = [self.stat], ascending = False)
                            val = season_stats[self.stat].iloc[0]
                        player.temp_franchise = season_stats['Franchise'].iloc[0]
                        player.temp_team = season_stats['Team'].iloc[0]
                        player.temp_ab = season_stats['AB'].iloc[0]
                        season_stats = season_stats[season_stats['G_by_pos'] / season_stats['G'] >= 0.2]
                        season_stats = season_stats.reset_index()
                        positions = season_stats['Pos']

                        pos = []
                        for i in range(len(positions)):
                            pos.append(positions[i])
                        for i in range(1, len(objects)):
                            objects[i].destroy()
                        objects = objects[:1]

                        #Remove DH if present in positions
                        if 'DH' in pos:
                            pos.remove('DH')
                        #If player is not qualified at any positions, add DH back
                        if len(pos) == 0:
                            pos.append('DH')
                        adj_pos = []
                        for i in pos:
                            adj_pos.append(i)

                        #Deals with players who played on multiple teams in the same season
                        teams = season_stats['Team'].unique().tolist()
                        if len(set(teams)) != 1:
                            #Remove teams that were already selected
                            if self.teamscar:
                                for t in teams:
                                    if t not in self.remteams:
                                        teams.remove(t)
                            if self.stat == "AVG":
                                season_stats = season_stats.sort_values(by = ['H'], ascending = False)
                            else:
                                season_stats = season_stats.sort_values(by = [self.stat], ascending = False)
                            team_stats = season_stats[season_stats['Team'] == teams[0]]
                            player.temp_team = team_stats['Team'].iloc[0]
                            player.temp_franchise = team_stats['Franchise'].iloc[0]
                            if self.stat == "AVG":
                                val = team_stats['H'].iloc[0]
                                player.temp_ab = team_stats['AB'].iloc[0]
                            else:
                                val = team_stats[self.stat].iloc[0]
                            adj_pos = list(set(adj_pos))

                        #Display eligible positions
                        objects.append(Label(center_frame, text = f'{player.temp_name} is eligible at {", ".join(adj_pos)}.'))
                        objects[1].grid(row = 1, column = 0, padx = 5, pady = 5)

                        #Remove positions that player already has
                        if 'C' in pos:
                            if player.catcher.name != "":
                                adj_pos.remove('C')
                        if '1B' in pos:
                            if player.first_base.name != "":
                                adj_pos.remove('1B')
                        if '2B' in pos:
                            if player.second_base.name != "":
                                adj_pos.remove('2B')
                        if '3B' in pos:
                            if player.third_base.name != "":
                                adj_pos.remove('3B')
                        if 'SS' in pos:
                            if player.short_stop.name != "":
                                adj_pos.remove('SS')
                        if 'LF' in pos:
                            if player.left_field.name != "":
                                adj_pos.remove('LF')
                        if 'CF' in pos:
                            if player.center_field.name != "":
                                adj_pos.remove('CF')
                        if 'RF' in pos:
                            if player.right_field.name != "":
                                adj_pos.remove('RF')
                        if 'DH' in pos:
                            if player.hitter.name != "":
                                adj_pos.remove('DH')
                        if 'P' in pos:
                            adj_pos.remove('P')
                        pos = list(set(pos))

                        #Player has all eligible positions filled
                        if len(adj_pos) == 0:
                            objects.append(Label(center_frame, text = f'You do not have {", ".join(pos)} available.'))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            #DH is also filled -> pick again
                            if player.hitter.name != "":
                                objects.append(Label(center_frame, text = f'You do not have DH available.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                            #DH is available -> use as DH
                            else:
                                objects.append(Label(center_frame, text = f'You have DH available.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                                pos.clear()
                                pos.append("DH")
                                objects.append(ttk.Button(center_frame, text = "Use as DH", command = lambda: self.select_player(player, pos, val, division)))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                        #Player has 1 eligible position open -> use at that position
                        elif(len(adj_pos) == 1):
                            objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = f'Use as {", ".join(adj_pos)}', command = lambda: self.select_player(player, adj_pos, val, division)))
                            objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        #Player has multiple eligible positions open -> choose position
                        else:
                            while self.loop2.get() == False:
                                print('While loop 3 called')
                                objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                                objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                                objects.append(Label(center_frame, text = f'Select position you would like {player.temp_name} at.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)

                                objects.append(ttk.Button(center_frame, text = adj_pos[0], command = lambda: self.select_player(player, [adj_pos[0]], val, division)))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = adj_pos[1], command = lambda: self.select_player(player, [adj_pos[1]], val, division)))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                                if len(adj_pos) > 2:
                                    objects.append(ttk.Button(center_frame, text = adj_pos[2], command = lambda: self.select_player(player, [adj_pos[2]], val, division)))
                                    objects[-1].grid(row = 6, column = 0, padx = 5, pady = 5)
                                    if len(adj_pos) > 3:
                                        objects.append(ttk.Button(center_frame, text = adj_pos[3], command = lambda: self.select_player(player, [adj_pos[3]], val, division)))
                                        objects[-1].grid(row = 7, column = 0, padx = 5, pady = 5)

                                objects.append(ttk.Button(center_frame, text = 'Select New Player', command = lambda: (self.loop3.set(True), self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 8, column = 0, padx = 5, pady = 25)

                                #Holds program until position is selected
                                center_frame.wait_variable(self.loop3)

                            #Skips loop2 waitvariable since player is already selected
                            skiploop2 = True

                            #Clear screen before next turn
                            for obj in objects:
                                obj.destroy()
                            objects.clear()

                #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                    #Pitching mode
                    else:
                        season_stats = season_stats[season_stats['Team'].isin(common_teams_div)]
                        if player.rem_turns == len(player.teams_needed):
                            season_stats = season_stats[season_stats['Team'].isin(common_teams_need)]
                        if self.stat == "ERA":
                            season_stats = season_stats.sort_values(by = ['ER'], ascending = True)
                            val = season_stats['ER'].iloc[0]
                        elif self.stat == "PWAR":
                            season_stats = season_stats.sort_values(by = ['WAR'], ascending = False)
                            val = season_stats['WAR'].iloc[0]
                        else:
                            season_stats = season_stats.sort_values(by = [self.stat], ascending = False)
                            val = season_stats[self.stat].iloc[0]
                        player.temp_team = season_stats['Team'].iloc[0]
                        player.temp_ip = season_stats['IP'].iloc[0]

                        for i in range(1, len(objects)):
                            objects[i].destroy()
                        objects = objects[:1]

                        pos = []
                        if season_stats['GS'].iloc[0] == 0:
                            pos.append('RP')
                        else:
                            pos.append('SP')
                            
                        if self.stat in ['W']:
                            num_starters = 9
                        else:
                            num_starters = 5

                        #Deals with players who played on multiple teams in the same season
                        teams = season_stats['Team'].unique().tolist()
                        if len(set(teams)) != 1:
                            #Remove teams that were already selected
                            if self.teamscar:
                                for t in teams:
                                    if t not in self.remteams:
                                        teams.remove(t)
                            if self.stat == "ERA":
                                season_stats = season_stats.sort_values(by = ['ERA'], ascending = True)
                            else:
                                season_stats = season_stats.sort_values(by = [self.stat], ascending = False)
                            team_stats = season_stats[season_stats['Team'] == teams[0]]
                            player.temp_team = team_stats['Team'].iloc[0]
                            player.temp_franchise = team_stats['Franchise'].iloc[0]
                            if self.stat == "ERA":
                                val = team_stats['ER'].iloc[0]
                                player.temp_ip = team_stats['IP'].iloc[0]
                            else:
                                val = team_stats[self.stat].iloc[0]

                        #Change IP from 0.1, 0.2 version to 0.33 or 0.67
                        if player.temp_ip - int(player.temp_ip) > 0.15:
                            player.temp_ip = int(player.temp_ip) + 0.67
                        elif player.temp_ip - int(player.temp_ip) > 0.05:
                            player.temp_ip = int(player.temp_ip) + 0.33
                        else:
                            player.temp_ip = int(player.temp_ip)


                        #Qualifies as RP but SP only -> pick again
                        if (pos[0] == 'RP') & (num_starters == 9):
                            helper.throw_error(objects[-1], message = f"Error: {player.temp_name} is not a SP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[4].destroy()
                            objects[5].destroy()
                            objects[6].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        #Qualifies as RP and RP filled -> pick again
                        elif (pos[0] == 'RP') & (player.num_rp == 4):
                            helper.throw_error(objects[-1], message = f"Error: Max number of RP reached. Please select a SP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[4].destroy()
                            objects[5].destroy()
                            objects[6].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        #Qualifies as SP and SP filled -> pick again
                        elif (pos[0] == 'SP') & (player.num_sp == 5) & (num_starters == 5):
                            helper.throw_error(objects[-1], message = f"Error: Max number of SP reached. Please select a RP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[4].destroy()
                            objects[5].destroy()
                            objects[6].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        else:
                            for i in range(1, len(objects)):
                                objects[i].destroy()
                            objects = objects[:1]
                            objects.append(Label(center_frame, text = f'{player.temp_year} {player.temp_name} is eligible at {", ".join(pos)}'))
                            objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = f'Use as {", ".join(pos)}', command = lambda: self.select_pitcher(player, pos, val, division)))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)

                #Holds program until selection is confirmed
                if not skiploop2:
                    center_frame.wait_variable(self.loop2)

            #Clear screen for next pick
            for obj in objects:
                obj.destroy()
            objects.clear()

        #If program closed, return
        if self.exit:
            return

    #Defines what program does when closed
    def on_close(self):
        self.loop1.set(True)
        self.loop2.set(True)
        self.play_again.set(True)
        self.exit = True
        quit(self.root)
    
    #Since divisions change over time, necessary to set divisions based on what year was selected
    def set_division(self, year, div):
        if div == "ALW":
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
        elif div == "ALC":
            if (year < 1998):
                division = ['CHW', 'CLE', 'KCR', 'MIL', 'MIN']
            elif (year > 1997):
                division = ['CHW', 'CLE', 'DET', 'KCR', 'MIN']
        elif div == "ALE":
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
        elif div == "NLW":
            if (year < 1993):
                division = ['ATL', 'CIN', 'HOU', 'LAD', 'SDP', 'SFG']
            elif (year > 1992) & (year < 1994):
                division = ['ATL', 'CIN', 'COL', 'HOU', 'LAD', 'SDP', 'SFG']
            elif (year > 1993) & (year < 1998):
                division = ['COL', 'LAD', 'SDP', 'SFG']
            elif (year > 1997):
                division = ['ARI', 'COL', 'LAD', 'SDP', 'SFG']
        elif div == "NLC":
            if (year < 1998):
                division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
            if (year > 1997) & (year < 2013):
                division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
            if (year > 2012):
                division = ['CHC', 'CIN', 'MIL', 'PIT', 'STL']
        elif div == "NLE":
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
        elif div == "AL":
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
        elif div == "NL":
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
            division = self.set_division(year, 'NL') + self.set_division(year, 'AL')

        return(division)

    #After batter is selected and passes checks, this function processes the pick
    def select_player(self, player, pos, val, division):
        position = pos[0]
        
        if position == 'C':
            player.catcher.name = player.temp_name
            player.catcher.total = val
            if self.stat == 'AVG': player.player_objects[0].config(text = f'C: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[0].config(text = f'C: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[0].config(text = f'C: {player.temp_year} {player.temp_name} [{val}]')
        elif position == '1B':
            player.first_base.name = player.temp_name
            player.first_base.total = val
            if self.stat == 'AVG': player.player_objects[1].config(text = f'1B: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[1].config(text = f'1B: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[1].config(text = f'1B: {player.temp_year} {player.temp_name} [{val}]')
        elif position == '2B':
            player.second_base.name = player.temp_name
            player.second_base.total = val
            if self.stat == 'AVG': player.player_objects[2].config(text = f'2B: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[2].config(text = f'2B: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[2].config(text = f'2B: {player.temp_year} {player.temp_name} [{val}]')
        elif position == '3B':
            player.third_base.name = player.temp_name
            player.third_base.total = val
            if self.stat == 'AVG': player.player_objects[3].config(text = f'3B: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[3].config(text = f'3B: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[3].config(text = f'3B: {player.temp_year} {player.temp_name} [{val}]')
        elif position == 'SS':
            player.short_stop.name = player.temp_name
            player.short_stop.total = val
            if self.stat == 'AVG': player.player_objects[4].config(text = f'SS: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[4].config(text = f'SS: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[4].config(text = f'SS: {player.temp_year} {player.temp_name} [{val}]')
        elif position == 'LF':
            player.left_field.name = player.temp_name
            player.left_field.total = val
            if self.stat == 'AVG': player.player_objects[5].config(text = f'LF: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[5].config(text = f'LF: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[5].config(text = f'LF: {player.temp_year} {player.temp_name} [{val}]')
        elif position == 'CF':
            player.center_field.name = player.temp_name
            player.center_field.total = val
            if self.stat == 'AVG': player.player_objects[6].config(text = f'CF: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[6].config(text = f'CF: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[6].config(text = f'CF: {player.temp_year} {player.temp_name} [{val}]')
        elif position == 'RF':
            player.right_field.name = player.temp_name
            player.right_field.total = val
            if self.stat == 'AVG': player.player_objects[7].config(text = f'RF: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[7].config(text = f'RF: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[7].config(text = f'RF: {player.temp_year} {player.temp_name} [{val}]')
        elif position == 'DH':
            player.hitter.name = player.temp_name
            player.hitter.total = val
            if self.stat == 'AVG': player.player_objects[8].config(text = f'DH: {player.temp_year} {player.temp_name} [{round(val / player.temp_ab, 3):.3f}]')
            elif self.stat == 'WAR': player.player_objects[8].config(text = f'DH: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
            else: player.player_objects[8].config(text = f'DH: {player.temp_year} {player.temp_name} [{val}]')

        #Update prev_player for top years display
        self.prev_player = player.temp_name
        self.prev_division = division
        player.rem_turns -= 1

        #Update player total
        if self.stat == 'AVG':
            player.ab += player.temp_ab
            player.total += val
            print(f'{player.temp_name}: {val} / {player.temp_ab}, {player.total} / {player.ab}')
            player.player_objects[9].config(text = f'Average: {round(player.total / player.ab, 3):.3f}')
        elif self.stat == 'WAR':
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total, 1):.1f}')
        else:
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total)}')

        #Remove team from needed teams if divisional game
        if self.division_tf:
            if player.temp_team in player.teams_needed: 
                player.teams_needed.remove(player.temp_team)
            player.player_objects[11].config(text = f'{", ".join(player.teams_needed)}')
        #Remove team from remaining teams if team scarcity is on
        elif self.teamscar:
            indices = [i for i, val in enumerate(self.remteams) if val == player.temp_franchise]
            if len(indices) > 1:
                self.remteams.pop(indices[1])
            else:
                self.remteams.pop(indices[0])

        self.loop2.set(True)
        self.loop3.set(True)

    #After pitcher is selected and passes checks, this function processes the pick
    def select_pitcher(self, player, pos, val, division):
        if pos[0] == 'SP':
            if player.num_sp == 0:
                player.sp1.name = player.temp_name
                player.sp1.total = val
                if self.stat == 'ERA': player.player_objects[0].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[0].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[0].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 1:
                player.sp2.name = player.temp_name
                player.sp2.total = val
                if self.stat == 'ERA': player.player_objects[1].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9* val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[1].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[1].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 2:
                player.sp3.name = player.temp_name
                player.sp3.total = val
                if self.stat == 'ERA': player.player_objects[2].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[2].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[2].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 3:
                player.sp4.name = player.temp_name
                player.sp4.total = val
                if self.stat == 'ERA': player.player_objects[3].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[3].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[3].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 4:
                player.sp5.name = player.temp_name
                player.sp5.total = val
                if self.stat == 'ERA': player.player_objects[4].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[4].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[4].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 5:
                player.sp6.name = player.temp_name
                player.sp6.total = val
                if self.stat == 'ERA': player.player_objects[5].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[5].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[5].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 6:
                player.sp7.name = player.temp_name
                player.sp7.total = val
                if self.stat == 'ERA': player.player_objects[6].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[6].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[6].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 7:
                player.sp8.name = player.temp_name
                player.sp8.total = val
                if self.stat == 'ERA': player.player_objects[7].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[7].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[7].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_sp == 8:
                player.sp9.name = player.temp_name
                player.sp9.total = val
                if self.stat == 'ERA': player.player_objects[8].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[8].config(text = f'SP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[8].config(text = f'SP: {player.temp_year} {player.temp_name} [{val}]')
        else:
            if player.num_rp == 0:
                player.rp1.name = player.temp_name
                player.rp1.total = val
                if self.stat == 'ERA': player.player_objects[5].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[5].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[5].config(text = f'RP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_rp == 1:
                player.rp2.name = player.temp_name
                player.rp2.total = val
                if self.stat == 'ERA': player.player_objects[6].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[6].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[6].config(text = f'RP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_rp == 2:
                player.rp3.name = player.temp_name
                player.rp3.total = val
                if self.stat == 'ERA': player.player_objects[7].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[7].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[7].config(text = f'RP: {player.temp_year} {player.temp_name} [{val}]')
            elif player.num_rp == 3:
                player.rp4.name = player.temp_name
                player.rp4.total = val
                if self.stat == 'ERA': player.player_objects[8].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                elif self.stat == 'PWAR': player.player_objects[8].config(text = f'RP: {player.temp_year} {player.temp_name} [{round(val, 1):.1f}]')
                else: player.player_objects[8].config(text = f'RP: {player.temp_year} {player.temp_name} [{val}]')

        #Update prev_player for top years display
        self.prev_player = player.temp_name
        self.prev_division = division
        player.rem_turns -= 1

        #Update RP or SP count
        if pos[0] == 'SP':
            player.num_sp += 1
        else:
            player.num_rp += 1

        #Update player total
        if self.stat == 'ERA':
            player.ip += player.temp_ip
            player.total += val
            print(f'{player.temp_name}: {val} / {player.temp_ip}, {player.total} / {player.ip}')
            player.player_objects[9].config(text = f'Average: {round(9 * player.total / player.ip, 2)}')
        else:
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total, 1)}')

        #Remove team from needed teams if divisional game
        if self.division_tf:
            if player.temp_team in player.teams_needed: 
                player.teams_needed.remove(player.temp_team)
            player.player_objects[11].config(text = f'{", ".join(player.teams_needed)}')
        #Remove team from remaining teams if team scarcity is on
        elif self.teamscar:
            indices = [i for i, val in enumerate(self.remteams) if val == player.temp_team]
            if len(indices) > 1:
                self.remteams.pop(indices[1])
            else:
                self.remteams.pop(indices[0])

        self.loop2.set(True)

    #Displays top seasons list at bottom of screen
    def prev_player_stats(self, center_frame, objects):
        if self.prev_player != "":
            player_stats = self.data
            player_stats = player_stats[player_stats['Name'] == self.prev_player]
            season_stats = player_stats[(player_stats['Season'] >= self.start_year) & (player_stats['Season'] <= self.end_year)]
            season_stats = season_stats[season_stats['Team'].isin(self.prev_division)]
            if self.stat == 'ERA':
                season_stats = season_stats.sort_values(by = self.stat, ascending = True).drop_duplicates(subset = 'Season', keep = 'first')
            elif self.stat == 'AVG':
                season_stats = season_stats.sort_values(by = 'H', ascending = False).drop_duplicates(subset = 'Season', keep = 'first')
            elif self.stat == 'PWAR':
                season_stats = season_stats.sort_values(by = 'WAR', ascending = False).drop_duplicates(subset = 'Season', keep = 'first')
            else:
                season_stats = season_stats.sort_values(by = self.stat, ascending = False).drop_duplicates(subset = 'Season', keep = 'first')
            #Display top 3 seasons
            if (len(season_stats) > 2):
                objects.append(ttk.Label(center_frame, text = f'Top 3 {self.prev_player} seasons in {self.division}:'))
                objects[-1].grid(row = 7, column = 0, padx = 5, pady = 10)
                if self.stat == 'ERA': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats[self.stat].iloc[0], 2):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats[self.stat].iloc[1], 2):.2f}     {season_stats['Season'].iloc[2]}: {round(season_stats[self.stat].iloc[2], 2):.2f}"))
                elif self.stat == 'AVG': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['H'].iloc[0], 3):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats['H'].iloc[1], 3):.2f}     {season_stats['Season'].iloc[2]}: {round(season_stats['H'].iloc[2], 3):.2f}"))
                elif (self.stat == 'PWAR') or (self.stat == 'WAR'): objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['WAR'].iloc[0], 3):.1f}     {season_stats['Season'].iloc[1]}: {round(season_stats['WAR'].iloc[1], 3):.1f}     {season_stats['Season'].iloc[2]}: {round(season_stats['WAR'].iloc[2], 3):.1f}"))
                else: objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {season_stats[self.stat].iloc[0]}     {season_stats['Season'].iloc[1]}: {season_stats[self.stat].iloc[1]}     {season_stats['Season'].iloc[2]}: {season_stats[self.stat].iloc[2]}"))
                objects[-1].grid(row = 8, column = 0, padx = 5, pady = 5)
            #Display only 2 seasons
            elif (len(season_stats) > 1):
                objects.append(ttk.Label(center_frame, text = f'{self.prev_player}\'s seasons in {self.division}:'))
                objects[-1].grid(row = 7, column = 0, padx = 5, pady = 10)
                if self.stat == 'ERA': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats[self.stat].iloc[0], 2):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats[self.stat].iloc[1], 2):.2f}"))
                elif self.stat == 'AVG': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['H'].iloc[0], 3):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats['H'].iloc[1], 3):.2f}"))
                elif (self.stat == 'PWAR') or (self.stat == 'WAR'): objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['WAR'].iloc[0], 3):.1f}     {season_stats['Season'].iloc[1]}: {round(season_stats['WAR'].iloc[1], 3):.1f}"))
                else: objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {season_stats[self.stat].iloc[0]}     {season_stats['Season'].iloc[1]}: {season_stats[self.stat].iloc[1]}"))
                objects[-1].grid(row = 8, column = 0, padx = 5, pady = 5)
            #Display only season
            elif (len(season_stats) > 0):
                objects.append(ttk.Label(center_frame, text = f'{self.prev_player}\'s seasons in {self.division}:'))
                objects[-1].grid(row = 7, column = 0, padx = 5, pady = 10)
                if self.stat == 'ERA': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats[self.stat].iloc[0], 2):.2f}"))
                elif self.stat == 'AVG': objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['H'].iloc[0], 3):.2f}"))
                elif (self.stat == 'PWAR') or (self.stat == 'WAR'): objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats['WAR'].iloc[0], 3):.1f}"))
                else: objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {season_stats[self.stat].iloc[0]}"))
                objects[-1].grid(row = 8, column = 0, padx = 5, pady = 5)

    #Displays remaining team list at bottom of screen
    def remaining_teams(self, center_frame, objects):
        if self.teamscar:
            rem_teams_set = sorted(set(self.remteams))
            objects.append(ttk.Label(center_frame, text = f'Remaining Teams:'))
            objects[-1].grid(row = 9, column = 0, padx = 5, pady = (30, 10))

            if len(rem_teams_set) > 15:
                midpoint = (len(rem_teams_set) + 1) // 2
                first_half = rem_teams_set[:midpoint]
                second_half = rem_teams_set[midpoint:]
                objects.append(ttk.Label(center_frame, text = f'{", ".join(first_half)}'))
                objects[-1].grid(row = 10, column = 0, padx = 5, pady = 5)
                objects.append(ttk.Label(center_frame, text = f'{", ".join(second_half)}'))
                objects[-1].grid(row = 11, column = 0, padx = 5, pady = 5)
                objects.append(Label(center_frame, text = "", fg = self.errorcolor))
                #objects[-1].grid(row = 12, column = 0, padx = 5, pady = 5)

            else:
                objects.append(ttk.Label(center_frame, text = f'{", ".join(rem_teams_set)}'))
                objects[-1].grid(row = 10, column = 0, padx = 5, pady = 5)
                objects.append(Label(center_frame, text = "", fg = self.errorcolor))
                #objects[-1].grid(row = 11, column = 0, padx = 5, pady = 5)
        else:
            objects.append(Label(center_frame, text = "", fg = self.errorcolor))
            #objects[-1].grid(row = 9, column = 0, padx = 5, pady = 5)

    #Returns name of stat to display
    def stat_disp(self):
        if self.stat == 'H':
            return 'Hits'
        elif self.stat == 'HR':
            return 'HRs'
        elif self.stat == 'W':
            return 'Wins'
        elif self.stat == 'SO':
            return 'Ks'
        elif self.stat == 'SB':
            return 'SBs'
        else:
            return self.stat
        
    def top_remaining(self, center_frame, objects):
        print(self.picked_players)
        data = self.data[~self.data['Name'].isin(self.picked_players)]
        data = data[data['Franchise'].isin(self.set_division(CURR_YEAR, self.division))]
        data = data[(data['Season'] >= self.start_year) & (data['Season'] <= self.end_year)]
        if self.stat == 'AVG':
            data['AVG'] = data['H'] / data['AB']
            data = data[data['AB'] >= 500]
            data = data.sort_values(by = [self.stat], ascending = False)
        elif self.stat == 'ERA':
            data = data[data['IP'] >= 150]
            data = data.sort_values(by = [self.stat], ascending = True)
        elif self.stat == 'PWAR':
            data = data.sort_values(by = ['WAR'], ascending = False)
        else:
            data = data.sort_values(by = [self.stat], ascending = False)

        if self.stat in ['SB', 'H', 'HR']:
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} {data['Pos'].iloc[0]} {data['Name'].iloc[0]} - {data[self.stat].iloc[0]}"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} {data['Pos'].iloc[0]} {data['Name'].iloc[1]} - {data[self.stat].iloc[1]}"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} {data['Pos'].iloc[2]} {data['Name'].iloc[2]} - {data[self.stat].iloc[2]}"))
            objects[-1].grid(row = 8, column = 0, pady = 5)
        elif self.stat == 'AVG':
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} {data['Pos'].iloc[0]} {data['Name'].iloc[0]} - {round(data[self.stat].iloc[0], 3):.3f}"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} {data['Pos'].iloc[0]} {data['Name'].iloc[1]} - {round(data[self.stat].iloc[1], 3):.3f}"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} {data['Pos'].iloc[2]} {data['Name'].iloc[2]} - {round(data[self.stat].iloc[2], 3):.3f}"))
            objects[-1].grid(row = 8, column = 0, pady = 5)
        elif self.stat == 'WAR':
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} {data['Pos'].iloc[0]} {data['Name'].iloc[0]} - {round(data['WAR'].iloc[0], 1):.1f}"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} {data['Pos'].iloc[1]} {data['Name'].iloc[1]} - {round(data['WAR'].iloc[1], 1):.1f}"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} {data['Pos'].iloc[2]} {data['Name'].iloc[2]} - {round(data['WAR'].iloc[2], 1):.1f}"))
            objects[-1].grid(row = 8, column = 0, pady = 5)
        elif self.stat == 'ERA':
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} SP {data['Name'].iloc[0]} - {round(data[self.stat].iloc[0], 2):.2f} over {data['IP'].iloc[0]} IP"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} SP {data['Name'].iloc[1]} - {round(data[self.stat].iloc[1], 2):.2f} over {data['IP'].iloc[1]} IP"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} SP {data['Name'].iloc[2]} - {round(data[self.stat].iloc[2], 2):.2f} over {data['IP'].iloc[2]} IP"))
            objects[-1].grid(row = 8, column = 0, pady = 5)
        elif self.stat == 'PWAR':
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} P {data['Name'].iloc[0]} - {round(data['WAR'].iloc[0], 1):.1f}"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} P {data['Name'].iloc[1]} - {round(data['WAR'].iloc[1], 1):.1f}"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} P {data['Name'].iloc[2]} - {round(data['WAR'].iloc[2], 1):.1f}"))
            objects[-1].grid(row = 8, column = 0, pady = 5)
        else:
            objects.append(ttk.Label(center_frame, text = "Best remaning picks:"))
            objects[-1].grid(row = 5, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[0]} {data['Franchise'].iloc[0]} P {data['Name'].iloc[0]} - {data[self.stat].iloc[0]}"))
            objects[-1].grid(row = 6, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[1]} {data['Franchise'].iloc[1]} P {data['Name'].iloc[1]} - {data[self.stat].iloc[1]}"))
            objects[-1].grid(row = 7, column = 0, pady = 5)
            objects.append(ttk.Label(center_frame, text = f"{data['Season'].iloc[2]} {data['Franchise'].iloc[2]} P {data['Name'].iloc[2]} - {data[self.stat].iloc[2]}"))
            objects[-1].grid(row = 8, column = 0, pady = 5)