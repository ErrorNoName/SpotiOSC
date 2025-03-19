#!/usr/bin/env python3

import subprocess
import time
from pythonosc import udp_client

def get_spotify_track():
    """
    Exécute 'wmctrl -l' pour récupérer la liste des fenêtres, 
    et extrait le titre de la fenêtre dont l'ID est '0x03800004'.
    Le titre est composé des colonnes à partir de la 4ème.
    """
    try:
        result = subprocess.run(["wmctrl", "-l"], stdout=subprocess.PIPE, text=True)
        for line in result.stdout.splitlines():
            if "0x03800004" in line:
                # Par exemple, la ligne est : 
                # "0x03800004  0 archlinux Naps - CŒUR DE ICE"
                # On ignore les 3 premiers éléments pour obtenir "Naps - CŒUR DE ICE"
                title = " ".join(line.split()[3:])
                return title
    except Exception as e:
        print("Erreur lors de la récupération du titre :", e)
    return None

def send_to_vrchat(track_title):
    """
    Envoie le titre via OSC à VRChat sur l'adresse '/chatbox/input' avec 
    un booléen pour envoyer automatiquement le message.
    """
    try:
        client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        message = f"♪ Now Playing: {track_title} ♪"
        client.send_message("/chatbox/input", [message, True])
        print(f"Envoyé à VRChat : {message}")
    except Exception as e:
        print("Erreur lors de l'envoi du message OSC :", e)

if __name__ == "__main__":
    while True:
        track = get_spotify_track()
        if track:
            send_to_vrchat(track)
        else:
            print("Spotify non trouvé ou fenêtre introuvable.")
        time.sleep(4)
