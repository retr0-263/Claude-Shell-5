# Master Umbrella Setup - Quick Reference

## 🚀 Getting Started

```bash
python3 master_umbrella_setup.py
```

## 📋 Main Menu Structure

### 🔧 Setup & Configuration
1. **Run Setup Wizard** - Complete 6-step configuration
2. **View Configuration** - See current settings
3. **Show Distribution Keys** - Keys for client distribution
4. **Manage Owners** - Add/remove authorized users
5. **Manage Targets** - Add/remove target machines

### ⚙️ Operations
6. **Start C2 Server** - Launch command & control
7. **Start Full System** - All components (C2, API, WhatsApp)
8. **Test Targets** - Verify connectivity
9. **Execute Command** - Send commands to targets (requires confirmation)

### 📊 Tools
10. **Build Client Executable** - Compile RAT payload
11. **Export Configuration** - Save to file
12. **View Logs** - System logging

## 🔒 Owner Recognition

### Hardcoded Owner
- **Phone:** `+263781564004` (immutable/cannot be removed)
- **Role:** PRIMARY_OWNER
- **Access:** Full system access

### Authorized Owners
- Add secondary owners through "Manage Owners"
- Each gets SECONDARY_OWNER role
- Can also add phone numbers through wizard

## 🎯 Target Confirmation System

### Before Executing Commands:
1. Targets must be added and confirmed active
2. To execute: system requires keyword confirmation
3. **Confirmation Keyword:** `CONFIRM_TARGETS_263`
4. Command only proceeds with correct keyword + active targets

### Example Workflow:
```
1. Add targets (Menu > Manage Targets > Add target)
2. Execute Command (Menu 9)
3. System shows active targets
4. Enter confirmation keyword: CONFIRM_TARGETS_263
5. Enter command to execute
6. Command queued to all targets
```

## 🔑 Distribution Keys

### Contents:
- C2 Server IP and ports
- Encryption key (Fernet format)
- List of authorized owners
- Version and creation timestamp

### Export Options:
- **Display on Screen:** Menu 3 > Shows formatted output
- **Save to File:** Menu 11 > Exports to JSON

### Sharing:
Share the exported JSON with clients - contains:
- C2 connection details
- Encryption key for payload
- Owner information

## ⚙️ Configuration

### Server Modes:
- **Local:** 127.0.0.1 (development/testing)
- **Network:** Auto-detect IP (LAN deployment)
- **Remote:** Custom IP (internet deployment)

### Ports (Customizable):
- **C2 Port:** Default 4444
- **API Port:** Default 5000
- **Webhook Port:** Default 8888

### Encryption:
- **Method:** Fernet (symmetric encryption)
- **Key Rotation:** 30 days (configurable)
- **Storage:** tool_base_263_master.json

## 📁 Configuration Files

### Primary Config:
`tool_base_263_master.json` - Master configuration (auto-created)

### Auto-Updated Files:
- `rat_ultimate.py` - RAT payload
- `rat_server_fixed.py` - C2 server
- `rat_api_bridge.py` - API bridge

## 🎨 Color Scheme

| Color | Usage |
|-------|-------|
| NEON_GREEN | Success, active status |
| NEON_PINK | Headers, emphasis |
| NEON_BLUE | Information |
| BR_RED | Errors, critical |
| BR_YELLOW | Warnings, secondary |
| BR_CYAN | Prompts, input |

## ⚠️ Important Notes

1. **Hardcoded Owner Cannot Be Removed** - +263781564004 is permanent
2. **Target Confirmation Required** - Commands need active targets + keyword
3. **Configuration Conflicts Prevented** - Single source of truth (no duplication)
4. **All Keys Exportable** - For easy client distribution
5. **Auto-Configuration** - Setup wizard applies to all RAT files
6. **Persistent Storage** - Settings saved to JSON (survives restarts)

## 🔧 Advanced Features

### Configuration Wizard (6 Steps)
1. Server Configuration (IP mode selection)
2. Port Configuration (C2, API, Webhook)
3. Encryption Setup (key generation)
4. Owner Authorization (hardcoded + secondary)
5. Target Configuration (add managed targets)
6. Review & Save (apply to all files)

### Multi-Component System
- **C2 Server:** rat_server_fixed.py
- **API Bridge:** rat_api_bridge.py
- **WhatsApp Bot:** whatsapp-c2/bot.js

Can start individually or as full system (Menu 7).

### Connectivity Testing
- Ping all configured targets
- Shows REACHABLE/UNREACHABLE status
- Helpful for pre-deployment verification

### Executable Builder
- Uses PyInstaller for compilation
- Creates single-file executable
- Takes 2-3 minutes

## 📝 Logging

- **Log File:** tool_base_263.log (auto-created)
- **Auto-Compression:** Enabled
- **View:** Menu 12 shows last 50 lines

## 🚀 Deployment Workflow

1. **Initial Setup:** Run Setup Wizard (Menu 1)
2. **Add Targets:** Menu 5 > Add target machine
3. **Build Client:** Menu 10 > Compile executable
4. **Get Keys:** Menu 3 > Show Distribution Keys
5. **Export Config:** Menu 11 > Save configuration
6. **Start System:** Menu 7 > Launch all components
7. **Test Connectivity:** Menu 8 > Verify targets
8. **Execute Commands:** Menu 9 > With confirmation

## 💡 Tips

- Always run Setup Wizard first (Menu 1)
- Test connectivity before sending commands (Menu 8)
- Export keys before distributing clients (Menu 11)
- Check logs regularly for issues (Menu 12)
- Hardcoded owner can always manage system

---

**Created by:** Hxcker-263  
**Owner:** +263781564004  
**Version:** 2.0  
**Last Updated:** 2025
