#############################
#     Project name      #
#      Class name       #
#        Date//         #
#############################
# NOTES :
"""

"""
# IMPORTS
import sys, time
from utility import GUI, File, Settings
import tkinter as tk
from typing import Union

# Settings
from pytools import logger
from pytools import SETTINGS_PATH


class Timer:
    """Timer class
    CARACTÉRISTIQUES : 
    - Affichage mis à jour après initialisation
    - (Interaction) uniquement bouton stop
    """
    def __init__(self, master: tk.Tk, seconds: int):
        self.master = master
        self.seconds_left = seconds


        self.seconds_var = tk.StringVar()
        self.seconds_var.set(str(seconds))

        self.label = tk.Label(master, textvariable=self.seconds_var, font=('Helvetica', 48))
        self.label.pack() 

        self.master.after(1000, self.update_timer)


    def update_timer(self):
        """Mise à jour du timer chaque seconde sans bloquer l'interface."""
        if self.seconds_left > 0:
            self.seconds_var.set(str(self.seconds_left))
            self.seconds_left -= 1
            # Replanifie l'appel de cette méthode dans 1 seconde (1000 ms)
            self.master.after(1000, self.update_timer)
        else:
            self.stop()

    def stop(self):
        self.master.quit()
        self.master.withdraw()


    class SubClass:

        def __init__(self, *att):
            logger.info('Initialized')
            pass

        def __str__(self):
            return ""


if __name__ == '__main__':
    # tests
    sys.exit()
    wind = tk.Tk()
    Timer(wind, 10)
    wind.mainloop()