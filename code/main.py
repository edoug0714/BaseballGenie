from tkinter import *
import playerNames
import subprocess
import gameSetup
import importlib
import sv_ttk
import Game
import os
import sys

CURR_YEAR = 2024
REQUIRED_FILES = ['Game.py', 'gameSetup.py', 'helper.py', 'playerNames.py', 'merged_batter_data.csv', 'merged_pitcher_data.csv', 'season_name_batters.csv', 'season_name_pitchers.csv']

def check_python():
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Python is installed: {result.stdout.strip()}")
        else:
            print("Python is not installed.")
            exit(1)
    except FileNotFoundError:
        print("Python is not installed.")
        exit(1)

def check_requirements():
    requirements_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'requirements.txt')
    try:
        with open(requirements_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        missing_packages = []
        for package in packages:
            try:
                # Attempt to import the package
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
    curr = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(curr, '..', 'data')
    missing_files = []
    for file in REQUIRED_FILES:
        try:
            if file.endswith('.csv'):
                file_path = os.path.join(data_folder, file)
            else:
                file_path = os.path.join(curr, file)
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
        print('NEW GAME!')
        inputs = gameSetup.gameSetup(root)
        if inputs[0] == -1:
            window_destroy = True
            break
        names = playerNames.playerNames(root, inputs)
        if names[0] == -1:
            window_destroy = True
            break
        game = Game.Game(root, inputs, names)

        print("Made it to the end")

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



