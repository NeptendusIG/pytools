# ----------------------------
#    YouTube Download Tool 
# ----------------------------
# Download YouTube videos with various options


# -- IMPORTS --
import os, platform, subprocess
import yt_dlp, pyperclip
from pytube import YouTube
from utility import Settings
import re
from utility import GUI

# Paramètres
logger = Settings.setup_logging("debugging")
__options__ = {
    "default": ("-d, --default", "Utiliser les paramètres par défaut"),
    "audio": ("-a, --audio", "Télécharge l'audio uniquement (format MP3)"),
    "resolution": ("-r=, --res=", "Imposer la résolution (144p, 240p, 360p, 480p, 720p, 1080p)"),
    "name": ("-n=, --name=", "Changer le nom du fichier"),
    "path": ("-p, --path", "Changer le dossier de téléchargement"),
    "open": ("-o, --open", "Ouvrir le dossier de téléchargement à la fin")
}

# -- FONCTIONS DÉFINIES --
# - 1 - Échange pour obtenir les paramètres
def validate_url(url):
    """Vérifie si l'URL est une URL YouTube valide"""
    try:
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        youtube_regex_match = re.match(youtube_regex, url)
        return bool(youtube_regex_match)
    except Exception as e:
        logger.error(f"URL Validation : ERROR - {str(e)}")
        return False

def get_url(first_arg):
    """Récupère l'URL de la vidéo YouTube
    Soit c'est le premier argument,
    Soit c'est dans le clipboard.
    """
    first_arg = first_arg.replace("\\", "")
    if "/" in first_arg:
        if validate_url(first_arg):
            return first_arg
        logger.error(f"URL not valid {first_arg}")
        return None
    from_clipboard = pyperclip.paste().replace("\\", "")
    if "/" in from_clipboard:
        if validate_url(from_clipboard):
            return from_clipboard
        logger.error(f"URL not valid in clipboard {from_clipboard}")
        return None
    logger.error(f"No URL found in arguments or clipboard")
    return None

def select_user_parameters(video_info, *args):
    # Fields :
    resolution = False
    name = False
    mode = False
    path = False

    settings = {
        "url": video_info['url'],
        "resolution": video_info['qualities'][-1],
        "mode": "mp4",
        "name": video_info['title'],
        "path": os.getcwd() + "/downloads"
    }

    for arg in args:
        if arg.startswith("--res=") or arg.startswith("-r="):
            settings["resolution"] = video_info['qualities'][int(arg.split("=")[1])]
        elif arg.startswith("--name=") or arg.startswith("-n="):
            settings["name"] = arg.split("=")[1]
        elif arg == "--audio" or arg == "-a":
            settings["mode"] = "mp3"
        elif arg == "--path" or arg == "-p":
            settings["path"] = GUI.ask_dir()
            if not settings["path"]:
                settings["path"] = os.getcwd()
    
    
    print("\n --- Video Informations ---")
    print(f"Title: {video_info['title']}")
    print(f"Author: {video_info['author']}")
    print(f"Length: {video_info['length']} seconds")
    index_qualities = ", ".join([f"({i})-{qual}" for i, qual in enumerate(video_info['qualities'])])
    print(f"Available qualities: {index_qualities}")
    
    print("\n --- Download Options ---")
    print(f"Resolution: \t{settings['resolution']} \t(choose with --res=<num> or -r=num>)")
    print(f"Mode      : \t{settings['mode']} \t (chose AUDIO with --audio or -a)")
    print(f"File name : \t{settings['name']} \t (change with --name=<name> or -n=<name>)")
    print(f"Dirercory : \t{settings['path']} \t (open nav with --path or -p)")
    print()
    input_args = input("Enter every arguments (-d for default) : ").split()
    for arg in input_args:
        if arg == "-d":
            break
        if arg.startswith("--res=") or arg.startswith("-r="):
            settings["resolution"] = video_info['qualities'][int(arg.split("=")[1])]
        elif arg.startswith("--name=") or arg.startswith("-n="):
            settings["name"] = arg.split("=")[1]
        elif arg == "--audio" or arg == "-a":
            settings["mode"] = "mp3"
        elif arg == "--path" or arg == "-p":
            settings["path"] = GUI.ask_dir()
            if not settings["path"]:
                settings["path"] = os.getcwd()
    return settings


# - 2 - Récupérer les informations de la vidéo
import yt_dlp
from typing import Optional, Dict, Any
import logging

def get_video_info(url: str) -> Optional[Dict[str, Any]]:
    """
    Récupère les informations d'une vidéo à partir de son URL.
    
    Args:
        url (str): URL de la vidéo
    
    Returns:
        Optional[Dict[str, Any]]: Dictionnaire contenant les informations de la vidéo,
                                 None en cas d'erreur
    """
    try:
        # Configuration des options
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Extraction des informations
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        # Récupération des résolutions disponibles
        formats = info.get('formats', [])
        qualities = sorted(list(set(
            f['height'] for f in formats 
            if f.get('height') is not None
        )))
        
        # Construction du dictionnaire de retour
        return {
            'title': info.get('title'),
            'author': info.get('uploader'),
            # 'length': info.get('duration'),
            # 'views': info.get('view_count'),
            # 'rating': info.get('average_rating'),
            'qualities': qualities,
            'url': url,
            # 'description': info.get('description'),
            # 'thumbnail': info.get('thumbnail'),
            # 'upload_date': info.get('upload_date')
        }
        
    except Exception as e:
        logging.error(f"Video Info : ERROR - {str(e)}")
        return None
    


# - 3 - Téléchargement de la vidéo
def download(settings):
    output_path = os.path.join(settings["path"], f'{settings["name"]}.{settings["mode"]}')
    if settings["mode"] == "mp3":
        return download_audio(settings["url"], output_path)
    if settings["mode"] == "mp4":
        return download_video(settings["url"], output_path, settings["resolution"])
    

def download_video(url, output_path, resolution):
    """
    Télécharge une vidéo depuis une URL vers un chemin spécifié avec une résolution donnée.
    
    Args:
        url (str): URL de la vidéo à télécharger
        output_path (str): Chemin complet où sauvegarder la vidéo (ex: "user/downloads/video.mp4")
        resolution (str): Résolution souhaitée (ex: "720p", "1080p", etc.)
    
    Returns:
        bool: True si le téléchargement est réussi, False sinon
    """
    try:
        # Configuration des options
        ydl_opts = {
            'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': True,
            'extract_flat': False
        }
        
        # Téléchargement de la vidéo
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {str(e)}")
        return False


def download_audio(url, output_path):
    try:
        pour_audio = {
            'format': 'bestaudio/best',  # Télécharge le meilleur audio disponible
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Qualité MP3
            }],
            'outtmpl': output_path,
        }
        with yt_dlp.YoutubeDL(pour_audio) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        logger.error(f"Download Audio : ERROR - {str(e)}")
        return False



def open_file_location(file_path):
    """Ouvre l'explorateur de fichiers à l'emplacement du fichier"""
    try:
        if platform.system().lower() == "windows":
            subprocess.run(["explorer", "/select,", file_path])
        elif platform.system().lower() == "darwin":  # macOS
            subprocess.run(["open", "-R", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", os.path.dirname(file_path)])
    except Exception as e:
        logger.error(f"Open Location : ERROR - {str(e)}")


# -- FONCTION PRINCIPALE --
def main_tool(*args):
    """
    Fonction principale du module
    Arguments possibles:
    --res=720p : Définir la résolution (144p, 240p, 360p, 480p, 720p, 1080p)
    --audio ou -a : Télécharger l'audio uniquement (format MP3)
    --open ou -o : Ouvrir le dossier de téléchargement à la fin
    """
    logger.info("START")
    
    # - 1 - Valider l'URL
    url = get_url(args[0] or "None")
    if not url:
        logger.error(f"Invalid YouTube URL")
        return False
    logger.info(f"URL validated: {url}")
    
    # - 2 - Récupérer les informations de la vidéo
    video_info = get_video_info(url)
    if not video_info:
        logger.error("Failed to get video information")
        return False
    logger.info(f"Video info retrieved: {video_info['title']}")
    
    # - 3 - Définir le chemin de sortie
    settings = select_user_parameters(video_info, *args)
    
    # - 4 - Télécharger la vidéo
    file_path = download(video_info['yt'], settings, *args)
    if not file_path:
        logger.error("Download failed")
        return False
    logger.info(f"Download completed: {file_path}")
    
    # - 5 - Ouvrir le dossier si demandé
    if "--open" in args or "-o" in args:
        open_file_location(file_path)
        logger.info("Opened file location")
    
    logger.info("END")
    return True


# -- EXEMPLE D'UTILISATION --
if __name__ == "__main__":
    # Exemple d'utilisation simple
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    main_tool(url)
    
    # Exemple avec options
    # main_tool(url, "--res=1080p", "--open")  # Télécharger en 1080p et ouvrir le dossier
    # main_tool(url, "--audio", "-o")  # Télécharger l'audio uniquement et ouvrir le dossier