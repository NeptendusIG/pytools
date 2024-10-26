######################
# File Backup System #
######################


# -- IMPORTS --
import os, time, shutil, sys
# local
from pytools import logger, AUTOBACKUP_SETTINGS_PATH
from utility import File, InputUtil, Settings, GUI

# -- METADATA --
__title__ = "Backup Automatique"
__options__ = {
    "add_a_path": ("-a, --addpath", "Ajouter un fichier/élément"),
}    
# -- FONCTIONS DÉFINIES --
def ajouter_fichier():
    # Montrer fichiers actuels
    logger.info("OP:Adding source: START"); time.sleep(0.01)
    path = GUI.ask_file("Ajouter élément pour backup")
    if not path:
        logger.info("OP:Adding source: CANCELED\n")
        return False
    if not os.path.exists(path):
        logger.info("OP:Adding source: FileNotFound\n\t%s\n" % path)
        return False
    backup_dir = GUI.ask_dir()
    if not backup_dir:
        logger.info("OP:Adding source: CANCELED\n")
        return False
    # Appliquer les infos
    

def retirer_target():
    pass

def changer_reglages():
    pass

def launch_auto_backup():
    pass

def quit():
    sys.exit(0)



# -- VARIABLES INITIALES --
major_actions = {
    "Activer Backup": launch_auto_backup,
    "Ajouter un fichier/élément": ajouter_fichier,
    "Retirer un fichier/élément": retirer_target,
    "Vérifier/Changer les réglages": changer_reglages,
    "Quitter": quit,
}


# -- OPÉRATIONS PRINCIPALES --
def main_tool():
    logger.info("OP:Autobackup: LAUNCHED")
    time.sleep(0.01)
    print("-- Programme de backup automatique --\n")
    while True:
        new_consol_command()


def new_consol_command():
    # set options
    logger.info(f"Master: New action: asked for")
    time.sleep(0.05)
    for idx, key in enumerate(major_actions, 1):
        print(f"{idx}: {key}")
    cmd = InputUtil.ask_int("une option, terminez par activer le backup.")
    print()
    cmd_keyname = list(major_actions.keys())[cmd-1]
    major_actions[cmd_keyname]()
    logger.info(f"Master: New action: processed ({cmd_keyname})\n")