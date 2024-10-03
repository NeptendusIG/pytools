#############################
#      Pytools Project      #
#  03/10/2024               #
#  __init__.py              #
#############################
# Pour le INIT 
import os
from pathlib import Path

# - NOTES -


# - IMPORTS -
import sys, time
from utility import GUI, File, Settings
import log_config

# - SETTINGS -
logger = Settings.setup_logging("debugging")


# - VARIABLES DE L'APPLICATION -
    # Chemin par défaut vers le fichier de configuration
DEFAULT_SETTINGS_PATH = Path(__file__).parent.parent / "config" / "settings.json"
    # Variable globale pour définir l'emplacement du fichier de configuration
SETTINGS_PATH = os.getenv("PYTOOLS_SETTINGS_PATH", DEFAULT_SETTINGS_PATH)
