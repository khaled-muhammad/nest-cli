import os
from colorama import Fore
import questionary
from .management import listSites, addReverseProxy, addStaticRoute, saveUpdatedSite, deleteSite
from .models import SiteBlock, Directive

def start():
    while True:
        print(Fore.MAGENTA + "\nCaddy Management:" + Fore.RESET)
        print("1- List Sites")
        print("2- Add Site")
        print("3- Update Site")
        print("4- Delete Site")
        print("0- Back to Main Menu")

        try:
            res = int(input("\nPlease, Enter your choice: "))
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
            sites = listSites()

            print("\n")
            for i, (domain, siteBlock) in enumerate(sites.items()):
                print(f"{i+1}. {domain}")
            print("\n")
        elif res == 3:
            sites   = listSites()
            choices = list(sites.keys())

            domain = questionary.select(
                    "Select a site:",
                    choices=choices
                ).ask()
            
            while True:
                updated_site       = sites[domain]
                encoding_directive = None
                root_directive     = None
                root_reverseproxy  = None
                handles            = []
                
                for directive in sites[domain].directives:
                    if directive.name in ('handle', 'handle_path') and len(directive.args) > 0:
                        handles.append(directive)
                    
                    if directive.name == 'encode':
                        encoding_directive = directive
                    if directive.name == 'root':
                        root_directive = directive
                    if directive.name == 'reverse_proxy':
                        root_reverseproxy = directive
                
                print(f"{Fore.MAGENTA}Domain Name:{Fore.RESET}", domain)
                if root_directive != None:
                    print(f"{Fore.MAGENTA}Root Directory:{Fore.RESET}", sites[domain].directives[0].args[1])
                if root_reverseproxy != None:
                    print(f"{Fore.MAGENTA}Root Reverse Proxy:{Fore.RESET}", root_reverseproxy.args[0])
                
                if len(handles) != 0:
                    print(Fore.MAGENTA + "Routes:" + Fore.RESET)

                for directive in handles:
                    print(" - ", directive.args[0], "→", directive.name)

                if root_directive != None:
                    print(" - (catch-all) → handle")

                print(Fore.MAGENTA + "\nEncoding:" + Fore.RESET, encoding_directive.args[0] if encoding_directive != None else None)
                
                print(Fore.MAGENTA + "\nActions:" + Fore.RESET)

                action = questionary.select(
                        "Choose an action:",
                        choices=['Add Reverse Proxy', 'Add Static Route', 'Delete Route', 'Save Changes', 'Cancel']
                    ).ask()
            

                if action == 'Add Reverse Proxy':
                    route_path = input("Enter Path (e.g. /api/*): ")
                    route_port = input("Enter Target (e.g. 8080): ")
                    
                    try:
                        updated_site = addReverseProxy(sites[domain], route_path, route_port)
                        print(f"Reverse Proxy Added:\n{route_path} → :{route_port}")
                    except ValueError as e:
                        print(f"{Fore.RED}{e}{Fore.RESET}")
                
                if action == 'Add Static Route':
                    route_path = input("Enter Path (e.g. /static/*): ")
                    path       = input("Enter Folder Path: ")

                    try:
                        updated_site = addStaticRoute(sites[domain], route_path, path)
                        print(f"Static Route Added:\n{route_path} → :{path}")
                    except ValueError as e:
                        print(f"{Fore.RED}{e}{Fore.RESET}")
                
                if action == 'Delete Route':
                    for i, route in enumerate(handles):
                        print(f"{i+1}. {route.args[0]}")
                    
                    route_to_delete = int(input("Which route would you like to delete? "))
                    if route_to_delete <= len(handles):
                        updated_site.directives.remove(handles[route_to_delete])
                        print(f"Route deleted successfully!")
                    else:
                        print("Sorry, but you chose a route that doesn't exist.")
                
                if action == 'Save Changes':
                    saveUpdatedSite(updated_site)
                    print("Updates saved successfully!")
                    break
                
                if action == 'Cancel':
                    break
        elif res == 4:
            sites   = listSites()
            choices = list(sites.keys())

            site_to_delete = questionary.select(
                    "Which site would you like to delete?",
                    choices=choices
                ).ask()

            confirmation = input(f"Are you sure you want to delete site \"{site_to_delete}\"? (y/n):")

            if confirmation == 'y':
                deleteSite(sites[site_to_delete])
                print("Site deleted successfully!")

                input("Press any key to continue ...")
        elif res == 2:
            print("Adding a new site:")
            domain    = input("Enter Domain: ")
            site      = SiteBlock(domain, [], f"unix//home/khaled/.{domain}.webserver.sock")
            site_type = questionary.select(
                    "Choose Site Type:",
                    choices=('Static File Hosting', 'Reverse Proxy', 'Mixed (Static + Reverse Proxy)')
                ).ask()

            if site_type == 'Static File Hosting':
                root_dir_path = input('Enter Root Folder Path: ')
                site.add_directive(Directive("root", ["*", root_dir_path]))
                site.add_directive(Directive("file_server", subdirectives=[
                    Directive("hide", [".git", ".env"])
                ]))
            elif site_type == 'Reverse Proxy':
                proxy_port = input('Enter Proxy Target (e.g. 8080): ')
                site.add_directive(Directive("reverse_proxy", [f"localhost:{proxy_port}"]))
            elif site_type == 'Mixed (Static + Reverse Proxy)':
                print("Add Reverse Proxy Routes:")
                while True:
                    path = input("Enter route Path: ")
                    port = input("Enter route Port: ")

                    site.add_directive(Directive("handle", [path], [
                        Directive("reverse_proxy", [f":{port}"])
                    ]))

                    wanna_another = input("Add another? (y/n): ")

                    if wanna_another.lower() != 'y':
                        break
                
                print("Add Static Routes:")
                while True:
                    path   = input("Enter route Path: ")
                    folder = input("Folder: ")

                    site.add_directive(Directive("handle_path", [path], [
                        Directive("root", ["*", folder]),
                        Directive("file_server")
                    ]))

                    wanna_another = input("Add another? (y/n): ")

                    if wanna_another.lower() != 'y':
                        break
                
                gzipEncoding = input("Enable gzip encoding? (y/n): ")

                if gzipEncoding.lower() == 'y':
                    site.add_directive(Directive("encode", ["gzip"]))
                
                print(Fore.GREEN + "Site created Successfully!" + Fore.RESET)
                saveUpdatedSite(site)