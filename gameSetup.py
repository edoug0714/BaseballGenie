from tkinter import *
from tkinter import ttk
import sv_ttk
import helper

CURR_YEAR = 2024

def set_num_players(value, numPlayers, button, prevButton, success):
    success.set("1")
    numPlayers.set(value)
    prevButton[0] = button

def set_division(value, division, button, prevButton):
    division.set(value)
    prevButton[0] = button

def set_stat(value, stat, button, prevButton, success):
    success.set("1")
    stat.set(value)
    prevButton[0] = button

def set_years(start_year, end_year, year1_entry, year2_entry, root, success1, success2, error_label, division):
    #Check for num_players entry
    if success1.get() != "1":
        helper.throw_error(error_label, message = "Error: Please select number of players.")
        return
  #Check for stat entry
    if success2.get() != "1":
        helper.throw_error(error_label, message = "Error: Please select stat.")
        return
    #Check for year1 entry
    if year1_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter year values.")
        return
    #Check for year2 entry
    if year2_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter year values.")
        return
    if not (year1_entry.get().isnumeric() or (year2_entry.get().isnumeric())):
        helper.throw_error(error_label, message = "Error: Years must be formatted as numbers.")
        return

    start_year.set(year1_entry.get())
    end_year.set(year2_entry.get())
    if start_year.get() > end_year.get():
        helper.throw_error(error_label, message = "Error: Please make sure start year < end year.")
        return
    if start_year.get() > CURR_YEAR:
        helper.throw_error(error_label, message = "Error: Sorry, we do not have stats from the future.")
        return
    if end_year.get() < 1901:
        helper.throw_error(error_label, message = "Error: Sorry, we do not have stats from before 1901.")
        return
    if (division.get() in ["ALW", "ALC", "ALE", "NLW", "NLC", "NLE"]) & (end_year.get() < 1969):
        helper.throw_error(error_label, message = f"Error: Divisions did not exist before 1969.")
        return
    if (division.get() in ["ALC", "NLC"]) & (end_year.get() < 1994):
        helper.throw_error(error_label, message = "Error: Central divisions did not exist before 1994.")
        return
    if division in ["ALC", "NLC"]:
        if start_year.get() < 1994:
            start_year.set(1993)
    else:
        if start_year.get() < 1901:
            start_year.set(1901)
    if end_year.get() > 2024:
        end_year.set(2024)

    helper.quit(root)

def gameSetup():
    list = []
    root = Tk()
    sv_ttk.set_theme('dark')
    root.geometry("700x600")
    root.protocol("WM_DELETE_WINDOW", lambda: helper.on_close(list, root))

    #Display grid for player selection
    success1 = StringVar()
    numPlayers = IntVar()
    prevButton_numPlayers = [None]
    num_players_label = Label(root, text = "Select Number of Players:", font=('System', 18), fg = '#39957b')
    num_players_label.pack(pady = 10)
    num_players_frame = ttk.Frame(root)
    num_players_frame.pack()
    button2 = ttk.Button(num_players_frame, text = "2", command = lambda: set_num_players(2, numPlayers, button2, prevButton_numPlayers, success1))
    button2.grid(row = 0, column = 0, padx = 5, pady = 5)
    button3 = ttk.Button(num_players_frame, text = "3", command = lambda: set_num_players(3, numPlayers, button3, prevButton_numPlayers, success1))
    button3.grid(row = 0, column = 1, padx = 5, pady = 5)
    button4 = ttk.Button(num_players_frame, text = "4", command = lambda: set_num_players(4, numPlayers, button4, prevButton_numPlayers, success1))
    button4.grid(row = 0, column = 2, padx = 5, pady = 5)

    #Display button grid for division selection
    division = StringVar()
    division.set("MLB")
    prevButton_division = [None]
    division_label = Label(root, text = "Select Division (leave blank for entire MLB):", font=('System', 18), fg = '#39957b')
    division_label.pack(pady = 10)
    division_frame = ttk.Frame(root)
    division_frame.pack()
    button_al = ttk.Button(division_frame, text = "AL", command = lambda: set_division("AL", division, button_al, prevButton_division))
    button_al.grid(row = 0, column = 0, padx = 5, pady = 5)
    button_alw = ttk.Button(division_frame, text = "AL West", command = lambda: set_division("ALW", division, button_alw, prevButton_division))
    button_alw.grid(row = 0, column = 1, padx = 5, pady = 5)
    button_alc = ttk.Button(division_frame, text = "AL Central", command = lambda: set_division("ALC", division, button_alc, prevButton_division))
    button_alc.grid(row = 0, column = 2, padx = 5, pady = 5)
    button_ale = ttk.Button(division_frame, text = "AL East", command = lambda: set_division("ALE", division, button_ale, prevButton_division))
    button_ale.grid(row = 0, column = 3, padx = 5, pady = 5)
    button_nl = ttk.Button(division_frame, text = "NL", command = lambda: set_division("NL", division, button_nl, prevButton_division))
    button_nl.grid(row = 1, column = 0, padx = 5, pady = 5)
    button_nlw = ttk.Button(division_frame, text = "NL West", command = lambda: set_division("NLW", division, button_nlw, prevButton_division))
    button_nlw.grid(row = 1, column = 1, padx = 5, pady = 5)
    button_nlc = ttk.Button(division_frame, text = "NL Central", command = lambda: set_division("NLC", division, button_nlc, prevButton_division))
    button_nlc.grid(row = 1, column = 2, padx = 5, pady = 5)
    button_nle = ttk.Button(division_frame, text = "NL East", command = lambda: set_division("NLE", division, button_nle, prevButton_division))
    button_nle.grid(row = 1, column = 3, padx = 5, pady = 5)

    #Display button grid for stat selection
    success2 = StringVar()
    stat = StringVar()
    prevButton_stat = [None]
    stat_label = Label(root, text = "Select Stat for Draft:", font=('System', 18), fg = '#39957b')
    stat_label.pack(pady = 10)
    stat_frame = ttk.Frame(root)
    stat_frame.pack()
    button_war = ttk.Button(stat_frame, text = "Batter WAR", command = lambda: set_stat("WAR", stat, button_war, prevButton_stat, success2))
    button_war.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")
    button_hits = ttk.Button(stat_frame, text = "Hits", command = lambda: set_stat("H", stat, button_hits, prevButton_stat, success2))
    button_hits.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "ew")
    button_hr = ttk.Button(stat_frame, text = "Home Runs", command = lambda: set_stat("HR", stat, button_hr, prevButton_stat, success2))
    button_hr.grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "ew")
    button_sb = ttk.Button(stat_frame, text = "Stolen Bases", command = lambda: set_stat("SB", stat, button_sb, prevButton_stat, success2))
    button_sb.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "ew")
    button_avg = ttk.Button(stat_frame, text = "Batting Avg", command = lambda: set_stat("AVG", stat, button_avg, prevButton_stat, success2))
    button_avg.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "ew")
    button_pwar = ttk.Button(stat_frame, text = "Pitcher WAR", command = lambda: set_stat("PWAR", stat, button_pwar, prevButton_stat, success2))
    button_pwar.grid(row = 1, column = 2, padx = 5, pady = 5, sticky = "ew")
    button_wins = ttk.Button(stat_frame, text = "Wins", command = lambda: set_stat("W", stat, button_wins, prevButton_stat, success2))
    button_wins.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "ew")
    button_era = ttk.Button(stat_frame, text = "ERA", command = lambda: set_stat("ERA", stat, button_era, prevButton_stat, success2))
    button_era.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "ew")
    button_so = ttk.Button(stat_frame, text = "Strikeouts", command = lambda: set_stat("SO", stat, button_so, prevButton_stat, success2))
    button_so.grid(row = 2, column = 2, padx = 5, pady = 5, sticky = "ew")

    #Display text boxes for year selection
    start_year = IntVar()
    end_year = IntVar()
    year_frame = Frame(root)
    year_frame.pack(pady = 10)
    year1_label = Label(year_frame, text = "Start Year", font=('System', 15), fg = '#39957b')
    year1_label.grid(row = 0, column = 0, padx = 5, pady = 5)
    year1_entry = ttk.Entry(year_frame, width = 10)
    year1_entry.grid(row = 1, column = 0, padx = 5, pady = 5)
    year2_label = Label(year_frame, text = "End Year", font=('System', 15), fg = '#39957b')
    year2_label.grid(row = 0, column = 1, padx = 5, pady = 5)
    year2_entry = ttk.Entry(year_frame, width = 10)
    year2_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

    #Display confirm button
    success = False
    confirm_frame = Frame(root)
    confirm_frame.pack(pady = 5)
    error_frame = Frame(root)
    error_frame.pack(pady = 2)
    error_label = Label(error_frame, text = "", fg = 'yellow')
    confirm_button = ttk.Button(confirm_frame, text = "Confirm Settings", command = lambda: set_years(start_year, end_year, year1_entry, year2_entry, root, success1, success2, error_label, division))
    confirm_button.pack(pady = 5)

    root.mainloop()

    if division.get() == "ALW":
        if (start_year.get() < 1970):
            division = ['CAL', 'CWS', 'KCR', 'MIN', 'OAK', 'SEA']
        elif (start_year.get() > 1969) & (start_year.get() < 1972):
            division = ['CAL', 'CWS', 'KCR', 'MIN', 'OAK', 'MIL']
        elif (start_year.get() > 1971) & (start_year.get() < 1977):
            division = ['CAL', 'CWS', 'KCR', 'MIN', 'OAK', 'TEX']
        elif (start_year.get() > 1976) & (start_year.get() < 2005):
            division = ['CAL', 'CWS', 'KCR', 'MIN', 'OAK', 'SEA', 'TEX']
        elif (start_year.get() > 2004) & (start_year.get() < 2013):
            division = ['CAL', 'CWS', 'KCR', 'MIN', 'OAK', 'TEX']
        elif (start_year.get() > 2004) & (start_year.get() < 2013):
            division = ['LAA', 'OAK', 'SEA', 'TEX']
        elif (start_year.get() > 2012):
            division = ['HOU', 'LAA', 'OAK', 'SEA', 'TEX']
    elif division.get() == "ALC":
        if (start_year.get() < 1998):
            division = ['CWS', 'CLE', 'KCR', 'MIL', 'MIN']
        elif (start_year.get() > 1997):
            division = ['CWS', 'CLE', 'DET', 'KCR', 'MIN']
    elif division.get() == "ALE":
        if (start_year.get() < 1972):
            ['BAL', 'BOS', 'CLE', 'DET', 'NYY', 'WAS']
        elif (start_year.get() > 1971) & (start_year.get() < 1977):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY']
        elif (start_year.get() > 1976) & (start_year.get() < 1994):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY', 'TOR']
        elif (start_year.get() > 1976) & (start_year.get() < 1994):
            division = ['BAL', 'BOS', 'CLE', 'DET', 'MIL', 'NYY', 'TOR']
    

    list.append(numPlayers.get())
    list.append(division.get())
    list.append(stat.get())
    list.append(start_year.get())
    list.append(end_year.get())

    return list
