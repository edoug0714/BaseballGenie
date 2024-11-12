from tkinter import *
from tkinter import ttk
import sv_ttk
import pybaseball as pyb
import pandas as pd
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
        self.picked_players = []
        self.numPlayers = inputs[0]
        self.division = inputs[1]
        self.stat = inputs[2]
        self.start_year = inputs[3]
        self.end_year = inputs[4]
        self.create_players(names)
        self.set_division()
        self.startGame()

    def create_players(self, names):
        self.player1 = Player(names[0])
        self.player2 = Player(names[1])
        if self.numPlayers > 2:
            self.player3 = Player(names[2])
            if self.numPlayers > 3:
                self.player4 = Player(names[3])

    def set_division(self):
        if self.division == "ALW":
            div = ['HOU', 'TEX', 'LAA', 'OAK', 'SEA']
            leag = []
        elif self.division == "ALC":
            div = ALC = ['CLE', 'MIN', 'DET', 'CWS', 'KCR']
            leag = []
        elif self.division == "ALE":
            div = ['NYY', 'TBR', 'TOR', 'BOS', 'BAL']
            leag = []
        elif self.division == "NLW":
            div = ['LAD', 'SDP', 'COL', 'ARI', 'SFG']
            leag = []
        elif self.division == "NLC":
            div = ['PIT', 'CIN', 'STL', 'MIL', 'CHC']
            leag = []
        elif self.division == "NLE":
            div = ['WSN', 'NYM', 'PHI', 'MIA', 'ATL']
            leag = []
        elif self.division == "AL":
            div = []
            leag = ['HOU', 'TEX', 'LAA', 'OAK', 'SEA', 'CLE', 'MIN', 'DET', 'CWS', 'KCR', 'NYY', 'TBR', 'TOR', 'BOS', 'BAL']
        elif self.division == "NL":
            div = []
            leag = ['LAD', 'SDP', 'COL', 'ARI', 'SFG', 'PIT', 'CIN', 'STL', 'MIL', 'CHC','WSN', 'NYM', 'PHI', 'MIA', 'ATL']
        else:
            div = []
            leag = []

        if len(div) > 0:
            self.division = list(div)
            self.player1.teams_needed = list(div)
            self.player2.teams_needed = list(div)
            if self.numPlayers > 2:
                self.player3.teams_needed = list(div)
                if self.numPlayers > 3:
                    self.player4.teams_needed = list(div)
        elif len(leag) > 0:
            self.division = list(leag)
        else:
            self.division = ['HOU', 'TEX', 'LAA', 'OAK', 'SEA', 'CLE', 'MIN', 'DET', 'CWS', 'KCR', 'NYY', 'TBR', 'TOR', 'BOS', 'BAL', 'LAD', 'SDP', 'COL', 'ARI', 'SFG', 'PIT', 'CIN', 'STL', 'MIL', 'CHC','WSN', 'NYM', 'PHI', 'MIA', 'ATL']


    def startGame(self):
        if (len(self.division) == 5) & (self.numPlayers == 2):
            self.root.geometry("1200x420")
        elif (len(self.division) == 5) & (self.numPlayers == 3):
            self.root.geometry("1500x420")
        elif (len(self.division) == 5) & (self.numPlayers == 4):
            self.root.geometry("1800x420")
        elif self.numPlayers == 2:
            self.root.geometry("1200x350")
        elif self.numPlayers == 3:
            self.root.geometry("1500x350")
        else:
            self.root.geometry("1800x350")
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

        #self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        #self.root.mainloop()

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
            
        if len(self.division) == 5:
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
        print(f'Called turn() - Player {player.name}\'s Turn')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.loop1 = BooleanVar(self.root)
        self.loop2 = BooleanVar(self.root)
        self.loop3 = BooleanVar(self.root)
        self.loop1.set(False)
        self.loop2.set(False)
        self.loop3.set(False)
        player_dne = False
        while self.loop1.get() == False:
            print('While loop 1 called')

            self.loop1.set(False)
            self.loop2.set(False)
            self.loop3.set(False)

            objects.append(Label(center_frame, text = f'{player.name}\'s Selection', font=('System', 28), fg = '#39957b'))
            objects.append(Label(center_frame, text = "Select Player", font=('Helvetica', 20)))
            objects.append(Label(center_frame, text = "EX: (1994 Michael Jordan)", font=('Helvetica', 10)))
            objects.append(ttk.Entry(center_frame))
            objects.append(ttk.Button(center_frame, text = "Confirm", command = lambda: self.verify_entry(player, objects)))
            objects.append(Label(center_frame, text = "", fg = 'yellow'))

            if player_dne:
                helper.throw_error(objects[-1], message = "Error: Player does not exist.", row = len(objects) - 1)
            player_dne = False

            for i, obj in enumerate(objects):
                if i == 0:
                    obj.grid(row = i, column = 0, padx = 5, pady = 25)
                else:
                    obj.grid(row = i, column = 0, padx = 5, pady = 5)

            center_frame.wait_variable(self.loop1)

            while self.loop2.get() == False:
                print('While loop 2 called')
                if self.stat in ['WAR', 'H', 'HR', 'SB', 'AVG']:
                    season_batting_stats = pyb.batting_stats(player.temp_year, ind = 1, qual = 50)
                    season_fielding_stats = pyb.fielding_stats(player.temp_year, qual = 1, ind = 1)
                    player_batting_stats = season_batting_stats[season_batting_stats['Name'] == player.temp_name]
                    player_fielding_stats = season_fielding_stats[season_fielding_stats['Name'] == player.temp_name]

                    if len(player_batting_stats) == 0:
                        self.loop2.set(True)
                        self.loop1.set(False)
                        player_dne = True
                        break

                    if self.stat == "AVG":
                        val = player_batting_stats['H'].iloc[0]
                    else:
                        val = player_batting_stats[self.stat].iloc[0]
                    player.temp_ab = player_batting_stats['AB'].iloc[0]
                    player.temp_team = player_batting_stats['Team'].iloc[0]
                    games_played = player_fielding_stats['G'].sum()
                    player_fielding_stats = player_fielding_stats.loc[season_fielding_stats['G'] / games_played >= 0.2]
                    player_fielding_stats = player_fielding_stats.reset_index(drop = True)
                    player_fielding_stats.to_csv('output.csv')
                    positions = player_fielding_stats['Pos']

                    print(f'TEST: {self.division}, {player.temp_team}')
                    if player.temp_team not in self.division:
                        helper.throw_error(objects[-1], message = "Error: Player is not from correct division.", row = len(objects) - 1)
                        objects.append(Button(center_frame, text = "Select New Player", font=('Helvetica', 12), command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[3].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif (player.temp_team not in player.teams_needed) & (player.rem_turns == len(player.teams_needed)):
                        helper.throw_error(objects[-1], message = f'Error: Must select a player from {", ".join(player.teams_needed)}', row = len(objects) - 1)
                        objects[3].destroy()
                        objects.append(Button(center_frame, text = "Select New Player", font=('Helvetica', 12), command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    else:
                        pos = []
                        for i in range(len(positions)):
                            pos.append(positions[i])

                        for i in range(1, len(objects)):
                            objects[i].destroy()
                        objects = objects[:1]

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
                                objects.append(ttk.Button(center_frame, text = "Use as DH", command = lambda: self.select_player(player, pos, val)))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                        elif(len(adj_pos) == 1):
                            objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = f'Use as {", ".join(adj_pos)}', command = lambda: self.select_player(player, adj_pos, val)))
                            objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        else:
                            while self.loop2.get() == False:
                                print('While loop 3 called')
                                objects.append(Label(center_frame, text = f'You have {", ".join(adj_pos)} available.'))
                                objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                                objects.append(Label(center_frame, text = f'Enter position you would like {player.temp_name} at.'))
                                objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Entry(center_frame))
                                objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                                objects.append(ttk.Button(center_frame, text = "Confirm Position", command = lambda: self.verify_position(adj_pos, pos, objects)))
                                objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
                                objects.append(Label(center_frame, text = "", fg = 'yellow'))
                                #print("Made it to wait variable 3")
                                center_frame.wait_variable(self.loop3)
                                #print("Made it past variable 3")

                            self.weird_case = True

                            for obj in objects:
                                obj.destroy()
                            objects.clear()

                #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                else:
                    season_pitching_stats = pyb.pitching_stats(player.temp_year, ind = 1, qual = 1)
                    player_pitching_stats = season_pitching_stats[season_pitching_stats['Name'] == player.temp_name]
                    player_pitching_stats.to_csv('output.csv')


                    if len(player_pitching_stats) == 0:
                        self.loop2.set(True)
                        self.loop1.set(False)
                        player_dne = True
                        print("Broke out")
                        break


                    if self.stat == "ERA":
                        val = player_pitching_stats['ER'].iloc[0]
                    elif self.stat == "PWAR":
                        val = player_pitching_stats['WAR'].iloc[0]
                    else:
                        val = player_pitching_stats[self.stat].iloc[0]
                    player.temp_ip = player_pitching_stats['IP'].iloc[0]
                    print(round(player.temp_ip, 1) - int(player.temp_ip))
                    player.temp_ip_disp = round(player.temp_ip, 1)
                    if round(player.temp_ip, 1) - int(player.temp_ip) > 0.15:
                        player.temp_ip = int(player.temp_ip) + 0.67
                    elif player.temp_ip - int(player.temp_ip) > 0.05:
                        player.temp_ip = int(player.temp_ip) + 0.33
                    player.temp_team = player_pitching_stats['Team'].iloc[0]
                    #print(f'{player.temp_name}, {val}, {player.temp_ip}, {player.temp_ip_disp}')

                    #print(f'TEST: {self.division}, {player.temp_team}')
                    if player.temp_team not in self.division:
                        helper.throw_error(objects[-1], message = "Error: Player is not from correct division.", row = len(objects) - 1)
                        objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[3].destroy()
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    elif (player.temp_team not in player.teams_needed) & (player.rem_turns == len(player.teams_needed)):
                        helper.throw_error(objects[-1], message = f'Error: Must select a player from {", ".join(player.teams_needed)}', row = len(objects) - 1)
                        objects[3].destroy()
                        objects.append(Button(center_frame, text = "Select New Player", font=('Helvetica', 12), command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                    else:
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
                            objects[3].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        elif (pos[0] == 'RP') & (player.num_rp == 4):
                            helper.throw_error(objects[-1], message = f"Error: Max number of RP reached. Please select a SP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[3].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        elif (pos[0] == 'SP') & (player.num_sp == 5) & (num_starters == 5):
                            helper.throw_error(objects[-1], message = f"Error: Max number of SP reached. Please select a RP.", row = len(objects) - 1)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[3].destroy()
                            objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
                        else:
                            for i in range(1, len(objects)):
                                objects[i].destroy()
                            objects = objects[:1]

                            objects.append(Label(center_frame, text = f'{player.temp_year} {player.temp_name} is eligible at {", ".join(pos)}'))
                            objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = f'Use as {", ".join(pos)}', command = lambda: self.select_pitcher(player, pos, val)))
                            objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
                            objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                            objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)


#----------------------------------------------------------------------------
                if self.weird_case:
                    objects.append(ttk.Button(center_frame, text = f'Confirm', command = lambda: self.select_player(player, adj_pos, val)))
                    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
                    objects.append(ttk.Button(center_frame, text = "Select New Player", command = lambda: (self.loop2.set(True), self.loop1.set(False))))
                    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
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
        if len(objects[3].get().split(' ', 1)) > 1:
            if objects[3].get().split(' ', 1)[0].isdigit():
                year = objects[3].get().split(' ', 1)[0]
                name = objects[3].get().split(' ', 1)[1]
            else:
                helper.throw_error(objects[-1], message = "Error: Check format of entry.", row = len(objects) - 1)
                objects[3].delete(0, END)
                return
        else:
            helper.throw_error(objects[-1], message = "Error: Check format of entry.", row = len(objects) - 1)
            objects[3].delete(0, END)
            return

        if (int(year) < self.start_year) or (int(year) > self.end_year):
            helper.throw_error(objects[-1], message = "Error: Year out of range.", row = len(objects) - 1)
            objects[3].delete(0, END)
            return
        
        if name in self.picked_players:
            helper.throw_error(objects[-1], message = "Error: Player already selected.", row = len(objects) - 1)
            objects[3].delete(0, END)
            return

        self.loop1.set(True)
        player.temp_name = name
        player.temp_year = year

    def verify_position(self, positions, pos, objects):
        print('Verify Positions Called')
        print(objects[4].get(), positions)
        if objects[4].get() not in positions:
            helper.throw_error(objects[-1], message = "Error: Please enter valid position.", row = len(objects) - 1)
            objects[4].delete(0, END)
            return
        else:
            self.loop3.set(True)
            self.loop2.set(True)
            self.loop1.set(True)
            positions.clear()
            positions.append(objects[4].get())

    def select_player(self, player, pos, val):
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

        player.rem_turns -= 1
        self.picked_players.append(player.temp_name)

        if self.stat == 'AVG':
            player.ab += player.temp_ab
            player.total += val
            print(f'{player.temp_name}: {val} / {player.temp_ab}, {player.total} / {player.ab}')
            player.player_objects[9].config(text = f'Average: {round(player.total / player.ab, 3)}')
        else:
            player.total += val
            player.player_objects[9].config(text = f'Total: {round(player.total, 1)}')

        if len(self.division) == 5:
            if player.temp_team in player.teams_needed: 
                player.teams_needed.remove(player.temp_team)
            player.player_objects[11].config(text = f'{", ".join(player.teams_needed)}')

        self.loop2.set(True)

    def select_pitcher(self, player, pos, val):
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
            elif player.num_sp == 1:
                player.rp2.name = player.temp_name
                player.rp2.total = val
                if self.stat == 'ERA': player.player_objects[6].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[6].config(text = f'RP: {player.temp_name} [{val}]')
            elif player.num_sp == 2:
                player.rp3.name = player.temp_name
                player.rp3.total = val
                if self.stat == 'ERA': player.player_objects[7].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[7].config(text = f'RP: {player.temp_name} [{val}]')
            elif player.num_sp == 3:
                player.rp4.name = player.temp_name
                player.rp4.total = val
                if self.stat == 'ERA': player.player_objects[8].config(text = f'RP: {player.temp_name} [{round(9 * val / player.temp_ip, 2)}]')
                else: player.player_objects[8].config(text = f'RP: {player.temp_name} [{val}]')

        player.rem_turns -= 1
        self.picked_players.append(player.temp_name)

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
