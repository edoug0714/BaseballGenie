from tkinter import ttk
from tkinter import *
import sv_ttk
import helper

CURR_YEAR = 2024

def gameSetup(root):
    list = []
    objects = []
    hold = BooleanVar(root)
    backgroundcolor = StringVar(value = "#1c1c1c")
    errorcolor = StringVar(value = 'yellow')
    textcolor = StringVar(value = '#39957b')
    root.geometry("1020x400")
    root.protocol("WM_DELETE_WINDOW", lambda: (helper.on_close(list, root), hold.set(True)))

    #Format frame to fill screen and have 6 columns, 3 rows
    objects.append(ttk.Frame(root)) #OBJECTS[0] ORIGINAL FRAME
    objects[-1].pack(fill = 'both', expand = 'True')
    for i in range(6):
        objects[-1].grid_rowconfigure(i, weight=1)
    for i in range(3):
        root.grid_columnconfigure(i, weight=1)

    #Display grid for player selection
    numPlayers = IntVar(value = 2)
    objects.append(ttk.Frame(objects[0])) #OBJECTS[1] SUBFRAME 0,0
    objects[-1].grid(row = 0, column = 0, rowspan = 3, padx = 25, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[1], text = "Select Number of Players:", font=('System', 18), fg = '#39957b'))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'nsew')
    objects.append(ttk.Frame(objects[1])) #OBJECTS[3]
    objects[-1].grid(row = 1, column = 0, pady = 10, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[3], text = "2", value = 2, variable = numPlayers))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[3], text = "3", value = 3, variable = numPlayers))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[3], text = "4", value = 4, variable = numPlayers))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nsew')

    #Display button grid for division selection
    division = StringVar(value = 'MLB')
    objects.append(ttk.Frame(objects[0])) #OBJECTS[7] SUBFRAME 1, 0
    objects[-1].grid(row = 3, column = 0, rowspan = 3, padx = 10, pady = 5, sticky = 'nsew')
    objects.append(Label(objects[7], text = "Select Division:", font=('System', 18), fg = textcolor.get()))
    objects[-1].grid(row = 0, column = 0, pady = 10, sticky = 'nsew')
    objects.append(ttk.Frame(objects[7])) #OBJECTS[9]
    objects[-1].grid(row = 1, column = 0, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'MLB', value = 'MLB', variable = division, width = 5))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'AL', value = 'AL', variable = division, width = 5))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'NL', value = 'NL', variable = division, width = 5))
    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'AL West', value = 'ALW', variable = division, width = 10))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'AL Central', value = 'ALC', variable = division, width = 10))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'AL East', value = 'ALE', variable = division, width = 10))
    objects[-1].grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'NL West', value = 'NLW', variable = division, width = 10))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'NL Central', value = 'NLC', variable = division, width = 10))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[9], text = 'NL East', value = 'NLE', variable = division, width = 10))
    objects[-1].grid(row = 2, column = 2, padx = 5, pady = 5, sticky = 'nsew')

    #Display text boxes for year selection
    start_year = IntVar()
    end_year = IntVar()
    objects.append(Frame(objects[0])) #OBJECTS[19]
    objects[-1].grid(row = 0, column = 1, rowspan = 3, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[19], text = "Start Year", font=('System', 18), fg = '#39957b', width = 8))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 10, sticky = 'nsew')
    objects.append(ttk.Entry(objects[19], width = 10))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(Label(objects[19], text = "End Year", font=('System', 18), fg = '#39957b', width = 8))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Entry(objects[19], width = 10))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')

    #Display button grid for stat selection
    stat = StringVar(value = 'H')
    objects.append(Frame(objects[0])) #OBJECTS[24]
    objects[-1].grid(row = 3, column = 1, rowspan = 3, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[24], text = "Select Stat for Draft:", font=('System', 18), fg = '#39957b'))
    objects[-1].grid(row = 1, column = 1, pady = 10, sticky = 'nsew')
    objects.append(ttk.Frame(objects[24])) #OBJECTS[26]
    objects[-1].grid(row = 2, column = 1, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Home Runs', value = 'HR', variable = stat, width = 10))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Batter WAR', value = 'WAR', variable = stat, width = 10))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Hits', value = 'H', variable = stat, width = 5))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Stolen Bases', value = 'SB', variable = stat, width = 10))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Batting Avg', value = 'AVG', variable = stat, width = 10))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'ERA', value = 'ERA', variable = stat, width = 5))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Strikeouts', value = 'SO', variable = stat, width = 10))
    objects[-1].grid(row = 2, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Pitcher WAR', value = 'PWAR', variable = stat, width = 10))
    objects[-1].grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[26], text = 'Wins', value = 'W', variable = stat, width = 5))
    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5, sticky = 'nsew')

    #Display switch for team scarcity
    teamscar = BooleanVar(value = True)
    objects.append(Frame(objects[0])) #OBJECTS[36]
    objects[-1].grid(row = 0, column = 2, rowspan = 2, padx = 25, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[36], text = "Team Scarcity", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(objects[36])) #OBJECTS[38]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Radiobutton(objects[38], text = 'On', value = True, variable = teamscar, width = 5))
    objects[-1].grid(row = 0, column = 0, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[38], text = 'Off', value = False, variable = teamscar, width = 4))
    objects[-1].grid(row = 0, column = 1, pady = 5, sticky = 'nsew')

    #Display buttons for themes
    theme = StringVar(value = 'dark')
    objects.append(Frame(objects[0])) #OBJECTS[41]
    objects[-1].grid(row = 2, column = 2, rowspan = 2, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[41], text = "Theme", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(objects[41])) #OBJECTS[43]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Radiobutton(objects[43], text = 'Dark', value = 'dark', variable = theme, width = 5, command = lambda: (sv_ttk.set_theme('dark'), backgroundcolor.set("#0078d7"), changeerrorcolor(objects, 'yellow', errorcolor))))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[43], text = 'Light', value = 'light', variable = theme, width = 4, command = lambda: (sv_ttk.set_theme('light'), backgroundcolor.set("#fafafa"), changeerrorcolor(objects, 'red', errorcolor))))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nsew')

    #Change color for text color radiobuttons
    style = ttk.Style()
    style.configure('Ocean.TRadiobutton', foreground = '#39957b', font = ('Fixedsys', 10))
    style.configure('Ruby.TRadiobutton', foreground = '#cd3f32', font = ('Fixedsys', 10))
    style.configure('Spooky.TRadiobutton', foreground = '#fc8f03', font = ('Fixedsys', 10))
    style.configure('Rose.TRadiobutton', foreground = '#e81747', font = ('Fixedsys', 10))
    style.configure('Lime.TRadiobutton', foreground = '#aee916', font = ('Fixedsys', 10))
    style.configure('Tulip.TRadiobutton', foreground = '#9415ea', font = ('Fixedsys', 10))

    #Display buttons for text color
    objects.append(Frame(objects[0])) #OBJECTS[46]
    objects[-1].grid(row = 4, column = 2, rowspan = 2, padx = 25, pady = 10, sticky = 'nsew')
    objects.append(Label(objects[46], text = "Text Color", font=('System', 12), fg = '#39957b'))
    objects[-1].pack(pady = 5)
    objects.append(Frame(objects[46])) #OBJECTS[48]
    objects[-1].pack(pady = 5)
    objects.append(ttk.Radiobutton(objects[48], text = 'Ocean', value = '#39957b', variable = textcolor, width = 5, style = 'Ocean.TRadiobutton', command = lambda: changetextcolor(objects, '#39957b')))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[48], text = 'Ruby', value = '#cd3f32', variable = textcolor, width = 4, style = 'Ruby.TRadiobutton', command = lambda: changetextcolor(objects, '#cd3f32')))
    objects[-1].grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[48], text = 'Spooky', value = '#fc8f03', variable = textcolor, width = 6, style = 'Spooky.TRadiobutton', command = lambda: changetextcolor(objects, '#fc8f03')))
    objects[-1].grid(row = 0, column = 2, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[48], text = 'Rose', value = '#e81747', variable = textcolor, width = 5, style = 'Rose.TRadiobutton', command = lambda: changetextcolor(objects, '#e81747')))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[48], text = 'Lime', value = '#aee916', variable = textcolor, width = 4, style = 'Lime.TRadiobutton', command = lambda: changetextcolor(objects, '#aee916')))
    objects[-1].grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')
    objects.append(ttk.Radiobutton(objects[48], text = 'Tulip', value = '#9415ea', variable = textcolor, width = 6, style = 'Tulip.TRadiobutton', command = lambda: changetextcolor(objects, '#9415ea')))
    objects[-1].grid(row = 1, column = 2, padx = 5, pady = 5, sticky = 'nsew')

    #Display confirm button
    objects.append(Frame(objects[0])) #OBJECTS[55]
    objects[-1].grid(row = 7, column = 1, rowspan = 1, pady = 10)
    objects.append(Frame(objects[0])) #OBJECTS[56]
    objects[-1].grid(row = 8, column = 1, rowspan = 1, pady = 10) 
    objects.append(Label(objects[56], text = "", fg = 'yellow')) #OBJECTS[57]
    objects.append(ttk.Button(objects[55], text = "Confirm Settings", command = lambda: set_years(start_year, end_year, objects[21], objects[23], objects[57], division, hold)))
    objects[-1].pack(pady = 5)

    #Hold screen until confirm button is pressed
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

    #Clear screen and objects list
    if list[0] != -1:
        for obj in objects:
            obj.destroy()
        objects.clear()

    return list

def set_years(start_year, end_year, year1_entry, year2_entry, error_label, division, hold):
    #Check for year1 entry
    if year1_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter year values.")
        return
    #Check for year2 entry
    if year2_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter year values.")
        return
    #Verify years are integers
    if not (year1_entry.get().isnumeric() or (year2_entry.get().isnumeric())):
        helper.throw_error(error_label, message = "Error: Years must be formatted as numbers.")
        return

    start_year.set(year1_entry.get())
    end_year.set(year2_entry.get())

    #Verify start year is less than end year
    if start_year.get() > end_year.get():
        helper.throw_error(error_label, message = "Error: Please make sure start year < end year.")
        return
    #Verify start year is not in the future
    if start_year.get() > CURR_YEAR:
        helper.throw_error(error_label, message = "Error: Sorry, we do not have stats from the future.")
        return
    #Verify end year is not from before 1901
    if end_year.get() < 1901:
        helper.throw_error(error_label, message = "Error: Sorry, we do not have stats from before 1901.")
        return
    #Verify division games start after 1969
    if (division.get() in ["ALW", "ALC", "ALE", "NLW", "NLC", "NLE"]) & (end_year.get() < 1969):
        helper.throw_error(error_label, message = f"Error: Divisions did not exist before 1969.")
        return
    #Verify central division games start after 1994
    if (division.get() in ["ALC", "NLC"]) & (end_year.get() < 1994):
        helper.throw_error(error_label, message = "Error: Central divisions did not exist before 1994.")
        return
    
    #Edit year ranges if out of scope
    if division in ["ALC", "NLC"]:
        if start_year.get() < 1994:
            start_year.set(1993)
    elif division in ["ALW", "ALE", "NLW", "NLE"]:
        if start_year.get() < 1969:
            start_year.set(1969)
    else:
        if start_year.get() < 1901:
            start_year.set(1901)
    if end_year.get() > CURR_YEAR:
        end_year.set(CURR_YEAR)

    hold.set(True)

def changetextcolor(objects, color):
    objects[2].config(fg = color)
    objects[8].config(fg = color)
    objects[20].config(fg = color)
    objects[22].config(fg = color)
    objects[25].config(fg = color)
    objects[37].config(fg = color)
    objects[42].config(fg = color)
    objects[47].config(fg = color)

def changeerrorcolor(objects, color, errorcolor):
    objects[50].config(fg = color)
    errorcolor.set(color)


    

