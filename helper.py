from tkinter import *
import pywinstyles, sys
import sv_ttk
import ctypes

def throw_error(error_label, message, row = 0):
    error_label.config(text = message)
    error_label.grid(row = row, column = 0, padx = 5, pady = 5)

def quit(root):
    root.destroy()

def on_close(var, root, var2 = 0):
    print('Helper called')

    if isinstance(var2, bool):
        print('var2 exists')
        var2 = True

    if isinstance(var, list):
        var.append(-1)
    elif isinstance(var, bool):
        print('bool')
        var = True
    elif isinstance(var, BooleanVar):
        print('boolean')
        var.set(True)
        print('before destroy')
    else:
        print('else')
        var = -1

    print("returning")
    quit(root)
    #root.destroy()

def apply_theme_to_titlebar(root):
    # Determine if the platform is Windows and version 10+
    if sys.platform == "win32":
        version = sys.getwindowsversion()
        
        if version.major == 10:
            # Get the theme color based on sv_ttk or similar theme management module
            theme_color = "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa"
            # Convert the color to a format usable by ctypes (RGB int)
            color = int(theme_color[1:], 16)

            # Apply custom color using ctypes
            hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(color)), ctypes.sizeof(ctypes.c_int))

            # On Windows 10, a quick alpha toggle can force a refresh in Tkinter
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)
    