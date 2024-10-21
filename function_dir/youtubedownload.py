# ----------------------------
#    YouTube Download Tool 
# ----------------------------
# Download YouTube videos with various options


# -- IMPORTS --
import os, platform, subprocess
import yt_dlp
from utility import Settings
import re

# Paramètres
logger = Settings.setup_logging("debugging")


# -- FONCTIONS DÉFINIES --
def validate_url(url):
    """Vérifie si l'URL est une URL YouTube valide"""
    try:
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        youtube_regex_match = re.match(youtube_regex, url)
        return bool(youtube_regex_match)
    except Exception as e:
        logger.error(f"URL Validation : ERROR - {str(e)}")
        return False


def get_video_info(url):
    """Récupère les informations de la vidéo"""
    try:
        yt = YouTube(url)
        return {
            'title': yt.title,
            'author': yt.author,
            'length': yt.length,
            'views': yt.views,
            'rating': yt.rating,
            'yt': yt
        }
    except Exception as e:
        logger.error(f"Video Info : ERROR - {str(e)}")
        return None


def download_video(yt, output_path, *args):
    """Télécharge la vidéo selon les options spécifiées"""
    try:
        # Paramètres par défaut
        resolution = "720p"
        format = "mp4"
        audio_only = False

        # Traitement des arguments
        for arg in args:
            if arg.startswith("--res="):
                resolution = arg.split("=")[1]
            elif arg == "--audio" or arg == "-a":
                audio_only = True
                format = "mp3"

        # Création du dossier de sortie s'il n'existe pas
        os.makedirs(output_path, exist_ok=True)

        if audio_only:
            # Téléchargement audio uniquement
            stream = yt.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path=output_path)
            
            # Conversion en MP3
            base, _ = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            
            return new_file
        else:
            # Téléchargement vidéo
            stream = None
            """stream = yt.streams.filter(
                progressive=True,
                file_extension=format,
                resolution=resolution
            ).first()"""
            
            # Si la résolution demandée n'est pas disponible, prendre la meilleure disponible
            if not stream:
                stream = yt.streams.filter(
                    progressive=True,
                    file_extension=format
                ).order_by('resolution').desc().first()
            
            return stream.download(output_path=output_path)
            
    except Exception as e:
        logger.error(f"Download : ERROR - {str(e)}")
        return None



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


def main_tool(url, *args):
    """
    Fonction principale du module
    Arguments possibles:
    --res=720p : Définir la résolution (144p, 240p, 360p, 480p, 720p, 1080p)
    --audio ou -a : Télécharger l'audio uniquement (format MP3)
    --open ou -o : Ouvrir le dossier de téléchargement à la fin
    """
    logger.info("START")
    
    # - 1 - Valider l'URL
    url = url.replace("\\", "")
    if not validate_url(url):
        logger.error(f"Invalid YouTube URL ({url})")
        return False
    logger.info(f"URL validated: {url}")
    
    # - 2 - Récupérer les informations de la vidéo
    video_info = get_video_info(url)
    if not video_info:
        logger.error("Failed to get video information")
        return False
    logger.info(f"Video info retrieved: {video_info['title']}")
    
    # - 3 - Définir le chemin de sortie
    output_path = os.path.join(os.getcwd(), "downloads")
    
    # - 4 - Télécharger la vidéo
    file_path = download_video(video_info['yt'], output_path, *args)
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