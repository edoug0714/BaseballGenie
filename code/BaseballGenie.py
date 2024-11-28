import horizontalSetup
from tkinter import *
import playerNames
import subprocess
import importlib
import pathlib
import sv_ttk
import Game
import os
import sys

CURR_YEAR = 2024
REQUIRED_FILES = ['code/Game.py', 'code/horizontalSetup.py', 'code/verticalSetup.py', 'code/helper.py', 'code/playerNames.py', 'data/merged_batter_data.csv', 'data/merged_pitcher_data.csv', 'data/season_name_batters.csv', 'data/season_name_pitchers.csv']

def check_python():
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Python is installed: {result.stdout.strip()}")
        else:
            print("Python is not installed. You can download the latest version from here: https://www.python.org/downloads/")
            exit(1)
    except FileNotFoundError:
        print("Python is not installed. You can download the latest version from here: https://www.python.org/downloads/")
        exit(1)

def check_requirements():
    requirements_file = pathlib.Path(sys._MEIPASS) / "requirements.txt"
    try:
        with open(requirements_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        missing_packages = []
        for package in packages:
            try:
                importlib.import_module(package)
            except ModuleNotFoundError:
                missing_packages.append(package)
        if missing_packages:
            print(f"The following packages are missing: {', '.join(missing_packages)}")
            print("Run 'pip install -r requirements.txt' to install them.")
            sys.exit(1)
        else:
            print("All required packages are installed.")
    except FileNotFoundError:
        print(f"Error: {requirements_file} not found.")
        sys.exit(1)

def check_files():
    missing_files = []
    for file in REQUIRED_FILES:
        try:
            file_path = pathlib.Path(sys._MEIPASS) / file
            if not os.path.isfile(file_path):
                missing_files.append(file)
        except Exception as e:
            print(f"Error checking file {file}: {e}")
            missing_files.append(file)
    if missing_files:
        print(f"Error: The following required files are missing: {', '.join(missing_files)}")
        sys.exit(2)
    else:
        print("All reqired files are present.")

def main():
    root = Tk()
    sv_ttk.set_theme('dark')
    window_destroy = False
    while True:
        inputs = horizontalSetup.gameSetup(root)
        if inputs[0] == -1:
            window_destroy = True
            break
        names = playerNames.playerNames(root, inputs)
        if names[0] == -1:
            window_destroy = True
            break
        game = Game.Game(root, inputs, names)

        if game.exit:
            break
        elif game.play_again:
            continue

    if window_destroy:
        return
    else:
        root.destroy()
        return

check_python()
check_requirements()
check_files()
main()



