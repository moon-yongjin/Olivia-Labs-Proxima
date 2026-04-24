const net = require('net');

const client = new net.Socket();
client.connect(19222, '127.0.0.1', () => {
    console.log('Connected to Agent Hub IPC port 19222');
    
    const request = {
        requestId: 1,
        action: 'grokAnimate',
        provider: 'grok',
        data: {}
    };
    
    client.write(JSON.stringify(request) + '\n');
});

client.on('data', (data) => {
    console.log('Received response:', data.toString());
    client.destroy();
});

client.on('error', (err) => {
    console.error('IPC Error:', err);
    client.destroy();
});
