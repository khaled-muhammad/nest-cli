import json
import os
import subprocess
from colorama import Fore, Style
import requests
import pathlib

from .models import NixOSSearchParser

def listProfilePackages():
    os.system("nix profile list")

def installProfilePackage(package_name):
    os.system(f"nix profile install nixpkgs#{package_name}")

def uninstallProfilePackage(package_name):
    try:
        int(package_name)
        os.system(f"nix profile remove {package_name}")
    except:
        os.system(f"nix profile remove nixpkgs#{package_name}")

def upgradeAllPackages():
    try:
        print(Fore.CYAN + "Updating all packages..." + Fore.RESET)

        result = subprocess.run(
            ["nix", "profile", "upgrade"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(Fore.RED + "Error upgrading packages:" + Fore.RESET)
            print(result.stderr.strip())
            return

        # Handle "nothing to upgrade" case
        if "Use 'nix profile list'" in result.stderr:
            print(Fore.YELLOW + "All packages are already up to date." + Fore.RESET)
        else:
            print(Fore.GREEN + "Packages upgraded successfully!" + Fore.RESET)
            if result.stdout.strip():
                print(Style.DIM + result.stdout.strip() + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Fore.RESET)

def nixShell(pkgs):
    subprocess.run(["nix", "shell"] + [f"nixpkgs#{p}" for p in pkgs])

def nixRun(pkg, cmds):
    command = ["nix", "run", f"nixpkgs#{pkg}"]

    if cmds:
        command += ["--"] + cmds.split()

    os.system(" ".join(command))

def nixPackagesSearch(query):
    res = requests.post(
        "https://search.nixos.org/backend/latest-44-nixos-25.05/_search",
        headers={
            "authorization": "Basic YVdWU0FMWHBadjpYOGdQSG56TDUyd0ZFZWt1eHNmUTljU2g=",
            "Content-Type": "application/json"
        },
        data=json.dumps(NixOSSearchParser.build_search_query(query))
    )

    if res.status_code != 200:
        return False

    try:
        response = NixOSSearchParser.parse_response(res.json())
        return response
    except Exception as e:
        print(e)
        return False

    # curl 'https://search.nixos.org/backend/latest-44-nixos-25.05/_search' \
    # -H 'accept: */*' \
    # -H 'accept-language: en-US,en-GB;q=0.9,en;q=0.8,ar-EG;q=0.7,ar;q=0.6' \
    # -H 'authorization: Basic YVdWU0FMWHBadjpYOGdQSG56TDUyd0ZFZWt1eHNmUTljU2g=' \
    # -H 'content-type: application/json' \
    # -H 'origin: https://search.nixos.org' \
    # -H 'priority: u=1, i' \
    # -H 'referer: https://search.nixos.org/packages?channel=25.05&query=python' \
    # -H 'sec-ch-ua: "Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"' \
    # -H 'sec-ch-ua-mobile: ?0' \
    # -H 'sec-ch-ua-platform: "Linux"' \
    # -H 'sec-fetch-dest: empty' \
    # -H 'sec-fetch-mode: cors' \
    # -H 'sec-fetch-site: same-origin' \
    # -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36' \
    # --data-raw '{"from":0,"size":50,"sort":[{"_score":"desc","package_attr_name":"desc","package_pversion":"desc"}],"aggs":{"package_attr_set":{"terms":{"field":"package_attr_set","size":20}},"package_license_set":{"terms":{"field":"package_license_set","size":20}},"package_maintainers_set":{"terms":{"field":"package_maintainers_set","size":20}},"package_teams_set":{"terms":{"field":"package_teams_set","size":20}},"package_platforms":{"terms":{"field":"package_platforms","size":20}},"all":{"global":{},"aggregations":{"package_attr_set":{"terms":{"field":"package_attr_set","size":20}},"package_license_set":{"terms":{"field":"package_license_set","size":20}},"package_maintainers_set":{"terms":{"field":"package_maintainers_set","size":20}},"package_teams_set":{"terms":{"field":"package_teams_set","size":20}},"package_platforms":{"terms":{"field":"package_platforms","size":20}}}}},"query":{"bool":{"filter":[{"term":{"type":{"value":"package","_name":"filter_packages"}}},{"bool":{"must":[{"bool":{"should":[]}},{"bool":{"should":[]}},{"bool":{"should":[]}},{"bool":{"should":[]}},{"bool":{"should":[]}}]}}],"must_not":[],"must":[{"dis_max":{"tie_breaker":0.7,"queries":[{"multi_match":{"type":"cross_fields","query":"python","analyzer":"whitespace","auto_generate_synonyms_phrase_query":false,"operator":"and","_name":"multi_match_python","fields":["package_attr_name^9","package_attr_name.*^5.3999999999999995","package_programs^9","package_programs.*^5.3999999999999995","package_pname^6","package_pname.*^3.5999999999999996","package_description^1.3","package_description.*^0.78","package_longDescription^1","package_longDescription.*^0.6","flake_name^0.5","flake_name.*^0.3"]}},{"wildcard":{"package_attr_name":{"value":"*python*","case_insensitive":true}}}]}}]}}}'

def initializeNixFlake(directory, template='default'):
    current_dir = str(os.getcwd())
    pathlib.Path(directory).mkdir(parents=True,exist_ok=True)
    os.chdir(directory)
    print("nix flake init -t templates#" + template)
    os.system("nix flake init -t templates#" + template)
    os.chdir(current_dir)