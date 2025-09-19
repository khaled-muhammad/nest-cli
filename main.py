import sys
from utils import welcome
from colorama import Fore
import os

#Import modules
from tools.domains import ui as domains_ui
import tools.databases.ui as db_ui
from tools.caddy import ui as caddy_ui
from tools.github import ui as github_ui
from tools.nix import ui as nix_ui
from ai import ai_assistant

os.system('clear')

welcome()

while True:
    print("1- Domains Management")
    print("2- DBs Management")
    print("3- Caddy Management")
    print("4- GitHub Management")
    print("5- Nix Management")
    print("0- Exit")
    print(Fore.CYAN + "\n* You can talk to the tool by starting your command with : character.\n" + Fore.RESET)

    user_input = input("Please, Enter your choice: ").strip()
    
    # Check if user wants to use AI assistant
    if user_input.startswith(":"):
        command = user_input[1:].strip()
        if command:
            ai_assistant.process_command(command)
        else:
            print(Fore.YELLOW + "Please provide a command after the colon." + Fore.RESET)
        input("\nPress ENTER to continue...")
        os.system('clear')
        welcome()
        continue
    
    try:
        res = int(user_input)
    except:
        print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
        continue
    
    if res < 0 or res > 5:
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
    elif res == 4:
        github_ui.start()
    elif res == 5:
        nix_ui.start()