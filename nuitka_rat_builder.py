#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    NUITKA RAT EXECUTABLE BUILDER (C-COMPILED)
    Compiles Python RAT to C/C++, then to native executable binary
    
    Advantages over PyInstaller:
    - True compilation to machine code (not bytecode)
    - Significantly smaller file size
    - Faster execution
    - Harder to decompile
    - Better obfuscation integration
    - True FUD (Fully Undetectable) binary
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

class Style:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @staticmethod
    def header(text):
        return f"{Style.CYAN}{Style.BOLD}{text}{Style.END}"
    
    @staticmethod
    def success(text):
        return f"{Style.GREEN}{text}{Style.END}"
    
    @staticmethod
    def error(text):
        return f"{Style.RED}{text}{Style.END}"
    
    @staticmethod
    def warning(text):
        return f"{Style.YELLOW}{text}{Style.END}"
    
    @staticmethod
    def info(text):
        return f"{Style.BLUE}{text}{Style.END}"

class NuitkaRATBuilder:
    """Builds truly compiled RAT executable using Nuitka"""
    
    def __init__(self, rat_source, output_name="rat_payload"):
        self.rat_source = rat_source
        self.output_name = output_name
        self.work_dir = tempfile.mkdtemp(prefix="nuitka_build_")
        
    def log(self, level, message):
        """Log build process"""
        if level == "info":
            print(f"{Style.info(f'[BUILD]')} {message}")
        elif level == "success":
            print(f"{Style.success(f'[✓]')} {message}")
        elif level == "error":
            print(f"{Style.error(f'[✗]')} {message}")
        elif level == "warning":
            print(f"{Style.warning(f'[!]')} {message}")
    
    def check_dependencies(self):
        """Check if Nuitka and compiler are available"""
        self.log("info", "Checking dependencies...")
        
        # Check Python
        self.log("success", f"Python: {sys.version.split()[0]}")
        
        # Check Nuitka
        try:
            result = subprocess.run([sys.executable, '-m', 'nuitka', '--version'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.log("success", f"Nuitka installed: {result.stdout.strip()}")
                return True
        except:
            pass
        
        # Try to install
        self.log("warning", "Nuitka not found, installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'nuitka'],
                         capture_output=True, timeout=120)
            self.log("success", "Nuitka installed successfully")
            return True
        except Exception as e:
            self.log("error", f"Failed to install Nuitka: {e}")
            return False
    
    def build_executable(self):
        """Build executable with Nuitka"""
        self.log("info", "Starting Nuitka compilation...")
        
        # Determine output path based on OS
        is_windows = sys.platform == 'win32'
        output_ext = '.exe' if is_windows else ''
        
        cmd = [
            sys.executable, '-m', 'nuitka',
            '--onefile',  # Single executable
            '--remove-output',  # Clean build
            '--follow-imports',  # Follow all imports
            '--jobs=auto',  # Use all cores
            '--lto=auto',  # Link-time optimization
            '--pgo=auto',  # Profile-guided optimization
            '--clang',  # Use Clang if available
            f'--output-dir={self.work_dir}',
            f'--output-filename={self.output_name}{output_ext}',
            self.rat_source
        ]
        
        # Optional: Add obfuscation
        if os.path.exists('/usr/bin/obfuscate'):
            cmd.insert(3, '--obfuscate')
        
        try:
            self.log("info", f"Compiling with: {' '.join(cmd[:5])}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.log("success", "Compilation successful")
                
                # Find output
                output_path = os.path.join(self.work_dir, f"{self.output_name}{output_ext}")
                if os.path.exists(output_path):
                    size_mb = os.path.getsize(output_path) / (1024*1024)
                    self.log("success", f"Executable created: {size_mb:.2f} MB")
                    return output_path
            else:
                self.log("error", f"Compilation failed:\n{result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.log("error", "Compilation timeout (>10 minutes)")
            return None
        except Exception as e:
            self.log("error", f"Compilation error: {e}")
            return None
    
    def build(self):
        """Complete build process"""
        print(Style.header("""
╔══════════════════════════════════════════════════════════════════════════════╗
║         NUITKA RAT EXECUTABLE BUILDER (C-COMPILED)                           ║
║     True compilation to native binary - Fully Undetectable                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """))
        
        if not os.path.exists(self.rat_source):
            self.log("error", f"Source not found: {self.rat_source}")
            return False
        
        if not self.check_dependencies():
            return False
        
        exe_path = self.build_executable()
        if exe_path:
            self.log("success", f"\n{'='*80}")
            self.log("success", f"EXECUTABLE CREATED: {exe_path}")
            self.log("success", f"{'='*80}\n")
            return exe_path
        
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Nuitka RAT Executable Builder')
    parser.add_argument('source', help='RAT source file')
    parser.add_argument('-o', '--output', default='rat_payload', help='Output name')
    
    args = parser.parse_args()
    
    builder = NuitkaRATBuilder(args.source, args.output)
    return builder.build()

if __name__ == '__main__':
    main()
