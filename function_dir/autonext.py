#   Module local de fonctions
# ----------------------------
#     Python Personal Tools
# DATE: 27/9/2024
# VERSION: 1.0
# ----------------------------
"""  -- Structures des fonctions disponibles --
Classement 1
 - function_name(arg1)
- f2(arg1)
Classement 2
"""


# -- IMPORTS --
# Modules basiques
import pyautogui
import os, time
# Modules renommés
import tkinter as tk
# Imports spécifiques
from typing import Any, Optional
# Imports locaux
from utility import File, Settings, GUI
from pytools.class_dir.Apps import Timer


# Paramètres
logger = Settings.setup_logging("debugging")

# -- FONCTIONS DÉFINIES --
def main_tool():
    """Lancer l'outil
    1 - Fichier à lire/ouvrir
    2 - La configuration
    3 - Lancer l'outil
    """
    logger.info("Tool: INITIALISE main tool")
    filepath, seconds, count = full_minimal_setup()
    logger.debug(f"Tool: given SETTINGS - seconds: {seconds}, count: {count}")
    logger.info(f"Tool: START autoslide with {seconds} seconds and {count} slides")
    File.open_file(filepath)
    start_autoslide(filepath=filepath, seconds=seconds, count=count)


# 1 - Set up
def full_minimal_setup():
    """Mise en place complète
    """
    logger.debug("Tool: Autonext: Setup: START")
    return GUI.ask_file(), int(input("Entrez le temps par élément (s): ")), int(input("Entrez le nombre de slides: "))


def choose_file():
    """Choisir le fichier à lire
    """
    path = GUI.ask_file()
    select_settings(path)
    File.open_file(path)


def select_settings(path: str):
    """Sélectionner les paramètres
    """
    window = GUI.set_basic_window("Paramètres")
    seconds = int(GUI.ask_entry("Entrez temps par élément", "250x100"))


# 2 - Actions
def next_slide():
    """Slide suivant
    """
    logger.debug("Tool: Autonext: Nextslide: Processing  slide")
    pyautogui.keyDown('option',)
    pyautogui.press('down')
    time.sleep(0.1)
    pyautogui.keyUp('option')


# 3 - Contrôle de l'outil 
def start_autoslide(filepath: str, seconds: int, count: int=10):
    """Démarre le diaporama automatique
    paramètres
    """
    logger.info("Tool: Autonext: Initialisation")
    i = 0
    time.sleep(5)
    logger.info("Tool: Autonext: START")
    temps = tk.StringVar()
    while i<50 and i<count:
        if i>=count:
            logger.info("Tool: Autonext: END")
            break
        # attendre
        timer(seconds)
        # slide suivant
        File.open_file(filepath)
        next_slide()
        logger.debug(f"Tool: Autonext: Loop: ACTIVE (i, count) = ({i}, {count})")
        i+=1

# 4 - Affichage

def timer(seconds: int):
    """Fenêtre affichant les secondes restantes"""
    wind = GUI.set_basic_window("Timer")
    app = Timer(wind, seconds)
    wind.mainloop()




def stop_slides():
    global is_running
    is_running = False

# -- TESTS ET EXEMPLES --
if __name__ == '__main__':
    # Variables
    variable = None
    objet = None
    # Programme test
    time.sleep(3)
    next_slide()
