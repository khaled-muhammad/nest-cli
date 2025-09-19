import os
from colorama import Fore
import questionary

from .management import github_auth, check_if_github_logged_in, github_logout, list_repos, clone_repo, create_repo

def start():
    while True:
        print(Fore.MAGENTA + "\nGitHub Management:" + Fore.RESET)
        print("1- Clone Repository")
        print("2- Create New Repository")
        print("3- Authentication / Tokens")
        print("0- Back to Main Menu")

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
            break
        

        if res == 1:
            if check_if_github_logged_in():
                user_repos = list_repos()
                
                user_choice = questionary.select(
                    "Choose repo to clone:",
                    [questionary.Choice(repo.name, repo) for repo in user_repos]
                ).ask()

                save_path = input("Enter save path: ")

                clone_repo(user_choice, save_path)
            else:
                repo_url   = input("Please, enter repo url: ")
                save_path  = input("Enter save path: ")

                clone_repo(repo_url, save_path)


        if res == 2:
            name = input("Repository name: ").strip()
            if not name:
                print("Name can't be empty!")
            
            description = input("Description (optional): ").strip()
            visibility  = input("Visibility (public/private) [public]: ").strip().lower() or "public"


            if visibility not in ["public", "private"]:
                print("Invalid visibility. Defaulting to public.")
                visibility = "public"
            
            local = input("Initialize in current folder? (y/N): ").lower()

            create_repo(name, visibility, description, None if local != 'y' else '.')
            
            


        if res == 3:
            if not check_if_github_logged_in():
                input("You need to login. Please enter any key to start logging in.")
                print("\nStarting GitHub authentication...\n")
                loggedIn = github_auth()

                if loggedIn:
                    print(Fore.GREEN + "\nAuthentication complete!" + Fore.RESET)
                else:
                    print(Fore.RED + "\nLogin failed. Try again." + Fore.RESET)
            else:
                print("You are logged in!")
                res = questionary.confirm("Logout?").ask()
                if res:
                    ret = github_logout()
                    if ret:
                        print("You are logged out successfully!")
                    else:
                        print("Failed to log you out :)")
                else:
                    print("Going back ...")