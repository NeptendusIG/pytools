# ----------------------------
#      Capture Text Tool 
# ----------------------------
# Retrive text from a screenshot to clipborad


# -- IMPORTS --
import platform, subprocess, os
import pytesseract, pyperclip, PIL.Image as Image
from utility import Settings

# Paramètres
logger = Settings.setup_logging("debugging")
__options__ = {
    "striping text" : ("-c, --clean", "Nettoie le teste (sauts de ligne, et tabulations)")
 } # Arguments accessibles sur cette application

# -- FONCTIONS DÉFINIES --
def select_screenshot():
    system = platform.system().lower()
    data_dir_path = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_dir_path):
        os.mkdir(data_dir_path)
    current_path = os.path.join(data_dir_path, "image.png")
    try:
        # Save to current directory
        subprocess.run(["screencapture", "-i", current_path], check=True)
        # Save to clipboard
            # subprocess.run(["screencapture", "-ic"], check=True)
        return current_path
    except Exception as e:
        logger.error(f"Screenshot : ERROR - {str(e)}")
        return False


def get_text_from_image(image_path):
    try:
        # Récupérer l'image depuis le presse-papiers
        image = Image.open(image_path)
        # Par défaut en anglais, mais on peut spécifier le français avec lang='fra'
        text = pytesseract.image_to_string(image, lang='fra')
        return text.strip()
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"
        

def traitement_texte(text, *args):
    for arg in args:
        if arg == "--clean" or arg == "-c":
            text = text.replace("\n", " ")
            text = text.replace("\t", " ")
            text = text.replace("  ", " ")
    return text
    
    

def main_tool(*args):
    logger.info("START")  # Capture_text: main tool: START
    # - 1 - Prendre une capture d'écran
    path = select_screenshot()
    logger.info(f"Screenshot taken: {path}")
    # - 2 - Extraire le texte
    text = get_text_from_image(path)
    logger.info(f"Text extracted: {text}")
    # - 3 - Traiter le texte si argument(s)
    if args:
        text = traitement_texte(text, *args)
    # - 4 - Copier le texte dans le presse-papiers
    pyperclip.copy(text)
    logger.info("Text copied to clipboard")
    logger.info("END")



