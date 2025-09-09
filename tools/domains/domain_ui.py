import os

from colorama import Fore
from .models import Domain
import whois


def start(domain:Domain):
    while True:
        print(Fore.MAGENTA + f"\nManaging Domain: {domain.name}" + Fore.RESET)
        print("  1- Check Domain Status")
        print("  2- Check SSL Status")
        print("  3- Delete Domain")
        print("  0- Back to Domain Management")

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
            from . import ui
            ui.start()
        
        if res == 1:
            print(Fore.YELLOW + f"\nDomain Details for {domain.name}:\n" + Fore.RESET)
            print(f"   Name: {domain.name}")
            print(f"   Created At: {domain.created_at}")
            print(f"   Updated At: {domain.updated_at}")
            input("\nPress Enter to continue...")
        
        elif res == 2:
            new_name = input("Enter new domain name: ")
            print(f"Updating domain from {domain.name} to {new_name}")
            # Placeholder for actual update logic
            domain.name = new_name
            print(Fore.GREEN + "Domain updated successfully!" + Fore.RESET)
        
        elif res == 3:
            confirm = input(f"Are you sure you want to delete the domain {domain.name}? (yes/no): ")
            if confirm.lower() == 'yes':
                print(f"Deleting domain: {domain.name}")
                # Placeholder for actual delete logic
                print(Fore.GREEN + "Domain deleted successfully!" + Fore.RESET)
                os.system('clear')
                import ui
                ui.start()
            else:
                print(Fore.YELLOW + "Domain deletion cancelled." + Fore.RESET)
        
        input("Press Enter to continue...")