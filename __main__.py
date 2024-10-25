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
from pytools import __title__, __options__, __call__
from pytools.function_dir import autonext, capturetxt, youtubedownload, obsidiansort
    # Main Functions
autonext_mt: Callable = autonext.main_tool
capturetxt_mt: Callable = capturetxt.main_tool 
ytdown_mt: Callable = youtubedownload.main_tool

# - SETTINGS IMPORTS -
from pytools import logger
from pytools import AUTONEXT_SETTINGS_PATH

# -- OPÉRATIONS DÉFINIES --


# -- VARIABLES INITIALES -- 
"""operations = {
    "Passwords": "pswmanage",
}

associate_longargs = {
    "--passwords": "Passwords",
}
associate_longargs_reversed = {value: key for key, value in associate_longargs.items()}

associate_shortargs = {
    "-p": "Passwords",
}
associate_shortargs_reversed = {value: key for key, value in associate_shortargs.items()}"""

tools = {
    "autonext": autonext_mt,
    "obsidiansort": None, 
    "capturetxt": capturetxt_mt,
    "ytdownload": ytdown_mt,
}

modules = {
    "autonext": autonext,
    "obsidiansort": obsidiansort,
    "capturetxt": capturetxt,
    "ytdownload": youtubedownload,
}

associate_longargs = {
    "--autonext": "autonext",
    "--obsort": "obsidiansort", 
    "--capttxt": "capturetxt",
    "--ytdownl": "ytdownload",
}

associate_midargs = {
    "-autn": "autonext",
    "-obs": "obsidiansort",
    "-ctxt": "capturetxt",
    "-ytd": "ytdownload",
}
associate_shortargs = {
    "-a": "autonext",
    "-o": "obsidiansort",
    "-c": "capturetxt",
    "-y": "ytdownload",
}

indicate_args = { # Indicate the arguments to be used for each tool
    "autonext": "",
    "obsidiansort": "",
    "capturetxt": "-c--clean" ,
    "ytdownload": "-o--open, -a-audio (only), --res=<resolution_def=720>p",
}

def make_h(help_texte, main_agrs, sub_args):
    for mod, help in main_agrs.items():
        help_texte += help 
        help_texte += sub_args[mod]
        help_texte += "\n\n"
    return help_texte

def make_help(modules):
    # Titre
    help_texte = f"\n{'='*50}\n{__title__.upper():^50}\n{'='*50}\n\n"
    help_texte += __call__ + "\n\n"
    # Récupérer les arguments et sous-arguments
    help_dict = {module: f"{args:<30}" + module for module, (args, help) in __options__.items()}
    sub_helps = {mod: "" for mod in modules.keys()}
    for name, mod in modules.items():
        if mod is not None:
            sub_helps[name] = "".join([f"\n\t{args:<30}{description}" for args, description in mod.__options__.values()])
    # Créer le texte d'aide
    return make_h(help_texte, help_dict, sub_helps)


        
help_summary = make_help(modules=modules)
# print(help_summary)

# -- FONCTIONS MAÎTRES --
def manage_by_args():
    if len(sys.argv) == 1:
        raise ValueError("Python Tools : ERROR - No arguments given")
    
    logger.info(f'CMD Window : CALL program "{sys.argv[1]}"')
    first_arg = sys.argv[1]
    if first_arg == "help" or first_arg == "--help" or first_arg == "-h":
        print(make_help(modules))
    elif first_arg.startswith("--"):
        # Si le premier argument est une option -> Lancer le package correspondant
        logger.info(f'CMD Window : Terminal mode "{first_arg}"')
        apply_tool_longarg(first_arg, *sys.argv[2:]) 
    elif first_arg.startswith("-") and len(first_arg) > 2:
        logger.info(f'CMD Window : Terminal mode "{first_arg}"')
        apply_tool_midarg(first_arg, *sys.argv[2:]) 
    elif first_arg.startswith("-") and len(first_arg) == 2:
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

def apply_tool_midarg(midarg: str, *args):
    if midarg not in associate_midargs:
        raise ValueError(f"Python Tools : ERROR - Mid argument '{midarg}' not found in associate_midargs")
    toolname = associate_midargs[midarg]
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
    
