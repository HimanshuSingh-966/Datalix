import express from "express";
import { createServer } from "http";
import { createProxyMiddleware } from "http-proxy-middleware";
import { spawn } from "child_process";
import { setupVite } from "./vite";

const app = express();

// Install Python dependencies and start backend
let pythonProcess: any = null;

console.log('Installing Python dependencies...');
const pipInstall = spawn('pip', ['install', '-r', 'requirements.txt'], {
  cwd: './python_backend',
  env: { ...process.env },
  stdio: 'inherit'
});

pipInstall.on('exit', (code) => {
  if (code !== 0) {
    console.error('Failed to install Python dependencies');
    return;
  }
  
  console.log('Starting Python backend...');
  pythonProcess = spawn('python', ['main.py'], {
    cwd: './python_backend',
    env: { ...process.env, PORT: '8001' },
    stdio: 'inherit'
  });

  pythonProcess.on('error', (error: Error) => {
    console.error('Failed to start Python backend:', error);
  });

  pythonProcess.on('exit', (code: number) => {
    console.log(`Python backend exited with code ${code}`);
  });
});

process.on('exit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// Register Express middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Create HTTP server
const httpServer = createServer(app);

// Register Express routes FIRST (highest priority)
import { registerRoutes } from "./routes";
await registerRoutes(app, httpServer);

// Proxy ALL /api/* requests to Python backend BEFORE Vite
// This ensures API requests (including auth) don't get caught by Vite's catch-all
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8001',
  changeOrigin: true,
  logLevel: 'silent',
  pathRewrite: {
    '^/api': '', // Strip /api prefix: /api/auth/signup -> /auth/signup
  },
  onProxyReq: (proxyReq, req, res) => {
    const targetPath = req.url.replace('/api', '');
    console.log(`[Proxy] ${req.method} ${req.url} -> http://localhost:8001${targetPath}`);
    if (req.headers.authorization) {
      proxyReq.setHeader('Authorization', req.headers.authorization);
    }
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`[Proxy] Response: ${proxyRes.statusCode} for ${req.url}`);
  },
  onError: (err, req, res) => {
    console.error('[Proxy] Error:', err.message);
    if (!res.headersSent) {
      res.writeHead(500, {
        'Content-Type': 'application/json',
      });
      res.end(JSON.stringify({
        error: 'Backend proxy error',
        message: err.message
      }));
    }
  }
}));

// Vite dev server setup LAST (lowest priority - catches remaining requests)
await setupVite(app, httpServer);

const PORT = Number(process.env.PORT) || 5000;
httpServer.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
  console.log(`Proxying /api requests to Python backend on http://localhost:8001`);
});
