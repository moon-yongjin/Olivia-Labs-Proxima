#!/usr/bin/env node

import { Proxima } from './sdk/proxima.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const client = new Proxima({ baseUrl: 'http://localhost:3210' });

const args = process.argv.slice(2);
const command = args[0];

async function main() {
    if (!command) {
        showHelp();
        return;
    }

    try {
        switch (command) {
            case 'status':
                await handleStatus();
                break;
            case 'models':
                await handleModels();
                break;
            case 'ask':
                await handleAsk(args.slice(1));
                break;
            case 'code':
                await handleCode(args.slice(1));
                break;
            case 'help':
            case '--help':
            case '-h':
                showHelp();
                break;
            default:
                console.error(`Unknown command: ${command}`);
                showHelp();
                process.exit(1);
        }
    } catch (err) {
        if (err.message.includes('fetch failed') || err.message.includes('Cannot connect')) {
            console.error('\n❌ Error: Cannot connect to Proxima.');
            console.error('   Make sure the Proxima app is running (npm start).\n');
        } else {
            console.error(`\n❌ Error: ${err.message}\n`);
        }
        process.exit(1);
    }
}

function showHelp() {
    console.log(`
⚡ Proxima CLI

Usage:
  proxima status               - Check connection and app status
  proxima models               - List available AI models
  proxima ask [model] "query"  - Ask a question (e.g., proxima ask "hello", proxima ask claude "hello")
  proxima code [action] [file] - Code tools (e.g., proxima code review test.py)
  
Examples:
  proxima ask "What's the weather?"
  proxima ask grok "Tell me a joke"
  proxima code review main.py
    `);
}

async function handleStatus() {
    console.log('Checking Proxima status...');
    try {
        const stats = await client.getStats();
        console.log('\n✅ Proxima is ONLINE');
        console.log(`   Uptime: ${stats.uptime}`);
        console.log(`   Total Requests: ${stats.totalRequests}`);
        
        const models = await client.getModels();
        const enabled = models.filter(m => m.status === 'enabled').map(m => m.id);
        console.log(`   Enabled Providers: ${enabled.join(', ')}`);
        console.log('');
    } catch (e) {
        throw new Error('Proxima app is not responding at http://localhost:3210');
    }
}

async function handleModels() {
    const models = await client.getModels();
    console.log('\nAvailable Models:');
    models.forEach(m => {
        const status = m.status === 'enabled' ? '✅' : '❌';
        console.log(`  ${status} ${m.id.padEnd(12)} (${(m.aliases || []).join(', ') || 'no aliases'})`);
    });
    console.log('');
}

async function handleAsk(askArgs) {
    if (askArgs.length === 0) {
        console.error('Usage: proxima ask [model] "message"');
        return;
    }

    let model = 'auto';
    let message = '';

    if (askArgs.length === 1) {
        message = askArgs[0];
    } else {
        model = askArgs[0];
        message = askArgs.slice(1).join(' ');
    }

    console.log(`\n🤖 Sending to ${model}...`);
    const res = await client.chat(message, { model });
    
    console.log('\n--------------------------------------------------');
    console.log(res.text);
    console.log('--------------------------------------------------');
    console.log(`(Response from ${res.provider} in ${res.responseTimeMs}ms)\n`);
}

async function handleCode(codeArgs) {
    if (codeArgs.length < 1) {
        console.error('Usage: proxima code [action] [file/query]');
        return;
    }

    const action = codeArgs[0];
    const target = codeArgs.slice(1).join(' ');

    if (action === 'review' || action === 'debug' || action === 'explain' || action === 'optimize') {
        // Check if target is a file
        if (fs.existsSync(target)) {
            const code = fs.readFileSync(target, 'utf8');
            console.log(`\n💻 ${action.toUpperCase()}ing file: ${target}...`);
            const res = await client.chat('', { 
                function: 'code', 
                action, 
                code, 
                language: path.extname(target).slice(1) 
            });
            console.log('\n--------------------------------------------------');
            console.log(res.text);
            console.log('--------------------------------------------------\n');
        } else {
            console.log(`\n💻 ${action.toUpperCase()}ing: ${target}...`);
            const res = await client.chat(target, { function: 'code', action });
            console.log('\n--------------------------------------------------');
            console.log(res.text);
            console.log('--------------------------------------------------\n');
        }
    } else {
        // Default to generate
        console.log(`\n💻 Generating code: ${target}...`);
        const res = await client.chat(target, { function: 'code', action: 'generate' });
        console.log('\n--------------------------------------------------');
        console.log(res.text);
        console.log('--------------------------------------------------\n');
    }
}

main();
