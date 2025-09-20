# 🏗️ Nest CLI

A powerful command-line interface for managing development infrastructure and services. Built with Python and featuring an AI assistant for natural language interactions.

## ✨ Features

### 🤖 **AI Assistant**
- **Natural Language Commands**: Use `:command` syntax to interact with all tools
- **Smart Function Mapping**: AI understands your intent and executes appropriate management functions
- **Cross-Tool Integration**: Seamlessly work across all services with conversational commands

### 🛠️ **Tool Management**
- **Nix Package Manager**: Install, manage, and search packages with flakes support
- **Domain Management**: Add, remove, and monitor domains with SSL information
- **Database Operations**: Create, list, and manage PostgreSQL databases
- **GitHub Integration**: Repository management, cloning, and authentication
- **Caddy Web Server**: Site configuration and reverse proxy management

## 🚀 Quick Start

### Installation

#### Option 1: From Source
```bash
# Clone the repository
git clone https://github.com/khaled-muhammad/nest-cli
cd nest-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python main.py
```

#### Option 2: Binary (Linux Only)
```bash
# Download and extract
wget https://github.com/khaled-muhammad/nest-cli/releases/latest/download/nest-cli-linux.tar.gz
tar -xzf nest-cli-linux.tar.gz
cd nest-cli-package

# Install system-wide
sudo ./install.sh

# Or run directly
./nest-cli
```

#### Option 3: Build from Source
```bash
# Clone and build
git clone https://github.com/khaled-muhammad/nest-cli
cd nest-cli
./build.sh

# Install the binary
sudo cp dist/nest-cli /usr/local/bin/
```

### First Run
```bash
python main.py
```

You'll see the welcome screen and main menu:
```
1- Domains Management
2- DBs Management  
3- Caddy Management
4- GitHub Management
5- Nix Management
0- Exit

* You can talk to the tool by starting your command with : character.
```

## 🎯 Usage Examples

### Traditional Menu Navigation
```bash
# Navigate through numbered menus
Please, Enter your choice: 5  # Nix Management
Please, Enter your choice: 2  # Install Package
Enter package name to install: nodejs
```

### AI Assistant Commands
```bash
# Natural language interactions
:install nodejs via nix
:list my domains
:create database called myapp
:show my github repositories
:check nix health
:add domain example.com
:what databases do I have
:run garbage collection on nix
:create a new flake in ./myproject
```

## 🛠️ Tool Details

### 📦 Nix Management
**Traditional Menu**: Option 5
**AI Commands**: `:nix [action] [package/query]`

- **Package Management**: Install, uninstall, list, upgrade packages
- **Search**: Find packages by name or description
- **Shell Environment**: Temporary environments with specific packages
- **One-off Commands**: Run packages without installation
- **Flakes**: Initialize, run, update, and inspect Nix flakes
- **Maintenance**: Garbage collection and health checks

**Examples**:
```bash
:install python3 via nix
:search for rust packages
:upgrade all nix packages
:run cowsay with message "hello world"
:init flake in ./myproject
:check nix system health
```

### 🌐 Domain Management
**Traditional Menu**: Option 1
**AI Commands**: `:domain [action] [domain]`

- **Domain Operations**: Add, remove, list managed domains
- **SSL Monitoring**: Check certificate status and expiry
- **Verification**: Ensure domains are properly configured

**Examples**:
```bash
:add domain example.com
:list my domains
:remove domain old-site.com
:check ssl for example.com
```

### 🗄️ Database Management
**Traditional Menu**: Option 2
**AI Commands**: `:database [action] [name]`

- **Database Operations**: Create, list, remove PostgreSQL databases
- **User-specific**: Automatically manages databases for your user account

**Examples**:
```bash
:create database called myapp
:list my databases
:remove database old_db
```

### 🐙 GitHub Management
**Traditional Menu**: Option 4
**AI Commands**: `:github [action] [repo/query]`

- **Authentication**: Login, logout, check status
- **Repository Management**: List, clone, create repositories
- **Visibility Control**: Public/private repository creation

**Examples**:
```bash
:check github login status
:list my repositories
:clone repository user/repo to ./local-path
:create repository my-new-project as public
```

### 🌐 Caddy Management
**Traditional Menu**: Option 3
**AI Commands**: `:caddy [action] [site/path]`

- **Site Management**: List, add, remove Caddy sites
- **Reverse Proxy**: Configure reverse proxy routes
- **Static Routes**: Set up static file serving
- **Configuration**: Manage Caddyfile updates

**Examples**:
```bash
:list caddy sites
:add reverse proxy to example.com for /api on port 3000
:add static route /static to /var/www/files
```

## 🎨 Interface Features

### Colorized Output
- **Green**: Success messages and confirmations
- **Red**: Errors and warnings
- **Yellow**: Information and prompts
- **Cyan**: Processing and status updates
- **Magenta**: Headers and section titles
- **Dim**: Secondary information and details

### Interactive Prompts
- **Smart Defaults**: Reasonable defaults for optional parameters
- **Validation**: Input validation with helpful error messages
- **Confirmation**: Clear prompts for destructive operations

## 🔧 Configuration

### Environment Setup
The tool automatically detects and uses:
- **Username**: From system for database operations
- **Nix**: System-installed Nix package manager
- **GitHub CLI**: For GitHub operations
- **PostgreSQL**: For database management
- **Caddy**: For web server configuration

### File Locations
- **Caddyfile**: `/home/khaled/nest-cli/CaddyfileTest` (configurable)
- **Nix Store**: System default location
- **Database**: User-specific PostgreSQL databases

## 🤖 AI Assistant Details

### How It Works
1. **Command Processing**: Parses natural language commands
2. **Intent Recognition**: Maps commands to appropriate functions
3. **Function Execution**: Calls management functions with proper arguments
4. **Result Display**: Shows results with colorized output

### Supported Command Patterns
- **Direct Actions**: `:install package`, `:list items`
- **Descriptive**: `:show me my domains`, `:what databases do I have`
- **Contextual**: `:create database called myapp`, `:add domain example.com`
- **Complex**: `:run garbage collection on nix`, `:init flake in ./myproject`

### Function Registry
The AI has access to **25+ management functions** across all tools:
- Nix: 13 functions (packages, flakes, maintenance)
- Domains: 4 functions (CRUD operations, SSL)
- Databases: 3 functions (create, list, remove)
- GitHub: 6 functions (auth, repos, clone, create)
- Caddy: 5 functions (sites, routes, configuration)

## 🛡️ Error Handling

### Graceful Failures
- **Network Issues**: Handles API timeouts and connection errors
- **Missing Dependencies**: Clear messages for missing tools
- **Permission Errors**: Helpful guidance for access issues
- **Invalid Input**: Validation with retry suggestions

### Recovery Options
- **Retry Commands**: Easy re-execution of failed operations
- **Fallback Methods**: Alternative approaches when primary methods fail
- **Clear Error Messages**: Actionable error descriptions

## 📋 Requirements

### System Dependencies
- **Python 3.8+**
- **Nix Package Manager** (for Nix operations)
- **GitHub CLI** (for GitHub operations)
- **PostgreSQL** (for database operations)
- **Caddy** (for web server operations)

### Python Dependencies
```
colorama>=0.4.6
requests>=2.31.0
questionary>=1.10.0
psycopg2-binary>=2.9.7
cryptography>=41.0.0
```

## 🚀 Advanced Usage

### Batch Operations
```bash
# Multiple operations in sequence
:install nodejs python3 git via nix
:create databases called app1 app2 app3
:add domains example.com api.example.com
```

### Complex Workflows
```bash
# Development environment setup
:init flake in ./myproject
:install nodejs python3 via nix
:create database called myproject_dev
:clone repository user/myproject to ./myproject
```

### System Maintenance
```bash
# Regular maintenance tasks
:check nix health
:run garbage collection on nix
:list my domains
:check ssl for all domains
```

## 🏗️ Building

### Build Binary (Linux)
```bash
# Quick build
./build.sh

# Or using Python build script
python build.py

# Or using Makefile
make build
```

### Build Options
- **Simple**: `./build.sh` - Quick single-file build
- **Advanced**: `python build.py` - Full build with environment handling
- **Make**: `make build` - Build with dependency checking

### Distribution Package
```bash
# Create distribution package
make package

# This creates: dist/nest-cli-linux.tar.gz
```

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
make dev

# Test AI assistant
python -c "from ai import ai_assistant; ai_assistant.process_command('list my packages')"
```

### Adding New Tools
1. Create `tools/newtool/management.py` with functions
2. Add functions to AI registry in `ai.py`
3. Create UI in `tools/newtool/ui.py`
4. Add menu option in `main.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hack Club AI**: For providing the AI API endpoint
- **Nix Community**: For the excellent package management system

---

**Made with ❤️ for developers who love powerful CLI tools**