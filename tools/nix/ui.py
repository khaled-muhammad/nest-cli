import os
from colorama import Fore
import questionary

from .management import *
from . import flake_ui

def start():
    while True:
        print(Fore.MAGENTA + "\nNix Management:" + Fore.RESET)
        print("01- List Installed Packages")
        print("02- Install Package")
        print("03- Remove Package")
        print("04- Update All Packages")
        print("05- Nix Shell (Temporary Environment)")
        print("06- Nix Run (One-Off Command)")
        print("07- Search for Packages")
        print("08- Flakes Management")
        print("09- Garbage Collect / Store Cleanup")
        print("10- Check Nix Health")
        print("0- Back to Main Menu")

        try:
            res = int(input("\nPlease, Enter your choice: "))
        except:
            print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
            continue
        
        if res < 0 or res > 10:
            print(Fore.RED + "Please, enter a choice in valid range!" + Fore.RESET)
            continue
        
        if res == 0:
            os.system('clear')
            break
        
        if res == 1:
            print(Fore.CYAN + 'Fetching installed packages...' + Fore.RESET)
            print("---------------------------------")
            listProfilePackages()
            print("---------------------------------")
            input("Press ENTER to return.")
        if res == 2:
            package_to_install = input("Enter package name to install (ex: nodejs, python3, git): ")

            installProfilePackage(package_to_install)
            input("Press ENTER to return.")
        if res == 3:
            package_to_remove  = input("Enter package index/name to remove: ")
            uninstallProfilePackage(package_to_remove)
            input("Press ENTER to return.")
        if res == 4:
            upgradeAllPackages()
        if res == 5:
            pkgs = input(Fore.CYAN + "Enter packages (space-separated): " + Fore.RESET).split()
            if not pkgs:
                print(Fore.YELLOW + "No packages entered, cancelling." + Fore.RESET)
                continue

            print(Fore.CYAN + f"Launching shell with: {', '.join(pkgs)}" + Fore.RESET)

            nixShell(pkgs)
        if res == 6:
            pkg = input(Fore.CYAN + "Enter package (ex: cowsay, fd, hello): " + Fore.RESET).strip()
            if not pkg:
                print(Fore.YELLOW + "No package entered, cancelling." + Fore.RESET)
                continue
            
            cmd_args = input(Fore.CYAN + f"Enter command/args to run with {pkg} (leave empty for default): " + Fore.RESET).strip()

            print(Fore.CYAN + f"Running '{pkg}' one-off..." + Fore.RESET)
            try:
                nixRun(pkg, cmd_args)
            except Exception as e:
                print(Fore.RED + f"Error running package: {e}" + Fore.RESET)
                input("Press any key to continue ....")
            print(Fore.GREEN + f"Finished running {pkg}." + Fore.RESET)
        
        if res == 7:
            print("Enter search term:")
            query = input("> ")
            search_res = nixPackagesSearch(query)

            if search_res != False:
                for i, package in enumerate(search_res.packages):
                    print(f"\nPackage {i+1}:")
                    print(f"  Name: {package.attr_name}")
                    print(f"  Version: {package.pversion}")
                    print(f"  Description: {package.description}")
                    print(f"  Maintainers: {[m.name for m in package.maintainers]}")
                    print(f"  Platforms: {len(package.platforms)} platforms")
                
            else:
                print(Fore.RED + "Failed to search. You can try again later.")
            questionary.press_any_key_to_continue().ask()
        
        if res == 8:
            flake_ui.start()