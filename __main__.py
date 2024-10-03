#####################################
#          Titre - Date             #
#####################################
# NOTES :
"""
"""
# -- IMPORTS --
# Modules
import sys
from utility import GUI, Settings # type: ignore
from pytools.function_dir.autonext import main_tool

# Settings
from pytools import logger
from pytools import SETTINGS_PATH

# -- OPÉRATIONS DÉFINIES --


# -- VARIABLES INITIALES --
tools = {
    "autonext": main_tool,
    "obsidiansort": None 
}


# -- FONCTIONS MAÎTRES --
def apply_tool():
    logger.debug(f"Argv target an existing tool: {sys.argv[1] in tools = }")
    logger.info(f"Target tool: '{sys.argv[1]}'")
    tools[sys.argv[1]]()


# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -
    # - Programme -
    logger.info("Starting program")
    print()
    apply_tool()
