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

# Settings
from pytools import logger
from pytools import AUTONEXT_SETTINGS_PATH


# -- FONCTIONS DÉFINIES --
def main_tool():
    """Lancer l'outil
    1 - Fichier à lire/ouvrir
    2 - La configuration
    3 - Lancer l'outil
    """
    logger.info("Tool: INITIALISE main tool")
    # 1 - Configuration / Paramètres (/annuler)
    session = setup_menu()
    if session is None:
        logger.error("Tool: CANCELD (No parameters)")
        return
    logger.debug(f"Tool: given SETTINGS - session set ({session})")
    # 2 - Lancer l'outil
    filepath, seconds, count = session["parameters"]
    logger.info(f"Tool: START autoslide with {seconds} seconds and {count} slides")
    start_autoslide(filepath, seconds, count)
    logger.info("")
    # 3 - Sauvegarder / Supprimer les paramètres
    quit_session(session)
    logger.info("Tool: END")



# - 1 - Set up
def setup_menu() -> Optional[dict]:
    """Gestion de l'historique des modifications
    """
    logger.debug("Tool: Autonext: Setup: START")
    """Proposer les config sauvegardées (/nouaaux paramètres)
    """
    # 1 - Charger les paramètres sauvegardés
    saved_session: dict[str, (str, tuple)] = File.JsonFile.get_value(AUTONEXT_SETTINGS_PATH, "saved_sessions")
    logger.debug(f"Tool: Autonext: Config_menu: saved_sessions = {saved_session}")
    # 2 - Proposer les config
    print("0: Nouvelle configuration")
    for i, session in enumerate(saved_session, 1):
        name = session["name"]
        path, seconds, count = session["parameters"]
        if not os.path.exists(path):
            logger.debug(f"Tool: Autonext: Config_menu: Stored File not found: {path}")
            continue
        print(f"{i}: {name} ({seconds}s, {count} steps)")
    # 3 - Traiter le choix
    choice = int(input("Choisissez une configuration: "))
    if choice == 0:
        selected_session = create_new_session()
    else:
        selected_session = saved_session[choice-1]
    return selected_session
    

def create_new_session() -> Optional[dict]:
    """Créer une nouvelle session, ou annuler.
    """
    logger.debug("Tool: Autonext: Setup-new: START (parameters + name)")
    filepath = GUI.ask_file()
    if not filepath:
        logger.error("Tool: Autonext: Setup-new: CANCELD (No file selected)")
        return
    interval = int(input("Entrez le temps par élément (s): "))
    if not interval:
        logger.error("Tool: Autonext: Setup-new: CANCELD (No interval selected)")
        return
    count = int(input("Entrez le nombre de slides: "))
    if not count:
        logger.error("Tool: Autonext: Setup-new: CANCELD (No count selected)")
        return
    name = input("Entrez un nom pour cette configuration: ")
    if not name:
        logger.error("Tool: Autonext: Setup-new: CANCELD (No name selected)")
        return
    return {"name": name, "parameters": (filepath, interval, count)}


def quit_session(used_session):
    print("Voulez-vous sauvegarder cette configuration ?")
    save = input("(S-save / D-delete): ")
    logger.debug(f"Quit session: get response")
    if "s" in save.lower():
        save_session(used_session)
    elif "d" in save.lower():
        delete_session(used_session)
    else:
        print("Configuration non sauvegardée")
    print("managed")

def save_session(used_session: dict):
    """Sauvegarder la session si elle est nouvelle (sinon rien faire)"""
    backup = File.JsonFile.get_value(AUTONEXT_SETTINGS_PATH, "saved_sessions")
    if used_session in backup:
        return
    backup.append(used_session)
    File.JsonFile.set_value(AUTONEXT_SETTINGS_PATH, "saved_sessions", backup)
    logger.info("Tool: Autonext: Session saved")


def delete_session(used_session: dict):
    backup = File.JsonFile.get_value(AUTONEXT_SETTINGS_PATH, "saved_sessions")
    if used_session not in backup:
        return
    backup.remove(used_session)
    File.JsonFile.set_value(AUTONEXT_SETTINGS_PATH, "saved_sessions", backup)
    logger.info("Tool: Autonext: Session deleted")




# - 2 - Actions
def next_slide():
    """Slide suivant
    """
    logger.debug("Tool: Autonext: Nextslide: Processing  slide")
    pyautogui.keyDown('option',)
    pyautogui.press('down')
    time.sleep(0.1)
    pyautogui.keyUp('option')


# - 3 - Contrôle de l'outil 
def start_autoslide(filepath: str, seconds: int, count: int=10):
    """Démarre le diaporama automatique
    paramètres
    """
    File.open_file(filepath)
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
        is_forced_stop = timer(seconds)
        if is_forced_stop:
            logger.info("Tool: Autonext: forced STOP")
            break
        # slide suivant
        File.open_file(filepath)
        next_slide()
        logger.debug(f"Tool: Autonext: Loop: ACTIVE (i, count) = ({i}, {count})")
        i+=1

# - 4 - Affichage

def timer(seconds: int):
    """Fenêtre affichant les secondes restantes"""
    wind = GUI.set_basic_window("Timer")
    app = Timer(wind, seconds)
    wind.mainloop()
    return app.get_result()



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
