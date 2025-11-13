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

// Create HTTP server
const httpServer = createServer(app);

// Proxy ALL /api/* requests to Python backend BEFORE any other middleware
// This is critical - proxy must run before body parsers
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8001',
  changeOrigin: true,
  pathRewrite: (path) => {
    // /api/auth/signup -> /auth/signup
    // /api/upload -> /upload
    const newPath = path.replace(/^\/api/, '');
    console.log(`[Proxy] Rewrite: ${path} -> ${newPath}`);
    return newPath;
  },
  onProxyReq: (proxyReq, req) => {
    console.log(`[Proxy] Request: ${req.method} ${req.url}`);
  },
  onProxyRes: (proxyRes, req) => {
    console.log(`[Proxy] Response: ${proxyRes.statusCode} for ${req.url}`);
  },
  onError: (err, req, res) => {
    console.error('[Proxy] Error:', err.message);
    if (!res.headersSent) {
      res.status(502).json({
        error: 'Backend service unavailable',
        message: err.message
      });
    }
  }
}));

// Register Express middleware (AFTER proxy)
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Register Express routes for session management
import { registerRoutes } from "./routes";
await registerRoutes(app, httpServer);

// Vite dev server setup LAST (lowest priority - catches remaining requests)
await setupVite(app, httpServer);

const PORT = Number(process.env.PORT) || 5000;
httpServer.listen(PORT, "0.0.0.0", () => {
  console.log(`Frontend server running on http://0.0.0.0:${PORT}`);
  console.log(`Proxying /api requests to Python backend on http://localhost:8001`);
});
