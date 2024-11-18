from tkinter import *
from tkinter import ttk
import sv_ttk
import pybaseball as pyb
import pandas as pd
import numpy as np
import helper

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
        self.temp_ab = 0
        self.temp_ip = 0
        self.temp_ip_disp = 0
        self.num_sp = 0
        self.num_rp = 0
        self.name = name
        self.temp_year = 0
        self.temp_name = ""
        self.temp_team = ""
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
        self.play_again = False
        self.prev_player = ""
        self.prev_division = []
        self.picked_players = []
        self.numPlayers = inputs[0]
        self.division = inputs[1]
        self.stat = inputs[2]
        self.start_year = inputs[3]
        self.end_year = inputs[4]

        if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
            self.data = pd.read_csv("C:\\Users\edoug\Code\Python\MLBDraft\merged_batter_data.csv").fillna(0)
            self.data.drop(columns=self.data.columns[0], axis=1, inplace=True)
            self.season_name = pd.read_csv("C:\\Users\edoug\Code\Python\MLBDraft\season_name_batters.csv").fillna(0)
            self.season_name = self.season_name['x'].tolist()
        else:
            self.data = pd.read_csv("C:\\Users\edoug\Code\Python\MLBDraft\merged_pitcher_data.csv").fillna(0)
            self.season_name = pd.read_csv("C:\\Users\edoug\Code\Python\MLBDraft\season_name_pitchers.csv").fillna(0)
            self.season_name = self.season_name['x'].tolist()

        self.create_players(names)
        self.set_division_tf()
        self.startGame()

    def create_players(self, names):
        self.player1 = Player(names[0])
        self.player1.teams_needed = self.set_division(2024)
        self.player2 = Player(names[1])
        self.player2.teams_needed = self.set_division(2024)
        if self.numPlayers > 2:
            self.player3 = Player(names[2])
            self.player3.teams_needed = self.set_division(2024)
            if self.numPlayers > 3:
                self.player4 = Player(names[3])
                self.player4.teams_needed = self.set_division(2024)

    def set_division_tf(self):
        if self.division in ['MLB', 'AL', 'NL']:
            self.division_tf = False
        else:
            self.division_tf = True

    def startGame(self):
        if self.numPlayers == 2:
            self.root.geometry("1200x500")
        elif self.numPlayers == 3:
            self.root.geometry("1500x500")
        else:
            self.root.geometry("1800x500")
        sv_ttk.set_theme('dark')
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_close)

        self.root.columnconfigure(0, weight = 1)
        self.root.columnconfigure(1, weight = 1)
        self.root.columnconfigure(2, weight = 1)

        left_frame = ttk.Frame(self.root)
        left_frame.grid(row = 0, column = 0, sticky = "nsw", padx = (10, 5), pady = 10)
        right_frame = ttk.Frame(self.root)
        right_frame.grid(row = 0, column = 2, sticky = "nse", padx = (5, 10), pady = 10)
        center_frame = ttk.Frame(self.root)
        center_frame.grid(row = 0, column = 1)

        draft_order, player = self.orient_screen(left_frame, right_frame)
        player_objects = self.paste_player(left_frame, right_frame)

        self.player1.player_objects = player_objects[0]
        self.player2.player_objects = player_objects[1]
        if self.numPlayers > 2:
            self.player3.player_objects = player_objects[2]
            if self.numPlayers > 3:
                self.player4.player_objects = player_objects[3]

        self.exit = False
        #START OF MAIN GAME LOOP
        for i in draft_order:
            print(f'Loop {i}: {self.exit}')
            if self.exit:
                break
            objects = []
            self.weird_case = False
            if i < len(player):
                self.turn(center_frame, player[i], objects)
            print('exit')
            
            if not self.exit:
                for obj in objects:
                    obj.destroy

        if self.exit:
            return

        for obj in objects:
            obj.destroy()
        objects.clear()

        balls = BooleanVar(self.root)
        balls.set(False)

        if self.numPlayers == 2:
            players = [self.player1, self.player2]
        elif self.numPlayers == 3:
            players = [self.player1, self.player2, self.player3]
        else:
            players = [self.player1, self.player2, self.player3, self.player4]

        if self.stat == 'AVG':
            sorted_players = sorted(players, key=lambda player: player.total / player.ab, reverse=False)
        if self.stat == 'ERA':
            sorted_players = sorted(players, key=lambda player: 9 * player.total / player.ip, reverse=False)
        else:
            sorted_players = sorted(players, key=lambda player: player.total, reverse=True)

        label1 = Label(center_frame, text = f'1st: {sorted_players[0].name}', font = ('System', 50), fg = '#FFD700')
        label1.grid(row = 0, column = 0, padx = 5, pady = 0)
        label2 = Label(center_frame, text = f'2nd: {sorted_players[1].name}', font = ('System', 40), fg = '#9e9d8f')
        label2.grid(row = 1, column = 0, padx = 5, pady = 10)
        if self.numPlayers > 2:
            label3 = Label(center_frame, text = f'3rd: {sorted_players[2].name}', font = ('System', 30), fg = '#915e25')
            label3.grid(row = 2, column = 0, padx = 5, pady = 5)
            if self.numPlayers > 3:
                label4 = Label(center_frame, text = f'4th: {sorted_players[3].name}', font = ('System', 20), fg = 'white')
                label4.grid(row = 3, column = 0, padx = 5, pady = 5)

        button = ttk.Button(center_frame, text = "Play Again", command = lambda: (self.play_again_action, balls.set(True)))
        button.grid(row = 5, column = 0, padx = 5, pady = 5)
        center_frame.wait_variable(balls)
        print("Made it past BALLS WALL")

    def orient_screen(self, left_frame, right_frame):
        if self.numPlayers == 2:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = '#39957b')
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(right_frame, text = self.player2.name, font=('System', 18), fg = '#39957b')
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            draft_order = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
            player = [self.player1, self.player2]
        elif self.numPlayers == 3:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = '#39957b')
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(left_frame, text = self.player2.name, font=('System', 18), fg = '#39957b')
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            player3_label = Label(right_frame, text = self.player3.name, font=('System', 18), fg = '#39957b')
            player3_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            draft_order = [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 3]
            player = [self.player1, self.player2, self.player3]
        elif self.numPlayers == 4:
            player1_label = Label(left_frame, text = self.player1.name, font=('System', 18), fg = '#39957b')
            player1_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player2_label = Label(left_frame, text = self.player2.name, font=('System', 18), fg = '#39957b')
            player2_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            player3_label = Label(right_frame, text = self.player3.name, font=('System', 18), fg = '#39957b')
            player3_label.grid(row = 0, column = 0, padx = 25, pady = 5)
            player4_label = Label(right_frame, text = self.player4.name, font=('System', 18), fg = '#39957b')
            player4_label.grid(row = 0, column = 1, padx = 25, pady = 5)
            draft_order = [0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1, 2, 3]
            player = [self.player1, self.player2, self.player3, self.player4]

        return draft_order, player

    def paste_player(self, left_frame, right_frame):
        if self.numPlayers == 2:
            player1_frame = left_frame
            player2_frame = right_frame
        else:
            player1_frame = left_frame
            player2_frame = left_frame

        if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
            pos = ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'DH', 'Total']
        elif self.stat == 'W':
            pos = ['SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'SP', 'Total']
        else:
            pos = ['SP', 'SP', 'SP', 'SP', 'SP', 'RP', 'RP', 'RP', 'RP', 'Total']
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
            
        if self.division_tf:
            player1_obj.append(Label(player1_frame, text = 'Teams Needed', font = ('Fixedsys', 10), fg = '#39957b'))
            player1_obj[10].grid(row = 11, column = 0, padx = 25, pady = 5)
            player1_obj.append(Label(player1_frame, text = f'{", ".join(self.player1.teams_needed)}', font = ('Fixedsys', 10), fg = '#39957b'))
            player1_obj[11].grid(row = 12, column = 0, padx = 25, pady = 5)
            player2_obj.append(Label(player2_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = '#39957b'))
            player2_obj[10].grid(row = 11, column = 1, padx = 25, pady = 5)
            player2_obj.append(Label(player2_frame, text = f'{", ".join(self.player2.teams_needed)}', font = ('Fixedsys', 10), fg = '#39957b'))
            player2_obj[11].grid(row = 12, column = 1, padx = 25, pady = 5)
            if self.numPlayers > 2:
                player3_obj.append(Label(right_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = '#39957b'))
                player3_obj[10].grid(row = 11, column = 0, padx = 25, pady = 5)
                player3_obj.append(Label(right_frame, text = f'{", ".join(self.player3.teams_needed)}', font = ('Fixedsys', 10), fg = '#39957b'))
                player3_obj[11].grid(row = 12, column = 0, padx = 25, pady = 5)
                if self.numPlayers > 3:
                    player4_obj.append(Label(right_frame, text = 'Teams Needed:', font = ('Fixedsys', 10), fg = '#39957b'))
                    player4_obj[10].grid(row = 11, column = 1, padx = 25, pady = 5)
                    player4_obj.append(Label(right_frame, text = f'{", ".join(self.player4.teams_needed)}', font = ('Fixedsys', 10), fg = '#39957b'))
                    player4_obj[11].grid(row = 12, column = 1, padx = 25, pady = 5)

        player_objects = [player1_obj, player2_obj, player3_obj, player4_obj]

        return player_objects

    def turn(self, center_frame, player, objects):
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
                objects[5].configure(background="#1c1c1c", foreground="white", selectbackground="#0078d7", selectforeground="white")
                objects.append(ttk.Button(frame, text="Confirm", command = lambda: (self.confirm_selection()))) #SELF.CONFIRM_BUTTON NOWW OBJECTS[6]

                objects[6].grid(row = 6, column = 0, pady = 10)

            def update_list(self, event=None):
                typed_text = objects[4].get().lower()

                if len(typed_text) >= 4:
                    self.filtered_options = [option for option in self.options if typed_text in option.lower()]

                    objects[5].delete(0, END) 
                    for option in self.filtered_options:
                        objects[5].insert(END, option)

                else:
                    objects[5].delete(0, END)

            def select_option(self, event):
                selection = objects[5].curselection()
                if selection:
                    selected_option = objects[5].get(selection[0])
                    objects[4].delete(0, END)
                    objects[4].insert(0, selected_option)
                    objects[5].grid_forget()

            def confirm_selection(self):
                year = objects[4].get().split(' ', 1)[0]
                name = objects[4].get().split(' ', 1)[1]
                player.temp_name = name
                player.temp_year = int(year)
                self.game.loop1.set(True)

        print(f'Called turn() - Player {player.name}\'s Turn')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.loop1 = BooleanVar(self.root)
        self.loop2 = BooleanVar(self.root)
        self.loop3 = BooleanVar(self.root)
        self.loop1.set(False)
        self.loop2.set(False)
        self.loop3.set(False)
        while self.loop1.get() == False:
            print('While loop 1 called')

            self.loop1.set(False)
            self.loop2.set(False)
            self.loop3.set(False)

            objects.append(Label(center_frame, text = f'{self.start_year}-{self.end_year} {self.division}', font=('System', 28)))
            objects.append(Label(center_frame, text = f'{player.name}\'s Selection', font=('System', 28), fg = '#39957b'))
            objects.append(Label(center_frame, text = "Select Player", font=('Helvetica', 20)))
            objects.append(Label(center_frame, text = "EX: (1994 Michael Jordan)", font=('Helvetica', 10)))

            for i, obj in enumerate(objects):
                if i == 0:
                    obj.grid(row = i, column = 0, padx = 5, pady = 10)
                elif i == 1:
                    obj.grid(row = i, column = 0, padx = 5, pady = 10)
                else:
                    obj.grid(row = i, column = 0, padx = 5, pady = 5)

            self.acd = AutoCompleteDropdown(self, center_frame, self.season_name)

            print(self.prev_player)
            if self.prev_player != "":
                player_stats = self.data
                player_stats = player_stats[player_stats['Name'] == self.prev_player]
                season_stats = player_stats[(player_stats['Season'] >= self.start_year) & (player_stats['Season'] <= self.end_year)]
                season_stats = season_stats[season_stats['Team'].isin(self.prev_division)]
                if self.stat == 'ERA':
                    season_stats = season_stats.sort_values(by = self.stat, ascending = True).drop_duplicates(subset = 'Season', keep = 'first')
                else:
                    season_stats = season_stats.sort_values(by = self.stat, ascending = False).drop_duplicates(subset = 'Season', keep = 'first')
                if len(season_stats) != 0:
                    objects.append(ttk.Label(center_frame, text = f'Top 3 {self.prev_player} seasons:'))
                    objects[-1].grid(row = 7, column = 0, padx = 5, pady = 10)
                    if self.stat == 'ERA':
                        objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats[self.stat].iloc[0], 2):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats[self.stat].iloc[1], 2):.2f}     {season_stats['Season'].iloc[2]}: {round(season_stats[self.stat].iloc[2], 2):.2f}"))
                    elif self.stat == 'AVG':
                        objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {round(season_stats[self.stat].iloc[0], 3):.2f}     {season_stats['Season'].iloc[1]}: {round(season_stats[self.stat].iloc[1], 3):.2f}     {season_stats['Season'].iloc[2]}: {round(season_stats[self.stat].iloc[2], 3):.2f}"))
                    else:
                        objects.append(ttk.Label(center_frame, text = f"{season_stats['Season'].iloc[0]}: {season_stats[self.stat].iloc[0]}     {season_stats['Season'].iloc[1]}: {season_stats[self.stat].iloc[1]}     {season_stats['Season'].iloc[2]}: {season_stats[self.stat].iloc[2]}"))
                    objects[-1].grid(row = 8, column = 0, padx = 5, pady = 5)
                    objects.append(Label(center_frame, text = "", fg = 'yellow'))
                    objects[-1].grid(row = 9, column = 0, padx = 5, pady = 5)
                else:
                    objects.append(Label(center_frame, text = "", fg = 'yellow'))
                    objects[-1].grid(row = 7, column = 0, padx = 5, pady = 5)
            else:
                objects.append(Label(center_frame, text = "", fg = 'yellow'))
                objects[-1].grid(row = 7, column = 0, padx = 5, pady = 5)

            center_frame.wait_variable(self.loop1)

            while self.loop2.get() == False:
                print('While loop 2 called')
                division = self.set_division(player.temp_year)
                self.picked_players.append(player.temp_name)

                if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
                    player_batting_stats = self.data
                    player_batting_stats = player_batting_stats[player_batting_stats['Name'] == player.temp_name]
                    season_batting_stats = player_batting_stats[player_batting_stats['Season'] == player.temp_year]
                    teams = season_batting_stats['Team'].unique()
                    common_teams_div = np.intersect1d(teams, division)
                    common_teams_need = np.intersect1d(teams, player.teams_needed)
                    print(teams)
                    print(player.teams_needed)
                    print(common_teams_need)
                    print(len(common_teams_need))

                    if len(player_batting_stats) == 0:
                        helper.throw_error(objects[-1], message = "Error: Player does not exist.", row = len(objects) - 1)
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif len(common_teams_div) == 0:
                        helper.throw_error(objects[-1], message = "Error: Player is not from correct division.", row = len(objects) - 1)
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif (len(common_teams_need) == 0) & (player.rem_turns == len(player.teams_needed)):
                        helper.throw_error(objects[-1], message = f'Error: Must select a player from {", ".join(player.teams_needed)}', row = len(objects) - 1)
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    else:
                        season_batting_stats = season_batting_stats[season_batting_stats['Team'].isin(common_teams_div)]
                        if player.rem_turns == len(player.teams_needed):
                            season_batting_stats = season_batting_stats[season_batting_stats['Team'].isin(common_teams_need)]
                        season_batting_stats = season_batting_stats.sort_values(by = [self.stat], ascending = False)
                        if self.stat == "AVG":
                            val = season_batting_stats['H'].iloc[0]
                        else:
                            val = season_batting_stats[self.stat].iloc[0]
                        player.temp_team = season_batting_stats['Team'].iloc[0]
                        player.temp_ab = season_batting_stats['AB'].iloc[0]

                        season_batting_stats = season_batting_stats[season_batting_stats['G_by_pos'] / season_batting_stats['G'] >= 0.2]
                        season_batting_stats = season_batting_stats.reset_index()
                        positions = season_batting_stats['Pos']
                        print(positions)
                        pos = []
                        for i in range(len(positions)):
                            print(i)
                            pos.append(positions[i])

                        for i in range(1, len(objects)):
                            objects[i].destroy()
                        objects = objects[:1]

                        if 'DH' in pos:
                            pos.remove('DH')

                        if len(pos) == 0:
                            pos.append('DH')

                        objects.append(Label(center_frame, text = f'{player.temp_name} is eligible at {", ".join(pos)}.'))
                        objects[1].grid(row = 1, column = 0, padx = 5, pady = 5)

                        adj_pos = []
                        for i in pos:
                            adj_pos.append(i)

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

                        if len(adj_pos) == 0:
                            objects.append(Label(center_frame, text = f'You do not have {", ".join(pos)} available.'))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            if player.hitter.name != "":
                                objects.append(Label(center_frame, text = f'You do not have DH available.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                            else:
                                objects.append(Label(center_frame, text = f'You have DH available.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                                pos.clear()
                                pos.append("DH")
                                objects.append(ttk.Button(center_frame, text = "Use as DH", command = lambda: self.select_player(player, pos, val, division)))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                        elif(len(adj_pos) == 1):
                            objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = f'Use as {", ".join(adj_pos)}', command = lambda: self.select_player(player, adj_pos, val, division)))
                            objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        else:
                            while self.loop2.get() == False:
                                print('While loop 3 called')
                                objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                                objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                                objects.append(Label(center_frame, text = f'Select position you would like {player.temp_name} at.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)

                                objects.append(ttk.Button(center_frame, text = adj_pos[0], command = lambda: self.verify_position(adj_pos, adj_pos[0], objects)))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = adj_pos[1], command = lambda: self.verify_position(adj_pos, adj_pos[1], objects)))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                                if len(adj_pos) > 2:
                                    objects.append(ttk.Button(center_frame, text = adj_pos[2], command = lambda: self.verify_position(adj_pos, adj_pos[2], objects)))
                                    objects[-1].grid(row = 6, column = 0, padx = 5, pady = 5)
                                    if len(adj_pos) > 3:
                                        objects.append(ttk.Button(center_frame, text = adj_pos[3], command = lambda: self.verify_position(adj_pos, adj_pos[3], objects)))
                                        objects[-1].grid(row = 7, column = 0, padx = 5, pady = 5)

                                center_frame.wait_variable(self.loop3)

                            self.weird_case = True

                            for obj in objects:
                                obj.destroy()
                            objects.clear()

                #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                else:
                    player_pitching_stats = self.data
                    player_pitching_stats = player_pitching_stats[player_pitching_stats['Name'] == player.temp_name]
                    season_pitching_stats = player_pitching_stats[player_pitching_stats['Season'] == player.temp_year]
                    teams = season_pitching_stats['Team'].unique()
                    common_teams_div = np.intersect1d(teams, division)
                    common_teams_need = np.intersect1d(teams, player.teams_needed)

                    print(player_pitching_stats)
                    print(len(player_pitching_stats))

                    if len(player_pitching_stats) == 0:
                        helper.throw_error(objects[-1], message = "Error: Player does not exist.", row = len(objects) - 1)
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif len(common_teams_div) == 0:
                        helper.throw_error(objects[-1], message = "Error: Player is not from correct division.", row = len(objects) - 1)
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif (len(common_teams_need) == 0) & (player.rem_turns == len(player.teams_needed)):
                        helper.throw_error(objects[-1], message = f'Error: Must select a player from {", ".join(player.teams_needed)}', row = len(objects) - 1)
                        objects[4].destroy()
                        objects[5].destroy()
                        objects[6].destroy()
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    else:
                        season_pitching_stats = season_pitching_stats[season_pitching_stats['Team'].isin(common_teams_div)]
                        if player.rem_turns == len(player.teams_needed):
                            season_pitching_stats = season_pitching_stats[season_pitching_stats['Team'].isin(common_teams_need)]
                        season_pitching_stats = season_pitching_stats.sort_values(by = [self.stat], ascending = False)
                        if self.stat == "ERA":
                            val = season_pitching_stats['ER'].iloc[0]
                        elif self.stat == "PWAR":
                            val = season_pitching_stats['WAR'].iloc[0]
                        else:
                            val = season_pitching_stats[self.stat].iloc[0]
                        player.temp_team = season_pitching_stats['Team'].iloc[0]
                        player.temp_ip = season_pitching_stats['IP'].iloc[0]

                        for i in range(1, len(objects)):
                            objects[i].destroy()
                        objects = objects[:1]

                        pos = []
                        if player_pitching_stats['GS'].iloc[0] == 0:
                            pos.append('RP')
                        else:
                            pos.append('SP')
                            
                        if self.stat in ['W']:
                            num_starters = 9
                        else:
                            num_starters = 5
                        if (pos[0] == 'RP') & (num_starters == 9):
                            helper.throw_error(objects[-1], message = f"Error: {player.temp_name} is not a SP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[4].destroy()
                            objects[5].destroy()
                            objects[6].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        elif (pos[0] == 'RP') & (player.num_rp == 4):
                            helper.throw_error(objects[-1], message = f"Error: Max number of RP reached. Please select a SP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[4].destroy()
                            objects[5].destroy()
                            objects[6].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
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


#----------------------------------------------------------------------------
                if self.weird_case:
                    objects.append(ttk.Label(center_frame, text = f'Select {player.temp_name} at {", ".join(adj_pos)}.'))
                    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
                    objects.append(ttk.Button(center_frame, text = f'Confirm', command = lambda: self.select_player(player, adj_pos, val, division)))
                    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                    objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                    objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                print("Made it to wait variable 2")
                center_frame.wait_variable(self.loop2)
                print("Made it past variable 2")

            for obj in objects:
                obj.destroy()
            objects.clear()

        if self.exit:
            return

    def on_close(self):
        #print('On Close Called')
        self.loop1.set(True)
        self.loop2.set(True)
        self.exit = True
        quit(self.root)

    def verify_entry(self, player, objects):
        #print('Verify Entry Called')
        if len(objects[4].get().split(' ', 1)) > 1:
            if objects[4].get().split(' ', 1)[0].isdigit():
                year = objects[4].get().split(' ', 1)[0]
                name = objects[4].get().split(' ', 1)[1]
            else:
                helper.throw_error(objects[-1], message = "Error: Check format of entry.", row = len(objects) - 1)
                objects[4].delete(0, END)
                return
        else:
            helper.throw_error(objects[-1], message = "Error: Check format of entry.", row = len(objects) - 1)
            objects[4].delete(0, END)
            return

        if (int(year) < self.start_year) or (int(year) > self.end_year):
            helper.throw_error(objects[-1], message = "Error: Year out of range.", row = len(objects) - 1)
            objects[4].delete(0, END)
            return
        
        if name in self.picked_players:
            helper.throw_error(objects[-1], message = "Error: Player already selected.", row = len(objects) - 1)
            objects[4].delete(0, END)
            return

        self.loop1.set(True)
        player.temp_name = name
        player.temp_year = int(year)
    
    def set_division(self, year):
        if self.division == "ALW":
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
        elif self.division == "ALC":
            if (year < 1998):
                division = ['CHW', 'CLE', 'KCR', 'MIL', 'MIN']
            elif (year > 1997):
                division = ['CHW', 'CLE', 'DET', 'KCR', 'MIN']
        elif self.division == "ALE":
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
        elif self.division == "NLW":
            if (year < 1993):
                division = ['ATL', 'CIN', 'HOU', 'LAD', 'SDP', 'SFG']
            elif (year > 1992) & (year < 1994):
                division = ['ATL', 'CIN', 'COL', 'HOU', 'LAD', 'SDP', 'SFG']
            elif (year > 1993) & (year < 1998):
                division = ['COL', 'LAD', 'SDP', 'SFG']
            elif (year > 1997):
                division = ['ARI', 'COL', 'LAD', 'SDP', 'SFG']
        elif self.division == "NLC":
            if (year < 1998):
                division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
            if (year > 1997) & (year < 2013):
                division = ['CHC', 'CIN', 'HOU', 'MIL', 'PIT', 'STL']
            if (year > 2012):
                division = ['CHC', 'CIN', 'MIL', 'PIT', 'STL']
        elif self.division == "NLE":
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
        elif self.division == "AL":
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
        elif self.division == "NL":
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

    def verify_position(self, positions, pos, objects):
        print('Verify Positions Called')

        self.loop3.set(True)
        self.loop2.set(True)
        self.loop1.set(True)
        positions.clear()
        positions.append(pos)

    def select_player(self, player, pos, val, division):
        position = pos[0]
        
        if position == 'C':
            player.catcher.name = player.temp_name
            player.catcher.total = val
            if self.stat == 'AVG':
                player.player_objects[0].config(text = f'C: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[0].config(text = f'C: {player.temp_name} [{val}]')
        elif position == '1B':
            player.first_base.name = player.temp_name
            player.first_base.total = val
            if self.stat == 'AVG':
                player.player_objects[1].config(text = f'1B: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[1].config(text = f'1B: {player.temp_name} [{val}]')
        elif position == '2B':
            player.second_base.name = player.temp_name
            player.second_base.total = val
            if self.stat == 'AVG':
                player.player_objects[2].config(text = f'2B: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[2].config(text = f'2B: {player.temp_name} [{val}]')
        elif position == '3B':
            player.third_base.name = player.temp_name
            player.third_base.total = val
            if self.stat == 'AVG':
                player.player_objects[3].config(text = f'3B: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[3].config(text = f'3B: {player.temp_name} [{val}]')
        
        elif position == 'SS':
            player.short_stop.name = player.temp_name
            player.short_stop.total = val
            if self.stat == 'AVG':
                player.player_objects[4].config(text = f'SS: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[4].config(text = f'SS: {player.temp_name} [{val}]')
        elif position == 'LF':
            player.left_field.name = player.temp_name
            player.left_field.total = val
            if self.stat == 'AVG':
                player.player_objects[5].config(text = f'LF: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[5].config(text = f'LF: {player.temp_name} [{val}]')
        elif position == 'CF':
            player.center_field.name = player.temp_name
            player.center_field.total = val
            if self.stat == 'AVG':
                player.player_objects[6].config(text = f'CF: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[6].config(text = f'CF: {player.temp_name} [{val}]')
        elif position == 'RF':
            player.right_field.name = player.temp_name
            player.right_field.total = val
            if self.stat == 'AVG':
                player.player_objects[7].config(text = f'RF: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[7].config(text = f'RF: {player.temp_name} [{val}]')
        elif position == 'DH':
            player.hitter.name = player.temp_name
            player.hitter.total = val
            if self.stat == 'AVG':
                player.player_objects[8].config(text = f'DH: {player.temp_name} [{round(val / player.temp_ab, 3)}]')
            else:
                player.player_objects[8].config(text = f'DH: {player.temp_name} [{val}]')

        self.prev_player = player.temp_name
        self.prev_division = division
        player.rem_turns -= 1

        if self.stat == 'AVG':
            player.ab += player.temp_ab
            player.total += val
            print(f'{player.temp_name}: {val} / {player.temp_ab}, {player.total} / {player.ab}')
            player.player_objects[9].config(text = f'Average: {round(player.total / player.ab, 3)}')
        else:
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total, 1)}')

        if self.division_tf:
            if player.temp_team in player.teams_needed: 
                player.teams_needed.remove(player.temp_team)
            player.player_objects[11].config(text = f'{", ".join(player.teams_needed)}')

        self.loop2.set(True)

    def select_pitcher(self, player, pos, val, division):
        if pos[0] == 'SP':
            if player.num_sp == 0:
                player.sp1.name = player.temp_name
                player.sp1.total = val
                if self.stat == 'ERA': player.player_objects[0].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[0].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 1:
                player.sp2.name = player.temp_name
                player.sp2.total = val
                if self.stat == 'ERA': player.player_objects[1].config(text = f'SP: {player.temp_name} [{round(9* val / player.temp_ip, 2)}]')
                else: player.player_objects[1].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 2:
                player.sp3.name = player.temp_name
                player.sp3.total = val
                if self.stat == 'ERA': player.player_objects[2].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[2].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 3:
                player.sp4.name = player.temp_name
                player.sp4.total = val
                if self.stat == 'ERA': player.player_objects[3].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[3].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 4:
                player.sp5.name = player.temp_name
                player.sp5.total = val
                if self.stat == 'ERA': player.player_objects[4].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[4].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 5:
                player.sp6.name = player.temp_name
                player.sp6.total = val
                if self.stat == 'ERA': player.player_objects[5].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[5].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 6:
                player.sp7.name = player.temp_name
                player.sp7.total = val
                if self.stat == 'ERA': player.player_objects[6].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[6].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 7:
                player.sp8.name = player.temp_name
                player.sp8.total = val
                if self.stat == 'ERA': player.player_objects[7].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[7].config(text = f'SP: {player.temp_name} [{val}]')
            elif player.num_sp == 8:
                player.sp9.name = player.temp_name
                player.sp9.total = val
                if self.stat == 'ERA': player.player_objects[8].config(text = f'SP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[8].config(text = f'SP: {player.temp_name} [{val}]')
        else:
            if player.num_rp == 0:
                player.rp1.name = player.temp_name
                player.rp1.total = val
                if self.stat == 'ERA': player.player_objects[5].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[5].config(text = f'RP: {player.temp_name} [{val}]')
            elif player.num_rp == 1:
                player.rp2.name = player.temp_name
                player.rp2.total = val
                if self.stat == 'ERA': player.player_objects[6].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[6].config(text = f'RP: {player.temp_name} [{val}]')
            elif player.num_rp == 2:
                player.rp3.name = player.temp_name
                player.rp3.total = val
                if self.stat == 'ERA': player.player_objects[7].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[7].config(text = f'RP: {player.temp_name} [{val}]')
            elif player.num_rp == 3:
                player.rp4.name = player.temp_name
                player.rp4.total = val
                if self.stat == 'ERA': player.player_objects[8].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[8].config(text = f'RP: {player.temp_name} [{val}]')

        self.prev_player = player.temp_name
        self.prev_division = division
        player.rem_turns -= 1

        if pos[0] == 'SP':
            player.num_sp += 1
        else:
            player.num_rp += 1

        if self.stat == 'ERA':
            player.ip += player.temp_ip
            player.total += val
            print(f'{player.temp_name}: {val} / {player.temp_ip}, {player.total} / {player.ip}')
            player.player_objects[9].config(text = f'Average: {round(9 * player.total / player.ip, 2)}')
        else:
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total, 1)}')

        if len(self.division) == 5:
            if player.temp_team in player.teams_needed: 
                player.teams_needed.remove(player.temp_team)
            player.player_objects[11].config(text = f'{", ".join(player.teams_needed)}')

        self.loop2.set(True)

    def play_again_action(self):
        self.root.destroy()
        self.play_again = True
