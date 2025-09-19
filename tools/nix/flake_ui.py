from colorama import Fore
import os
import questionary

from .management import flakeInit, flakeRun, flakeUpdate, flakeInfo


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
            directory = input(Fore.CYAN + "Directory to init (default: .): " + Fore.RESET).strip() or "."
            use_template = input(Fore.CYAN + "Template (leave empty for default): " + Fore.RESET).strip()
            force_refresh = input(Fore.CYAN + "Refresh/force template fetch? (y/N): " + Fore.RESET).strip().lower() == 'y'
            flakeInit(directory, template=use_template or None, force=force_refresh)
            questionary.press_any_key_to_continue().ask()
        if res == 2:
            ref_or_path = input(Fore.CYAN + "Flake ref or path (default: .): " + Fore.RESET).strip() or "."
            target = input(Fore.CYAN + "Target (e.g., app, package, default): " + Fore.RESET).strip()
            extra_args = input(Fore.CYAN + "Extra args after -- (optional): " + Fore.RESET).strip()
            flakeRun(ref_or_path, target=target or None, args=extra_args or None)
            questionary.press_any_key_to_continue().ask()
        if res == 3:
            directory = input(Fore.CYAN + "Directory (default: .): " + Fore.RESET).strip() or "."
            flakeUpdate(directory)
            questionary.press_any_key_to_continue().ask()
        if res == 4:
            ref_or_path = input(Fore.CYAN + "Flake ref or path (default: .): " + Fore.RESET).strip() or "."
            flakeInfo(ref_or_path)
            questionary.press_any_key_to_continue().ask()