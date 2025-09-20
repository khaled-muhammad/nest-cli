import os
import sys

from colorama import Fore
from .models import Domain
from .management import getSSLInfo
from datetime import datetime, timezone
import whois

# Fix whois data file path for PyInstaller
def setup_whois_data():
    """Setup whois data file path for PyInstaller compatibility"""
    try:
        if getattr(sys, 'frozen', False):
            # Running in PyInstaller bundle
            base_path = sys._MEIPASS
            whois_data_file = os.path.join(base_path, 'whois', 'data', 'public_suffix_list.dat')
            
            # Check if the file exists and set it
            if os.path.exists(whois_data_file):
                whois.PSL_FILE = whois_data_file
            else:
                # Fallback: try to find it in the whois package
                import whois as whois_pkg
                whois_pkg_path = os.path.dirname(whois_pkg.__file__)
                fallback_file = os.path.join(whois_pkg_path, 'data', 'public_suffix_list.dat')
                if os.path.exists(fallback_file):
                    whois.PSL_FILE = fallback_file
    except Exception as e:
        # If anything fails, whois will use its default behavior
        pass

# Initialize whois data path
setup_whois_data()


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
            print(f"   Socket: {domain.sock_path}")
            if ".hackclub.app" in domain.name:
                print(Fore.RED + "   Note: This is a Hack Club's Nest subdomain. So no useful details about it." + Fore.RESET)
            else:
                domain_lookup = whois.whois(domain.name)
                print("   Registeration Date:", domain_lookup.creation_date)
                print("   Expiration Date:", domain_lookup.expiration_date)
                print("   Registrar:", domain_lookup.registrar)
                print("   Name Servers:")
                for ns in domain_lookup.name_servers:
                    print("    -", ns)

        elif res == 2:
            print(Fore.YELLOW + f"\nSSL Details for {domain.name}:\n" + Fore.RESET)
            try:
                ssl_info = getSSLInfo(domain.name)
                print(f"   Subject: {ssl_info.subject}")
                print(f"   Issuer: {ssl_info.issuer}")
                print(f"   Issued On: {ssl_info.issued}")
                print(f"   Expiry Date: {ssl_info.expiry}")
                if ssl_info.expiry < datetime.now(timezone.utc):
                    print(Fore.RED + "   Status: Expired" + Fore.RESET)
                else:
                    print(Fore.GREEN + "   Status: Valid" + Fore.RESET)
            except Exception as e:
                print(Fore.RED + f"   Failed to retrieve SSL info: {e}" + Fore.RESET)
        
        elif res == 3:
            confirm = input(f"Are you sure you want to delete the domain {domain.name}? (yes/no): ")
            if confirm.lower() == 'yes':
                print(f"Deleting domain: {domain.name}")
                os.system(f'nest caddy rm {domain.name}')
            else:
                print(Fore.YELLOW + "Domain deletion cancelled." + Fore.RESET)
        
        input("Press Enter to continue...")