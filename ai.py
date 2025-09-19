import json
import requests
from colorama import Fore, Style
from typing import Dict, Any, List, Optional

# Import all management modules
from tools.nix import management as nix_mgmt
from tools.domains import management as domains_mgmt
from tools.databases import management as db_mgmt
from tools.github import management as github_mgmt
from tools.caddy import management as caddy_mgmt


class AIAssistant:
    """AI Assistant that can execute management functions across all tools"""
    
    def __init__(self):
        self.api_url = "https://ai.hackclub.com/chat/completions"
        self.available_functions = self._build_function_registry()
    
    def _build_function_registry(self) -> Dict[str, Any]:
        """Build registry of all available management functions"""
        return {
            # Nix Management
            "list_nix_packages": {
                "function": nix_mgmt.listProfilePackages,
                "description": "List installed Nix packages",
                "args": []
            },
            "install_nix_package": {
                "function": nix_mgmt.installProfilePackage,
                "description": "Install a Nix package",
                "args": ["package_name"]
            },
            "uninstall_nix_package": {
                "function": nix_mgmt.uninstallProfilePackage,
                "description": "Uninstall a Nix package",
                "args": ["package_name"]
            },
            "upgrade_nix_packages": {
                "function": nix_mgmt.upgradeAllPackages,
                "description": "Upgrade all Nix packages",
                "args": []
            },
            "nix_shell": {
                "function": nix_mgmt.nixShell,
                "description": "Start Nix shell with packages",
                "args": ["packages_list"]
            },
            "nix_run": {
                "function": nix_mgmt.nixRun,
                "description": "Run a Nix package one-off",
                "args": ["package", "commands"]
            },
            "search_nix_packages": {
                "function": nix_mgmt.nixPackagesSearch,
                "description": "Search for Nix packages",
                "args": ["query"]
            },
            "nix_garbage_collect": {
                "function": nix_mgmt.garbageCollect,
                "description": "Run Nix garbage collection",
                "args": ["delete_old", "optimise_store"]
            },
            "check_nix_health": {
                "function": nix_mgmt.checkNixHealth,
                "description": "Check Nix system health",
                "args": []
            },
            "init_flake": {
                "function": nix_mgmt.flakeInit,
                "description": "Initialize a new Nix flake",
                "args": ["directory", "template", "force"]
            },
            "run_flake": {
                "function": nix_mgmt.flakeRun,
                "description": "Run a Nix flake",
                "args": ["flake_ref_or_path", "target", "args"]
            },
            "update_flake": {
                "function": nix_mgmt.flakeUpdate,
                "description": "Update a Nix flake",
                "args": ["directory"]
            },
            "flake_info": {
                "function": nix_mgmt.flakeInfo,
                "description": "Show Nix flake information",
                "args": ["flake_ref_or_path"]
            },
            
            # Domain Management
            "list_domains": {
                "function": domains_mgmt.listDomains,
                "description": "List all managed domains",
                "args": []
            },
            "add_domain": {
                "function": domains_mgmt.addDomain,
                "description": "Add a new domain",
                "args": ["domain"]
            },
            "remove_domain": {
                "function": domains_mgmt.removeDomain,
                "description": "Remove a domain",
                "args": ["domain"]
            },
            "get_ssl_info": {
                "function": domains_mgmt.getSSLInfo,
                "description": "Get SSL certificate information for a domain",
                "args": ["domain"]
            },
            
            # Database Management
            "create_database": {
                "function": db_mgmt.create_db,
                "description": "Create new databases",
                "args": ['db_name']
            },
            "list_databases": {
                "function": db_mgmt.list_user_databases,
                "description": "List user databases",
                "args": []
            },
            "remove_database": {
                "function": db_mgmt.remove_database,
                "description": "Remove a database",
                "args": ["db_name"]
            },
            
            # GitHub Management
            "check_github_auth": {
                "function": github_mgmt.check_if_github_logged_in,
                "description": "Check if logged into GitHub",
                "args": []
            },
            "github_login": {
                "function": github_mgmt.github_auth,
                "description": "Login to GitHub",
                "args": []
            },
            "github_logout": {
                "function": github_mgmt.github_logout,
                "description": "Logout from GitHub",
                "args": []
            },
            "list_repos": {
                "function": github_mgmt.list_repos,
                "description": "List GitHub repositories",
                "args": ["limit"]
            },
            "clone_repo": {
                "function": github_mgmt.clone_repo,
                "description": "Clone a repository",
                "args": ["repo", "save_path"]
            },
            "create_repo": {
                "function": github_mgmt.create_repo,
                "description": "Create a new repository",
                "args": ["name", "visibility", "description", "local_path"]
            },
            
            # Caddy Management
            "list_caddy_sites": {
                "function": caddy_mgmt.listSites,
                "description": "List Caddy sites",
                "args": []
            },
            "add_reverse_proxy": {
                "function": caddy_mgmt.addReverseProxy,
                "description": "Add reverse proxy to site",
                "args": ["site", "path", "port"]
            },
            "add_static_route": {
                "function": caddy_mgmt.addStaticRoute,
                "description": "Add static route to site",
                "args": ["site", "route_path", "path"]
            },
            "save_updated_site": {
                "function": caddy_mgmt.saveUpdatedSite,
                "description": "Save updated site configuration",
                "args": ["site"]
            },
            "delete_caddy_site": {
                "function": caddy_mgmt.deleteSite,
                "description": "Delete a Caddy site",
                "args": ["site"]
            }
        }
    
    def _get_function_descriptions(self) -> str:
        """Generate function descriptions for the AI"""
        descriptions = []
        for name, info in self.available_functions.items():
            args_str = ", ".join(info["args"]) if info["args"] else "no arguments"
            descriptions.append(f"- {name}({args_str}): {info['description']}")
        return "\n".join(descriptions)
    
    def _call_ai(self, user_message: str) -> Optional[str]:
        """Call the Hack Club AI API"""
        try:
            system_prompt = f"""You are a helpful assistant for a CLI tool that manages various services (Nix packages, domains, databases, GitHub repos, Caddy web server).

Available functions you can call:
{self._get_function_descriptions()}

When the user asks for something that requires calling functions:
1. Identify which function(s) to call
2. Respond with function calls in this JSON format:
{{"function_calls": [{{"name": "function_name", "args": {{"arg1": "value1", "arg2": "value2"}}}}]}}

For simple questions or when no function calls are needed, respond normally.

Examples:
- "list my nix packages" → call list_nix_packages
- "install nodejs via nix" → call install_nix_package with package_name="nodejs"
- "show my domains" → call list_domains
- "check github login status" → call check_github_auth

Be concise and helpful. Always consider the user's intent and suggest the most appropriate function calls."""

            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            }
            
            response = requests.post(
                self.api_url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(Fore.RED + f"AI API Error: {response.status_code}" + Fore.RESET)
                return None
                
        except Exception as e:
            print(Fore.RED + f"Error calling AI: {e}" + Fore.RESET)
            return None
    
    def _parse_function_calls(self, ai_response: str) -> List[Dict[str, Any]]:
        """Parse function calls from AI response"""
        try:
            # Look for JSON in the response
            start = ai_response.find('{"function_calls":')
            if start == -1:
                return []
            
            end = ai_response.find('}}]', start) + 3
            if end == 2:  # Not found
                return []
            
            json_str = ai_response[start:end]
            data = json.loads(json_str)
            return data.get("function_calls", [])
            
        except Exception as e:
            print(Fore.YELLOW + f"Could not parse function calls: {e}" + Fore.RESET)
            return []
    
    def _execute_function(self, function_name: str, args: Dict[str, Any]) -> Any:
        """Execute a management function"""
        if function_name not in self.available_functions:
            print(Fore.RED + f"Unknown function: {function_name}" + Fore.RESET)
            return None
        
        func_info = self.available_functions[function_name]
        func = func_info["function"]
        
        try:
            # Convert args dict to positional args based on function signature
            expected_args = func_info["args"]
            positional_args = []
            
            for arg_name in expected_args:
                if arg_name in args:
                    positional_args.append(args[arg_name])
                else:
                    # Use reasonable defaults for missing args
                    if arg_name in ["delete_old", "optimise_store", "force"]:
                        positional_args.append(True)
                    elif arg_name in ["template", "target", "commands", "args", "description", "local_path"]:
                        positional_args.append(None)
                    elif arg_name == "limit":
                        positional_args.append(30)
                    elif arg_name == "visibility":
                        positional_args.append("public")
                    else:
                        positional_args.append("")
            
            print(Fore.CYAN + f"Executing: {function_name}" + Fore.RESET)
            result = func(*positional_args) if positional_args else func()
            return result
            
        except Exception as e:
            print(Fore.RED + f"Error executing {function_name}: {e}" + Fore.RESET)
            return None
    
    def process_command(self, user_input: str) -> None:
        """Process a user command with AI assistance"""
        print(Fore.MAGENTA + "AI Assistant:" + Fore.RESET + " Processing your request...")
        
        ai_response = self._call_ai(user_input)
        if not ai_response:
            print(Fore.RED + "Failed to get AI response" + Fore.RESET)
            return
        
        # Check if AI wants to call functions
        function_calls = self._parse_function_calls(ai_response)
        
        if function_calls:
            print(Fore.CYAN + "Executing requested actions..." + Fore.RESET)
            for call in function_calls:
                function_name = call.get("name")
                args = call.get("args", {})
                result = self._execute_function(function_name, args)
                
                # Show result if it's informational
                if result and function_name.startswith(("list_", "check_", "search_")):
                    if isinstance(result, (list, dict)):
                        print(Style.DIM + str(result) + Style.RESET_ALL)
        else:
            # Just show AI response
            print(Fore.MAGENTA + "AI:" + Fore.RESET, ai_response)


# Global instance
ai_assistant = AIAssistant()
