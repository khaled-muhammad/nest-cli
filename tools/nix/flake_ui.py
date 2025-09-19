from colorama import Fore
import questionary

from .management import *


def start():
    print(Fore.CYAN + "\nFLAKES MANAGEMENT")
    print("-----------------" + Fore.RESET)

    while True:
        print("1. Init New Flake")
        print("2. Run Flake")
        print("3. Update Flake")
        print("4. Show Flake Info")
        print("0. Back")

        try:
            res = int(input("\n> "))
        except:
            print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
            continue

        if res < 0 or res > 4:
            print(Fore.RED + "Please, enter a choice in valid range!" + Fore.RESET)
            continue
        
        if res == 0:
            os.system('clear')
            break

        if res == 1:
            templates = ["default", "node", "python", "rust"]
            choice = questionary.select("Choose a template:", templates).ask()
            directory = input("Enter creation directory: ")
            initializeNixFlake(directory, choice)
            print("New flake initialized with template:", choice)
        