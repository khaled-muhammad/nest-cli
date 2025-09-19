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

def garbageCollect(delete_old: bool = True, optimise_store: bool = True):
    try:
        print(Fore.CYAN + "Starting Nix store cleanup..." + Fore.RESET)

        if delete_old:
            print(Fore.YELLOW + "- Deleting old generations and collecting garbage (-d)" + Fore.RESET)
            gc = subprocess.run([
                "nix-collect-garbage", "-d"
            ], capture_output=True, text=True)
            if gc.stdout.strip():
                print(Style.DIM + gc.stdout.strip() + Style.RESET_ALL)
            if gc.returncode != 0:
                print(Fore.RED + gc.stderr.strip() + Fore.RESET)

        if optimise_store:
            print(Fore.YELLOW + "- Optimising store (hard-link duplicates)" + Fore.RESET)
            opt = subprocess.run([
                "nix", "store", "optimise"
            ], capture_output=True, text=True)
            if opt.stdout.strip():
                print(Style.DIM + opt.stdout.strip() + Style.RESET_ALL)
            if opt.returncode != 0:
                print(Fore.RED + opt.stderr.strip() + Fore.RESET)

        print(Fore.GREEN + "Nix store cleanup finished." + Fore.RESET)
    except FileNotFoundError:
        print(Fore.RED + "Nix is not installed or not on PATH." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Fore.RESET)

def checkNixHealth():
    try:
        print(Fore.CYAN + "Running Nix health checks..." + Fore.RESET)

        # Prefer `nix doctor` when available
        doctor = subprocess.run([
            "nix", "doctor"
        ], capture_output=True, text=True)

        if doctor.returncode == 0:
            if doctor.stdout.strip():
                print(Style.DIM + doctor.stdout.strip() + Style.RESET_ALL)
            print(Fore.GREEN + "Nix doctor completed successfully." + Fore.RESET)
            return

        # Fallback: verify store contents
        print(Fore.YELLOW + "`nix doctor` failed or unavailable, verifying store contents..." + Fore.RESET)
        verify = subprocess.run([
            "nix-store", "--verify", "--check-contents"
        ], capture_output=True, text=True)

        if verify.stdout.strip():
            print(Style.DIM + verify.stdout.strip() + Style.RESET_ALL)
        if verify.returncode != 0:
            print(Fore.RED + verify.stderr.strip() + Fore.RESET)
        else:
            print(Fore.GREEN + "Nix store verification completed successfully." + Fore.RESET)
    except FileNotFoundError:
        print(Fore.RED + "Nix is not installed or not on PATH." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}" + Fore.RESET)

def flakeInit(directory: str, template: str | None = None, force: bool = False):
    try:
        path = pathlib.Path(directory).expanduser().resolve()
        if not path.exists():
            print(Fore.YELLOW + f"Creating directory: {path}" + Fore.RESET)
            path.mkdir(parents=True, exist_ok=True)

        cmd = ["nix", "flake", "init"]
        if template:
            # Allow plain template name (uses nixpkgs) or full ref
            ref = template if ("#" in template or ":" in template) else f"nixpkgs#{template}"
            cmd += ["-t", ref]
        if force:
            cmd.append("--refresh")

        print(Fore.CYAN + f"Initializing flake in {path}" + Fore.RESET)
        res = subprocess.run(cmd, cwd=str(path), capture_output=True, text=True)

        if res.stdout.strip():
            print(Style.DIM + res.stdout.strip() + Style.RESET_ALL)
        if res.returncode != 0:
            print(Fore.RED + res.stderr.strip() + Fore.RESET)
            return False
        print(Fore.GREEN + "Flake initialized." + Fore.RESET)
        return True
    except Exception as e:
        print(Fore.RED + f"Failed to init flake: {e}" + Fore.RESET)
        return False

def flakeRun(flake_ref_or_path: str, target: str | None = None, args: str | None = None):
    try:
        ref = flake_ref_or_path
        if pathlib.Path(flake_ref_or_path).expanduser().exists():
            ref = str(pathlib.Path(flake_ref_or_path).expanduser().resolve())

        full_ref = ref if target is None or target.strip() == "" else f"{ref}#{target}"
        cmd = ["nix", "run", full_ref]
        if args and args.strip():
            cmd += ["--"] + args.split()

        print(Fore.CYAN + f"Running flake: {full_ref}" + Fore.RESET)
        os.system(" ".join(cmd))
    except Exception as e:
        print(Fore.RED + f"Failed to run flake: {e}" + Fore.RESET)

def flakeUpdate(directory: str):
    try:
        path = pathlib.Path(directory).expanduser().resolve()
        print(Fore.CYAN + f"Updating flake in {path}" + Fore.RESET)
        res = subprocess.run(["nix", "flake", "update"], cwd=str(path), capture_output=True, text=True)
        if res.stdout.strip():
            print(Style.DIM + res.stdout.strip() + Style.RESET_ALL)
        if res.returncode != 0:
            print(Fore.RED + res.stderr.strip() + Fore.RESET)
            return False
        print(Fore.GREEN + "Flake updated." + Fore.RESET)
        return True
    except Exception as e:
        print(Fore.RED + f"Failed to update flake: {e}" + Fore.RESET)
        return False

def flakeInfo(flake_ref_or_path: str):
    try:
        ref = flake_ref_or_path
        if pathlib.Path(flake_ref_or_path).expanduser().exists():
            ref = str(pathlib.Path(flake_ref_or_path).expanduser().resolve())

        print(Fore.CYAN + f"Fetching flake metadata for {ref}" + Fore.RESET)
        res = subprocess.run(["nix", "flake", "metadata", ref, "--json"], capture_output=True, text=True)
        if res.returncode != 0:
            print(Fore.RED + res.stderr.strip() + Fore.RESET)
            return None

        data = json.loads(res.stdout)
        # Minimal pretty output here; callers can post-process if needed
        print(Fore.YELLOW + "- Description:" + Fore.RESET, str(data.get("description", "")))
        print(Fore.YELLOW + "- Path:" + Fore.RESET, str(data.get("path", "")))
        print(Fore.YELLOW + "- Resolved URL:" + Fore.RESET, data.get("resolvedUrl", ""))
        inputs = data.get("inputs", {})
        if inputs:
            print(Fore.MAGENTA + "- Inputs:" + Fore.RESET)
            for k, v in inputs.items():
                print("  " + Fore.CYAN + k + Fore.RESET + ":", v.get("locked", {}).get("rev" , v.get("original", {}).get("url", "")))
        return data
    except Exception as e:
        print(Fore.RED + f"Failed to get flake info: {e}" + Fore.RESET)
        return None

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
