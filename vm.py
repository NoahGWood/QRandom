import os
import socket

def start_servers():
    try:
        os.system("gnome-terminal -e 'qvm -S'")
        os.system("gnome-terminal -e 'quilc -S'")
    except:
        try:
            os.system("terminal -e 'qvm -S'")
            os.system("terminal -e 'quilc -S'")
        except:
            exit()
