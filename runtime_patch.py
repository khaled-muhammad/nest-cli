"""
Runtime patches for PyInstaller binary
Fixes os.system and subprocess calls by ensuring proper PATH and environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Store originals
_original_system = os.system
_original_run = subprocess.run

def get_enhanced_env():
    """Get environment with enhanced PATH for Linux systems"""
    env = os.environ.copy()
    
    # Common Linux binary paths
    system_paths = [
        "/usr/local/bin",
        "/usr/bin", 
        "/bin",
        "/usr/sbin",
        "/sbin"
    ]
    
    # User-specific paths
    home = Path.home()
    user_paths = [
        str(home / ".local" / "bin"),
        str(home / "bin")
    ]
    
    # Nix paths (if Nix is installed)
    nix_paths = [
        "/nix/var/nix/profiles/default/bin",
        str(home / ".nix-profile" / "bin")
    ]
    
    # GitHub CLI path
    gh_paths = [
        "/usr/local/github-cli/bin"
    ]
    
    # Collect existing paths
    all_paths = system_paths + user_paths + nix_paths + gh_paths
    existing_paths = [p for p in all_paths if Path(p).exists()]
    
    # Get current PATH and prepend our paths
    current_path = env.get("PATH", "")
    if existing_paths:
        new_path = ":".join(existing_paths)
        env["PATH"] = f"{new_path}:{current_path}" if current_path else new_path
    
    # Set locale to avoid encoding issues
    env.setdefault("LC_ALL", "C.UTF-8")
    env.setdefault("LANG", "C.UTF-8")
    
    return env

def patched_system(command):
    """Enhanced os.system that works better in PyInstaller"""
    try:
        env = get_enhanced_env()
        
        # Use subprocess.run instead of os.system for better control
        result = subprocess.run(
            command,
            shell=True,
            env=env,
            capture_output=False,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode
        
    except subprocess.TimeoutExpired:
        print(f"Command timed out: {command}")
        return 124
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        return 1

def patched_run(*args, **kwargs):
    """Enhanced subprocess.run with proper environment"""
    # Add enhanced environment if not provided
    if 'env' not in kwargs:
        kwargs['env'] = get_enhanced_env()
    
    # Add timeout if not provided for safety
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 300
    
    try:
        return _original_run(*args, **kwargs)
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out: {e}")
        raise
    except FileNotFoundError as e:
        # Try to give a helpful error message
        if args and args[0]:
            cmd = args[0][0] if isinstance(args[0], list) else str(args[0])
            print(f"Command not found: {cmd}")
            print("Make sure the required tool is installed and in PATH")
        raise

def apply_patches():
    """Apply all runtime patches"""
    # Only patch if we're running from a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        os.system = patched_system
        subprocess.run = patched_run
        
        # Also patch any modules that might import these
        import tools.nix.management
        import tools.domains.management  
        import tools.databases.management
        import tools.github.management
        import tools.caddy.management
        
        # Patch the modules directly
        for module in [tools.nix.management, tools.domains.management, 
                      tools.databases.management, tools.github.management, 
                      tools.caddy.management]:
            if hasattr(module, 'os'):
                module.os.system = patched_system
            if hasattr(module, 'subprocess'):
                module.subprocess.run = patched_run

# Auto-apply patches when imported
apply_patches()
