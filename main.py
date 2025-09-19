import sys
from utils import welcome
from colorama import Fore
import os

#Import modules
from tools.domains import ui as domains_ui
import tools.databases.ui as db_ui
from tools.caddy import ui as caddy_ui

os.system('clear')

welcome()

while True:
    print("1- Domains Management")
    print("2- DBs Management")
    print("3- Caddy Management")
    print("4- Projects Management")
    print("5- Send/Retrieve Files")
    print("6- GitHub Management")
    print("7- Nix Management")
    print("0- Exit")
    print(Fore.CYAN + "\n* You can talk to the tool by starting your command with : character.\n" + Fore.RESET)

    try:
        res = int(input("Please, Enter your choice: "))
    except:
        print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
        continue
    
    if res < 0 or res > 7:
        print(Fore.RED + "Please, enter a choice in valid range!" + Fore.RESET)
        continue
    
    if res == 0:
        print(Fore.CYAN + "Bye, see you soon." + Fore.RESET)
        sys.exit()
    
    if res == 1:
        domains_ui.start()
    elif res == 2:
        db_ui.start()
    elif res == 3:
        caddy_ui.start()