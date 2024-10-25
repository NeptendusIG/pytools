#############################
#      Pytools Project      #
#  03/10/2024               #
#  __init__.py              #
#############################
# Pour le INIT 
import os
from pathlib import Path
import log_config
from utility import Settings


# - METADATA -
__version__ = "0.1.0"
__author__ = "Gaétan Lepage"
__help__ = """
    -a, --autonext : (autonext) Outil de lecture automatique de slides
    -c, --capttxt : (capturetxt) Capture le texte de l'écran
    -y, --ytdownl : (ytdownload) Téléchargement de vidéo YouTube
    -o, --obsort : (obsidiansort) Trie les notes Obsidian
""" # Arguments accessibles sur cette application
__call__ = "pytools"
__options__ = {
    "autonext": ("-a, --autonext", "Outil de lecture automatique de slides"),
    "capturetxt": ("-c, --capttxt", "Capture le texte de l'écran"),
    "ytdownload": ("-y, --ytdownl", "Téléchargement de vidéo YouTube"),
    "obsidiansort": ("-o, --obsort", "Trie et gère les notes Obsidian"),
}
__title__ = "Python Tools"


# - SET ENVIRONMENT -
default_autonext_config = {"saved_sessions": []}
rootpath: Path = Settings.ConfigPath.set_directories("pytools", "autonext")
Settings.ConfigPath.set_jsonfile(rootpath, "config.json", default_autonext_config, exist_ok=True)  
AUTONEXT_SETTINGS_PATH = Settings.ConfigPath.get_path("pytools", "autonext", "config.json")  


# - IMPORTS EXTERNES -
import sys, time
from utility import GUI, File

# - SETTINGS -
logger = Settings.setup_logging("debugging")
logger.info("PYTOOLS: INIT: Logger initialized")