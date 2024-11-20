from tkinter import ttk
from tkinter import *
import sv_ttk
import helper

CURR_YEAR = 2024

def set_num_players(value, numPlayers, success):
    success.set("1")
    numPlayers.set(value)

def set_division(value, division):
    division.set(value)

def set_stat(value, stat, success):
    success.set("1")
    stat.set(value)

def set_years(start_year, end_year, year1_entry, year2_entry, success1, success2, error_label, division, hold):
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
    if end_year.get() > CURR_YEAR:
        end_year.set(CURR_YEAR)

    hold.set(True)

def gameSetup(root):
    list = []
    objects = []
    hold = BooleanVar(root)
    textcolor = StringVar(root)
    backgroundcolor = StringVar(root)
    errorcolor = StringVar(root)
    textcolor.set('#39957b')
    backgroundcolor.set("#1c1c1c")
    errorcolor.set('yellow')
    root.geometry("700x900")
    root.protocol("WM_DELETE_WINDOW", lambda: (helper.on_close(list, root), hold.set(True)))

    root.grid_columnconfigure(0, weight=1)  # Center the column

    #Display grid for player selection
    success1 = StringVar()
    numPlayers = IntVar()
    objects.append(Label(root, text = "Select Number of Players:", font=('System', 18), fg = '#39957b'))
    objects[-1].pack(pady = 10)
    objects.append(ttk.Frame(root))
    objects[-1].pack() #OBJECTS[1]
    objects.append(ttk.Button(objects[1], text = "2", command = lambda: set_num_players(2, numPlayers, success1)))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[1], text = "3", command = lambda: set_num_players(3, numPlayers, success1)))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[1], text = "4", command = lambda: set_num_players(4, numPlayers, success1)))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5)

    #Display button grid for division selection
    division = StringVar()
    division.set("MLB")
    objects.append(Label(root, text = "Select Division (leave blank for entire MLB):", font=('System', 18), fg = textcolor.get()))
    objects[-1].pack(pady = 10)
    objects.append(ttk.Frame(root)) #OBJECTS[6]
    objects[-1].pack()
    objects.append(ttk.Button(objects[6], text = "AL", command = lambda: set_division("AL", division)))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "AL West", command = lambda: set_division("ALW", division)))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "AL Central", command = lambda: set_division("ALC", division)))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "AL East", command = lambda: set_division("ALE", division)))
    objects[-1].grid(row = 0, column = 3, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "NL", command = lambda: set_division("NL", division)))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "NL West", command = lambda: set_division("NLW", division)))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "NL Central", command = lambda: set_division("NLC", division)))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[6], text = "NL East", command = lambda: set_division("NLE", division)))
    objects[-1].grid(row = 1, column = 3, padx = 5, pady = 5)

    #Display button grid for stat selection
    success2 = StringVar()
    stat = StringVar()
    objects.append(Label(root, text = "Select Stat for Draft:", font=('System', 18), fg = '#39957b'))
    objects[-1].pack(pady = 10)
    objects.append(ttk.Frame(root)) #OBJECTS[16]
    objects[-1].pack()
    objects.append(ttk.Button(objects[16], text = "Batter WAR", command = lambda: set_stat("WAR", stat, success2)))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Hits", command = lambda: set_stat("H", stat, success2)))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Home Runs", command = lambda: set_stat("HR", stat, success2)))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Stolen Bases", command = lambda: set_stat("SB", stat, success2)))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Batting Avg", command = lambda: set_stat("AVG", stat, success2)))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Pitcher WAR", command = lambda: set_stat("PWAR", stat, success2)))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Wins", command = lambda: set_stat("W", stat, success2)))
    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "ERA", command = lambda: set_stat("ERA", stat, success2)))
    objects[-1].grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "ew")
    objects.append(ttk.Button(objects[16], text = "Strikeouts", command = lambda: set_stat("SO", stat, success2)))
    objects[-1].grid(row = 2, column = 2, padx = 5, pady = 5, sticky = "ew")

    #Display text boxes for year selection
    start_year = IntVar()
    end_year = IntVar()
    objects.append(Frame(root)) #OBJECTS[26]
    objects[-1].pack(pady = 10)
    objects.append(Label(objects[26], text = "Start Year", font=('System', 15), fg = '#39957b'))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Entry(objects[26], width = 10))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
    objects.append(Label(objects[26], text = "End Year", font=('System', 15), fg = '#39957b'))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5)
    objects.append(ttk.Entry(objects[26], width = 10))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5)

    #Display switch for team scarcity
    teamscar = BooleanVar(root)
    teamscar.set(True)
    objects.append(Label(root, text = "Team Scarcity", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(root)) #OBJECTS[32]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Button(objects[32], text = "Toggle On", command = lambda: changeteamscarcity(objects, "On", teamscar))) #OBJECTS[33]
    objects.append(ttk.Button(objects[32], text = "Toggle Off", command = lambda: changeteamscarcity(objects, "Off", teamscar))) #OBJECTS[34]
    objects[-1].grid(row = 0, column = 0, pady = 5)

    #Display buttons for themes
    objects.append(Label(root, text = "Theme", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(root)) #OBJECTS[36]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Button(objects[36], text = "Light", command = lambda: (sv_ttk.set_theme('light'), backgroundcolor.set("#fafafa"), changeerrorcolor(objects, 'red', errorcolor))))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Button(objects[36], text = "Dark", command = lambda: (sv_ttk.set_theme('dark'), backgroundcolor.set("#0078d7"), changeerrorcolor(objects, 'yellow', errorcolor))))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5)

    #Display buttons for text color
    objects.append(Label(root, text = "Text Color", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(root)) #OBJECTS[40]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Button(objects[40], text = "Ocean", command = lambda: changetextcolor(objects, '#39957b', textcolor)))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'ew')
    objects.append(ttk.Button(objects[40], text = "Rose", command = lambda: changetextcolor(objects, '#e81747', textcolor)))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'ew')
    objects.append(ttk.Button(objects[40], text = "Spooky", command = lambda: changetextcolor(objects, '#fc8f03', textcolor)))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'ew')
    objects.append(ttk.Button(objects[40], text = "Lime", command = lambda: changetextcolor(objects, '#aee916', textcolor)))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'ew')
    objects.append(ttk.Button(objects[40], text = "Tulip", command = lambda: changetextcolor(objects, '#9415ea', textcolor)))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'ew')
    objects.append(ttk.Button(objects[40], text = "Ruby", command = lambda: changetextcolor(objects, '#cd3f32', textcolor)))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'ew')

    #Display confirm button
    objects.append(Frame(root)) #OBJECTS[47]
    objects[-1].pack(pady = 5)
    objects.append(Frame(root))
    objects[-1].pack(pady = 2)
    objects.append(Label(objects[48], text = "", fg = 'yellow'))
    objects.append(ttk.Button(objects[47], text = "Confirm Settings", command = lambda: set_years(start_year, end_year, objects[28], objects[30], success1, success2, objects[49], division, hold)))
    objects[-1].pack(pady = 5)


    root.wait_variable(hold)

    list.append(numPlayers.get())
    list.append(division.get())
    list.append(stat.get())
    list.append(start_year.get())
    list.append(end_year.get())
    list.append(textcolor.get())
    list.append(backgroundcolor.get())
    list.append(errorcolor.get())
    list.append(teamscar.get())

    if list[0] != -1:
        for obj in objects:
            obj.destroy()
        objects.clear()

    return list

def changetextcolor(objects, color, textcolor):
    objects[0].config(fg = color)
    objects[5].config(fg = color)
    objects[15].config(fg = color)
    objects[27].config(fg = color)
    objects[29].config(fg = color)
    objects[31].config(fg = color)
    objects[35].config(fg = color)
    objects[39].config(fg = color)
    textcolor.set(color)

def changeerrorcolor(objects, color, errorcolor):
    objects[45].config(fg = color)
    errorcolor.set(color)

def changeteamscarcity(objects, state, tf):
    if state == "Off":
        objects[34].grid_forget()
        objects[33].grid(row = 0, column = 0, pady = 5)
        tf.set(False)
    else:
        objects[33].grid_forget
        objects[34].grid(row = 0, column = 0, pady = 5)
        tf.set(True)


    

