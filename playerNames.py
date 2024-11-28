from tkinter import ttk
from tkinter import *
import helper

def playerNames(root, inputs):
    numPlayers = inputs[0]
    textcolor = inputs[5]
    errorcolor = inputs[7]
    names = []
    objects = []
    hold = BooleanVar(root)

    if numPlayers == 2:
        root.geometry("500x380")
    elif numPlayers == 3:
        root.geometry("500x465")
    elif numPlayers == 4:
        root.geometry("500x550")
    root.protocol("WM_DELETE_WINDOW", lambda: (helper.on_close(names, root), hold.set(True)))

    #Display textboxes for entering player names
    objects.append(ttk.Frame(root))
    objects[-1].pack(pady = 10)
    objects.append(Label(objects[0], text = "Player 1 Name", font=('System', 18), fg = textcolor))
    objects[-1].grid(row = 0, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Entry(objects[0]))
    objects[-1].grid(row = 1, column = 0, padx = 5, pady = 5)
    objects.append(Label(objects[0], text = "Player 2 Name", font=('System', 18), fg = textcolor))
    objects[-1].grid(row = 2, column = 0, padx = 5, pady = 5)
    objects.append(ttk.Entry(objects[0])) #OBJECTS[4]
    objects[-1].grid(row = 3, column = 0, padx = 5, pady = 5)
    if numPlayers > 2:
        objects.append(Label(objects[0], text = "Player 3 Name", font=('System', 18), fg = textcolor))
        objects[-1].grid(row = 4, column = 0, padx = 5, pady = 5)
        objects.append(ttk.Entry(objects[0])) #Objects[6]
        objects[-1].grid(row = 5, column = 0, padx = 5, pady = 5)
        if numPlayers > 3:
            objects.append(Label(objects[0], text = "Player 4 Name", font=('System', 18), fg = textcolor))
            objects[-1].grid(row = 6, column = 0, padx = 5, pady = 5)
            objects.append(ttk.Entry(objects[0])) #Objects[8]
            objects[-1].grid(row = 7, column = 0, padx = 5, pady = 5)
    
    #Display radiobuttons for turning on/off random order
    tf = BooleanVar(value = True)
    objects.append(ttk.Frame(root))
    objects[-1].pack(pady = 10)
    objects.append(Label(objects[-1], text = "Randomize Order", font=('Fixedsys', 12), fg = textcolor))
    objects[-1].grid(row = 0, column = 0, pady = 5)
    objects.append(ttk.Radiobutton(objects[-2], text = 'On', value = True, variable = tf))
    objects[-1].grid(row = 1, column = 0, pady = 5)
    objects.append(ttk.Radiobutton(objects[-3], text = 'Off', value = False, variable = tf))
    objects[-1].grid(row = 2, column = 0, pady = 5)

    #Define frames for confirm button and error messages
    objects.append(ttk.Frame(root)) #Confirm button frame
    objects[-1].pack(pady = 10)
    objects.append(ttk.Frame(root)) #Error message frame
    objects[-1].pack(pady = 10)

    if numPlayers == 2:
        objects.append(Label(objects[-1], text = "", fg = errorcolor))
        objects.append(ttk.Button(objects[-3], text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, objects[-2], hold, tf, objects[2], objects[4])))
    elif numPlayers == 3:
        objects.append(Label(objects[-1], text = "", fg = errorcolor))
        objects.append(ttk.Button(objects[-3], text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, objects[-2], hold, tf, objects[2], objects[4], objects[6])))
    else:
        objects.append(Label(objects[-1], text = "", fg = errorcolor))
        objects.append(ttk.Button(objects[-3], text = "Confirm", command = lambda: confirm_player_names(numPlayers, names, objects[-2], hold, tf, objects[2], objects[4], objects[6], objects[8])))
    objects[-1].pack(pady = 5)

    #Hold screen until confirm button is pressed
    root.wait_variable(hold)

    #If the program has not been exited, clear screen
    if names[0] != -1:
        for obj in objects:
            obj.destroy()
        objects.clear()

    return(names)

def confirm_player_names(numPlayers, names, error_label, hold, tf, player1_entry, player2_entry, player3_entry = 0, player4_entry = 0):
    #Verify player1 entry is not empty
    if player1_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter name for player 1")
        return
    #Verify player2 entry is not empty
    if player2_entry.get() == "":
        helper.throw_error(error_label, message = "Error: Please enter name for player 2")
        return
    #Verify player3 entry is not empty
    if numPlayers > 2:
        if player3_entry.get() == "":
            helper.throw_error(error_label, message = "Error: Please enter name for player 3")
            return
        #Verify player4 entry is not empty
        if numPlayers > 3:
            if player4_entry.get() == "":
                helper.throw_error(error_label, message = "Error: Please enter name for player 4")
                return

    #Add random order setting and player names to list and return
    names.append(tf)
    names.append(player1_entry.get())
    names.append(player2_entry.get())
    if numPlayers > 2:
        names.append(player3_entry.get())
        if numPlayers > 3:
            names.append(player4_entry.get())
    
    hold.set(True)