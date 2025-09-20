#!/usr/bin/env python3
"""
Build script for nest-cli using PyInstaller
Handles subprocess and os.system calls properly for Linux
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if all required tools are available"""
    print("🔍 Checking dependencies...")
    
    required_commands = [
        'nix', 'nix-collect-garbage', 'nix-store',
        'gh', 'git', 'psql', 'caddy', 'nest'
    ]
    
    missing = []
    for cmd in required_commands:
        if not shutil.which(cmd):
            missing.append(cmd)
    
    if missing:
        print(f"⚠️  Warning: Missing commands: {', '.join(missing)}")
        print("   The built binary will require these to be installed on target systems")
    else:
        print("✅ All dependencies found")

def create_wrapper_script():
    """Create a wrapper script to handle PATH and environment"""
    wrapper_content = '''#!/bin/bash
# Nest CLI Wrapper Script
# Ensures proper PATH and environment for subprocess calls

# Add common binary paths
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

# Add user's local bin if it exists
if [ -d "$HOME/.local/bin" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# Add nix paths if they exist
if [ -d "/nix/var/nix/profiles/default/bin" ]; then
    export PATH="/nix/var/nix/profiles/default/bin:$PATH"
fi

if [ -d "$HOME/.nix-profile/bin" ]; then
    export PATH="$HOME/.nix-profile/bin:$PATH"
fi

# Set proper locale
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Run the actual binary
exec "$(dirname "$0")/nest-cli-bin" "$@"
'''
    
    with open('dist/nest-cli', 'w') as f:
        f.write(wrapper_content)
    
    os.chmod('dist/nest-cli', 0o755)
    print("✅ Created wrapper script")

def patch_subprocess_calls():
    """Create a patched version that handles subprocess calls better"""
    print("🔧 Patching subprocess calls...")
    
    # Create a runtime patch file
    patch_content = '''
import os
import sys
import subprocess
from pathlib import Path

# Store original functions
_original_system = os.system
_original_run = subprocess.run
_original_popen = subprocess.Popen

def patched_system(command):
    """Patched os.system that handles PATH properly"""
    # Ensure we have a proper shell environment
    env = os.environ.copy()
    
    # Add common paths
    paths = [
        "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin",
        str(Path.home() / ".local" / "bin"),
        "/nix/var/nix/profiles/default/bin",
        str(Path.home() / ".nix-profile" / "bin")
    ]
    
    current_path = env.get("PATH", "")
    new_paths = [p for p in paths if Path(p).exists()]
    if new_paths:
        env["PATH"] = ":".join(new_paths + [current_path])
    
    # Use subprocess instead of os.system for better control
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            env=env,
            capture_output=False,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"Error executing command: {e}")
        return 1

def patched_run(*args, **kwargs):
    """Patched subprocess.run with proper environment"""
    if 'env' not in kwargs:
        env = os.environ.copy()
        
        # Add common paths
        paths = [
            "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin",
            str(Path.home() / ".local" / "bin"),
            "/nix/var/nix/profiles/default/bin",
            str(Path.home() / ".nix-profile" / "bin")
        ]
        
        current_path = env.get("PATH", "")
        new_paths = [p for p in paths if Path(p).exists()]
        if new_paths:
            env["PATH"] = ":".join(new_paths + [current_path])
        
        kwargs['env'] = env
    
    return _original_run(*args, **kwargs)

def patched_popen(*args, **kwargs):
    """Patched subprocess.Popen with proper environment"""
    if 'env' not in kwargs:
        env = os.environ.copy()
        
        # Add common paths  
        paths = [
            "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin",
            str(Path.home() / ".local" / "bin"),
            "/nix/var/nix/profiles/default/bin", 
            str(Path.home() / ".nix-profile" / "bin")
        ]
        
        current_path = env.get("PATH", "")
        new_paths = [p for p in paths if Path(p).exists()]
        if new_paths:
            env["PATH"] = ":".join(new_paths + [current_path])
            
        kwargs['env'] = env
    
    return _original_popen(*args, **kwargs)

# Apply patches
os.system = patched_system
subprocess.run = patched_run  
subprocess.Popen = patched_popen
'''
    
    with open('subprocess_patch.py', 'w') as f:
        f.write(patch_content)

def build_binary():
    """Build the binary using PyInstaller"""
    print("🏗️  Building binary with PyInstaller...")
    
    # Create the patch file
    patch_subprocess_calls()
    
    # Get whois data file path
    try:
        import whois
        whois_path = os.path.dirname(whois.__file__)
        whois_data_file = os.path.join(whois_path, 'data', 'public_suffix_list.dat')
        print(f"📄 Including whois data from: {whois_data_file}")
    except ImportError:
        whois_data_file = None
        print("⚠️  Warning: whois package not found, domain whois lookup may not work")
    
    # Build command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--name=nest-cli-bin',
        '--specpath=.',
        '--distpath=dist',
        '--workpath=build',
        '--add-data=tools:tools',
        '--hidden-import=runtime_patch',
        '--hidden-import=tools.nix.management',
        '--hidden-import=tools.domains.management', 
        '--hidden-import=tools.databases.management',
        '--hidden-import=tools.github.management',
        '--hidden-import=tools.caddy.management',
        '--hidden-import=ai',
        '--hidden-import=utils',
        '--hidden-import=colorama',
        '--hidden-import=requests',
        '--hidden-import=questionary',
        '--hidden-import=psycopg2',
        '--hidden-import=cryptography',
        '--hidden-import=whois',
        '--hidden-import=whois.parser',
        '--additional-hooks-dir=.',
        'main.py'
    ]
    
    # Add whois data if available
    if whois_data_file and os.path.exists(whois_data_file):
        cmd.insert(-1, f'--add-data={whois_data_file}:whois/data')
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Binary built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def create_hook_file():
    """Create PyInstaller hook for subprocess patching"""
    hook_content = '''
from PyInstaller.utils.hooks import collect_all

# Collect all data and imports
datas, binaries, hiddenimports = collect_all('subprocess_patch')

# Add the patch to the runtime
def get_hook_dirs():
    return ['.']
'''
    
    os.makedirs('hooks', exist_ok=True)
    with open('hooks/hook-subprocess_patch.py', 'w') as f:
        f.write(hook_content)

def main():
    """Main build process"""
    print("🚀 Building nest-cli for Linux...")
    
    # Check if we're on Linux
    if sys.platform != 'linux':
        print("⚠️  Warning: This build is optimized for Linux")
    
    # Check dependencies
    check_dependencies()
    
    # Create hook file
    create_hook_file()
    
    # Clean previous builds
    if Path('dist').exists():
        shutil.rmtree('dist')
    if Path('build').exists():
        shutil.rmtree('build')
    
    # Build the binary
    if not build_binary():
        sys.exit(1)
    
    # Create wrapper script
    create_wrapper_script()
    
    # Clean up temporary files
    for temp_file in ['subprocess_patch.py', 'nest-cli-bin.spec']:
        if Path(temp_file).exists():
            os.remove(temp_file)
    
    if Path('hooks').exists():
        shutil.rmtree('hooks')
    
    print("\n🎉 Build complete!")
    print(f"📦 Binary location: {Path('dist/nest-cli').absolute()}")
    print(f"📦 Raw binary: {Path('dist/nest-cli-bin').absolute()}")
    print("\n📋 Installation:")
    print("   sudo cp dist/nest-cli /usr/local/bin/")
    print("   sudo cp dist/nest-cli-bin /usr/local/bin/")
    print("\n🧪 Test the build:")
    print("   ./dist/nest-cli")

if __name__ == '__main__':
    main()
