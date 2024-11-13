from tkinter import *
from tkinter import ttk
import sv_ttk
import helper

def test_input(numPlayers, division, stat, startYear, endYear, root):
    test_frame = Frame(root)
    test_frame.pack(pady = 10)
    numPlayers_label = Label(test_frame, text = f'Num Players: {numPlayers}')
    numPlayers_label.grid(row = 0, column = 0, padx = 5, pady = 5)
    division_label = Label(test_frame, text = f'Division: {division}')
    division_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    stat_label = Label(test_frame, text = f'Stat: {stat}')
    stat_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    year_label = Label(test_frame, text = f'Years: ({startYear}, {endYear})')
    year_label.grid(row = 3, column = 0, padx = 5, pady = 5)

def confirm_player_names(numPlayers, names, root, error_label, player1_entry, player2_entry, player3_entry = 0, player4_entry = 0):
    if player1_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter name for player 1")
        return
    if player2_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter name for player 2")
        return
    if numPlayers > 2:
        if player3_entry.get() == "":
            helper.throw_error(error_label, message = "Error: Please enter name for player 3")
            return
        if numPlayers > 3:
            if player4_entry.get() == "":
                helper.throw_error(error_label, message = "Error: Please enter name for player 4")
                return

    names.append(player1_entry.get())
    names.append(player2_entry.get())
    if numPlayers > 2:
        names.append(player3_entry.get())
        if numPlayers > 3:
            names.append(player4_entry.get())

    helper.quit(root)

def set_player_names(numPlayers, names, root):
    player_frame = ttk.Frame(root)
    player_frame.pack(pady = 10)

    player1_label = Label(player_frame, text = "Player 1 Name", font=('System', 18), fg = '#39957b')
    player1_label.grid(row = 0, column = 0, padx = 5, pady = 5)
    player1_entry = ttk.Entry(player_frame)
    player1_entry.grid(row = 1, column = 0, padx = 5, pady = 5)

    player2_label = Label(player_frame, text = "Player 2 Name", font=('System', 18), fg = '#39957b')
    player2_label.grid(row = 2, column = 0, padx = 5, pady = 5)
    player2_entry = ttk.Entry(player_frame)
    player2_entry.grid(row = 3, column = 0, padx = 5, pady = 5)

    if numPlayers > 2:
        player3_label = Label(player_frame, text = "Player 3 Name", font=('System', 18), fg = '#39957b')
        player3_label.grid(row = 4, column = 0, padx = 5, pady = 5)
        player3_entry = ttk.Entry(player_frame)
        player3_entry.grid(row = 5, column = 0, padx = 5, pady = 5)

        if numPlayers > 3:
            player4_label = Label(player_frame, text = "Player 4 Name", font=('System', 18), fg = '#39957b')
            player4_label.grid(row = 6, column = 0, padx = 5, pady = 5)
            player4_entry = ttk.Entry(player_frame)
            player4_entry.grid(row = 7, column = 0, padx = 5, pady = 5)

    confirm_frame = ttk.Frame(root)
    confirm_frame.pack(pady = 5)

    error_frame = ttk.Frame(root)
    error_frame.pack(pady = 2)
    error_label = Label(error_frame, text = "", fg = 'yellow')

    if numPlayers == 2:
        confirm_button = ttk.Button(confirm_frame, text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, root, error_label, player1_entry, player2_entry))
    elif numPlayers == 3:
        confirm_button = ttk.Button(confirm_frame, text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, root, error_label, player1_entry, player2_entry, player3_entry))
    else:
        confirm_button = ttk.Button(confirm_frame, text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, root, error_label, player1_entry, player2_entry, player3_entry, player4_entry))
    confirm_button.pack(pady = 5)

    return(names)

def playerNames(inputs):
    numPlayers = inputs[0]
    division = inputs[1]
    stat = inputs[2]
    startYear = inputs[3]
    endYear = inputs[4]

    names = []
    root = Tk()
    sv_ttk.set_theme('dark')
    if numPlayers == 2:
        root.geometry("500x300")
    elif numPlayers == 3:
        root.geometry("500x385")
    elif numPlayers == 4:
        root.geometry("500x470")
    root.protocol("WM_DELETE_WINDOW", lambda: helper.on_close(names, root))

    #test_input(numPlayers, division, stat, startYear, endYear, root2)
    set_player_names(numPlayers, names, root)

    root.mainloop()

    return(names)