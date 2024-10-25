# ----------------------------
#   Module local de fonctions
#     Python Personal Tools 
# DATE: 28/9/2024
# VERSION: 1.0
# ----------------------------
"""  -- Structures des fonctions disponibles --
Classement 1
 - function_name(arg1)
Classement 2
- f2(arg1)
"""


# -- IMPORTS --
# Modules basiques
import os, logging
# Modules renommés
import tkinter as tk
# Imports spécifiques
from typing import Any, Optional
# Imports locaux
from utility import File, Settings, GUI


# Paramètres
logger = Settings.setup_logging("debugging")
__options__ = {
    "administrator": ("-s, --sudo", "Exécute le script en privilèges administrateur")
}

OBSIDIAN_PATH = "/Users/gaetan/Library/Mobile Documents/iCloud~md~obsidian/Documents/VaultCODE"

TAGS_DIR_ASSIGNATIONS = {
    "#type/project": "01 - Projects",
    "#type/area": "02 - Areas",
    "#type/input": "03 - Resources",
    "#type/evergreen": "04 - Evergreen",
    "#type/thoughts": "05 - Thoughts",
    "#type/journal": "06 - Journal",
    "#type/brainstorm": "07 - Brainstorm",
    "#type/moc": "03 - Resources/01 - MOC"
}

TAGS_EMOJI_ASSIGNATIONS = {
    "#type/project": "F09F9AA7",
    "#type/area": "02 - Areas",
    "#type/input": "03 - Resources",
    "#type/evergreen": "04 - Evergreen",
    "#type/thoughts": "05 - Thoughts",
    "#type/journal": "06 - Journal",
    "#type/brainstorm": "07 - Brainstorm",
}

DIR_TO_INSPECT = [
    "/00 - Inbox",
]



# -- FONCTIONS DÉFINIES --
# 1 - Analysis
def inspect_each_dir():
    """
    """
    pass


# 2 - Auto classement
def apply_autoclassification():
    """
    @param: Global dict TAGS_DIR_ASSIGNATIONS
    @param: Global dict DIR_TO_INSPECT
    @param: Global str OBSIDIAN_PATH
    """
    assert os.path.exists(OBSIDIAN_PATH), f"Le dossier '{OBSIDIAN_PATH}' n'existe pas ou n'est pas accessible."

    
    for dir in DIR_TO_INSPECT:
        for file in os.listdir(f"{OBSIDIAN_PATH}/{dir}"):
            if file.endswith(".md"):
                file_path = f"{OBSIDIAN_PATH}/{dir}/{file}"
                tags = File.get_tags(file_path)
                for tag in tags:
                    if tag in TAGS_DIR_ASSIGNATIONS:
                        new_dir = TAGS_DIR_ASSIGNATIONS[tag]
                        File.move_file(file_path, f"{OBSIDIAN_PATH}/{new_dir}/{file}")
                        break
    


# -- TESTS ET EXEMPLES --
if __name__ == '__main__':
    # Variables
    variable = None
    objet = None
    # Programme test
    function_name(arg)
