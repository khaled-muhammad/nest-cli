import sys
import os
import json
import re
from typing import Any, Dict, List
import requests
from colorama import Fore, Style
from utils import welcome

#Import modules
from tools.domains import ui as domains_ui
import tools.databases.ui as db_ui
from tools.caddy import ui as caddy_ui
from tools.github import ui as github_ui
from tools.nix import ui as nix_ui
from tools.nix.management import (
    listProfilePackages,
    installProfilePackage,
    uninstallProfilePackage,
    upgradeAllPackages,
    nixShell,
    nixRun,
    nixPackagesSearch,
    garbageCollect,
    checkNixHealth,
    flakeInit,
    flakeRun,
    flakeUpdate,
    flakeInfo,
)
from tools.domains.management import (
    listDomains as domains_list,
    addDomain as domains_add,
    removeDomain as domains_remove,
    getSSLInfo as domains_ssl_info,
)


AI_CHAT_ENDPOINT = "https://ai.hackclub.com/chat/completions"

# Single-session memory
_ai_messages: List[Dict[str, str]] = []

AI_SYSTEM_PROMPT = (
    "You are an AI command router for a CLI. You MUST respond with strict JSON only. "
    "Schema: {\"actions\":[{\"tool\": string, \"operation\": string, \"params\": object}], \"reply\": optional string}. "
    "Available tools and operations: "
    "nix: list_packages(), install_package(package_name), remove_package(package_name_or_index), upgrade_all(), "
    "shell(pkgs:list), run(pkg, cmds?), search(query), gc(optimise_store?), health(), "
    "flake_init(directory, template?, force?), flake_run(ref_or_path, target?, args?), flake_update(directory), flake_info(ref_or_path). "
    "domains: list_domains(), add_domain(domain), remove_domain(domain), ssl_info(domain). "
    "Prefer minimal actions that map 1:1. Never include commentary. Return ONLY JSON."
)


def _ai_call(user_text: str) -> Dict[str, Any] | None:
    if not _ai_messages:
        _ai_messages.append({"role": "system", "content": AI_SYSTEM_PROMPT})
    _ai_messages.append({"role": "user", "content": user_text})

    try:
        res = requests.post(
            AI_CHAT_ENDPOINT,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"messages": _ai_messages[-6:]})  # keep short context
        )
        if res.status_code != 200:
            print(Fore.RED + f"AI API error: {res.status_code}" + Fore.RESET)
            return None
        data = res.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            print(Fore.RED + "AI returned empty content." + Fore.RESET)
            return None
        # Extract first JSON object
        match = re.search(r"\{[\s\S]*\}", content)
        if not match:
            print(Fore.RED + "AI response not JSON." + Fore.RESET)
            return None
        payload = json.loads(match.group(0))
        _ai_messages.append({"role": "assistant", "content": json.dumps(payload)})
        return payload
    except Exception as e:
        print(Fore.RED + f"Failed calling AI: {e}" + Fore.RESET)
        return None


def _dispatch_action(action: Dict[str, Any]):
    tool = action.get("tool")
    op = action.get("operation")
    params = action.get("params") or {}

    if tool == "nix":
        if op == "list_packages":
            print(Fore.CYAN + "Listing nix profile packages" + Fore.RESET)
            listProfilePackages()
            return
        if op == "install_package":
            installProfilePackage(params.get("package_name", ""))
            return
        if op == "remove_package":
            uninstallProfilePackage(params.get("package_name_or_index", params.get("package_name", "")))
            return
        if op == "upgrade_all":
            upgradeAllPackages()
            return
        if op == "shell":
            pkgs = params.get("pkgs") or []
            if isinstance(pkgs, str):
                pkgs = pkgs.split()
            nixShell(pkgs)
            return
        if op == "run":
            nixRun(params.get("pkg", ""), params.get("cmds"))
            return
        if op == "search":
            result = nixPackagesSearch(params.get("query", ""))
            if result:
                print(Fore.MAGENTA + f"Found {len(result.packages)} packages" + Fore.RESET)
                for i, package in enumerate(result.packages[:20]):
                    print(
                        Fore.YELLOW + f"{i+1}. " + Fore.RESET +
                        f"{package.attr_name} " + Style.DIM + f"{package.pversion}" + Style.RESET_ALL
                    )
            return
        if op == "gc":
            garbageCollect(delete_old=True, optimise_store=bool(params.get("optimise_store", True)))
            return
        if op == "health":
            checkNixHealth()
            return
        if op == "flake_init":
            flakeInit(
                params.get("directory", "."),
                template=params.get("template"),
                force=bool(params.get("force", False))
            )
            return
        if op == "flake_run":
            flakeRun(
                params.get("ref_or_path", "."),
                target=params.get("target"),
                args=params.get("args")
            )
            return
        if op == "flake_update":
            flakeUpdate(params.get("directory", "."))
            return
        if op == "flake_info":
            flakeInfo(params.get("ref_or_path", "."))
            return

    if tool == "domains":
        if op == "list_domains":
            domains = domains_list()
            print(Fore.CYAN + f"{len(domains)} domain(s):" + Fore.RESET)
            for i, d in enumerate(domains):
                print(f"  {i+1}. {d.name}")
            return
        if op == "add_domain":
            success, msg = domains_add(params.get("domain", ""))
            print((Fore.GREEN if success else Fore.RED) + msg + Fore.RESET)
            return
        if op == "remove_domain":
            domains_remove(params.get("domain", ""))
            return
        if op == "ssl_info":
            info = domains_ssl_info(params.get("domain", ""))
            print(Fore.YELLOW + "Subject:" + Fore.RESET, info.subject)
            print(Fore.YELLOW + "Issuer:" + Fore.RESET, info.issuer)
            print(Fore.YELLOW + "Issued:" + Fore.RESET, info.issued)
            print(Fore.YELLOW + "Expiry:" + Fore.RESET, info.expiry)
            return

    print(Fore.RED + f"Unknown action: {tool}.{op}" + Fore.RESET)


def handle_ai_command(raw: str):
    user_text = raw[1:].strip()
    if not user_text:
        print(Fore.YELLOW + "Empty AI command." + Fore.RESET)
        return
    print(Fore.CYAN + "Asking AI..." + Fore.RESET)
    payload = _ai_call(user_text)
    if not payload:
        return
    reply = payload.get("reply")
    if reply:
        print(Fore.GREEN + reply + Fore.RESET)
    actions = payload.get("actions", [])
    if not isinstance(actions, list):
        print(Fore.RED + "AI returned invalid actions." + Fore.RESET)
        return
    for action in actions:
        _dispatch_action(action)

os.system('clear')

welcome()

while True:
    print("1- Domains Management")
    print("2- DBs Management")
    print("3- Caddy Management")
    print("4- GitHub Management")
    print("5- Nix Management")
    print("0- Exit")
    print(Fore.CYAN + "\n* You can talk to the tool by starting your command with : character.\n" + Fore.RESET)

    raw = input("Please, Enter your choice: ")
    if raw.strip().startswith(":"):
        handle_ai_command(raw)
        continue
    try:
        res = int(raw)
    except:
        print(Fore.RED + "Please, enter a valid choice!" + Fore.RESET)
        continue
    
    if res < 0 or res > 5:
        print(Fore.RED + "Please, enter a choice in valid range!" + Fore.RESET)
        continue
    
    if res == 0:
        print(Fore.CYAN + "Bye, see you soon." + Fore.RESET)
        sys.exit()
    
    if res == 1:
        domains_ui.start()
    elif res == 2:
        db_ui.start()
    elif res == 3:
        caddy_ui.start()
    elif res == 4:
        github_ui.start()
    elif res == 5:
        nix_ui.start()