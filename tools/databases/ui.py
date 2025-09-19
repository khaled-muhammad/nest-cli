import os
import sys
from colorama import Fore
from .management import list_user_databases, remove_database


def start():
    while True:
        print(Fore.MAGENTA + "\nDatabases Management:" + Fore.RESET)
        print("  1- List Databases")
        print("  2- Create new Database")
        print("  3- Remove Database")
        print("  0- Back to Main Menu")

        try:
            res = int(input("\nPlease, Enter your choice: "))
        except:
            print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
            continue
        
        if res < 0 or res > 3:
            print(Fore.RED + "Please, enter a choice in valid range!" + Fore.RESET)
            continue
        
        if res == 0:
            os.system('clear')
            import main
        
        if res == 1:
            print(Fore.YELLOW + "\nListing Databases...\n" + Fore.RESET)
            db_list = list_user_databases()
            if not db_list:
                print("No databases found.")
            else:
                for i, db in enumerate(db_list):
                    print(f"   {i + 1}. {db}")
            input("\nPress Enter to continue...")
        
        if res == 2:
            db_name = input("Enter the name for the new database: ")
            print(f"Creating database: {db_name}")
            os.system(f'nest db create {db_name}')
            input("Press Enter to continue...")
        
        if res == 3:
            print(Fore.YELLOW + "\nListing Databases...\n" + Fore.RESET)
            db_list = list_user_databases()
            if not db_list:
                print("No databases found.")
            else:
                for i, db in enumerate(db_list):
                    print(f"   {i + 1}. {db}")

            db_name = input("\nEnter the name of the database to remove: ")
            print(f"Removing database: {db_name}")
            success, message = remove_database(db_name)
            if success:
                print(Fore.GREEN + message + Fore.RESET)
            else:
                print(Fore.RED + message + Fore.RESET)
            input("Press Enter to continue...")