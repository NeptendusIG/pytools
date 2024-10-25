#####################################
#          Titre - Date             #
#####################################
# NOTES :
"""
"""
# -- IMPORTS --
import sys
from typing import Callable 
from utility import GUI, Settings # type: ignore

# - TOOLS IMPORTS -     
from pytools.function_dir import autonext, capturetxt, youtubedownload, obsidiansort
    # Main Functions
autonext_mt: Callable = autonext.main_tool
capturetxt_mt: Callable = capturetxt.main_tool 
ytdown_mt: Callable = youtubedownload.main_tool

# - SETTINGS IMPORTS -
from pytools import logger
from pytools import AUTONEXT_SETTINGS_PATH

    # Construction du résumé des options de commandes
__title__ = "Python Tools"
modules = {
    "autonext": autonext,
    "obsidiansort": obsidiansort,
    "capturetxt": capturetxt,
    "ytdownload": youtubedownload,
}
__options__ = {
    "autonext": ("-a, --autonext", "Outil de lecture automatique de slides"),
    "capturetxt": ("-c, --capttxt", "Capture le texte de l'écran"),
    "ytdownload": ("-y, --ytdownl", "Téléchargement de vidéo YouTube"),
    "obsidiansort": ("-o, --obsort", "Trie et gère les notes Obsidian"),
}

__help__ = Settings.PackageMetadata.make_help(__title__, __options__, modules)
print(__help__)


# -- OPÉRATIONS DÉFINIES --


# -- VARIABLES INITIALES -- 
tools = {
    "autonext": autonext_mt,
    "obsidiansort": None, 
    "capturetxt": capturetxt_mt,
    "ytdownload": ytdown_mt,
}



associate_longargs = {
    "--autonext": "autonext",
    "--obsort": "obsidiansort", 
    "--capttxt": "capturetxt",
    "--ytdownl": "ytdownload",
}

associate_shortargs = {
    "-a": "autonext",
    "-o": "obsidiansort",
    "-c": "capturetxt",
    "-y": "ytdownload",
}




# -- FONCTIONS MAÎTRES --
def manage_by_args():
    if len(sys.argv) == 1:
        raise ValueError("Python Tools : ERROR - No arguments given")
    
    logger.info(f'CMD Window : CALL program "{sys.argv[1]}"')
    first_arg = sys.argv[1]
    if first_arg == "help" or first_arg == "--help" or first_arg == "-h":
        print(__help__)
    elif first_arg.startswith("--"):
        # Si le premier argument est une option -> Lancer le package correspondant
        logger.info(f'CMD Window : Terminal mode "{first_arg}"')
        apply_tool_longarg(first_arg, *sys.argv[2:]) 
    elif first_arg.startswith("-"):
        logger.info(f'CMD Window : Terminal mode "{first_arg}"')
        apply_tool_shortarg(first_arg, *sys.argv[2:])



"""def apply_tool():
    logger.debug(f"Argv target an existing tool: {sys.argv[1] in tools = }")
    logger.info(f"Target tool: '{sys.argv[1]}'")
    tools[sys.argv[1]]()"""

def apply_tool_longarg(longarg: str, *args):
    if longarg not in associate_longargs:
        raise ValueError(f"Python Tools : ERROR - Long argument '{longarg}' not found in associate_longargs")
    toolname = associate_longargs[longarg]
    tools[toolname](*args)


def apply_tool_shortarg(shortarg: str, *args):
    if shortarg not in associate_shortargs:
        raise ValueError(f"Python Tools : ERROR - Short argument '{shortarg}' not found in associate_shortargs")
    toolname = associate_shortargs[shortarg]
    tools[toolname](*args)


# -- PROGRAMME --
if __name__ == '__main__':
    # - Variables -
    # - Programme -
    logger.info("PYTHON TOOLS: Starting program")
    print()
    manage_by_args()
    
