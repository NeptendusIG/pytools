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