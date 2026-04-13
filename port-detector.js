#!/usr/bin/env node

/**
 * Port detection utility for Node.js and Python servers
 * Finds first available port in a range
 */

const net = require('net');
const { spawn } = require('child_process');
const path = require('path');

async function findAvailablePort(startPort, endPort) {
  for (let port = startPort; port <= endPort; port++) {
    try {
      const available = await checkPort(port);
      if (available) {
        return port;
      }
    } catch (err) {
      continue;
    }
  }
  return startPort; // Fallback to start if none available
}

function checkPort(port) {
  return new Promise((resolve) => {
    const server = net.createServer();
    
    server.once('error', (err) => {
      if (err.code === 'EADDRINUSE') {
        resolve(false);
      } else {
        resolve(false);
      }
    });
    
    server.once('listening', () => {
      server.close();
      resolve(true);
    });
    
    server.listen(port, '0.0.0.0');
  });
}

async function runBackend() {
  const port = await findAvailablePort(8000, 8009);
  console.log(`\n✓ Starting Django backend on port ${port}...`);
  
  const backendDir = path.join(__dirname, 'backend');
  const server = spawn('python', ['manage.py', 'runserver', `0.0.0.0:${port}`], {
    cwd: backendDir,
    stdio: 'inherit',
    env: { ...process.env, PYTHONUNBUFFERED: '1' }
  });
  
  server.on('error', (err) => {
    console.error('Backend failed to start:', err);
    process.exit(1);
  });
}

async function runFrontend() {
  const port = await findAvailablePort(3000, 3009);
  console.log(`\n✓ Starting Next.js frontend on port ${port}...`);
  
  const frontendDir = __dirname;
  const server = spawn('npm', ['run', 'dev', '--', '-p', port.toString()], {
    cwd: frontendDir,
    stdio: 'inherit',
  });
  
  server.on('error', (err) => {
    console.error('Frontend failed to start:', err);
    process.exit(1);
  });
}

// Parse command line argument
const command = process.argv[2];

if (command === 'backend') {
  runBackend().catch(err => {
    console.error('Error:', err);
    process.exit(1);
  });
} else if (command === 'frontend') {
  runFrontend().catch(err => {
    console.error('Error:', err);
    process.exit(1);
  });
} else {
  console.log('Usage:');
  console.log('  node port-detector.js backend   # Find available port for Django (8000-8009)');
  console.log('  node port-detector.js frontend  # Find available port for Next.js (3000-3009)');
}
