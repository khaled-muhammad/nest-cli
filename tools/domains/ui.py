import sys
from colorama import Fore
import os
from .management import listDomains

def start():
    while True:
        print(Fore.MAGENTA + "\nDomain Management:" + Fore.RESET)
        print("  1- List Domains")
        print("  2- Add Domain")
        print("  3- Remove Domain")
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
            sys.exit()
        
        if res == 1:
            print(Fore.YELLOW + "\nListing Domains...\n" + Fore.RESET)
            domain_list = listDomains()
            for i, domain in enumerate(domain_list):
                print(f"   {i + 1}. {domain.name}")

            selected_domain = input("\nChoose domain to start working with it or 0 to go back: ")

            if selected_domain == '0':
                os.system('clear')
                continue
            try:
                selected_domain = int(selected_domain)
                if selected_domain < 1 or selected_domain > len(domain_list):
                    print(Fore.RED + "Invalid selection!" + Fore.RESET)
                    continue
                domain = domain_list[selected_domain - 1]
                os.system('clear')
                import tools.domains.domain_ui as domain_ui
                domain_ui.start(domain)
            except ValueError:
                print(Fore.RED + "Please enter a valid number!" + Fore.RESET)
                continue

            input("Press Enter to continue...")
        elif res == 2:
            domain = input("Enter the domain to add: ")
            print(f"Adding domain: {domain}")
            # Placeholder for actual domain adding logic
        elif res == 3:
            domain = input("Enter the domain to remove: ")
            print(f"Removing domain: {domain}")
            # Placeholder for actual domain removing logic