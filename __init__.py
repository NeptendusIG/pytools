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



# - SET ENVIRONMENT -
default_settings = {
    ""
}
Settings.ConfigPath.force_existence("autonext", {"saved_sessions": []}, file_name="autonext_config.json")  # Crée le fichier de configuration s'il n'existe pas


# - IMPORTS EXTERNES -
import sys, time
from utility import GUI, File

# - SETTINGS -
logger = Settings.setup_logging("debugging")
logger.info("PYTOOLS: INIT: Logger initialized")
    # SETTINGS_PATH = os.getenv("PYTOOLS_SETTINGS_PATH", DEFAULT_SETTINGS_PATH)
AUTONEXT_SETTINGS_PATH = Settings.ConfigPath.set_path("pytools", file_name="autonext_config.json")



