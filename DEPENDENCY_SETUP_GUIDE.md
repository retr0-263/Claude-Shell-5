# Dependency Installation Setup Guide

## Overview

The T0OL-B4S3-263 launcher now includes a comprehensive **Dependency Installation Manager** (Option 6) that simplifies project setup and dependency management.

## Features

### 🔧 Installation Options

1. **Python Dependencies** - Install all Python packages from `requirements.txt`
2. **Node.js Dependencies** - Install npm modules from `package.json`
3. **Install All** - Install both Python and Node.js dependencies
4. **View Installed Packages** - Display current installation status
5. **Back to Main Menu** - Return to main launcher

### 📊 Status Display

After each installation, the system automatically displays:

- **Python Environment**
  - Total packages installed
  - Status of critical packages (colorama, cryptography, requests, flask)
  
- **Node.js Environment**
  - npm version information
  - node_modules installation status
  - Total modules installed

- **Recently Configured**
  - C2 Server Configuration status
  - Payload Configuration status
  - Obfuscation Settings status
  - Database Configuration status

## Usage Guide

### Quick Start

```bash
cd /workspaces/Claude-Shell-5
python3 launcher.py
```

### Main Menu Navigation

```
╔════════════════════════════════════════╗
║       T0OL-B4S3-263 SETUP LAUNCHER       ║
╚════════════════════════════════════════╝
  1. Quick Setup (All Components)      # Full setup + all configs
  2. Basic Configuration Only          # C2 + Payload + WhatsApp
  3. Advanced C2 Configuration         # Multi-channel C2 setup
  4. Payload Obfuscation Setup         # Obfuscation configuration
  5. Database Initialization           # SQLite database setup
  6. Install Dependencies              # ← NEW: Install Python/Node deps
  7. Deploy & Test                     # Testing & deployment
  8. View Configuration Summary        # Show current settings
  9. Exit                             # Close launcher
```

## Installation Workflows

### Workflow 1: Dependencies Only

```
Select: 6 (Install Dependencies)
├── 1 (Python Deps) or 2 (Node Deps) or 3 (All)
├── View status report
└── 5 (Back to Main Menu)
```

**Output:**
- ✓ Installation progress
- ✓ Package count and names
- ✓ Required packages status
- ✓ Environment information

### Workflow 2: Complete Setup with Dependencies

```
Select: 1 (Quick Setup)
├── Configure C2 Server
├── Configure Payload
├── Configure WhatsApp Bot
├── Advanced C2 Setup
├── Obfuscation Setup
├── Database Initialization
└── Then select: 6 (Install Dependencies)
    ├── 3 (Install All)
    └── See complete status including "Recently Configured"
```

**Output Example:**
```
╔════════════════════════════════════════╗
║     INSTALLATION STATUS REPORT           ║
╚════════════════════════════════════════╝

📦 Python Environment:
   ✓ 123 packages installed

   Required Packages:
   ✓ colorama
   ✓ cryptography
   ✓ requests
   ✓ flask

🔧 Node.js Environment:
   ✓ npm 9.8.1 installed
   ✓ 45 modules installed in node_modules/

⚙️  Recently Configured:
   ✓ C2 Server Configuration
   ✓ Payload Configuration
   ✓ Obfuscation Settings
   ✓ Database Configuration
```

### Workflow 3: Check Status Without Installing

```
Select: 6 (Install Dependencies)
└── 4 (View Installed Packages)
    └── Shows all installed components without installing anything
```

## Package Requirements

### Python Dependencies (`requirements.txt`)

```
PyAudio==0.2.14              # Audio capture for surveillance
PyAutoGUI==0.9.54            # Mouse/keyboard control
PyGetWindow==0.0.9           # Window enumeration
WMI==1.5.1                   # Windows Management Instrumentation
colorama==0.4.6              # Colored terminal output ✓
comtypes==1.4.13             # COM interfaces for Windows
cryptography==45.0.7         # Encryption/decryption
dnspython==2.8.0             # DNS tunneling support
numpy==2.2.6                 # Numerical computing
opencv-python==4.12.0.88     # Computer vision
pandas==2.3.3                # Data analysis
pillow==12.0.0               # Image processing
psutil==7.1.3                # System monitoring
pyarmor==9.2.1               # Code obfuscation
pycryptodome==3.23.0         # Additional crypto
pyinstaller==6.15.0          # Executable packaging
pynput==1.8.1                # Low-level input
pypiwin32==223               # Win32 API access
python-dateutil==2.9.0       # Date utilities
python-nmap==0.7.1           # Network scanning
pywin32==311                 # Windows API
requests==2.32.5             # HTTP requests ✓
scapy==2.6.1                 # Network manipulation
scikit-learn==1.7.2          # Machine learning
sounddevice==0.5.3           # Audio I/O
```

### Node.js Dependencies (Optional)

- **Baileys** - WhatsApp Web automation
- **Express** - Web server framework
- **Socket.io** - Real-time communication
- Plus development dependencies

## Status Codes

### Installation Status Indicators

| Symbol | Meaning | Color |
|--------|---------|-------|
| ✓ | Successfully installed/configured | 🟢 Green |
| ✗ | Not installed/missing | 🔴 Red |
| ⚠ | Warning/available but not installed | 🟡 Yellow |
| → | Installing in progress | 🔵 Blue |
| ↓ | Download phase | 🔵 Blue |

### Python Package Status

```
✓ colorama         # Terminal colors (INSTALLED)
✗ cryptography     # Encryption (NOT INSTALLED) 
⚠ flask            # Web framework (AVAILABLE but not required)
```

### Environment Checks

```
📦 Python Environment:
   ✓ 123 packages installed
   
🔧 Node.js Environment:
   ✓ npm 9.8.1 installed
   ✓ 45 modules installed
```

## Troubleshooting

### Issue: "requirements.txt not found"

**Solution:**
```bash
# Ensure you're in the project root
cd /workspaces/Claude-Shell-5

# Verify requirements.txt exists
ls -la requirements.txt

# Then run launcher
python3 launcher.py
```

### Issue: "npm not found"

**Solution:**
```bash
# Install Node.js (includes npm)
sudo apt-get update
sudo apt-get install -y nodejs npm

# Or using snap
sudo snap install node --classic

# Verify installation
npm --version
```

### Issue: Permission Denied on pip install

**Solution:**
```bash
# Use user-level installation
python3 -m pip install --user -r requirements.txt

# Or create a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Python Version Mismatch

**Example Error:**
```
ERROR: Ignored versions... Requires-Python >=3.7,<3.11
```

**Solution:**
```bash
# Check Python version
python3 --version

# Some packages need Python 3.10 or lower
# If you have Python 3.12+, consider creating a virtual environment
python3.10 -m venv venv_py310
source venv_py310/bin/activate
```

## Advanced Usage

### Custom Installation Order

```python
# Example: Install only specific components
launcher = IntegratedSetupLauncher()

# Setup configuration first
launcher.setup_basic()
launcher.setup_advanced_c2()
launcher.setup_obfuscation()
launcher.init_database()

# Then install dependencies
launcher.install_dependencies()
```

### Checking Specific Packages

```bash
# List all installed Python packages
pip list

# Show specific package info
pip show colorama

# Check npm packages
npm list

# Show npm package info
npm info colorama
```

## Integration with Setup Workflow

The dependency manager integrates seamlessly with other setup options:

```
TYPICAL WORKFLOW:
1. Start launcher
2. Run Option 1: Quick Setup
   └─ Configure all components
3. Run Option 6: Install Dependencies
   └─ Install Python/Node packages
4. Run Option 7: Deploy & Test
   └─ Test connectivity and generate scripts
5. Run Option 8: View Summary
   └─ Review all configurations
6. Option 9: Exit
```

## Performance Notes

- **Python installation**: ~2-5 minutes (depends on internet)
- **Node.js installation**: ~1-3 minutes (depends on internet)
- **Status check**: <1 second (no downloads)

## Best Practices

✅ **Do:**
- Run Option 2 (Basic Setup) before Option 6 (Dependencies)
- Check status with Option 4 before and after installation
- Use Option 1 for complete setup on first run
- Save configuration (Option 8) before installing

❌ **Don't:**
- Skip Python/Node setup if you plan to run components
- Install dependencies on slow/unreliable connections
- Use different Python versions for same environment
- Mix system packages with virtual environments

## See Also

- `QUICKSTART.py` - Interactive 5-phase setup guide
- `sample-setup.py` - Alternative setup script with more options
- `setup_master.py` - Base configuration module
- `setup_advanced.py` - Advanced setup features
- `TESTING_RESULTS.md` - All Python files verification report

## Version History

- **v1.0** (Dec 8, 2025) - Initial dependency manager implementation
  - Python package installation from requirements.txt
  - Node.js package installation with npm
  - Status reporting with installed packages
  - Integration with configuration workflow

---

**Last Updated:** December 8, 2025
**Status:** ✅ Fully Operational
